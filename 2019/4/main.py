def is_valid(password):
    digits = str(password)
    if len(digits) != 6:
        return False
    has_duplicate = False
    for i in range(1, len(digits)):
        if digits[i] < digits[i - 1]:
            return False
        if digits[i] == digits[i - 1]:
            has_duplicate = True

    return has_duplicate


def is_valid_stricter(password):
    digits = str(password)
    if len(digits) != 6:
        return False
    has_exact_duplicate = False
    repeat_length = 1
    for i in range(1, len(digits)):
        if digits[i] < digits[i - 1]:
            return False
        if digits[i] == digits[i - 1]:
            repeat_length += 1
        else:
            if repeat_length == 2:
                has_exact_duplicate = True
            repeat_length = 1

    return has_exact_duplicate or repeat_length == 2


def count_possible_passwords(lower, upper):
    count = 0
    for candidate in range(lower, upper + 1):
        count += bool(is_valid(candidate))

    return count


def count_possible_passwords_stricter(lower, upper):
    count = 0
    for candidate in range(lower, upper + 1):
        count += bool(is_valid_stricter(candidate))

    return count


def part_one():
    return count_possible_passwords(367479, 893698)


def part_two():
    return count_possible_passwords_stricter(367479, 893698)


if __name__ == '__main__':
    print("Part one answer: {0}".format(part_one()))
    print("Part two answer: {0}".format(part_two()))
