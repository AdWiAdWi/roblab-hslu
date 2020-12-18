# Go to resting position
def resting(robot):
    motion_service = robot.ALMotion
    posture_service = robot.ALRobotPosture

    # Go to init pose
    posture_service.goToPosture("StandInit", 0.5)

    # Go to rest position
    motion_service.rest()
