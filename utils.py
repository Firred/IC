goal = 0
start = 0

goal_active = 0
goal_button = {False: "forest green", True: "dark olive green"}


def get_goal_color():
    global goal_active
    goal_active = not goal_active
    return goal_button[goal_active]

