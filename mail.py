import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class Mail:
    def __init__(self):
        self.set_mail_config()
        self.set_mail_list()
        self.msg = MIMEMultipart()
        self.msg['From'] = self.mail_id

    def login(self):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(self.mail_id, self.mail_pw)

    def set_mail_config(self):
        with open("mail.config") as f:
            self.mail_id, self.mail_pw = f.readlines()

    def set_mail_list(self):
        with open("mail.list") as f:
            self.mail_list = f.readlines()

    def set_subject(self, subject):
        self.msg['Subject'] = subject

    def add_text(self, text):
         text_part = MIMEText(text, "plain")
         self.msg.attach(text_part)

    def add_img(self, image):
         with open(image, 'rb') as file:
             img = MIMEImage(file.read())
             img.add_header('Content-Disposition', 'attachment', filename=image)
             self.msg.attach(img)

    def clear(self):
        self.msg = MIMEMultipart()

    def send(self):
        self.login()
        for mail_ in self.mail_list:
            self.msg['To'] = mail_
            self.server.sendmail(self.mail_id, mail_, self.msg.as_string())
        self.clear()
        self.quit()

    def quit(self):
        self.server.quit()

if __name__ == "__main__":
    mail = Mail()
    mail.set_subject("test")
    mail.add_text("hihi")
    #mail.add_img("Lenna.png")
    mail.send()
