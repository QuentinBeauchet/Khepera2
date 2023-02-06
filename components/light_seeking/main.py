LIGHT_DETECTION_THRESHOLD = 700
MAX_SPEED = 10

MATRIX = [
    [-MAX_SPEED, MAX_SPEED],
    [-MAX_SPEED / 2, MAX_SPEED / 2],
    [MAX_SPEED, MAX_SPEED],
    [MAX_SPEED, MAX_SPEED],
    [MAX_SPEED / 2, -MAX_SPEED / 2],
    [MAX_SPEED, -MAX_SPEED],
    [-MAX_SPEED, MAX_SPEED],
    [MAX_SPEED, -MAX_SPEED],
]

# Returns the max light detected and the index of the corresponding sensor.
def get_light_infos(light_sensors):
    max_light = 0
    max_index = 0
    for i in range(len(light_sensors)):
        value = light_sensors[i]
        if value > max_light:
            max_light = value
            max_index = i
    return (max_light, max_index)


# Light following detection algorithm
def follow_light(light_sensors):
    max_light, max_index = get_light_infos(light_sensors)

    if max_light < LIGHT_DETECTION_THRESHOLD:
        return [0, 0]

    return MATRIX[max_index]


if __name__ == "__main__":
    print(follow_light([100]))
