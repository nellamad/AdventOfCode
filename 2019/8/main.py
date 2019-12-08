from sys import maxsize

INPUT_PATH = "input.txt"


def get_program():
    with open(INPUT_PATH) as fp:
        return fp.readline().strip()


class Pixel:
    pixel_to_display_char = {
        '0': ' ',
        '1': '#',
        '2': '?',
    }

    def __init__(self, colour):
        self.colour, self.display_colour = colour, self.pixel_to_display_char[colour]

    def __repr__(self):
        return self.colour

    def __str__(self):
        return self.colour

    def __eq__(self, other):
        return self.colour == other

    def __hash__(self):
        return self.colour.__hash__()


class Layer:
    def __init__(self, rows):
        self.rows = rows

    def __iter__(self):
        yield from self.rows

    def __getitem__(self, i):
        return self.rows[i]

    def count(self, elem):
        total = 0
        for row in self:
            total += row.count(elem)
        return total

    def print(self):
        for row in self.rows:
            print([p.display_colour for p in row])


class Image:
    def __init__(self, pixels, width, height):
        self.width, self.height = width, height
        self.layers = self.__decode__(pixels)

    def __decode__(self, pixels):
        layers = []
        while len(pixels) > 0:
            rows = []
            for n in range(self.height):
                row = []
                for m in range(self.width):
                    row.append(Pixel(pixels.pop(0)))
                rows.append(row)
            layers.append(Layer(rows))
        return layers

    def print(self):
        final_rows = []
        for n in range(self.height):
            row = []
            for m in range(self.width):
                for i, layer in enumerate(self.layers):
                    pixel = layer[n][m]
                    if pixel == '2':
                        continue
                    else:
                        row.append(pixel)
                        break
            final_rows.append(row)

        Layer(final_rows).print()
        # print("".join(["".join([str(p) for p in row]) for row in final_rows]))


def part_one():
    image = Image(list(get_program()), 25, 6)
    min_zero_layer, min_zeroes = 0, maxsize
    for i, layer in enumerate(image.layers):
        zeroes = layer.count('0')
        if zeroes < min_zeroes:
            min_zero_layer, min_zeroes = layer, zeroes

    ones, twos = min_zero_layer.count('1'), min_zero_layer.count('2')
    return ones * twos


def part_two():
    Image(list(get_program()), 25, 6).print()
    return "Read picture printed above"


if __name__ == '__main__':
    print("Part one answer: {0}".format(part_one()))
    print("Part two answer: {0}".format(part_two()))
