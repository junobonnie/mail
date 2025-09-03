import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class Mail:
    def __init__(self):
        self.set_mail_config()
        self.set_mail_list()
        self.msg = MIMEMultipart("alternative")
        self.msg['From'] = self.mail_id
        self.image_count = 0
        self.html_body = ""

    def login(self):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(self.mail_id, self.mail_pw)

    def set_mail_config(self):
        with open("mail.config") as f:
            self.mail_id, self.mail_pw = f.readlines()

    def set_mail_list(self):
        with open("mail.list") as f:
            self.mail_list = f.read().splitlines()

    def set_subject(self, subject):
        self.msg['Subject'] = subject

    def add_text(self, text):
         text_part = MIMEText(text, "plain")
         self.msg.attach(text_part)

    def add_text_html(self, text):
        """HTML 본문에 텍스트/링크 추가"""
        # 링크 자동 감지: 단순히 http/https를 포함한 텍스트는 a 태그로 감싸기
        import re
        def replace_link(match):
            url = match.group(0)
            return f'<a href="{url}">{url}</a>'

        html_text = re.sub(r'https?://[^\s]+', replace_link, text)
        self.html_body += f'<p>{html_text}</p>\n'

    def add_img(self, image):
         self.image_count += 1
         with open(image, 'rb') as file:
             img = MIMEImage(file.read(), name=image)
         img.add_header('Content-ID', '<image%d>'%(self.image_count))
         self.msg.attach(img)

    def add_img_url(self, url, scale=1.0):
        """
        외부 URL 이미지 본문 삽입
        scale: 0~1 사이, 이미지 크기 비율
        """
        self.html_body += f'<p><img src="{url}" alt="image" style="width:{scale*100}%"></p>\n'

    def clear(self):
        self.msg = MIMEMultipart("alternative")  # HTML + plain text 가능
        self.msg['From'] = self.mail_id
        self.image_count = 0
        self.html_body = ""

    def send(self):
        self.login()

        # HTML 본문 생성
        if self.html_body:
            html_part = MIMEText(self.html_body, "html")
            self.msg.attach(html_part)

        # 모든 수신자를 To 헤더에 한 번에 설정
        self.msg['To'] = ", ".join(self.mail_list)

        # 실제 전송할 때는 리스트 그대로 사용
        self.server.sendmail(self.mail_id, self.mail_list, self.msg.as_string())

        self.clear()
        self.quit()

    def quit(self):
        self.server.quit()

if __name__ == "__main__":
    mail = Mail()
    mail.set_subject("test")
    mail.add_text("hihi")
    mail.add_text("hihi")
    mail.add_text("hihi")
    mail.add_text("hihi")
    mail.add_img("Lenna.png")
    mail.add_img("Lenna.png")
    mail.send()
