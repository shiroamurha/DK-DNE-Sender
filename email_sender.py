from email.message import EmailMessage
import smtplib



def send_dne_by_email(email, name):

    msg = EmailMessage()
    msg['Subject'] = 'DNE DIGITAL GERADA'
    msg['From'] = 'dce@restinga.ifrs.edu.br'
    msg['To'] = email
    msg.set_content('Segue em anexo o PDF da DNE digital solicitada.\n\nAproveite bastante!')

    # Ler o arquivo que será anexado
    with open(f'./DNEs/{name}.pdf', 'rb') as pdf:
        file_data = pdf.read()
        file_name = pdf.name

    # Adicionar o anexo
    msg.add_attachment(file_data,
                    maintype='application',
                    subtype='octet-stream',
                    filename=file_name)

    # Enviar (exemplo com SMTP do Gmail)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('2023009548@gmail.com', 'sua_senha')
        smtp.send_message(msg)