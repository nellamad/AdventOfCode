from sys import maxsize
from itertools import permutations

INPUT_PATH = "input.txt"


class Image:
    def __init__(self, pixels, width, height):
        self.width, self.height = width, height
        self.layers = self.__decode__(pixels)

    def __decode__(self, pixels):
        print(pixels)
        layers = []
        while len(pixels) > 0:
            layer = []
            for n in range(self.height):
                row = []
                for m in range(self.width):
                    if len(pixels) > 0:
                        row.append(pixels.pop(0))
                layer.append(row)
            layers.append(layer)
        return layers

    def print(self):
        for layer in self.layers:
            print(layer)

    def __str__(self):
        return "".join(["".join(row) for layer in self.layers for row in layer])


def get_program():
    with open(INPUT_PATH) as fp:
        return fp.readline().strip()


def part_one():
    image = Image(list(get_program()), 25, 6)
    #image.print()
    min_zero_layer, min_zeroes = 0, maxsize
    for i, layer in enumerate(image.layers):
        zeroes = layer.count('0')
        for row in layer:
            zeroes += row.count('0')
        if zeroes < min_zeroes:
            min_zero_layer, min_zeroes = layer, zeroes

    ones, twos = 0, 0
    for row in min_zero_layer:
        ones += row.count('1')
        twos += row.count('2')
    return ones * twos


def part_two():
    image = Image(list(get_program()), 25, 6)
    decoded = []
    for n in range(image.height):
        row = []
        for m in range(image.width):
            for i, layer in enumerate(image.layers):
                pixel = layer[n][m]
                if pixel == '2':
                    continue
                else:
                    print("Found non-transparent pixel {0} at layer {1} for coord {2},{3}".format(pixel, i, m, n))
                    row.append(pixel)
                    break
        decoded.append(row)

    return str("".join(["".join(row) for layer in decoded for row in layer]))


if __name__ == '__main__':
    print("Part one answer: {0}".format(part_one()))
    print("Part two answer: {0}".format(part_two()))
