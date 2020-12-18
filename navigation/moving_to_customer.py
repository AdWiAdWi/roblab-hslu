from navigation.utils.get_position import get_position
import almath
import time


# Moving to the customer
def moving_to_customer(robot, bar_position):
    memory_service = robot.ALMemory

    # Get distance to customer and move
    motion = robot.ALMotion
    sonar_front = memory_service.getData("Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value")
    motion.moveTo(sonar_front - 0.6, 0, 0)

    time.sleep(1)
    customer_position = get_position(robot)

    bar_position = almath.Pose2D(bar_position)
    customer_position = almath.Pose2D(customer_position)

    bar_position = almath.pose2DInverse(bar_position)

    # Calculate position of the customer
    robot_move = bar_position * customer_position
    return robot_move
