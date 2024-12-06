import logging

from statemachine import StateMachine, State
from statemachine.exceptions import TransitionNotAllowed

from util.utils import singleton


@singleton
class DefconHandler(StateMachine):
    """Defcon modes handler"""

    defcon_3_normal = State(initial=True)
    defcon_2_monitoring = State()
    defcon_1_localize = State()

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

    def on_enter_defcon_3_normal(self):
        pass

    def on_enter_defcon_2_monitoring(self):
        pass

    def on_enter_defcon_1_localize(self):
        pass

    def get_current_state(self):
        return self.current_state.id
