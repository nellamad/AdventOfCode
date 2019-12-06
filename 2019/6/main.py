INPUT_PATH = "input.txt"


def get_program():
    with open(INPUT_PATH) as fp:
        return fp.readlines()


def build_orbit_map(orbits):
    orbiter_to_orbitee = {}
    for orbit in orbits:
        objects = orbit.strip().split(')')
        orbiter_to_orbitee[objects[1]] = objects[0]

    return orbiter_to_orbitee


def count_orbits(orbits):
    orbiter_to_orbitee = build_orbit_map(orbits)
    orbits = 0
    for orbiter in orbiter_to_orbitee.keys():
        current_obj = orbiter
        while current_obj != "COM":
            orbits += 1
            current_obj = orbiter_to_orbitee[current_obj]

    return orbits


def build_orbit_graph(orbiter_to_orbitee):
    node_to_neighbours = {}
    for orbiter, orbitee in orbiter_to_orbitee.items():
        node_to_neighbours[orbiter] = node_to_neighbours.get(orbiter, []) + [orbitee]
        node_to_neighbours[orbitee] = node_to_neighbours.get(orbitee, []) + [orbiter]

    return node_to_neighbours


class Queue:
    def __init__(self):
        self.entrance = []
        self.exit = []
        self.length = 0

    def enqueue(self, el):
        self.entrance.insert(0, el)
        self.length += 1

    def dequeue(self):
        self.check_and_fill_exit()
        if len(self.exit) > 0:
            popped = self.exit[0]
            del self.exit[0]
            self.length -= 1
            return popped

    def check_and_fill_exit(self):
        if len(self.exit) < 1:
            while len(self.entrance) > 0:
                popped = self.entrance[0]
                del self.entrance[0]
                self.exit.insert(0, popped)

    def __len__(self):
        return self.length


def count_orbital_transfers(orbits):
    def breadth_first_search(node_to_neighbours, a, b):
        to_visit = Queue()
        visited = set()
        to_visit.enqueue((a, 0))
        while len(to_visit) > 0:
            visiting, distance = to_visit.dequeue()
            if visiting == b:
                return distance - 2
            if visiting not in visited:
                for neighbour in node_to_neighbours[visiting]:
                    to_visit.enqueue((neighbour, distance + 1))
            visited.add(visiting)
        return False

    return breadth_first_search(build_orbit_graph(build_orbit_map(orbits)), "YOU", "SAN")


def part_one():
    return count_orbits( get_program())


def part_two():
    return count_orbital_transfers(get_program())


if __name__ == '__main__':
    print("Part one answer: {0}".format(part_one()))
    print("Part two answer: {0}".format(part_two()))
