from sys import maxsize

INPUT_PATH = "input.txt"


direction_to_mods = {
    'U': (0, 1),
    'R': (1, 0),
    'D': (0, -1),
    'L': (-1, 0)
}


def get_paths():
    with open(INPUT_PATH) as fp:
        return fp.readline().split(','), fp.readline().split(',')


def calculate_shortest_manhattan_distance_intersection(paths):
    travelled_xy = set()
    x, y = 0, 0
    smallest_intersection_distance = maxsize
    for edge in paths[0]:
        direction, length = edge[0], int(edge[1:])
        xy_mod = direction_to_mods[direction]
        for i in range(0, length):
            x, y = (x + xy_mod[0]), (y + xy_mod[1])
            travelled_xy.add((x, y))

    x, y = 0, 0
    for edge in paths[1]:
        direction, length = edge[0], int(edge[1:])
        xy_mod = direction_to_mods[direction]
        for i in range(0, length):
            x, y = (x + xy_mod[0]), (y + xy_mod[1])
            if (x, y) in travelled_xy:
                smallest_intersection_distance = min(smallest_intersection_distance, abs(x) + abs(y))

    return smallest_intersection_distance


def calculate_fewest_steps_to_intersection(paths):
    # step 1: calculate a list of intersections
    travelled_xy, intersection_to_weights = set(), {}
    x, y = 0, 0
    for edge in paths[0]:
        direction, length = edge[0], int(edge[1:])
        xy_mod = direction_to_mods[direction]
        for i in range(0, length):
            x, y = (x + xy_mod[0]), (y + xy_mod[1])
            travelled_xy.add((x, y))

    x, y = 0, 0
    for edge in paths[1]:
        direction, length = edge[0], int(edge[1:])
        xy_mod = direction_to_mods[direction]
        for i in range(0, length):
            x, y = (x + xy_mod[0]), (y + xy_mod[1])
            if (x, y) in travelled_xy:
                intersection_to_weights[(x, y)] = (maxsize, maxsize)

    # step 2: calculate weight for path to each intersection for each line/wire
    x, y = 0, 0
    first_line_weight = 0
    for edge in paths[0]:
        direction, length = edge[0], int(edge[1:])
        xy_mod = direction_to_mods[direction]
        for i in range(0, length):
            x, y = (x + xy_mod[0]), (y + xy_mod[1])
            first_line_weight += 1
            if (x, y) in intersection_to_weights:
                old_weights = intersection_to_weights[(x, y)]
                intersection_to_weights[(x, y)] = (min(old_weights[0], first_line_weight), old_weights[1])

    x, y = 0, 0
    second_line_weight = 0
    for edge in paths[1]:
        direction, length = edge[0], int(edge[1:])
        xy_mod = direction_to_mods[direction]
        for i in range(0, length):
            x, y = (x + xy_mod[0]), (y + xy_mod[1])
            second_line_weight += 1
            if (x, y) in intersection_to_weights:
                old_weights = intersection_to_weights[(x, y)]
                intersection_to_weights[(x, y)] = (old_weights[0], min(old_weights[1], second_line_weight))

    return min([w[0] + w[1] for w in intersection_to_weights.values()])


def part_one():
    return calculate_shortest_manhattan_distance_intersection(get_paths())


def part_two():
    return calculate_fewest_steps_to_intersection(get_paths())


if __name__ == '__main__':
    print("Part one answer: {0}".format(part_one()))
    print("Part two answer: {0}".format(part_two()))
