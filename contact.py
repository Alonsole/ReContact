from pprint import pprint
import re
import csv

def convert_contact():
    # TODO 1: выполните пункты 1-3 ДЗ
    """читаем адресную книгу в формате CSV в список contacts_list"""
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    # pprint(contacts_list)

    """создаю пустой словарь, чтобы хранить информацию"""
    final_contact = {}
    for contact in contacts_list:
        """Регулярное выражение для обработки номера"""
        pattern = re.compile(r'\+?(7|8)\s?\(?(\d{3})\)?[ -]?(\d{3})(?:[-]?)(\d{2})(?:[-]?)(\d{2})')
        sub_pattern = r'+7(\2)\3-\4-\5'
        contact_edit = (contact[5].replace('(', '').
                        replace(')', '').
                        replace('доб. ', 'доб.'))
        if contact[0].count(" ") > 0:
            """Если фамилия содержит пробел"""
            new_contact_name = contact[0].split()
            if len(new_contact_name) == 2:
                """Если в поле фамилия 2 слова"""
                final_contact[new_contact_name[0] + ' ' + new_contact_name[1]] = \
                [new_contact_name[0],
                 new_contact_name[1],
                 contact[2] if contact[2] != '' else final_contact[new_contact_name[0] + ' ' + new_contact_name[1]][2],
                 contact[3] if contact[3] != '' else final_contact[new_contact_name[0] + ' ' + new_contact_name[1]][3],
                 contact[4],
                 pattern.sub(sub_pattern, contact_edit) if contact[5] != '' else
                 final_contact[new_contact_name[0] + ' ' + new_contact_name[1]][5],
                 contact[6] if contact[6] != '' else
                 final_contact[new_contact_name[0] + ' ' + new_contact_name[1]][6]]

            else:
                final_contact[new_contact_name[0] + ' ' + new_contact_name[1]] = \
                  [new_contact_name[0],
                   new_contact_name[1],
                   new_contact_name[2],
                   contact[3],
                   contact[4],
                   pattern.sub(sub_pattern, contact_edit),
                   contact[6]]

        elif contact[0] != 'lastname':
            """Исключаю заголовок"""
            if contact[1].count(" ") > 0:
                """Если в поле Имя 2 слова"""
                new_contact_name = contact[1].split()
                final_contact[contact[0] + ' ' + new_contact_name[0]] = \
                  [contact[0],
                   new_contact_name[0],
                   new_contact_name[1],
                   contact[3],
                   contact[4],
                   pattern.sub(sub_pattern, contact_edit),
                   contact[6]]

    result = []
    result.append(contacts_list[0])
    """Получаю значения словаря и добавляю в список"""
    [result.append(value) for key, value in final_contact.items()]

    pprint(result)

    # TODO 2: сохраните получившиеся данные в другой файл
    # код для записи файла в формате CSV
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(result)

if __name__ == '__main__':
    convert_contact()
    print("Задача выполнена")