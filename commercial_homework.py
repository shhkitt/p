def third(x, left, right):
    if x[3] == 1959:
        return left
    return right


def second(x, left, middle, right):
    if x[2] == 1957:
        return left
    if x[2] == 1984:
        return middle
    return right


def work6(x):

    if x[4] == 1986:
        if x[1] == 2018:
            return third(x, second(x, 3, 2, 1), 0)
        if x[1] == 1967:
            return second(x, 7, 6, third(x, 5, 4))
        return 8
    if x[4] == 2004:
        return second(x, 12, 11, third(x, 10, 9))
    return 13


def work7(input_number):
    c1 = input_number & (2 ** 9 - 1)
    c2 = (input_number & ((2 ** 9 - 1) << 9)) >> 9
    c3 = (input_number & ((2 ** 6 - 1) << 18)) >> 18
    c4 = (input_number & ((2 ** 8 - 1) << 24)) >> 24
    return hex((c2 << 23) | (c1 << 14) | (c3 << 8) | c4)

def main(fields):
    # Создаем маску для всех битовых полей
    mask = 0
    for bit_range in [(0, 5), (6, 11), (12, 16), (17, 23), (24, 24)]:
        start, end = bit_range
        for i in range(start, end + 1):
            mask |= (1 << i)

    # Получаем значения битовых полей и применяем маску
    n1 = (int(fields.get('N1', '0'), 16) << 0) & mask
    n2 = (int(fields.get('N2', '0'), 16) << 6) & mask
    n3 = (int(fields.get('N3', '0'), 16) << 12) & mask
    n4 = (int(fields.get('N4', '0'), 16) << 17) & mask
    n5 = (int(fields.get('N5', '0'), 16) << 24) & mask

    # Собираем все биты вместе
    value = hex( n1 | n2 | n3 | n4 | n5 )

    return value

import re


def work8(input_str):
    match = re.findall(r'<block>\s*var\s*(-?\w+)\s*\|>\s*(\w+)\s*\.\s*</block>,', input_str)
    parse_list = list()
    for i in range(len(match)):
        parse_list.append((match[i][1], int(match[i][0])))
    return parse_list


def work9(table):
    new_table = []
    for row in table:
        name, number = row[1:3]

        name = name.split(" ")[1]
        tel, number = number.split(";")[::]
        tel = tel[:-2] + "-" + tel[-2:]
        number = "{:.4f}".format(float(number))
        new_row = [name, tel, number]
        print(name, tel, number)
        if new_row not in new_table:
            new_table.append(new_row)

    new_table = sorted(new_table, key=lambda x: x[0])

    new_table = [[new_table[j][i] for j in range(len(new_table))] for i in range(len(new_table[0]))]

    return new_table


class MealyError(BaseException):
    def __init__(self, method_name) -> None:
        self.method_name = method_name
        super().__init__(method_name)


class MealyAutomata:
    dict_of_states = {
        'A': {'check': ('B', 0), 'chain': None, 'edit': None, "rig": None},
        'B': {'check': None, 'chain': ('C', 1), 'edit': None, "rig": None},
        'C': {'check': None, 'chain': None, 'edit': ('D', 2), "rig": None},
        'D': {'check': ('E', 3), 'chain': None, 'edit': None, "rig": None},
        'E': {'check': ('G', 5), 'chain': None, 'edit': ('F', 4), "rig": ('H', 6)},
        'F': {'check': ('G', 7), 'chain': ('A', 10), 'edit': ('H', 9), "rig": ('B', 8)},
        'G': {'check': None, 'chain': None, 'edit': ('H', 11), "rig": None},
        'H': {'check': None, 'chain': None, 'edit': None, "rig": None},

    }

    def __init__(self):
        self.state = 'A'

    def do(self, method_name):
        supposed_state = self.dict_of_states[self.state][method_name]
        if supposed_state is not None:
            self.state = supposed_state[0]
            return supposed_state[1]
        else:
            raise MealyError(method_name)

    def check(self):
        return self.do('check')

    def chain(self):
        return self.do('chain')

    def edit(self):
        return self.do('edit')

    def rig(self):
        return self.do('rig')


def work10():
    return MealyAutomata()


def test():
    o = work10()
    o.check()
    o.chain()
    o.edit()
    o.check()
    o.rig()
    o.state = 'E'
    o.check()
    o.edit()
    o.state = 'E'
    o.edit()
    o.check()
    o.state = 'F'
    o.rig()
    o.state = 'F'
    o.chain()
    o.state = 'F'
    o.edit()
    try:
        o.check()
    except MealyError as e:
        pass
    try:
        o.chain()
    except MealyError as e:
        pass
    try:
        o.edit()
    except MealyError as e:
        pass
    try:
        o.rig()
    except MealyError as e:
        pass


import struct as s


def parse_f(b_stream, offset):
    f1 = list(s.unpack_from('2i', b_stream, offset))
    offset += 4 * 2
    f2 = s.unpack_from('b', b_stream, offset)[0]
    offset += 1
    f3 = s.unpack_from('d', b_stream, offset)[0]
    offset += 8
    f4 = s.unpack_from('Q', b_stream, offset)[0]
    offset += 8
    f5_size = s.unpack_from('H', b_stream, offset)[0]
    offset += 2
    f5_addr = s.unpack_from('I', b_stream, offset)[0]
    offset += 4
    f5 = list(s.unpack_from('{0}B'.format(f5_size), b_stream, f5_addr))
    return {'F1': f1, 'F2': f2, 'F3': f3, 'F4': f4, 'F5': f5}, offset


def parse_e(b_stream, offset):
    e1, offset = parse_f(b_stream, offset)
    e2 = s.unpack_from('f', b_stream, offset)[0]
    offset += 4
    e3 = s.unpack_from('i', b_stream, offset)[0]
    offset += 4
    e4 = s.unpack_from('q', b_stream, offset)[0]
    offset += 8
    e5 = s.unpack_from('H', b_stream, offset)[0]
    offset += 2
    e6 = s.unpack_from('h', b_stream, offset)[0]
    offset += 2
    return {'E1': e1, 'E2': e2, 'E3': e3, 'E4': e4, 'E5': e5, 'E6': e6}, offset


def parse_d(b_stream, offset):
    d1 = s.unpack_from("h", b_stream, offset)[0]
    offset += 2
    d2 = s.unpack_from("h", b_stream, offset)[0]
    offset += 2
    return {'D1': d1, 'D2': d2}, offset


def parse_c(b_stream, offset):
    c1 = list(s.unpack_from("3b", b_stream, offset))
    offset += 3
    c2, offset = parse_d(b_stream, offset)
    return {'C1': c1, 'C2': c2}, offset


def parse_b(b_stream, offset):
    b1, offset = parse_c(b_stream, offset)
    b2 = s.unpack_from("i", b_stream, offset)[0]
    return {'B1': b1, 'B2': b2}, offset


def parse_a(b_stream, offset):

    a1 = s.unpack_from(">I", b_stream, offset)[0]
    offset += 4
    a2 = list()
    for i in range(3):
        b, offset = parse_b(b_stream, offset)
        a2.append(b)
    print(a2)
    a3, offset = parse_e(b_stream, offset)
    a4 = s.unpack_from(">I", b_stream, offset)[0]
    return {'A1': a1, 'A2': a2, 'A3': a3, 'A4': a4}, offset


def work11(stream):
    offset = stream.find(b'0x1a0x570x530x41') + 5
    return parse_a(stream, offset)[0]
