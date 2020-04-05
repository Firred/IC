import math

goal_active = 0
goal_button = {False: ("forest green", "white", 2, "raised"), True: ("dark olive green", "black", 2, "sunken")}

start_active = 0
start_button = {False: ("grey", "black", 2, "raised"), True: ("black", "white", 2, "sunken")}

obstacle_active = 0
obstacle_button = {False: ("red", "white", 2, "raised"), True: ("dark red", "white", 2, "sunken")}

clear_active = 0
clear_button = {False: ("white", "black", 2, "raised"), True: ("grey", "black", 2, "sunken")}


def get_goal_color():
    global goal_active
    goal_active = not goal_active
    return goal_button[goal_active]


def get_start_color():
    global start_active
    start_active = not start_active
    return start_button[start_active]


def get_obstacle_color():
    global obstacle_active
    obstacle_active = not obstacle_active
    return obstacle_button[obstacle_active]


def get_clear_color():
    global clear_active
    clear_active = not clear_active
    return clear_button[clear_active]


def get_color(name, enabled):
    return globals()[name][enabled]


def calculate_dist(pos1, pos2):
    return math.sqrt((math.pow(pos1[0]-pos2[0], 2) + (math.pow(pos1[1]-pos2[1], 2))))


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
