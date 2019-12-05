import math

INPUT_PATH = "input.txt"


def get_masses():
    with open(INPUT_PATH) as fp:
        return fp.readlines()


def calculate_fuel_requirement(mass):
    return math.floor(int(mass) / 3) - 2


def part_one():
    fuel_requirement = 0
    for mass in get_masses():
        fuel_requirement += math.floor(int(mass) / 3) - 2

    return fuel_requirement


def part_two():
    total_fuel_requirement = 0
    for mass in get_masses():
        fuel_requirement = calculate_fuel_requirement(mass)
        while fuel_requirement > 0:
            total_fuel_requirement += fuel_requirement
            fuel_requirement = calculate_fuel_requirement(fuel_requirement)

    return total_fuel_requirement


if __name__ == '__main__':
    print("Part one answer: {0}".format(part_one()))
    print("Part two answer: {0}".format(part_two()))