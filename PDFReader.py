#!/usr/bin/env python3

import pdfplumber

def scanPDF(file, totalTips):    
    with pdfplumber.open(file) as pdf:
        pages = pdf.pages
        heading = []
        partners = []
        for i, page in enumerate(pages):
            #print('\n\nPage {}'.format(i + 1))
            lines = page.extract_text().split('\n')
            for i, line in enumerate(lines):
                if line[0:5].isnumeric():
                    partners.append({
                        'store': line[0:5],
                        'last': line[6:line.index(',')],
                        'first': line[line.index(',') + 2:line.index('US') - 1],
                        'numbers': line[line.index('US'):line.index(' ', line.index('US'))],
                        'hours': line[line.index(' ', line.index('US')) + 1:],
                    })
                elif i > 0 and i < 5:
                    heading.append(line)
        lastPage = pages[len(pages) - 1]
        lines = lastPage.extract_text().split('\n')
        lastLine = lines[len(lines) - 1]
        totalHours = float(lastLine[lastLine.index(':') + 2:])

        # totalTips =  351 #int(input('Enter the total amount of tips:'))
        rate = totalTips / totalHours
        print('Total hours:', totalHours)
        print('Raw rate:', rate)
        print('Tip rate:', round(rate, 2), end = '\n\n')

        while True:    
            total = 0
            for partner in partners:
                print('Store:', partner['store'])
                print('First:', partner['first'])
                print('Last:', partner['last'])
                print('Numbers:', partner['numbers'])
                print('Hours:', partner['hours'])
                rawTips = float(partner['hours']) * rate
                tips = round(rawTips)
                partner['tips'] = tips
                print('Raw tips:', rawTips)
                print('Tips:', tips, end = '\n\n')
                total += tips
            if total <= totalTips:
                break
            rate -= 0.001

        print('\n\nTotal after payout:', total)
        print('Final rate:', rate)

        return {
            'heading': heading,
            'partners': partners,
            'totalHours': totalHours,
            'totalTips': totalTips,
            'rate': rate,
        }




