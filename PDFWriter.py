#!/usr/bin/env python3

import os

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


def writePDF(pdf, key):
    # pathOnly = pathToWrite[:pathToWrite.rindex('/')]
    # fileOnly = pathToWrite[pathToWrite.rindex('/') + 1:]
    # os.makedirs(pathOnly, exist_ok=True)
    # os.chdir(pathOnly)



    #Register fonts and create styles
    pdfmetrics.registerFont(TTFont('Helvetica', 'Helvetica.ttc'))

    normal = getSampleStyleSheet()['Normal']
    normal.fontName = 'Helvetica'
    normal.leading = 15

    normalSpace = getSampleStyleSheet()['Normal']
    normalSpace.fontName = 'Helvetica'
    normalSpace.leading = 15
    normalSpace.spaceBefore = 6

    title = getSampleStyleSheet()['Heading1']
    title.fontName = 'Helvetica'





    doc = SimpleDocTemplate('static/{}.pdf'.format(key), pagesize=LETTER)
    modules = []

    #Create the title and headings
    modules.append(Paragraph("Tip Distribution Report", title))
    for head in pdf['heading']:
        modules.append(Paragraph(head, normal))
    modules.append(Paragraph('Total tips: $' + str(pdf['totalTips']), normalSpace))
    modules.append(Paragraph('Tip rate: $' + str(round(pdf['rate'], 3)), normal))

    #Print all the partner names
    data = []
    data.append(['Home Store', 'Partner Name', 'Partner Numbers', 'Tippable Hours', 'Tip Amount'])
    partners = pdf['partners']
    for partner in partners:
        data.append([partner['store'], '{}, {}'.format(partner['last'], partner['first']), partner['numbers'], partner['hours'].rjust(5, ' ').replace(' ', '  '), str(partner['tips']).rjust(2, ' ').replace(' ', '  ')])
    data.append(['Totals:', '', '', pdf['totalHours'], pdf['totalTips']])

    tableStyle = TableStyle([
            ('LINEBELOW', (0,0), (4,0), 1, colors.black),
            ('LINEABOVE', (0,-1), (-1,-1), 1, colors.black)
        ])
    widths = [0.9 * inch, 2 * inch, 1.5 * inch, 1.1 * inch, inch]
    table = Table(data, widths)
    table.setStyle(tableStyle)
    modules.append(table)

    doc.build(modules)





