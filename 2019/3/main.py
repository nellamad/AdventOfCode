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


def traverse(path, step_action):
    x, y = 0, 0
    for edge in path:
        direction, length = edge[0], int(edge[1:])
        xy_mod = direction_to_mods[direction]
        for i in range(0, length):
            x, y = (x + xy_mod[0]), (y + xy_mod[1])
            step_action(x, y)


def calculate_shortest_manhattan_distance_intersection(paths):
    def update_smallest_distance(x, y):
        nonlocal smallest_intersection_distance
        if (x, y) in travelled_xy:
            smallest_intersection_distance = min(smallest_intersection_distance, abs(x) + abs(y))

    travelled_xy = set()
    smallest_intersection_distance = maxsize
    traverse(paths[0], lambda x, y: travelled_xy.add((x, y)))
    traverse(paths[1], update_smallest_distance)

    return smallest_intersection_distance


def calculate_fewest_steps_to_intersection(paths):
    def check_and_initialize_intersection(x, y):
        if (x, y) in travelled_xy:
            intersection_to_weights[(x, y)] = [maxsize, maxsize]

    def gen_update_intersection_weights(wire_id):
        path_weight = 0

        def update_intersection_weights(x, y):
            nonlocal path_weight
            path_weight += 1
            if (x, y) in intersection_to_weights:
                old_weights = intersection_to_weights[(x, y)]
                for i in range(2):
                    if i != wire_id:
                        intersection_to_weights[(x, y)][i] = old_weights[i]
                    else:
                        intersection_to_weights[(x, y)][i] = min(old_weights[i], path_weight)

        return update_intersection_weights

    travelled_xy, intersection_to_weights = set(), {}
    # step 1: calculate a list of intersections
    traverse(paths[0], lambda x, y: travelled_xy.add((x, y)))
    traverse(paths[1], check_and_initialize_intersection)

    # step 2: calculate weight for path to each intersection for each line/wire
    traverse(paths[0], gen_update_intersection_weights(0))
    traverse(paths[1], gen_update_intersection_weights(1))

    return min([w[0] + w[1] for w in intersection_to_weights.values()])


def part_one():
    return calculate_shortest_manhattan_distance_intersection(get_paths())


def part_two():
    return calculate_fewest_steps_to_intersection(get_paths())


if __name__ == '__main__':
    print("Part one answer: {0}".format(part_one()))
    print("Part two answer: {0}".format(part_two()))
