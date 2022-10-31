import email
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from csv import writer
import os


subject = "Bugün, {} itibarıyle sayım raporudur.".format(
    time.strftime('%H:%M'))
sender_email = "netartyazilim@gmail.com"

receiver_emails = [m[:-1] for m in open('emails.txt', 'r').readlines()]

password = open('.xword', 'r').readline()[:-1]


for receiver_email in receiver_emails:
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    filenames = open('/home/mendel/files/files.csv', 'r').read().splitlines()

    # filename = "besas_{}.csv".format(time.strftime('%d%m%Y'))  # In same directory as script
    print(filenames)
    filename = filenames[-1] if os.path.exists(
        filenames[-1]) else filenames[-2]

    import csv
    ffff = []
    with open(filename, newline='') as csvfile:
        freader = csv.reader(csvfile, delimiter=',', quotechar='|')
        ffff.append(['Tarih - Saat', 'Ekmek turu ',
                    'Firin no', 'Son 5 dk', 'Toplam'])
        toplam = 0
        body = finbody = ''
        for i, row in enumerate(freader):
            row=row[0].split(';')
            print(i, row)
            
            if i == 0:
                body += '\n'+str(row[0]) + ' - '
            finbody = str(row[0])
            toplam += int(row[-2])
            row[-1] = toplam
            row[2] = row[2].split('_')[1]
            ffff.append(row)

    body += finbody + ' Tarihleri arasi\n'
    message.attach(MIMEText(body, "plain"))

    filename = filename.split('.csv')[0]+'_.xlsx'
    import xlsxwriter

    with xlsxwriter.Workbook(filename) as workbook:
        worksheet = workbook.add_worksheet()
        for rnum, row in enumerate(ffff):
            worksheet.write_row(rnum, 0, row)

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    filename = filename.split('/')[-1]
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    try:
        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
        print('{} E mail gitti'.format(receiver_email))
    except:
        print('HATA: {} e gitmedi '.format(receiver_email))
