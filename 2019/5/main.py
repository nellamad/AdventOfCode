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
    params = read_params(p, i, op_to_param_length[op], modes)

    #print('Parsed {0} as {1} {2} with params {3}'.format(modes_ops, modes, op, params))
    return op, params


def run_program(p):
    i = 0
    while i < len(p):
        #print(p)
        op, params = parse_instruction(p, i)
        if op == 1:
            p[p[i + 3]] = params[0] + params[1]
        elif op == 2:
            p[p[i + 3]] = params[0] * params[1]
        elif op == 3:
            print("Input:")
            p[p[i + 1]] = int(input())
        elif op == 4:
            print(p[p[i + 1]])
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


def part_one():
    # input 1
    program = get_program()
    run_program(program)


def part_two():
    # input 5
    program = get_program()
    run_program(program)


if __name__ == '__main__':
    #part_one()
    part_two()
