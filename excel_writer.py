from xlsxwriter import Workbook
import os.path


def write_to_excel(link_list, list_title, path='Desktop'):
    '''
    Takes a list of links and writes them to an excel document called list_title

    :Params:
    List: link_list: list of strings
    Str: lead_list_name: name of lead list
    Str: path; defaults to Desktop directory
    '''
    print('\n    Writing list to excel...')

    if path == 'Desktop':
        path = os.path.expanduser('~/Desktop')
    elif not os.path.isdir(path):
        print(f'Error: Unable to locate path: {path}')
        path = os.path.expanduser('~/Desktop')

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
    print(f'\nSaved {len(link_list)} lead links to {file_location}')
