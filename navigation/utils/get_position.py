import almath


# Returns the current position as [x, y, theta] of the robot
def get_position(robot):
    motion_service = robot.ALMotion
    posture_service = robot.ALRobotPosture

    motion_service.wakeUp()
    posture_service.goToPosture("StandInit", 0.5)

    use_sensor_values = False
    position = motion_service.getRobotPosition(use_sensor_values)
    print("Got position ", str(position))
    return position
