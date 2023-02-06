MAX_SPEED = 10
SPEED_UNIT = 0.00053429
DISTANCE_RANGE = 2000

MATRIX = [
    [-5000, -5000],
    [-20000, 40000],
    [-30000, 50000],
    [-70000, 70000],
    [70000, -60000],
    [50000, -40000],
    [40000, -20000],
    [-5000, -5000],
    [-10000, -10000],
]


def bound(x, a, b):
    return a if x < a else (b if x > b else x)


# Wall avoidance algorithm
def braitengerg(sensors_values):
    speed = [0, 0]

    for i in range(2):
        for j in range(len(sensors_values)):
            speed[i] += SPEED_UNIT * MATRIX[j][i] * (1.0 - (sensors_values[j] / DISTANCE_RANGE))
        speed[i] = bound(speed[i], -MAX_SPEED, MAX_SPEED)

    return speed


if __name__ == "__main__":
    print(braitengerg([100]))
