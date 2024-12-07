import logging

from statemachine import StateMachine, State
from statemachine.exceptions import TransitionNotAllowed

from sec_levels.icmp_control.icmp_control import ICMPThreadMonitor, ICMPThreadRateLimiting, \
    ICMPThreadBlocker
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
        self.icmp_normal_monitor_thread = ICMPThreadMonitor()
        self.icmp_limited_thread = ICMPThreadRateLimiting(10, 5)
        self.icmp_blocking_thread = ICMPThreadBlocker()
        # start threads
        self.icmp_normal_monitor_thread.start()
        self.icmp_limited_thread.start()
        self.icmp_blocking_thread.start()
        # pause the ones that aren't the initial levels
        self.icmp_limited_thread.pause()
        self.icmp_blocking_thread.pause()
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
            self.icmp_limited_thread.pause()
        self.icmp_limited_thread.resume()

    def on_enter_defcon_2_monitoring(self):
        if self.previous_state == self.defcon_1_localize:
            self.icmp_blocking_thread.pause()
        elif self.previous_state == self.defcon_3_normal:
            self.icmp_normal_monitor_thread.pause()
        self.icmp_limited_thread.resume()

    def on_enter_defcon_1_localize(self):
        self.icmp_limited_thread.pause()
        self.icmp_blocking_thread.resume()

    def get_current_security_level(self):
        return self.current_state
