import logging

from statemachine import StateMachine, State
from statemachine.exceptions import TransitionNotAllowed

from sec_levels.icmp_control.icmp_control import ICMPThread
from util.PausibleMonitoringThread import PausableMonitoringThread
from util.utils import singleton


class SecurityLevel(State):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@singleton
class DefconHandler(StateMachine):
    """Defcon modes handler"""

    defcon_3_normal = SecurityLevel(initial=True, value=1)
    defcon_2_monitoring = SecurityLevel(value=2)
    defcon_1_localize = SecurityLevel(value=3)

    do_increase = (
            defcon_3_normal.to(defcon_2_monitoring)
            | defcon_2_monitoring.to(defcon_1_localize)
    )

    do_decrease = (
            defcon_1_localize.to(defcon_2_monitoring)
            | defcon_2_monitoring.to(defcon_3_normal)
    )

    def __init__(self):
        # init base monitoring
        self.previous_state = None
        # create monitors
        self.normal_monitoring_thread = ICMPThread()
        self.decrease_ICMP_threads = PausableMonitoringThread(5)
        self.maximum_monitoring_thread = PausableMonitoringThread(2.5)
        # start threads
        self.normal_monitoring_thread.start()
        self.decrease_ICMP_threads.start()
        self.maximum_monitoring_thread.start()
        # pause the ones that aren't the initial levels
        self.decrease_ICMP_threads.pause()
        self.maximum_monitoring_thread.pause()
        super().__init__()

    def increase(self):
        self.previous_state = self.current_state
        try:
            self.do_increase()
            logging.info(f"Increased defcon mode to: {self.current_state.id}")


        except TransitionNotAllowed as e:
            logging.error(f'Increase defcon mode not possible: {str(e)}')

    def decrease(self):
        self.previous_state = self.current_state
        try:
            self.do_decrease()
            logging.info(f"Decreased defcon mode to: {self.current_state.id}")

        except TransitionNotAllowed as e:
            logging.error(f'Decrease defcon mode not possible: {str(e)}')

    def increase_security_level(self, target_level):
        while self.current_state.value != target_level:
            self.do_increase()

    def on_enter_defcon_3_normal(self):
        if self.previous_state == self.defcon_2_monitoring:
            self.decrease_ICMP_threads.pause()
        self.decrease_ICMP_threads.resume()

    def on_enter_defcon_2_monitoring(self):
        if self.previous_state == self.defcon_1_localize:
            self.maximum_monitoring_thread.pause()
        elif self.previous_state == self.defcon_3_normal:
            self.normal_monitoring_thread.pause()
        self.decrease_ICMP_threads.resume()

    def on_enter_defcon_1_localize(self):
        self.decrease_ICMP_threads.pause()
        self.maximum_monitoring_thread.resume()

    def get_current_security_level(self):
        return self.current_state
