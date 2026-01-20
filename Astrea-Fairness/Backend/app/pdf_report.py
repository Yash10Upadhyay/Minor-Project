from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from io import BytesIO


def generate_pdf_report(report: dict, output_path=None):
    try:
        # Use BytesIO if no output path provided
        if output_path is None:
            pdf_buffer = BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
        else:
            doc = SimpleDocTemplate(output_path, pagesize=A4)
        
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("<b>Astrea Fairness Audit Report</b>", styles["Title"]))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph(f"<b>Fairness Score:</b> {report['fairness_score']}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Bias Level:</b> {report['bias_level']}", styles["Normal"]))
        elements.append(Spacer(1, 12))

        # Metrics Table
        elements.append(Paragraph("<b>Fairness Metrics</b>", styles["Heading2"]))

        metric_table = [["Metric", "Value"]]
        for k, v in report["metrics"].items():
            metric_table.append([k, f"{v:.4f}"])

        # Add TableStyle to make it valid
        table = Table(metric_table)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 12))

        # Mitigation
        elements.append(Paragraph("<b>Bias Mitigation Recommendations</b>", styles["Heading2"]))

        for rec in report["mitigation"]:
            elements.append(Paragraph(f"<b>Issue:</b> {rec['issue']}", styles["Normal"]))
            elements.append(Paragraph(f"<b>Fix:</b> {rec['fix']}", styles["Normal"]))
            elements.append(Spacer(1, 8))

        doc.build(elements)
        
        # Return PDF bytes if using BytesIO
        if output_path is None:
            pdf_buffer.seek(0)
            return pdf_buffer.getvalue()
        return None
    except Exception as e:
        raise Exception(f"Error generating PDF: {str(e)}")