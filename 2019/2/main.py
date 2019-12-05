INPUT_PATH = "input.txt"


def get_program():
    with open(INPUT_PATH) as fp:
        return [int(x) for x in fp.readline().split(',')]


def set_program_params(program, param1, param2):
    program[1], program[2] = param1, param2


def run_program(program):
    for i in range(0, len(program), 4):
        op = program[i]
        if op == 1:
            program[program[i + 3]] = program[program[i + 1]] + program[program[i + 2]]
        elif op == 2:
            program[program[i + 3]] = program[program[i + 1]] * program[program[i + 2]]
        elif op == 99:
            return
        else:
            print("Invalid op: {0}".format(op))


def part_one():
    program = get_program()
    set_program_params(program, 12, 2)

    run_program(program)
    return program[0]


def part_two():
    base_program = get_program()

    for noun in range(0, 100):
        for verb in range(0, 100):
            current_program = base_program.copy()
            set_program_params(current_program, noun, verb)
            run_program(current_program)
            if current_program[0] == 19690720:
                return 100 * noun + verb


if __name__ == '__main__':
    print("Part one answer: {0}".format(part_one()))
    print("Part two answer: {0}".format(part_two()))
