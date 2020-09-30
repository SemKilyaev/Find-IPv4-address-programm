import ipaddress
import sys
import argparse
import re

# Для тестов
# ip_list =['192.168.20.129',
# '192.168.20.224',
# '192.168.20.226',
# '192.168.20.230']
ip_list = []  # Для запуска программы


# Функция для получения параметров командной строки
def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=argparse.FileType(mode='r', bufsize=-1, encoding=None, errors=None))
    return parser

# Функция для получения первых трех октетов ip адресов
def ip_network(ip_list) -> str:
    count = 0
    a = ''
    b = ''
    for g in ip_list:
        count += 1
        if count == 1:
            a = g
        elif count == len(ip_list):
            b = g
    c: list = a.split('.')
    t: list = b.split('.')
    net: str = ''
    for i in c:
        # Счетчик отслеживает сколько октетов прошло
        count: int = 0
        for j in t:
            count += 1
            if count == 4:
                break
            if i == j:
                net = net + i + '.'
    return net

# Функция для поиска ip адреса с самым большим четвертым октетом
def max_element(ip_list) -> int:
    max_el: int = 0
    for i in ip_list:
        a: list = i.split('.')
        count: int = 0
        for j in a:
            count += 1
            if count == 4:
                if int(j) > max_el:
                    max_el = int(j)
    return max_el


# Функция для поиска ip адреса с наименьшим четвертым октетом
def min_element(ip_list) -> int:
    min_el: int = 255
    for i in ip_list:
        a: list = i.split('.')
        count: int = 0
        for j in a:
            count += 1
            if count == 4:
                if int(j) < min_el:
                    min_el = int(j)
    return min_el


# Функция для поиска префикса, в зависимости от числа ip адресов
def find_under_web(ip_list) -> int:
    if len(ip_list) == 1:
        return 32
    elif len(ip_list) == 2:
        return 31
    elif len(ip_list) <= 4:
        return 30
    elif len(ip_list) <= 8:
        return 29
    elif len(ip_list) <= 16:
        return 28
    elif len(ip_list) <= 32:
        return 27
    elif len(ip_list) <= 64:
        return 26
    elif len(ip_list) <= 128:
        return 25
    elif len(ip_list) <= 255:
        return 24


# Функция для поиска 4 октета, как точки начала последующего поиска подсетей
def find_4_oktet(ip_list) -> int:
    max_el: int = max_element(ip_list)
    if max_el == 0:
        return max_el
    elif max_el >= 192:
        if find_under_web(ip_list) == 31:
            return 254
        elif find_under_web(ip_list) == 30:
            return 252
        elif find_under_web(ip_list) == 29:
            return 248
        elif find_under_web(ip_list) == 28:
            return 240
        elif find_under_web(ip_list) == 27:
            return 234
        elif find_under_web(ip_list) == 26:
            return 192
        return max_el
    elif max_el >= 128 and max_el < 192:
        return 192
    elif max_el >= 64 and max_el < 128:
        return 128
    elif max_el >= 0 and max_el < 64:
        return 64


# Функция для поиска подсети
def find_ip(ip_list, a=find_under_web(ip_list), b=find_4_oktet(ip_list)):
    count: int = 0
    res: list = list()
    subnet = ipaddress.IPv4Network(f'{ip_network(ip_list)}{b}/{a}')
    for i in ip_list:
        new_ip = ipaddress.IPv4Address(i)
        h: bool = new_ip in subnet
        res.append(h)
    for j in res:
        if j == False:
            count = 0
        elif j == True:
            count = count + 1
    if count == len(res):
        return subnet
    elif count != len(res):
        return ip_reformat(a, b)


# Функция изменяющая параметры поиска функции find_ip()
def ip_reformat(a, b) -> int:
    if a == 32 and b != 0:
        return find_ip(ip_list, 32, b - 1)
    elif a == 32 and b == 0:
        return find_ip(ip_list, 31, 254)
    elif a == 31 and b != 0:
        return find_ip(ip_list, 31, b - 2)
    elif a == 31 and b == 0:
        return find_ip(ip_list, 30, 252)
    elif a == 30 and b != 0:
        return find_ip(ip_list, 30, b - 4)
    elif a == 30 and b == 0:
        return find_ip(ip_list, 29, 248)
    elif a == 29 and b != 0:
        return find_ip(ip_list, 29, b - 8)
    elif a == 29 and b == 0:
        return find_ip(ip_list, 28, 240)
    elif a == 28 and b != 0:
        return find_ip(ip_list, 28, b - 16)
    elif a == 28 and b == 0:
        return find_ip(ip_list, 27, 224)
    elif a == 27 and b != 0:
        return find_ip(ip_list, 27, b - 32)
    elif a == 27 and b == 0:
        return find_ip(ip_list, 26, 192)
    elif a == 26 and b != 0:
        return find_ip(ip_list, 26, b - 64)
    elif a == 26 and b == 0:
        return find_ip(ip_list, 25, 128)
    elif a == 25 and b != 0:
        return find_ip(ip_list, 25, b - 128)
    elif a == 25 and b == 0:
        return find_ip(ip_list, 24, 0)

# Для теста задокументировать все с 19 строки до 37
if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    ip_list_maybe = namespace.name.read().splitlines()
    # Проверка соответствия списка ip адресов формату IPv4
    count: int = 0
    print(ip_list_maybe)
    for i in ip_list_maybe:
        if re.match(r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', i):
            count += 1
        else:
            count = 0
    if count == len(ip_list_maybe):
        ip_list = ip_list_maybe
    elif count != len(ip_list_maybe):
        print('Contains non-IPv4 ip addresses')
        exit()

result = find_ip(ip_list)
print(f"Result net: {result}")
