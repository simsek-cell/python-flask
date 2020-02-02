import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendmessage(username,password,msg_sink,msg):
    
    mail = smtplib.SMTP("smtp.gmail.com",587)
    mail.ehlo()
    mail.starttls()
    mail.login(username,password)

    mesaj = MIMEMultipart()
    mesaj["From"] = f"SIMSEKCELL {username}"          # Gönderen
    mesaj["Subject"] = "Doğrulama Parolanız"
    mesaj["To"] = str(msg_sink)

    body =f"""
    <h1 align='center'>Doğrulama Kodunuz</h1>
    <font color='purple' style='text-align: center; font-weight: bold;'>{msg}</font>
    """
    body_text = MIMEText(body,"html")  
    mesaj.attach(body_text)
    mail.sendmail(mesaj["From"], mesaj["To"], mesaj.as_string())
    mail.close()
