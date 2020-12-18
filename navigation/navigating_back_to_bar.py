# Navigates back to the bar using built-in goToHome function
def navigating_back_to_bar(robot):
    localization_service = robot.ALLocalization
    ret = localization_service.goToHome()

    if ret == 0:
        print("Succesfull, moving now back to the bar")
    else:
        print("Error occured")
