from xlsxwriter import Workbook


def write_to_excel(link_list, list_title, path=''):
    '''
    Takes a list of links and writes them to an excel document called list_title

    :Params:
    List: link_list: list of strings
    Str: lead_list_name: name of lead list
    Str: path; defaults to same dir as module
    '''
    print('\n    Writing list to excel...')

    title = ((list_title.split()[0]) + ' leads')

    wb = Workbook(f'{path}{title}.xlsx')
    sheet = wb.add_worksheet()
    sheet.write('A1', f'{title}')

    row, col = 1, 0
    for link in link_list:
        sheet.write(row, col, link)
        row += 1

    wb.close()
    print(f'\nSaved {len(link_list)} lead links to {path}{title}.xlsx')
