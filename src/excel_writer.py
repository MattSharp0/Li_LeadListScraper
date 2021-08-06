from os import mkdir
from xlsxwriter import Workbook
import os.path


def write_to_excel(data_list, list_title, path=''):
    '''
    Takes a list of links and writes them to an excel document called list_title

    :Params:
    List: link_list: list of strings
    Str: lead_list_name: name of lead list
    Str: path; defaults to Desktop directory
    '''
    print('\n- Writing list to excel...')

    if path == '':
        path = os.path.expanduser('~/Desktop/leads')
        if not os.path.isdir(path):
            mkdir(path)
    elif not os.path.isdir(path):
        print(
            f'\n- Error: Unable to locate path: {path}, defaulting to Desktop')
        path = os.path.expanduser('~/Desktop/')
        mkdir(path)

    BAD_CHARS = '!@#$%^&*{}[]+=\\|/.,><~`\'\":;'

    file_name = (list_title.split('[')[0]).strip()

    for char in BAD_CHARS:
        file_name = (file_name.title()).replace(char, '')

    # file_name = file_name.replace('/', '')
    # name = ((file_name.split()[0]) + ' leads')
    file_location = os.path.join(path, file_name + '_leads.xlsx')

    wb = Workbook(f'{file_location}')
    sheet = wb.add_worksheet()
    sheet.write('A1', list_title)
    sheet.write('A2', 'Lead name')
    sheet.write('B2', 'Title')
    sheet.write('C2', 'Account')
    sheet.write('D2', 'Location')
    sheet.write('E2', 'Link')

    row, col = 2, 0
    for lead in data_list:
        col = 0
        while col < 5:
            for item in lead:
                sheet.write(row, col, item)
                col += 1
        row += 1

    wb.close()
    print(f'\nSucces: saved {len(data_list)} lead links to {file_location}')
