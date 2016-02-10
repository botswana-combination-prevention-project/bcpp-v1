from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph


class CommunityComparisonPDF(object):

    def __init__(self, pdf_data):
        self.community1_name = pdf_data['community1']
        self.community2_name = pdf_data['community2']
        self.communities = "%s - %s" % (self.community1_name, self.community2_name)
        self.report_period = "%s - %s" % (pdf_data["start_date"], pdf_data["end_date"])
        self.report_title = "%s Report" % pdf_data['title']
        self.report_variables = pdf_data['report_variables']
        self.data = pdf_data['data']
        self.style = getSampleStyleSheet()
        self.p_style = self._paragraph_styles()

    def draw(self, output, story):
        from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

        PAGE_SIZE = A4
        MARGIN_SIZE = 15 * mm
        doc = BaseDocTemplate(output, pagesize=PAGE_SIZE, leftMargin=MARGIN_SIZE, rightMargin=MARGIN_SIZE,
                              topMargin=MARGIN_SIZE, bottomMargin=MARGIN_SIZE)
        main_frame = Frame(MARGIN_SIZE, MARGIN_SIZE, PAGE_SIZE[0] - 2 * MARGIN_SIZE, PAGE_SIZE[1] - 2 * MARGIN_SIZE,
                           leftPadding=0, rightPadding=0, bottomPadding=0, topPadding=0, id='main_frame')
        main_template = PageTemplate(id='main_template', frames=[main_frame])
        doc.addPageTemplates([main_template])
        doc.build(story)

    def build(self, output):
        from .lib.spreadsheet_table import SpreadsheetTable

        story = []
        self._populate_report_title(story)
        report_data = []
        self._populate_table_header(report_data)
        report_contents, extra_styles = self._populate_report()
        report_data.extend(report_contents)
        report_table = SpreadsheetTable(report_data, repeatRows=1)
        table_style = [
            ('LINEABOVE', (0, 0), (-1, 0), 0.25, colors.orange),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
        table_style.extend(extra_styles)
        report_table.setStyle(table_style)
        story.append(report_table)
        self.draw(output, story)

    def _populate_report_title(self, story):
        from reportlab.platypus.flowables import Spacer

        story.append(Paragraph(self.report_title, self.p_style['ReportName']))
        story.append(Paragraph(self.communities, self.p_style['CommunityName']))
        story.append(Paragraph(self.report_period, self.p_style['report_period']))
        story.append(Spacer(0, 3 * mm))

    def _populate_table_header(self, report_data):
        report_table_headers = [Paragraph(self.report_variables, self.p_style['report_vars'])]
        for header in [self.community1_name, self.community2_name]:
            report_table_headers.append(Paragraph(header, self.p_style['community_column']))
        report_data.append(report_table_headers)

    def _populate_report(self):
        from itertools import izip

        row_no = 0
        report_contents = []
        extra_styles = []
        empty_column = " "
        for sect1, sect2 in self.data:
            report_contents.append([sect1.display_title(), empty_column, empty_column])
            row_no += 1
            extra_styles.append(('BACKGROUND', (0, row_no), (2, row_no), colors.HexColor('#ffeb94')))
            extra_styles.append(('LINEBELOW', (0, row_no), (2, row_no), 1, colors.HexColor('#1f8dd6')))
            extra_styles.append(('FONT', (0, row_no), (1, row_no), 'Helvetica-Bold'))
            for comm1_row, comm2_row in izip(sect1.data, sect2.data):
                row_no += 1
                if row_no % 2 != 0:
                    extra_styles.append(('BACKGROUND', (0, row_no), (-1, row_no), colors.HexColor('#e1f2fa')))
                value1 = Paragraph(comm1_row.display_value(), self.p_style['value'])
                value2 = Paragraph(comm2_row.display_value(), self.p_style['value'])
                row_data = [comm1_row.label, value1, value2]
                report_contents.append(row_data)
        return (report_contents, extra_styles)

    def _paragraph_styles(self):
        from reportlab.lib.styles import ParagraphStyle, StyleSheet1
        from reportlab.lib.enums import TA_CENTER, TA_RIGHT

        stylesheet = StyleSheet1()
        stylesheet.add(ParagraphStyle(
            name='CommunityName',
            fontName='Helvetica',
            fontSize=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#505050'),
            leading=24,
        ))
        stylesheet.add(ParagraphStyle(
            name='ReportName',
            fontName='Helvetica',
            fontSize=18,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#565656'),
        ))
        stylesheet.add(ParagraphStyle(
            name='community_column',
            fontName='Helvetica',
            fontSize=14,
            leading=30,
            alignment=TA_RIGHT,
            textColor=colors.HexColor('#565656'),
        ))
        stylesheet.add(ParagraphStyle(
            name='report_period',
            fontName='Helvetica',
            fontSize=11,
            leading=22,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#333333'),
        ))
        stylesheet.add(ParagraphStyle(
            name='report_vars',
            fontName='Helvetica',
            fontSize=14,
            leading=26,
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
            fontSize=9,
            textColor=colors.HexColor('#444444'),
        ))
        return stylesheet
