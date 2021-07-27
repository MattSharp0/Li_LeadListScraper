from xlsxwriter import Workbook
import os.path


def write_to_excel(link_list, list_title, path=''):
    '''
    Takes a list of links and writes them to an excel document called list_title

    :Params:
    List: link_list: list of strings
    Str: lead_list_name: name of lead list
    Str: path; defaults to Desktop directory
    '''
    print('\n- Writing list to excel...')

    if path == '':
        path = os.path.expanduser('~/Desktop')
    elif not os.path.isdir(path):
        print(
            f'\n- Error: Unable to locate path: {path}, defaulting to Desktop')
        path = os.path.expanduser('~/Desktop')

    list_title = list_title.replace('/', '')
    title = ((list_title.split()[0]) + ' leads')
    file_location = os.path.join(path, title + '.xlsx')

    wb = Workbook(f'{file_location}')
    sheet = wb.add_worksheet()
    sheet.write('A1', f'{title}')

    row, col = 1, 0
    for link in link_list:
        sheet.write(row, col, link)
        row += 1

    wb.close()
    print(f'\nSucces: saved {len(link_list)} lead links to {file_location}')
