from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, LongTable, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_RIGHT


class AccrualPDFReport(object):

    def __init__(self, data):
        self.style = getSampleStyleSheet()
        self.p_style = self.para_style()
        self.report_data = data['report_data']
        self.data1 = data['community1_data']
        self.data2 = data['community2_data']
        self.community1 = self.data1[0].community
        self.community2 = self.data2[0].community
        self.date_range = "{start} - {end}".format(start=data['start_date'], end=data['end_date'])

    def display(self, request):
        from django.http import HttpResponse

        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = 'inline;filename=community_accrual.pdf'
        self.create(response)
        return response

    def create(self, destination):
        doc = SimpleDocTemplate(destination, pagesize=A4)
        story = []
        styles = self.para_style()
        comm_style = styles['CommunityName']
        h5 = self.style['Heading5']
        story.append(Paragraph("Community Accrual Report", styles['ReportName']))
        container_data = [[Paragraph(self.community1, comm_style), Paragraph(self.community2, comm_style)],
                          [Paragraph(self.date_range, h5), Paragraph(self.date_range, h5)]]
        report_style = self.inner_style()
        tables_data = []
        for community_data in [self.data1, self.data2]:
            table_data, added_styles = self.community_table_data(community_data)
            tables_data.append(table_data)
        tables = []
        report_style.extend(added_styles)
        for report_data in tables_data:
            table = LongTable(report_data, repeatRows=1)
            table.setStyle(report_style)
            tables.append(table)
        container_data.append(tables)
        container_table = Table(container_data, 2 * [3.6 * inch])
        container_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.HexColor('#ed4694')),
        ]))
        story.append(container_table)
        doc.build(story)

    def draw(self, output, story):
        from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

        MARGIN_SIZE = 15 * mm
        PAGE_SIZE = A4

        doc = BaseDocTemplate(output, pagesize=PAGE_SIZE, leftMargin=MARGIN_SIZE, rightMargin=MARGIN_SIZE,
                              topMargin=MARGIN_SIZE, bottomMargin=MARGIN_SIZE)
        main_frame = Frame(MARGIN_SIZE, MARGIN_SIZE, PAGE_SIZE[0] - 2 * MARGIN_SIZE, PAGE_SIZE[1] - 2 * MARGIN_SIZE,
                           leftPadding=0, rightPadding=0, bottomPadding=0, topPadding=0, id='main_frame')
        main_template = PageTemplate(id='main_template', frames=[main_frame])
        doc.addPageTemplates([main_template])
        doc.build(story)

    def build_up(self):
        from .lib.spreadsheet_table import SpreadsheetTable
        from reportlab.platypus.flowables import PageBreak, Spacer
        from django.http import HttpResponse
        from itertools import izip

        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = 'inline;filename=community_accrual.pdf'

        story = []
        hd1 = self.p_style['ReportName']
        hd2 = self.p_style['CommunityName']
        hd3 = self.style["Heading5"]
        story.append(Paragraph("Community Accrual Report", hd1))
        story.append(Spacer(0, 5 * mm))
        report_data = []
        empty_column = " "
        # report_spacer = ["   ", "   "]
        report_headers = [Paragraph(self.community1, hd2), empty_column]
        report_headers.append(empty_column)
        report_headers.extend([Paragraph(self.community2, hd2), empty_column])
        date_range = Paragraph(self.date_range, hd3)
        report_period = [date_range, empty_column]
        report_period.append(empty_column)
        report_period.extend([date_range, empty_column])
        report_data.append(report_headers)
        report_data.append(report_period)

        row_no = 1
        report_numbers = []
        add_styles = []
        for sect1, sect2 in izip(self.data1, self.data2):
            report_numbers.append([sect1.display_title(), empty_column, empty_column, sect1.display_title()])
            row_no += 1
            add_styles.append(('BACKGROUND', (0, row_no), (1, row_no), colors.HexColor('#ffeb94')))
            add_styles.append(('BACKGROUND', (3, row_no), (4, row_no), colors.HexColor('#ffeb94')))
            add_styles.append(('SPAN', (0, row_no), (1, row_no)))
            add_styles.append(('SPAN', (3, row_no), (4, row_no)))
            add_styles.append(('LINEBELOW', (0, row_no), (1, row_no), 1, colors.HexColor('#1f8dd6')))
            add_styles.append(('LINEBELOW', (3, row_no), (4, row_no), 1, colors.HexColor('#1f8dd6')))
            add_styles.append(('FONT', (0, row_no), (-1, row_no), 'Helvetica-Bold'))
            for row1, row2 in izip(sect1.data, sect2.data):
                row_no += 1
                if row_no % 2 != 0:
                    add_styles.append(('BACKGROUND', (0, row_no), (-1, row_no), colors.HexColor('#e1f2fa')))
                value1 = Paragraph(row1.display_value(), self.p_style['value'])
                value2 = Paragraph(row2.display_value(), self.p_style['value'])
                row_data = [row1.label, value1, empty_column, row2.label, value2]
                report_data.append(row_data)
        report_data.extend(report_numbers)
        report_table = SpreadsheetTable(report_data, repeatRows=2)
        table_style = [
            # ('GRID', (0, 0), (-1, -1), 0.25, colors.gray),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.orange),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (3, 0), (4, 0)),
            ('SPAN', (3, 1), (4, 1)),
        ]
        add_styles.append(('LINEAFTER', (1, 0), (1, -1), 5, colors.white))
        table_style.extend(add_styles)
        report_table.setStyle(table_style)
        story.append(report_table)
        self.draw(response, story)
        return response

    def inner_style(self):
        return [
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#1f8dd6')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFEB94')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#e1f2fa')])
        ]

    def community_table_data(self, community_context_data):
        data = []
        row_no = -1
        add_styles = []
        for i, component in enumerate(community_context_data):
            print i
            data.append([component.display_title()])
            row_no += 1
            add_styles.append(('BACKGROUND', (0, row_no), (-1, row_no), colors.HexColor('#ffeb94')))
            add_styles.append(('LINEBELOW', (0, row_no), (-1, row_no), 1, colors.HexColor('#1f8dd6')))
            add_styles.append(('FONT', (0, row_no), (-1, row_no), 'Helvetica-Bold'))
            for datarow in component.data:
                row_data = []
                row_no += 1
                row_data.append(Paragraph(datarow.label, self.p_style['normal']))
                row_data.append(Paragraph(datarow.display_value(), self.p_style['value']))
                data.append(row_data)
        return (data, add_styles)

    def para_style(self):
        from reportlab.lib.styles import ParagraphStyle, StyleSheet1

        stylesheet = StyleSheet1()
        stylesheet.add(ParagraphStyle(
            name='CommunityName',
            fontName='Helvetica',
            fontSize=16,
            textColor=colors.HexColor('#656565'),
            leading=18,
        ))
        stylesheet.add(ParagraphStyle(
            name='ReportName',
            fontName='Helvetica',
            fontSize=18,
            leading=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#565656'),
        ))
        stylesheet.add(ParagraphStyle(
            name='normal',
            fontName='Helvetica',
            fontSize=8,
            textColor=colors.HexColor('#333333'),
        ))
        stylesheet.add(ParagraphStyle(
            name='value',
            alignment=TA_RIGHT,
            fontName='Helvetica',
            fontSize=8,
            textColor=colors.HexColor('#505050'),
        ))
        return stylesheet
