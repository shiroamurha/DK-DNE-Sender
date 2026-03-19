from email.message import EmailMessage
import smtplib
from utils import debug



def send_dne_by_email(email, name, filename):

    filename += '.pdf'

    with open('p.txt', 'r') as p:
        password = p.read()

    msg = EmailMessage()
    msg['Subject'] = 'DNE digital gerada :D'
    msg['From'] = 'entregadordedne.dceifrestinga@gmail.com'
    msg['To'] = email
    msg["Reply-To"] = "dce@restinga.ifrs.edu.br"

    msg.set_content('Segue em anexo o PDF da DNE digital solicitada.\n\nAproveite bastante!')
    msg.add_alternative("""
<html>
  <body>
    <p>Segue em anexo o PDF da DNE digital solicitada.\n\nAproveite bastante!</p>
  </body>
</html>
""", subtype="html")

    # Ler o arquivo que será anexado
    with open(f'./DNEs/{filename}', 'rb') as pdf:
        file_data = pdf.read()

    # Adicionar o anexo
    msg.add_attachment(file_data,
                    maintype='application',
                    subtype='octet-stream',
                    filename=filename)

    # Enviar (exemplo com SMTP do Gmail)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('entregadordedne.dceifrestinga@gmail.com', password)
        smtp.send_message(msg)

    debug(f'Sent to {name} ({email})')



if __name__ == "__main__":
    send_dne_by_email('alayouey@gmail.com', 'andre', 'dne_list')