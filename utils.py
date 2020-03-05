goal = 0
start = 0

goal_active = 0
goal_button = {False: ("forest green", "white", 2, "flat"), True: ("dark olive green", "black", 2, "sunken")}

start_active = 0
start_button = {False: ("grey", "black", 2, "flat"), True: ("black", "white", 2, "sunken")}

obstacle_active = 0
obstacle_button = {False: ("red", "white", 2, "flat"), True: ("dark red", "white", 2, "sunken")}

clear_active = 0
clear_button = {False: ("white", "black", 2, "flat"), True: ("grey", "black", 2, "sunken")}


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
