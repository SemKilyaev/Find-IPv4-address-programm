import Find_IP
import ipaddress


def test_max_element():
    ip_list_test1 = ['192.168.20.12',
                     '192.168.20.58',
                     '192.168.20.100',
                     '192.168.20.128']
    assert Find_IP.max_element(ip_list_test1) == 128
    ip_list_test2 = ['192.168.20.115',
                     '192.168.20.130',
                     '192.168.20.20',
                     '192.168.20.255']
    assert Find_IP.max_element(ip_list_test2) == 255
    ip_list_test3 = ['192.168.20.0']
    assert Find_IP.max_element(ip_list_test3) == 0


def test_min_element():
    ip_list_test = ['192.168.20.129',
                    '192.168.20.224',
                    '192.168.20.226',
                    '192.168.20.230']
    assert Find_IP.min_element(ip_list_test) == 129
    ip_list_test2 = ['192.168.20.0',
                     '192.168.20.10',
                     '192.168.20.20',
                     '192.168.20.255']
    assert Find_IP.max_element(ip_list_test2) == 0
    ip_list_test3 = ['192.168.20.255']
    assert Find_IP.max_element(ip_list_test3) == 255


def test_ip_network():
    ip_list_test1 = ['192.168.20.129',
                     '192.168.20.224',
                     '192.168.20.226',
                     '192.168.20.230']
    assert Find_IP.ip_network(ip_list_test1) == '192.168.20.'
    ip_list_test2 = ['192.190.48.129',
                     '192.190.48.224',
                     '192.190.48.226',
                     '192.190.48.230']
    assert Find_IP.ip_network(ip_list_test2) == '192.190.48.'


def test_find_under_web():
    ip_list_test = ['192.168.20.129',
                    '192.168.20.224',
                    '192.168.20.226',
                    '192.168.20.230']
    assert Find_IP.find_under_web(ip_list_test) == 30


def test_find_4_oktet():
    ip_list_test = ['192.168.20.129',
                    '192.168.20.224',
                    '192.168.20.226',
                    '192.168.20.230']
    assert Find_IP.find_4_oktet(ip_list_test) == 252
    ip_list_test2 = ['192.168.20.3',
                     '192.168.20.4',
                     '192.168.20.5',
                     '192.168.20.6']
    assert Find_IP.find_4_oktet(ip_list_test2) == 64


def test_find_ip():
    ip_list_test = ['192.168.20.129',
                    '192.168.20.224',
                    '192.168.20.226',
                    '192.168.20.230']
    assert Find_IP.find_ip(ip_list_test) == ipaddress.IPv4Network('192.168.20.128/25')
