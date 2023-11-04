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
len_list_spec  = [len(elem) for elem in info_pattern]
limit = len(list_spec)

while True:
    # termination_check()

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
                            sym = [let in alfa for let in spec_value]
                            if len(sym) == len(spec_value):
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
                                            list_index = []
                                            flag, index = 0, -1
                                            for cur_index in range(len(lines)):
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
                            if len(sym) == len(spec_value):
                                with open('accounting.txt', 'a', encoding = 'UTF8') as file:
                                    file.write(spec_value +'\n')
                                break
                            else:
                                print("ERROR: название цвета может состоять только из букв")
                        else:
                            with open('accounting.txt', 'a', encoding = 'UTF8') as file:
                                file.write(spec_value+'\n')
                            break

            # elif list_spec[spec_name] == 'float':
            #     spec_value = float_input(spec_name)

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
                            if 1 <= int(num) <= len(choose_dict) :
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
        # removal()
    elif act == '3':
        print("\nОТОБРАЖЕНИЕ ВСЕГО УЧЁТА\n")
        # display()
    elif act == '4':
        print("\nИЗМЕНЕНИЕ ХАРАКТЕРИСТИКИ МАШИНЫ\n")
        # change()
    elif act == '5':
        print("\nСОРТИРОВКА МАШИН ПО ХАРАКТЕРИСТИКЕ\n")
        # sorting()
    elif act == '6':
        print("\nОТОБРАЖЕНИЕ ХАРАКТЕРИСТИК ОДНОЙ МАШИНЫ\n")
        # display()
    else:
        print("ERROR: такой команды не существует\n")
