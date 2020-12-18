import re
import math


# Navigates back to the customer, which ordered a drink
def navigate_to_customer(old_coord, robot):
    # Get all floats of "Pose2D(x=1.324, y=2.3421, theta=-0.32)"
    numbs = re.findall(r"[-+]?\d*\.\d+|\d+", str(old_coord))

    x_ = float(numbs[1])
    y_ = float(numbs[2])
    theta_ = float(numbs[3])

    # Turn PepperTheWaiter 180 degrees to navigate in the correct direction. Works generic.
    compass_service = robot.ALVisualCompass
    compass_service.moveTo(0, 0, theta=math.radians(180))
    print('turn 180 grad')

    # Move to the customer
    motion_service = robot.ALMotion
    motion_service.moveTo(x_, y_, theta_)
