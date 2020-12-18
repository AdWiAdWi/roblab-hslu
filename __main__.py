from lib.Robot import Robot
from lib.PepperConfiguration import PepperConfiguration
from core import PepperTheWaiter


def main():
    # Set correct Pepper robot
    config = PepperConfiguration("Porter")
    robot = Robot(config)

    # Disable basic awareness to avoid unplanned speech recognition
    al_service = robot.ALAutonomousLife
    al_service.setAutonomousAbilityEnabled(False)

    # Create Instance of PepperTheWaiter and start
    pepper_the_waiter = PepperTheWaiter(robot)
    pepper_the_waiter.start()


if __name__ == "__main__":
    main()
