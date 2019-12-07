from sys import maxsize
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


def get_param_value(p, i, mode):
    if mode == '0':
        return int(p[p[i]])
    elif mode == '1':
        return int(p[i])
    else:
        print('Unrecognized parameter mode: {0}'.format(mode))


def read_params(p, i, num, modes):
    params = []
    for offset in range(1, num + 1):
        if offset > len(modes):
            mode = '0'
        else:
            mode = modes[-offset]
        params.append(get_param_value(p, i + offset, mode))
    return params


def parse_instruction(p, i):
    #print('Parsing index {0} of {1}'.format(i, p))
    modes_ops = str(p[i])
    modes, op = modes_ops[:-2], int(modes_ops[-2:])
    assert op in op_to_param_length, "unrecognized op: {0}".format(op)
    params = read_params(p, i, op_to_param_length[op], modes)

    #print('Parsed {0} as {1} {2} with params {3}'.format(modes_ops, modes, op, params))
    return op, params


def run_program(p, inputs):
    i = 0
    #print("running with inputs: {0}".format(inputs))
    while i < len(p):
        op, params = parse_instruction(p, i)
        if op == 1:
            p[p[i + 3]] = params[0] + params[1]
        elif op == 2:
            p[p[i + 3]] = params[0] * params[1]
        elif op == 3:
            #print("Ingesting input")
            input = inputs.pop()
            #print("popped {0}".format(input))
            p[p[i + 1]] = input
        elif op == 4:
            #print(p[p[i + 1]])
            return p[p[i + 1]]
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
            return
        else:
            print("Invalid op: {0}".format(op))

        i += len(params) + 1


def resume_program(p, i, inputs):
    #print("running with inputs: {0}".format(inputs))
    while i < len(p):
        op, params = parse_instruction(p, i)
        if op == 1:
            p[p[i + 3]] = params[0] + params[1]
        elif op == 2:
            p[p[i + 3]] = params[0] * params[1]
        elif op == 3:
            #print("Ingesting input")
            input = inputs.pop()
            #print("popped {0}".format(input))
            p[p[i + 1]] = input
        elif op == 4:
            #print(p[p[i + 1]])
            return i + len(params) + 1, p[p[i + 1]]
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
            return i + len(params) + 1, None
        else:
            print("Invalid op: {0}".format(op))

        i += len(params) + 1


def compute_permutations(s):
    def compute_permutations_rec(char_counts, prefix):
        if char_counts is None:
            return None
        if len(char_counts) == 0:
            return [prefix]

        new_permutations = []
        for char, char_count in char_counts.items():
            new_counts = char_counts.copy()
            new_counts[char] -= 1
            if new_counts[char] == 0:
                del new_counts[char]
            new_permutations += compute_permutations_rec(new_counts, prefix + char)

        return new_permutations

    if s is None:
        return None
    char_counts = {}
    for c in s:
        char_counts[c] = char_counts[c] + 1 if c in char_counts else 1

    return compute_permutations_rec(char_counts, '')


class Amplifier:
    def __init__(self, i, program, phase):
        self.program = program
        self.phase = phase
        self.inputs = [phase]
        self.instruction_pointer = 0
        int_to_id = {
            0: 'A',
            1: 'B',
            2: 'C',
            3: 'D',
            4: 'E'
        }
        self.id = int_to_id[i]

    def run(self, inputs):
        assert len(self.inputs) == 0 or self.program == get_program(), "Running wrong version of program"
        combined = inputs + self.inputs
        #print("{0}:{1} running input {2}".format(self.id, self.phase, combined))
        self.inputs = []
        self.instruction_pointer, output = resume_program(self.program, self.instruction_pointer, combined.copy())
        #print("{0}:{1} ran input {2} and output {3}".format(self.id, self.phase, combined, output))
        return output


def part_one():
    program = get_program()
    max_output = -maxsize
    for setting in compute_permutations("01234"):
        input_signal = 0
        for i in range(5):
            input_signal = run_program(program.copy(), [input_signal, setting[i]])
            #print("output: {0}".format(input_signal))
        max_output = max(max_output, input_signal)
    return max_output


def part_two():
    program = get_program()
    max_output = -maxsize
    for setting in compute_permutations("56789"):
        input_signal = 0
        amplifiers = [Amplifier(i, program.copy(), int(setting[i])) for i in range(5)]
        output = None
        while input_signal is not None:
            for a in amplifiers:
                input_signal = a.run([input_signal])
            # input_signal is now the output of E
            if input_signal is not None:
                output = input_signal
                max_output = max(max_output, output)

    return max_output


if __name__ == '__main__':
    print("Part one answer: {0}".format(part_one()))
    print("Part two answer: {0}".format(part_two()))
