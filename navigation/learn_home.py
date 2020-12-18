# Sets the home base of the robot
def set_home(robot):
    localization_service = robot.ALLocalization
    ret = localization_service.learnHome()

    if ret == 0:
        print("Succesfull, learnt home")
    else:
        print("Error occured")
