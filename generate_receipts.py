from fpdf import FPDF
def create_pdf(payment_data,transcode):
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font('Arial',size=12)
    pdf.multi_cell(200,10,txt=payment_data,align='C')
    pdf.output(f'receipts/{transcode}.pdf')
# create_pdf("Transaction Code : UFGTG854944, Amount :1, Date : 15/10/2026",'UFGTG854944')