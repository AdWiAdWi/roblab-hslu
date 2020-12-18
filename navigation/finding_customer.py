from navigation.utils.take_and_get_picture import TakePicture
import requests
import math
from navigation.utils.get_position import get_position


# Find customer in room
def find_people(robot):
    # Set starting position, pepper will then turn into correct position after inital input
    compass_service = robot.ALVisualCompass
    compass_service.moveTo(0, 0, theta=math.radians(180))
    print('turn 180 grad')

    # Get the position of the bar
    bar_position = get_position(robot)

    # Search on side of the room for customer
    customer_detected = search_customer(robot)
    counter = 0
    while customer_detected is False and counter <= 3:
        print('No one detected')
        compass_service.moveTo(0, 0, theta=math.radians(30))
        customer_detected = search_customer(robot)
        counter += 1

    # Turn back to search the other part of the room
    compass_service.moveTo(0, 0, theta=math.radians(-90))

    # Search other side of the room for customer
    customer_detected = search_customer(robot)
    counter = 0
    while customer_detected is False and counter <= 3:
        print('No one detected')
        compass_service.moveTo(0, 0, theta=math.radians(-30))
        customer_detected = search_customer(robot)
        counter += 1

    if counter == 3:
        print('Didn\'t find costumer')

    if customer_detected:
        return True, bar_position
    else:
        return False


# Check if there is a customer in front of the robot
def search_customer(robot):
    position = robot.ALTracker
    position.lookAt([7, 0, 0], 0, 0.7, True)

    # using picture service to take and save picture
    picture_service = TakePicture()
    path = picture_service.take_picture(robot)

    URL = "http://127.0.0.1:5000/"
    PARAMS = {'path': path}
    r = requests.get(url=URL, params=PARAMS)
    print(r.content)
    if r.content == "True":
        print("is really string")
        return True
    else:
        return False
