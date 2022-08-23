from constants import BASE_SPEED

def get_speed(initial_time, curr_time):
    """
    initial_time, curr_time: time object
    """
    return (BASE_SPEED + 0.5 * ((curr_time - initial_time) // 20)) / 800