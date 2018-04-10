import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

def sendMail(username,password, send_to, subject, text, files={},server="smtp.gmail.com",port=587):
    assert isinstance(send_to, list)
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text, 'html'))
    for i in files:
        part = MIMEApplication(
                files[i],
                Name=i
            )
        part['Content-Disposition'] = 'attachment; filename="%s"' % i
        msg.attach(part)
    smtp = smtplib.SMTP()
    smtp.connect(server,port)
    smtp.starttls()
    smtp.login(username,password)
    smtp.sendmail(username,send_to,msg.as_string())
    smtp.close()
    return True

if __name__ == '__main__':
    # sendMail("noreply@m1om.me", "bananaballs123!", ["aaron.bu@m1om.me"], "test_email", "This is test Text!")
    sendMail("noreply@m1om.me", "bananaballs123!", ["aaron@monaco1.ph"], "test_email", "This is test Text!")