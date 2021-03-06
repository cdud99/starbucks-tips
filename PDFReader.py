#!/usr/bin/env python3

import pdfplumber

def validatePDF(pdf):
    documentTemplate = [
        'Tip Distribution Report',
        'Store Number:',
        'Time Period:',
        'Executed By:',
        'Executed On:',
        'Data Disclaimer Includes all updates made at least 15 minutes before the report'
    ]

    pdfGiven = []
    for i, line in enumerate(pdf.pages[0].extract_text().split('\n')):
        if i == 0:
            pdfGiven.append(line)
        elif i > 0 and i < 5:
            pdfGiven.append(line if line.find(':') == -1 else line[:line.find(':') + 1])
        elif i == 5:
            pdfGiven.append(line)

    if pdfGiven != documentTemplate:
        return False

    return True

def scanPDF(file, totalTips):

    # Open tip report generated by Starbucks
    with pdfplumber.open(file) as pdf:

        if not validatePDF(pdf):
            return None

        # Create variable "returnData" which will hold the dictionary being returned
        # Add 'partners' with an empty list so it can be appended to later
        # Add total tips now so it can be used to write the new pdf later
        returnData = {'partners': [], 'totalTips': totalTips}

        # Loop through every page of the tip report (Though it's typically only one)
        for x, page in enumerate(pdf.pages):

            # Extract all text and split it by '\n' to get a list with every line
            lines = page.extract_text().split('\n')

            # Set the heading text with list comprehension using the "lines" variable
            if x == 0:
                returnData['heading'] = [line for i, line in enumerate(lines) if i > 0 and i < 6]

            # Loop through all lines
            for line in lines:

                # If first five characters are numbers it indicates a store number
                # and therefore a line with partner info
                if line[0:5].isnumeric():
                    returnData['partners'].append({
                        'store': line[0 : 5],
                        'last': line[6 : line.index(',')],
                        'first': line[line.index(',') + 2 : line.index(' US')],
                        'numbers': line[line.index('US') : line.index(' ', line.index('US'))],
                        'hours': float(line[line.index(' ', line.index('US')) : ]),
                    })

                # If its the last page of the document and the last line of the page
                elif pdf.pages.index(page) == len(pdf.pages) - 1 and lines.index(line) == len(lines) - 1:
                    returnData['totalHours'] = float(line[line.index(':') + 2:])

        # Set the calculated tip rate
        returnData['rate'] = totalTips / returnData['totalHours']

        while True:   

            # Variable to total up amount payed to partners 
            total = 0

            # For each partner calculate the amount of tips they earn based off the
            # current tip rate and add that amount to the total payout
            for partner in returnData['partners']:
                partner['tips'] = round(partner['hours'] * returnData['rate'])
                total += partner['tips']

            # If the payout is less than or equal to the amount of tips break the loop
            if total <= totalTips:
                break

            # If the payout requires more than the amount of tips reduce the rate
            returnData['rate'] -= 0.001

        # Set the total payout to be used in the summary when creating the new report
        returnData['totalAfterPayout'] = total

        return returnData


# For debugging

if __name__ == '__main__':

    pdf = scanPDF('/Users/cdudley/Downloads/TipReport_6:20_6:26.pdf', 400)

    # print(pdf['heading'], end='\n\n')
    # print('Total hours:', pdf['totalHours'])
    # print('Total tips:', pdf['totalTips'])
    # print('Total after payout:', pdf['totalAfterPayout'])
    # print('Rate:', pdf['rate'], end='\n\n')
    # for partner in pdf['partners']:
    #     print('Store:', partner['store'])
    #     print('First:', partner['first'])
    #     print('Last:', partner['last'])
    #     print('Numbers:', partner['numbers'])
    #     print('Hours:', partner['hours'])
    #     print('Tips:', partner['tips'], end='\n\n')


