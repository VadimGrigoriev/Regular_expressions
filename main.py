import csv
import re


num_pattern = r'(\+7|8)\s*\(*(\d{3})\)*[\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})\s*\(*(доб\.)*\s*(\d+)*\)*'
num_sub = r'+7(\2)\3-\4-\5 \6\7'


def change_list(check_list):
    res_list = list()
    for data in check_list:
        fullname = ' '.join(data[:3]).split(' ')
        contact = [fullname[0], fullname[1], fullname[2], data[3], data[4],
                   re.sub(num_pattern, num_sub, data[5]).strip(), data[6]]
        res_list.append(contact)
    return res_list


def check_contact(check_list):
    for contact in check_list:
        for next_contact in check_list:
            if contact == next_contact:
                continue
            if contact[0] == next_contact[0] and contact[1] == next_contact[1]:
                if not contact[2]: contact[2] = next_contact[2]
                if contact[3] != next_contact[3]: contact[3] = f'{contact[3]};{next_contact[3]}'.strip(';')
                if contact[4] != next_contact[4]: contact[4] = f'{contact[4]};{next_contact[4]}'.strip(';')
                if contact[5] != next_contact[5]: contact[5] = f'{contact[5]};{next_contact[5]}'.strip(';')
                if contact[6] != next_contact[6]: contact[6] = f'{contact[6]};{next_contact[6]}'.strip(';')
    return check_list


def del_duplicate(check_list):
    res_list = []
    res_list.extend(contact for contact in check_list if contact not in res_list)
    return res_list


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    first_list = change_list(contacts_list)
    second_list = check_contact(first_list)
    final_list = del_duplicate(second_list)

    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(final_list)
