#TODO весь функциональный стиль переписать в процедурный, расскрыть встроенные функции

info_pattern = {'Номер машины': 'str',
                'Производитель': 'str',
                'Модельный ряд': 'str',
                'Цвет': 'str',
                'Тип двигателя': ['бензиновые', 'дизельные', 'газовые', 'газодизельные', 'роторно-поршневые'],
                'Тип привода': ['задний', 'передний', 'полный'],
                'Тип коробки передач': ['механическая', 'автоматическая', 'роботизированная', 'вариативная (бесступенчатая)'],
                'Длинa кузова(м)': 'float',
                'Ширина кузова(м)':'float'}

list_spec  = [elem for elem in info_pattern]
limit = 0
len_list_spec = []
for elem in list_spec:
    limit += 1
    i = 0
    for i_sym in elem:
        i += 1
    len_list_spec.append(i)

while True:
    # воостановление работы
    with open('accounting.txt', 'r', encoding = 'UTF8') as file:
        lines = file.readlines()
        if 'end' not in lines[-1]:
            while True:
                request = input("Продолжить добавление машины в учёт? да(1) нет(2) ")
                if request == '1':
                    for _ in lines:
                        len_lines += 1
                    if len_lines // limit != 0:
                        start_spec = len(lines) % (limit+1)
                    else:
                        start_spec = len(lines) % limit
                    for spec_name in list_spec[start_spec:]:
                        if info_pattern[spec_name] == 'str':
                            while True:
                                spec_value = input( f'{spec_name}: ')
                                special_signs = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.',\
                                                '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
                                # проверка на специальные символы
                                for elem in spec_value:
                                    if elem in special_signs:
                                        print('ERROR: можно вводить только буквы и цифры')
                                        break
                                else:
                                    if spec_name == 'Производитель':
                                        # проверка на вхождение только букв
                                        alfa = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфх\
                                                цчшщъыьэюяABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
                                        sym = [1 for let in spec_value if let in alfa]
                                        len_sym, len_spec_value = 0, 0
                                        for _ in sym:
                                            len_sym += 1
                                        for _ in spec_value:
                                            len_spec_value += 1
                                        if len_sym == len_spec_value:
                                            with open('accounting.txt', 'a', encoding = 'UTF8') as file:
                                                file.write(spec_value+'\n')
                                            break
                                        else:
                                            print("ERROR: название производителя может состоять только из букв")

                                    elif spec_name == 'Номер машины':
                                        # проверка на правильность номера
                                        try:
                                            if len(spec_value) >= 8\
                                                and spec_value[0] in 'АВЕКМНОРСТУХ' and (0 <= int(spec_value[1:4]) < 1000)\
                                                and spec_value[4] in 'АВЕКМНОРСТУХ'\
                                                and spec_value[5] in 'АВЕКМНОРСТУХ'and (0 <= int(spec_value[-2:]) < 1000):
                                                    # проверка на уникальность номера
                                                    with open('accounting.txt', 'r', encoding = 'UTF8') as file:
                                                        lines = file.readlines()
                                                        len_lines = 0
                                                        for _ in lines:
                                                            len_lines += 1
                                                        list_index = []
                                                        flag, index = 0, -1
                                                        for cur_index in range(len_lines):
                                                            if spec_value == lines[cur_index][:-1]:
                                                                flag = 1
                                                            if 'end' in lines[cur_index] and flag == 1:
                                                                index = (cur_index// (limit-1) - 1) * (limit-1) + cur_index%(limit-1) -1
                                                                flag = 0
                                                                list_index.append(index)
                                                                break
                                                    if len(list_index) == 0:
                                                        with open('accounting.txt', 'a', encoding = 'UTF8') as file:
                                                            file.write(spec_value+'\n')
                                                        break
                                                    else: print("ERROR: машина с таким номером существует в файле.")
                                            else: raise Exception
                                        except Exception:
                                            print("ERROR: некорректный номер машины")

                                    elif spec_name == 'Цвет':
                                        # проверка на вхождение только букв
                                        alfa = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфх\
                                                цчшщъыьэюяABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
                                        sym = [1 for let in spec_value if let in alfa]
                                        len_sym, len_spec_value = 0, 0
                                        for _ in sym:
                                            len_sym += 1
                                        for _ in spec_value:
                                            len_spec_value += 1
                                        if len_sym == len_spec_value:
                                            with open('accounting.txt', 'a', encoding = 'UTF8') as file:
                                                file.write(spec_value +'\n')
                                            break
                                        else:
                                            print("ERROR: название цвета может состоять только из букв")
                                    else:
                                        with open('accounting.txt', 'a', encoding = 'UTF8') as file:
                                            file.write(spec_value+'\n')
                                        break

                        elif info_pattern[spec_name] == 'float':
                            # длина кузова, ширина кузова
                            while True:
                                num = input( f'{spec_name}: ')
                                # проверка на число
                                try:
                                    float(num)
                                    spec_value = float(num)
                                    with open('accounting.txt', 'a', encoding = 'UTF8') as file:
                                            file.write(str(spec_value)+'\n')
                                            break
                                except Exception: print('ERROR: введите число')

                        else:
                            choose_dict = {}
                            num = 1
                            # создание выборки
                            for choice in info_pattern[spec_name]:
                                choose_dict[num] = choice
                                num += 1
                            print(spec_name, ": ", *[choose_dict[i] + '(' + str(i) + ')' for i in choose_dict.keys()])
                            while True:
                                num = input( f'{spec_name}: ')
                                # проверка выборки
                                try:
                                    float(num)
                                    try:
                                        len_choose_dict = 0
                                        for _ in choose_dict:
                                            len_choose_dict += 1
                                        if 1 <= int(num) <= len_choose_dict:
                                            choice = choose_dict[int(num)]
                                            with open('accounting.txt', 'a', encoding = 'UTF8') as file:
                                                file.write(choice+'\n')
                                            break
                                    except Exception:
                                        print("ERROR: введите номер целочисленно")
                                except Exception: print('ERROR: введите число')
                    with open('accounting.txt', 'a', encoding = 'UTF8') as file:
                        file.write("end\n")
                    break
                elif request == '2':
                    for i, value in enumerate(lines):
                        if value[:-1] == 'end':
                            start = i+1
                    with open('accounting.txt', 'r', encoding='UTF8') as file:
                        lines = file.readlines()
                        del lines[start:]
                        with open('accounting.txt', 'w', encoding='UTF8') as file:
                            file.writelines(lines)
                    break
                else:
                    print("ERROR: введите да или нет")

    print("\n MENU\n\
          \n Выйти из меню (0)\
          \n Добавление машины в учёт (1)\
          \n Удаление машины из учета (2)\
          \n Отображение всего учёта (3)\
          \n Изменение характеристики машины (4)\
          \n Сортировка машин по характеристике (5)")

    try:
        act = input("\n Выберите команду (введите её номер): ")
        if act == '0':
            print("\nЗАВЕРШЕНИЕ РАБОТЫ \n")
            break

        elif act == '1':
            print("\nДОБАВЛЕНИЕ МАШИНЫ В УЧЁТ\n")
            for spec_name in list_spec:
                # номер машины, производитель, модельный ряд, цвет
                if info_pattern[spec_name] == 'str':
                    while True:
                        spec_value = input( f'{spec_name}: ')
                        special_signs = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.',\
                                        '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
                        # проверка на специальные символы
                        for elem in spec_value:
                            if elem in special_signs:
                                print('ERROR: можно вводить только буквы и цифры')
                                break
                        else:
                            if spec_name == 'Производитель':
                                # проверка на вхождение только букв
                                alfa = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфх\
                                        цчшщъыьэюяABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
                                sym = [1 for let in spec_value if let in alfa]
                                len_sym, len_spec_value = 0, 0
                                for _ in sym:
                                    len_sym += 1
                                for _ in spec_value:
                                    len_spec_value += 1
                                if len_sym == len_spec_value:
                                    with open('accounting.txt', 'a', encoding = 'UTF8') as file:
                                        file.write(spec_value+'\n')
                                    break
                                else:
                                    print("ERROR: название производителя может состоять только из букв")

                            elif spec_name == 'Номер машины':
                                # проверка на правильность номера
                                try:
                                    if len(spec_value) >= 8\
                                        and spec_value[0] in 'АВЕКМНОРСТУХ' and (0 <= int(spec_value[1:4]) < 1000)\
                                        and spec_value[4] in 'АВЕКМНОРСТУХ'\
                                        and spec_value[5] in 'АВЕКМНОРСТУХ'and (0 <= int(spec_value[-2:]) < 1000):
                                            # проверка на уникальность номера
                                            with open('accounting.txt', 'r', encoding = 'UTF8') as file:
                                                lines = file.readlines()
                                                len_lines = 0
                                                for _ in lines:
                                                    len_lines += 1
                                                list_index = []
                                                flag, index = 0, -1
                                                for cur_index in range(len_lines):
                                                    if spec_value == lines[cur_index][:-1]:
                                                        flag = 1
                                                    if 'end' in lines[cur_index] and flag == 1:
                                                        index = (cur_index// (limit-1) - 1) * (limit-1) + cur_index%(limit-1) -1
                                                        flag = 0
                                                        list_index.append(index)
                                                        break
                                            if len(list_index) == 0:
                                                with open('accounting.txt', 'a', encoding = 'UTF8') as file:
                                                    file.write(spec_value+'\n')
                                                break
                                            else: print("ERROR: машина с таким номером существует в файле.")
                                    else: raise Exception
                                except Exception:
                                    print("ERROR: некорректный номер машины")

                            elif spec_name == 'Цвет':
                                # проверка на вхождение только букв
                                alfa = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфх\
                                        цчшщъыьэюяABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
                                sym = [1 for let in spec_value if let in alfa]
                                len_sym, len_spec_value = 0, 0
                                for _ in sym:
                                    len_sym += 1
                                for _ in spec_value:
                                    len_spec_value += 1
                                if len_sym == len_spec_value:
                                    with open('accounting.txt', 'a', encoding = 'UTF8') as file:
                                        file.write(spec_value +'\n')
                                    break
                                else:
                                    print("ERROR: название цвета может состоять только из букв")
                            else:
                                with open('accounting.txt', 'a', encoding = 'UTF8') as file:
                                    file.write(spec_value+'\n')
                                break

                elif info_pattern[spec_name] == 'float':
                    # длина кузова, ширина кузова
                    while True:
                        num = input( f'{spec_name}: ')
                        # проверка на число
                        try:
                            float(num)
                            spec_value = float(num)
                            with open('accounting.txt', 'a', encoding = 'UTF8') as file:
                                    file.write(str(spec_value)+'\n')
                                    break
                        except Exception: print('ERROR: введите число')

                else:
                    choose_dict = {}
                    num = 1
                    # создание выборки
                    for choice in info_pattern[spec_name]:
                        choose_dict[num] = choice
                        num += 1
                    print(spec_name, ": ", *[choose_dict[i] + '(' + str(i) + ')' for i in choose_dict.keys()])
                    while True:
                        num = input( f'{spec_name}: ')
                        # проверка выборки
                        try:
                            float(num)
                            try:
                                len_choose_dict = 0
                                for _ in choose_dict:
                                    len_choose_dict += 1
                                if 1 <= int(num) <= len_choose_dict:
                                    choice = choose_dict[int(num)]
                                    with open('accounting.txt', 'a', encoding = 'UTF8') as file:
                                        file.write(choice+'\n')
                                    break
                            except Exception:
                                print("ERROR: введите номер целочисленно")
                        except Exception: print('ERROR: введите число')

            with open('accounting.txt', 'a', encoding = 'UTF8') as file:
                file.write("end\n")

        elif act == '2':
            print("\nУДАЛЕНИЕ МАШИНЫ ИЗ УЧЁТА\n")
            num_car= input("Введите номер машины: ")
            try:
                if len(num_car) >= 8\
                    and num_car[0] in 'АВЕКМНОРСТУХ' and (0 <= int(num_car[1:4]) < 1000)\
                    and num_car[4] in 'АВЕКМНОРСТУХ'\
                    and num_car[5] in 'АВЕКМНОРСТУХ'and (0 <= int(num_car[-2:]) < 1000):
                        with open('accounting.txt', 'r', encoding = 'UTF8') as file:
                            lines = file.readlines()
                            list_index = []
                            flag = 0
                            for cur_index in range(len(lines)):
                                if num_car == lines[cur_index][:-1]:
                                    flag == 1
                                    list_index.append(cur_index)
                                    break
                            if flag == 0:
                                print("ERROR: машины с таким номером не существует")
                        if len(list_index) != 0:
                            with open('accounting.txt', 'r', encoding='UTF8') as file:
                                lines = file.readlines()
                                for i in list_index:
                                    del lines[i:i+limit+1]
                                    with open('accounting.txt', 'w', encoding='UTF8') as file:
                                        file.writelines(lines)
                else: raise Exception
            except Exception:
                print("ERROR: некорректный номер машины")

        elif act == '3':
            print("\nОТОБРАЖЕНИЕ ВСЕГО УЧЁТА\n")
            with open('accounting.txt', 'r', encoding = 'UTF8') as file:
                print('     '.join(list_spec[:7]))
                index, start = 0, 1
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
                        if value[:-1] in info_pattern['Тип коробки передач']:
                            print(start, string_car)
                            index += (limit+1)
                            start += 1

        elif act == '4':
            print("\nИЗМЕНЕНИЕ ХАРАКТЕРИСТИКИ МАШИНЫ\n")
            num_car = input("Введите номер машины: ")
            try:
                if len(num_car) >= 8\
                    and num_car[0] in 'АВЕКМНОРСТУХ' and (0 <= int(num_car[1:4]) < 1000)\
                    and num_car[4] in 'АВЕКМНОРСТУХ'\
                    and num_car[5] in 'АВЕКМНОРСТУХ'and (0 <= int(num_car[-2:]) < 1000):
                        with open('accounting.txt', 'r', encoding = 'UTF8') as file:
                            lines = file.readlines()
                            list_index = []
                            for cur_index in range(len(lines)):
                                if num_car == lines[cur_index][:-1]:
                                    list_index.append(cur_index)
                                    break
                            else:
                                print("ERROR: машины с таким номером не существует")

                        if len(list_index)!=0:
                            start_index = list_index[0]
                            work = 0
                            output_string = []
                            print()
                            for i in range(len(lines)):
                                if "end" in lines[i] and work != 0:
                                    break
                                if start_index == i or work >= 1:
                                    work += 1
                                    if start_index != 0:
                                        output_string.append(f'{list_spec[i%(limit+1)]}: {lines[i][:-1]}')
                                    else:
                                        output_string.append(f'{list_spec[i%limit]}: {lines[i][:-1]}')

                            for i, value in enumerate(output_string):
                                if i >= 3:
                                    print(f'{value} ({i+1-3})')
                                else:
                                    print(f'{value}')

                            num_spec = input("\nВыберите характеристику для изменения: ")
                            try:
                                float(num_spec)
                                num_spec = int(num_spec)
                                if 1 <= num_spec <= 9-3:
                                    num_spec += 3
                                    index_spec = list_index[0] + num_spec - 1
                                    spec_name = list_spec[num_spec-1]
                                    if info_pattern[spec_name] == 'str':
                                        while True:
                                            spec_value = input( f'{spec_name}: ')
                                            special_signs = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.',\
                                                            '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
                                            # проверка на специальные символы
                                            for elem in spec_value:
                                                if elem in special_signs:
                                                    print('ERROR: можно вводить только буквы и цифры')
                                                    break
                                            else:
                                                if spec_name == 'Производитель':
                                                    # проверка на вхождение только букв
                                                    alfa = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфх\
                                                            цчшщъыьэюяABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
                                                    sym = [1 for let in spec_value if let in alfa]
                                                    len_sym, len_spec_value = 0, 0
                                                    for _ in sym:
                                                        len_sym += 1
                                                    for _ in spec_value:
                                                        len_spec_value += 1
                                                    if len_sym == len_spec_value:
                                                        break
                                                    else:
                                                        print("ERROR: название производителя может состоять только из букв")

                                                elif spec_name == 'Номер машины':
                                                    # проверка на правильность номера
                                                    try:
                                                        if len(spec_value) >= 8\
                                                            and spec_value[0] in 'АВЕКМНОРСТУХ' and (0 <= int(spec_value[1:4]) < 1000)\
                                                            and spec_value[4] in 'АВЕКМНОРСТУХ'\
                                                            and spec_value[5] in 'АВЕКМНОРСТУХ'and (0 <= int(spec_value[-2:]) < 1000):
                                                                # проверка на уникальность номера
                                                                with open('accounting.txt', 'r', encoding = 'UTF8') as file:
                                                                    lines = file.readlines()
                                                                    len_lines = 0
                                                                    for _ in lines:
                                                                        len_lines += 1
                                                                    list_index = []
                                                                    flag, index = 0, -1
                                                                    for cur_index in range(len_lines):
                                                                        if spec_value == lines[cur_index][:-1]:
                                                                            flag = 1
                                                                        if 'end' in lines[cur_index] and flag == 1:
                                                                            index = (cur_index// (limit-1) - 1) * (limit-1) + cur_index%(limit-1) -1
                                                                            flag = 0
                                                                            list_index.append(index)
                                                                            break
                                                                if len(list_index) == 0:
                                                                    break
                                                                else: print("ERROR: машина с таким номером существует в файле.")
                                                        else: raise Exception
                                                    except Exception:
                                                        print("ERROR: некорректный номер машины")

                                                elif spec_name == 'Цвет':
                                                    # проверка на вхождение только букв
                                                    alfa = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфх\
                                                            цчшщъыьэюяABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
                                                    sym = [1 for let in spec_value if let in alfa]
                                                    len_sym, len_spec_value = 0, 0
                                                    for _ in sym:
                                                        len_sym += 1
                                                    for _ in spec_value:
                                                        len_spec_value += 1
                                                    if len_sym == len_spec_value:
                                                        break
                                                    else:
                                                        print("ERROR: название цвета может состоять только из букв")
                                                else:
                                                    with open('accounting.txt', 'a', encoding = 'UTF8') as file:
                                                        file.write(spec_value+'\n')
                                                    break

                                    elif info_pattern[spec_name] == 'float':
                                        # длина кузова, ширина кузова
                                        while True:
                                            num = input( f'{spec_name}: ')
                                            # проверка на число
                                            try:
                                                float(num)
                                                spec_value = float(num)
                                                break
                                            except Exception: print('ERROR: введите число')

                                    else:
                                        choose_dict = {}
                                        num = 1
                                        # создание выборки
                                        for choice in info_pattern[spec_name]:
                                            choose_dict[num] = choice
                                            num += 1
                                        print(spec_name, ": ", *[choose_dict[i] + '(' + str(i) + ')' for i in choose_dict.keys()])
                                        while True:
                                            num = input( f'{spec_name}: ')
                                            # проверка выборки
                                            try:
                                                float(num)
                                                try:
                                                    len_choose_dict = 0
                                                    for _ in choose_dict:
                                                        len_choose_dict += 1
                                                    if 1 <= int(num) <= len_choose_dict:
                                                        spec_value = choose_dict[int(num)]
                                                        break
                                                except Exception:
                                                    print("ERROR: введите номер целочисленно")
                                            except Exception: print('ERROR: введите число')

                                    with open('accounting.txt', 'r', encoding='UTF8') as file:
                                        lines = file.readlines()
                                        lines[index_spec] = str(spec_value)+'\n'
                                        with open('accounting.txt', 'w', encoding='UTF8') as file:
                                            file.writelines(lines)
                                else:
                                    print("ERROR: некорректный номер характеристики")

                            except Exception: print('ERROR: введите число')
                else: raise Exception
            except Exception:
                print("ERROR: некорректный номер машины")

        elif act == '5':
            print("\nСОРТИРОВКА МАШИН ПО ХАРАКТЕРИСТИКЕ\n")
            # sorting()
        elif act == '6':
            print("\nОТОБРАЖЕНИЕ ХАРАКТЕРИСТИК ОДНОЙ МАШИНЫ\n")
            # display()
        else:
            raise Exception
    except Exception:
        print("ERROR: такой команды не существует\n")
