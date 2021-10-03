from xlsxwriter import Workbook
import os.path
import csv


def write_to_csv(data_list: list, domain: str, file_name: str, path: str = ''):
    '''
    Takes a list of links and writes them to a CSV file. Formatted for upload to Zoominfo Enhance

    :Params:
    List: link_list: list of strings
    Str: lead_list_name: name of lead list
    Str: path; defaults to Desktop directory
    '''
    file_location = os.path.join(path, file_name + '_leads.csv')

    data_for_csv = []

    if domain:
        for lead in data_list:
            csv_lead = [lead[0], lead[1], domain]
            data_for_csv.append(csv_lead)
    else:
        for lead in data_list:
            csv_lead = [lead[0], lead[1], lead[3]]

            data_for_csv.append(csv_lead)

    with open(file_location, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['First Name', 'Last Name', 'Company'])
        writer.writerows(data_for_csv)


def write_to_excel(data_list: list, file_name: str, path: str = ''):
    '''
    Takes a list of links and writes them to an .xlsx document

    :Params:
    List: link_list: list of strings
    Str: lead_list_name: name of lead list
    Str: path; defaults to Desktop directory
    '''

    file_location = os.path.join(path, file_name + '_leads.xlsx')

    xlsx_data_list = []
    for lead in data_list:
        full_name = lead.pop(0)
        name = (full_name.split(',')[0]).split()
        last_name = name[-1]
        first_names = name[0:(len(name)-1)]
        first_name = ' '.join(first_names)
        lead.insert(0, last_name)
        lead.insert(0, first_name)
        xlsx_data_list.append(lead)

    wb = Workbook(file_location)
    sheet = wb.add_worksheet()
    sheet.write('A1', file_name)
    sheet.write('A2', 'First Name(s)')
    sheet.write('B2', 'Last Name')
    sheet.write('C2', 'Title')
    sheet.write('D2', 'Account')
    sheet.write('E2', 'Location')
    sheet.write('F2', 'Notes')
    sheet.write('G2', 'Link')

    row, col = 2, 0
    for lead in xlsx_data_list:
        col = 0
        while col < 7:
            for item in lead:
                sheet.write(row, col, item)
                col += 1
        row += 1

    wb.close()
