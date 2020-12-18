from communication.ask_customer_for_drink import AskCustomerForDrink
from communication.order_drink_bar import OrderDrinkBar
from communication.serve_the_drink import ServeTheDrink
from communication.waiting_for_initial_input import WaitingForInput
from navigation.navigating_back_to_customer import navigate_to_customer
from navigation.navigating_back_to_bar import navigating_back_to_bar
from navigation.finding_customer import find_people
from navigation.learn_home import set_home
from navigation.moving_to_customer import moving_to_customer
from navigation.resting import resting
from automat import MethodicalMachine


# State machine for PepperTheWaiter
class PepperTheWaiter(object):
    _machine = MethodicalMachine()

    def __init__(self, robot):
        # Position of the customer, who ordered drink
        self.position_customer = None
        # Position of the counter
        self.position_bar = None
        # Instance of robot
        self.robot = robot
        # Ordered drink
        self.drink = ""

    " STATES of PepperTheWaiter "

    @_machine.state(initial=True)
    def initialize_state(self):
        "Initialization"

    @_machine.state()
    def waiting_for_input_state(self):
        "Waiting for an input from the barkeeper"

    @_machine.state()
    def finding_customer_state(self):
        "Finding customer"

    @_machine.state()
    def moving_to_customer_state(self):
        "Moving to customer"

    @_machine.state()
    def ask_customer_for_drink_state(self):
        "Asking customer, if he likes something to drink"

    @_machine.state()
    def moving_back_to_bar_state(self):
        "Moving back to the bar"

    @_machine.state()
    def order_drink_state(self):
        "Ordering drink at the bar"

    @_machine.state()
    def moving_back_to_customer_state(self):
        "Moving back to the customer who ordered drink"

    @_machine.state()
    def serve_drink_state(self):
        "Serving drink to the customer"

    @_machine.state()
    def moving_back_to_start_state(self):
        "Moving back to the starting position"

    @_machine.state()
    def resting_state(self):
        "Resting"

    ''' INPUTS to change states'''

    @_machine.input()
    def start(self):
        "Start behavior"

    @_machine.input()
    def search(self):
        "Search customer in bar"

    @_machine.input()
    def start_interaction(self):
        "Start interacting with customer or barkeeper"

    @_machine.input()
    def start_moving(self):
        "Start moving to desired position"

    @_machine.input()
    def go_to_start(self):
        "Go to start position"

    @_machine.input()
    def go_to_rest(self):
        "Go to rest position"

    ''' OUTPUTS performed in states'''

    @_machine.output()
    def listen_to_barkeeper(self):
        # Set home base of the roboter
        set_home(self.robot)

        # Wait for input of barkeeper
        waiting = WaitingForInput(self.robot)
        waiting.run()
        while waiting.running():
            pass

        # Trigger change to next state - always the same
        self.search()

    @_machine.output()
    def finding_customer(self):
        # Find and move to customer. Furthermore save position of customer
        found_customer, self.position_bar = find_people(self.robot)

        if found_customer:
            self.start_moving()
        else:
            self.go_to_rest()

    @_machine.output()
    def moving_to_customer(self):
        # Move to customer and return position
        self.position_customer = moving_to_customer(self.robot, self.position_bar)
        self.start_interaction()

    @_machine.output()
    def talking_to_customer(self):
        # Ask customer if he likes something to drink
        asking = AskCustomerForDrink(self.robot)

        # Save drink which customer ordered
        self.drink, want_drink = asking.run()
        while asking.running():
            pass

        if want_drink:
            self.start_moving()
        else:
            self.go_to_start()

    @_machine.output()
    def navigate_to_bar1(self):
        # Move back to the bar
        navigating_back_to_bar(self.robot)
        self.start_interaction()

    @_machine.output()
    def order_drink(self):
        # Order drink at the bar
        ordering = OrderDrinkBar(self.robot)
        ordering.run(self.drink)
        while ordering.running():
            pass

        self.start_moving()

    @_machine.output()
    def navigate_to_customer(self):
        # Navigate back to the customer
        navigate_to_customer(self.position_customer, self.robot)
        self.start_interaction()

    @_machine.output()
    def serve_drink(self):
        # Serve drink to the customer
        serving = ServeTheDrink(self.robot)
        serving.run(self.drink)
        while serving.running():
            pass

        self.go_to_start()

    @_machine.output()
    def navigate_to_bar2(self):
        # Finally move back one last time to the bar ;)
        navigating_back_to_bar(self.robot)

    @_machine.output()
    def rest(self):
        # Rest
        resting(self.robot)

    ''' TRANSITIONS '''

    # Current state -> (input=change, enter=new_state, output=what_to_do)
    initialize_state.upon(start, enter=waiting_for_input_state, outputs=[listen_to_barkeeper])
    waiting_for_input_state.upon(search, enter=finding_customer_state, outputs=[finding_customer])
    finding_customer_state.upon(start_moving, enter=moving_to_customer_state, outputs=[moving_to_customer])
    finding_customer_state.upon(go_to_rest, enter=resting_state, outputs=[rest])
    moving_to_customer_state.upon(start_interaction, enter=ask_customer_for_drink_state, outputs=[talking_to_customer])
    ask_customer_for_drink_state.upon(start_moving, enter=moving_back_to_bar_state, outputs=[navigate_to_bar1])
    ask_customer_for_drink_state.upon(go_to_start, enter=moving_back_to_start_state, outputs=[navigate_to_bar2])
    moving_back_to_bar_state.upon(start_interaction, enter=order_drink_state, outputs=[order_drink])
    order_drink_state.upon(start_moving, enter=moving_back_to_customer_state, outputs=[navigate_to_customer])
    moving_back_to_customer_state.upon(start_interaction, enter=serve_drink_state, outputs=[serve_drink])
    serve_drink_state.upon(go_to_start, enter=moving_back_to_start_state, outputs=[navigate_to_bar2])
    moving_back_to_bar_state.upon(go_to_rest, enter=resting_state, outputs=[rest])
