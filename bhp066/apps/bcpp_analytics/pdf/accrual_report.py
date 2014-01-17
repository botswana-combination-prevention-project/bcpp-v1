from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate,LongTable, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER


class AccrualPDFReport(object):

    def __init__(self, data):
        self.style = getSampleStyleSheet()
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
            table = LongTable(report_data)
            table.setStyle(report_style)
            tables.append(table)
        container_data.append(tables)
        container_table = Table(container_data, 2 * [3.6 * inch])
        container_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.HexColor('#ed4694')),
        ]))
        story.append(container_table)
        doc.build(story)

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
            data.append([component.display_title()])
            row_no += 1
            add_styles.append(('BACKGROUND', (0, row_no), (-1, row_no), colors.HexColor('#ffeb94')))
            add_styles.append(('LINEBELOW', (0, row_no), (-1, row_no), 1, colors.HexColor('#1f8dd6')))
            add_styles.append(('FONT', (0, row_no), (-1, row_no), 'Helvetica-Bold'))
            for datarow in component.data:
                row_data = []
                row_no += 1
                row_data.append(datarow.label)
                row_data.append(Paragraph(datarow.display_value(), self.para_style()['normal']))
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
            textColor=colors.HexColor('#666666'),
        ))

        return stylesheet
