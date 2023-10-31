import pattern_ch
from typing import Callable, Any, Dict

def is_no_spec(text:str) -> Any:
    ''' Функция проверки ввода на отсутствие спец символов'''
    spec = [chr(i) for i in range(33, 48)]+[chr(i) for i in range(58, 65)] +\
    [chr(i) for i in range(91, 97)] + [chr(i) for i in range(123, 127)]
    for elem in text:
        if elem in spec:
            print('ERROR: можно вводить только буквы и цифры')
            return 0
    return 1

def check_num_car(text:str) -> bool:
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
    return 1
    # try:
    #     index = search_num(num)
    #     return index == None
    # except Exception:
    #     return 1

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


def adding():
    with open('accounting.txt', 'w', encoding = 'UTF8') as file:
        info_pattern_proxy = pattern_ch.info_pattern
        for spec_name in info_pattern_proxy:
            spec_value = ""
            if info_pattern_proxy[spec_name] == 'str':
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
            elif isinstance(info_pattern_proxy[spec_name], list):
                spec_value = str(make_a_choice(spec_name, info_pattern_proxy[spec_name]))
            elif info_pattern_proxy[spec_name] == 'float':
                spec_value = input( f'{spec_name}: ')
            else:
                print("супер мега ошибка")

            file.write(spec_value+"\n")
        file.write("end")


def removal():
    pass


def display_cur_car(index:int)->None:
    '''Функция форматированного вывода характеристик одной машины'''
    with open('accounting.txt', 'r', encoding = 'UTF8') as file:
        list_spec = [elem for elem in pattern_ch.info_pattern]
        list_lines = file.readlines()
        start_index = index
        work = 0
        print()
        for i in range(len(list_lines)):
            if "end" in list_lines[i] and work != 0:
                break
            if index == i or work >= 1:
                work += 1
                if start_index != 0:
                    print(f'{list_spec[(i-1)%9]}: {list_lines[i][:-1]}')
                else:
                    print(f'{list_spec[i%9]}: {list_lines[i][:-1]}')

def display()->None:
    '''Функция вывода основной информации машин учёта в виде таблицы'''
    with open('accounting.txt', 'r', encoding = 'UTF8') as file:
        list_spec = [elem for elem in pattern_ch.info_pattern]
        string_spec = '    '.join(list_spec[:3])
        print(string_spec)
        start, num = 1, 1
        string_car = ""
        for line in file:
            if line[:-1] not in pattern_ch.info_pattern['Тип двигателя'] and start == 1:
                string_car += (line[:-1]+ '     ' +'\t')
            else:
                if 'end' in line:
                    start = 1
                    print(str(num) +' '+ string_car)
                    num += 1
                    string_car = ""
                else:
                    start = 0

        # string_car = ""
        # k,flag = 0, 0
        # for line in file:
        #     if "end" in line:
        #         k += 1
        #         print(k, string_car[:len(string_spec)+10])
        #         string_car = ""
        #     else:
        #         if flag == 3:
        #         string_car += (line[:-1] + "        ")

def change(num_car:str)->Any:
    ''' Функция изменения одной характеристики машины по ее номору'''
    # num_car = input("Введите номер машины: ")
    # search(num_car)
    pass

def search(*args, **kwargs)->Any:
    '''Функция машин с одной и той же характеристикой'''
    spec = args
    spec = input("Введите слово для поиска: ")
    with open('accounting.txt', 'r', encoding = 'UTF8') as file:
        lines = file.readlines()
        flag = 0
        search_index = 0
        for cur_index in range(len(lines)):
            if spec in lines[cur_index]:
                flag = 1
            if 'end' in lines[cur_index] and flag == 1:
                search_index = (cur_index// 9 - 1) * 9 + cur_index%9
                display_cur_car(search_index)
        if flag != 1:
            print("ERROR: машин с таким параметром не существует")

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
          \n Изменение характеристик машины (4)\
          \n Поиск машин по характеристике (5)")

    act = input("\n Выберите команду (введите её номер): ")
    if act == '0':
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
        print("\nПОИСК МАШИНЫ\n")
        search()
    else:
        print("ERROR: неверный ввод\n")


while True:
    if menu() == 0:
        break
