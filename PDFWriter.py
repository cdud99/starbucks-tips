#!/usr/bin/env python3

import os

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics





def writePDF(pdf, path):
    # "pdf" is a dictionary that holds various info that will be printed
    # on the pdf

    # Path is absolute and includes pdf file name


    # Register Helvetica Font (Won't work if system doesn't have this font)
    pdfmetrics.registerFont(TTFont('Helvetica', 'Helvetica.ttc'))

    # Create the normal font size
    normal = getSampleStyleSheet()['Normal']
    normal.fontName = 'Helvetica'
    normal.leading = 15

    # Create the normal font size with a space above it for new section of text
    normalSpace = getSampleStyleSheet()['Normal']
    normalSpace.fontName = 'Helvetica'
    normalSpace.leading = 15
    normalSpace.spaceBefore = 6

    # Font only used for the title
    title = getSampleStyleSheet()['Heading1']
    title.fontName = 'Helvetica'





    # Create the document that will build all the Flowable modules at the end
    doc = SimpleDocTemplate(path, pagesize=LETTER)
    
    # List that holds all the Flowables
    modules = []



    # Create the title flowable
    modules.append(Paragraph("Tip Distribution Report", title))

    # Create the heading which is copied from the original tip report

    # Includes information such as store number, partner who created the report,
    # date report was created, and days the report corresponds to
    for head in pdf['heading']:
        modules.append(Paragraph(head, normal))

    # Add a heading that shows the total amount in tips as well as the hourly tip rate
    modules.append(Paragraph('Total tips: $' + str(pdf['totalTips']), normalSpace))
    modules.append(Paragraph('Tip rate: $' + str(round(pdf['rate'], 3)), normal))



    # Print all the partner names in a table which are sorted in the PDFReader script and put in
    # the "pdf" dictionary

    # "data" variable holds all the lines of data that will be inserted into the table
    data = []

    # Create the heading
    data.append(['Home Store', 'Partner Name', 'Partner Numbers', 'Tippable Hours', 'Tip Amount'])

    # Adds each partners info on a new line
    for partner in pdf['partners']:

        partnerName = partner['last'] + ', ' + partner['first']

        # Right justifys text by adding a space, however two spaces equal one character
        # so this replaces the one space with two so it lines up in the document
        partnerHours = str(partner['hours']).rjust(5, ' ').replace(' ', '  ')
        partnerTips = str(partner['tips']).rjust(2, ' ').replace(' ', '  ')

        data.append([partner['store'], partnerName, partner['numbers'], partnerHours, partnerTips])
    
    # Create summary at the bottom of the table
    data.append(['Totals:', '', '', pdf['totalHours'], pdf['totalAfterPayout']])

    # Creates a table style that adds a line under the table heading and above the table summary
    tableStyle = TableStyle([
            ('LINEBELOW', (0,0), (4,0), 1, colors.black),
            ('LINEABOVE', (0,-1), (-1,-1), 1, colors.black)
        ])

    # Set the width of each column
    widths = [0.9 * inch, 2 * inch, 1.5 * inch, 1.1 * inch, inch]

    # Create the actual table flowable
    table = Table(data, widths)
    table.setStyle(tableStyle)
    modules.append(table)



    # Build the document with all flowables
    doc.build(modules)





