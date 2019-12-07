from sys import maxsize
from itertools import permutations

INPUT_PATH = "input.txt"
op_to_param_length = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    99: 0
}


def get_program():
    with open(INPUT_PATH) as fp:
        return [int(x) for x in fp.readline().split(',')]


def parse_instruction(p, i):
    def read_params(p, i, num, modes):
        def get_param_value(p, i, mode):
            if mode == '0':
                return int(p[p[i]])
            elif mode == '1':
                return int(p[i])
            else:
                print('Unrecognized parameter mode: {0}'.format(mode))

        params = []
        for offset in range(1, num + 1):
            if offset > len(modes):
                mode = '0'
            else:
                mode = modes[-offset]
            params.append(get_param_value(p, i + offset, mode))
        return params

    modes_ops = str(p[i])
    modes, op = modes_ops[:-2], int(modes_ops[-2:])
    assert op in op_to_param_length, "unrecognized op: {0}".format(op)

    return op, read_params(p, i, op_to_param_length[op], modes)


def resume_program(p, i, inputs):
    def increment_instruction(i, params):
        return i + len(params) + 1

    # print("running with inputs: {0}".format(inputs))
    while i < len(p):
        op, params = parse_instruction(p, i)
        if op == 1:
            p[p[i + 3]] = params[0] + params[1]
        elif op == 2:
            p[p[i + 3]] = params[0] * params[1]
        elif op == 3:
            p[p[i + 1]] = inputs.pop()
        elif op == 4:
            return increment_instruction(i, params), p[p[i + 1]]
        elif op == 5:
            if params[0] != 0:
                i = params[1]
                continue
        elif op == 6:
            if params[0] == 0:
                i = params[1]
                continue
        elif op == 7:
            p[p[i + 3]] = int(params[0] < params[1])
        elif op == 8:
            p[p[i + 3]] = int(params[0] == params[1])
        elif op == 99:
            return None, None
        else:
            print("Invalid op: {0}".format(op))

        i = increment_instruction(i, params)


class Amplifier:
    def __init__(self, i, program, phase):
        self.id = chr(ord('A') + i)
        self.program = program
        self.inputs = [phase]
        self.instruction_pointer = 0

    def run(self, inputs):
        assert len(self.inputs) == 0 or self.program == get_program(), "Running wrong version of program"
        self.instruction_pointer, output = resume_program(self.program, self.instruction_pointer, inputs + self.inputs)
        self.inputs = []
        return output


def part_one():
    program = get_program()
    max_output = -maxsize
    for phase in permutations("01234"):
        input_signal = 0
        amplifiers = [Amplifier(i, program.copy(), int(phase[i])) for i in range(5)]
        for a in amplifiers:
            input_signal = a.run([input_signal])
        max_output = max(max_output, input_signal)
    return max_output


def part_two():
    program = get_program()
    max_output = -maxsize
    for phase in permutations("56789"):
        input_signal = 0
        amplifiers = [Amplifier(i, program.copy(), int(phase[i])) for i in range(5)]
        while input_signal is not None:
            for a in amplifiers:
                input_signal = a.run([input_signal])
            if input_signal is not None:
                max_output = max(max_output, input_signal)

    return max_output


if __name__ == '__main__':
    print("Part one answer: {0}".format(part_one()))
    print("Part two answer: {0}".format(part_two()))
