goal_button = {False: ("forest green", "white", 2, "raised"), True: ("dark olive green", "black", 2, "sunken")}

start_button = {False: ("grey", "black", 2, "raised"), True: ("black", "white", 2, "sunken")}

obstacle_button = {False: ("red", "white", 2, "raised"), True: ("dark red", "white", 2, "sunken")}

clear_button = {False: ("white", "black", 2, "raised"), True: ("grey", "black", 2, "sunken")}


def get_color(name, enabled):
    return globals()[name][enabled]


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
