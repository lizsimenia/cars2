import pattern_ch
from typing import Callable, Any, Dict

list_spec = [elem for elem in pattern_ch.info_pattern]
len_list_spec = [len(elem) for elem in pattern_ch.info_pattern]
limit = len(list_spec)

def is_no_spec(text:str) -> bool:
    ''' Функция проверки ввода на отсутствие спец символов'''
    spec = [chr(i) for i in range(33, 48)]+[chr(i) for i in range(58, 65)] +\
    [chr(i) for i in range(91, 97)] + [chr(i) for i in range(123, 127)]
    for elem in text:
        if elem in spec:
            print('ERROR: можно вводить только буквы и цифры')
            return 0
    return 1

def check_num_car(text:str) -> Any:
    '''Функция проверки корректности номера машины'''
    try:
        if len(text) >= 8\
            and text[0] in 'АВЕКМНОРСТУХ' and (0 <= int(text[1:4]) < 1000)\
            and text[4] in 'АВЕКМНОРСТУХ'\
            and text[5] in 'АВЕКМНОРСТУХ'and (0 <= int(text[-2:]) < 1000):
                return 1
        else: raise Exception
    except Exception:
        print("ERROR: некорректный номер машины")


def is_word(text:str) -> bool:
    ''' Функция проверки ввода только букв'''
    alfa = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    return all(i in alfa for i in text)

def unique_num(num:str)->bool:
    '''Функция проверки единственности номера'''
    if len(search_index(num)) == 0:
        return 1

def is_digit(num:str) -> float:
    ''' Функция проверки ввода на число '''
    try:
        return float(num)
    except Exception: print('ERROR: введите число')


def make_a_choice(key:str, data:list) -> int:
    """
    Функция задания характеристики из списка

    выбирает характеристику из предложенных
    с помощью ввода числа

    """
    num_list = {choice[0]: choice[1] for choice in enumerate(data)}
    print(key, ": ", *[num_list[i] + '(' + str(i+1) + ')' for i in num_list.keys()])
    while True:
        num = input( f'{key}: ')
        if is_digit(num):
            if 1 <= int(num) <= len(num_list):
                choice = num_list[int(num)-1]
                break
    return choice

def string_input(spec_name:str) -> str:
    while True:
        spec_value = input( f'{spec_name}: ')
        if is_no_spec(spec_value):
            if spec_name == 'Производитель':
                if is_word(spec_name):
                    break
                else:
                    print("ERROR: название производителя может состоять только из букв")
            elif spec_name == 'Номер машины':
                if check_num_car(spec_value):
                    if unique_num(spec_value):
                        break
                    else: print("ERROR: машина с таким номером существует в файле.")
            else:
                break
    return spec_value

def choose_input(spec_name):
    return str(make_a_choice(spec_name, pattern_ch.info_pattern[spec_name]))

def float_input(spec_name):
    return input( f'{spec_name}: ')

def input_data(spec_name):
    info_pattern_proxy = pattern_ch.info_pattern
    if info_pattern_proxy[spec_name] == 'str':
        spec_value = string_input(spec_name)
    elif isinstance(info_pattern_proxy[spec_name], list):
        spec_value = choose_input(spec_name)
    elif info_pattern_proxy[spec_name] == 'float':
        spec_value = float_input(spec_name)
    else:
        print("супер мега ошибка")
    return spec_value

def adding():
    with open('accounting.txt', 'a', encoding = 'UTF8') as file:
        info_pattern_proxy = pattern_ch.info_pattern
        for spec_name in info_pattern_proxy:
            spec_value = input_data(spec_name)
            file.write(spec_value +"\n")
        file.write("end")


def removal():
    num_car = input("Введите номер машины:")
    index = search_index(num_car)
    with open('accounting.txt', 'r', encoding='UTF8') as file:
        lines = file.readlines()
        for i in index:
            del lines[i:i+limit+1]
            with open('accounting.txt', 'w', encoding='UTF8') as file:
                file.writelines(lines)

def format_car(index:int)->str:
    '''Функция форматированного вывода характеристик одной машины'''
    with open('accounting.txt', 'r', encoding = 'UTF8') as file:
        list_spec = [elem for elem in pattern_ch.info_pattern]
        list_lines = file.readlines()
        start_index = index
        work = 0
        output_string = []
        print()
        for i in range(len(list_lines)):
            if "end" in list_lines[i] and work != 0:
                break
            if index == i or work >= 1:
                work += 1
                if start_index != 0:
                    output_string.append(f'{list_spec[(i-1)%limit]}: {list_lines[i][:-1]}')
                else:
                    output_string.append(f'{list_spec[i%limit]}: {list_lines[i][:-1]}')
        return output_string

def display()->None:
    '''Функция вывода основной информации машин учёта в виде таблицы'''
    with open('accounting.txt', 'r', encoding = 'UTF8') as file:
        print('     '.join(list_spec[:7]))
        index, start = 0, 1
        for line in file:
            display_car_string(index, start)
            index += (limit+1)
            start += 1

def change()->Any:
    ''' Функция изменения одной характеристики машины по ее номору'''
    num_car = input("Введите номер машины: ")
    for i, value in enumerate(format_car(search_index(num_car)[0])):
        print(f'{value} ({i+1})')
    num_spec = input("\nВыберите характеристику для изменения: ")
    if is_digit(num_spec):
        num_spec = int(num_spec)
        if 1 <= int(num_spec) <= 9:
            index_spec = search_index(num_car)[0] + int(num_spec) - 1
            new_data = input_data(list_spec[num_spec-1])
            with open('accounting.txt', 'r', encoding='UTF8') as file:
                lines = file.readlines()
                lines[index_spec] = new_data+'\n'
                with open('accounting.txt', 'w', encoding='UTF8') as file:
                    file.writelines(lines)
        else:
            print("ERROR")


def display_car_string(index, start=1):
    with open('accounting.txt', 'r', encoding = 'UTF8') as file:
        data_base = file.readlines()
        flag = 0
        for i, value in enumerate(data_base):
            if i == index:
                string_car = ""
                flag = 1
            if flag == 1:
                if index != 0:
                    tab = len_list_spec[(i-index//limit*limit)%limit-1] -len(value[:-1]) + 5
                else:
                    tab = len_list_spec[(i-index//limit*limit)%limit] -len(value[:-1]) + 5
                string_car += (value[:-1] + tab * ' ')
                if value[:-1] in pattern_ch.info_pattern['Тип коробки передач']:
                    print(start, string_car)
                    break

def search_index(spec:str)->int:
    with open('accounting.txt', 'r', encoding = 'UTF8') as file:
        lines = file.readlines()
        list_index = []
        flag, index = 0, -1
        num = 0
        for cur_index in range(len(lines)):
            if spec in lines[cur_index][:-1]:
                flag = 1
            if 'end' in lines[cur_index] and flag == 1:
                index = (cur_index// (limit-1) - 1) * (limit-1) + cur_index%(limit-1) -1
                flag = 0
                list_index.append(index)
        if flag == -1:
            print("ERROR: машин с таким параметром не существует")
        return list_index


def sorting()->Any:
    '''Функция вывода машин с одной и той же характеристикой'''
    spec = input("Введите значение общей характеристики для поиска: ")
    for i, value in enumerate(search_index(spec)):
        if i == 0:
            print('     '.join(list_spec[:7]))
        display_car_string(value, i+1)

def menu():
    """
    Функция вызова меню

    выборка одного из предложенных действий,
    выполение соотвествующей функции выбранного действия
    """
    print(f"\n MENU\n\
          \n Выйти из меню (0)\
          \n Добавление машины в учёт (1)\
          \n Удаление машины из учета (2)\
          \n Отображение всего учёта (3)\
          \n Изменение характеристики машины (4)\
          \n Сортировка машин по характеристике (5)")

    act = input("\n Выберите команду (введите её номер): ")
    if act == '0':
        print("\nЗАВЕРШЕНИЕ РАБОТЫ \n")
        return 0
    elif act == '1':
        print("\nДОБАВЛЕНИЕ МАШИНЫ В УЧЁТ\n")
        adding()
    elif act == '2':
        print("\nУДАЛЕНИЕ МАШИНЫ ИЗ УЧЁТА\n")
        removal()
    elif act == '3':
        print("\nОТОБРАЖЕНИЕ ВСЕГО УЧЁТА\n")
        display()
    elif act == '4':
        print("\nИЗМЕНЕНИЕ ХАРАКТЕРИСТИКИ МАШИНЫ\n")
        change()
    elif act == '5':
        print("\nСОРТИРОВКА МАШИН ПО ХАРАКТЕРИСТИКЕ\n")
        sorting()
    elif act == '6':
        print("\nОТОБРАЖЕНИЕ ХАРАКТЕРИСТИК ОДНОЙ МАШИНЫ\n")
        display()
    else:
        print("ERROR: такой команды не существует\n")


while True:
    if menu() == 0:
        break
