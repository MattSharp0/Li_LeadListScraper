from xlsxwriter import Workbook
import os.path
import csv


def write_to_csv(data_list, file_name, path=''):
    '''
    Takes a list of links and writes them to a CSV file. Formatted for upload to Zoominfo Enhance

    :Params:
    List: link_list: list of strings
    Str: lead_list_name: name of lead list
    Str: path; defaults to Desktop directory
    '''
    file_location = os.path.join(path, file_name + '_leads.csv')

    csv_data_list = []
    for lead in data_list:
        full_name = lead.pop(0)
        name = (full_name.split(',')[0]).split()
        first_name, last_name = name[0], name[-1]
        lead.insert(0, last_name)
        lead.insert(0, first_name)
        csv_data_list.append(lead)

    with open(file_location, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['First Name', 'Last Name', 'Title', 'Account',
                        'Location', 'Link', 'Email', 'Phone'])
        writer.writerows(csv_data_list)


def write_to_excel(data_list, file_name, path=''):
    '''
    Takes a list of links and writes them to an .xlsx document

    :Params:
    List: link_list: list of strings
    Str: lead_list_name: name of lead list
    Str: path; defaults to Desktop directory
    '''

    file_location = os.path.join(path, file_name + '_leads.xlsx')

    wb = Workbook(file_location)
    sheet = wb.add_worksheet()
    sheet.write('A1', file_name)
    sheet.write('A2', 'Name')
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
