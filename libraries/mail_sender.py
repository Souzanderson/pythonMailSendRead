from smtplib import SMTP_SSL, SMTP_SSL_PORT
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64

from libraries.mail_config import ConfigMail


class MailSender:
    def __init__(self, config: ConfigMail):
        self.config = config
        self.server = SMTP_SSL(self.config.host, port=SMTP_SSL_PORT)
        self.server.login(self.config.user, self.config.key)
        self.mail_message = MIMEMultipart()
        self.__message_text__ =  ''
        self.__to_mails__ = []
        
    def setHeader(self, to_mails:list, subject, priority="1"):
        try:
            self.__to_mails__ = to_mails
            self.mail_message.add_header('To', ', '.join(to_mails))
            self.mail_message.add_header('From', self.config.user)
            self.mail_message.add_header('Subject', subject)
            self.mail_message.add_header('X-Priority', priority)
        except Exception as e:
            print("[ERROR HEADER] => ", str(e))
        return self
    
    def setMessageText(self, text:str):
        try:
            self.__message_text__ = MIMEText(text, 'plain')
            self.mail_message.attach(self.__message_text__)
        except Exception as e:
            print("[ERROR MESSAGE TEXT] => ", str(e))
        return self
    
    def setAttachment(self, file_location, file_name):
        try:
            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(open(file_location, 'rb').read())
            encode_base64(attachment)
            attachment.add_header("Content-Disposition", f"attachment; filename={file_name}")
            self.mail_message.attach(attachment)
        except Exception as e:
            print("[ERROR ATTACHMENT] => ", str(e))
        return self
        
    def sendMail(self):
        try:
            self.server.sendmail(self.config.user, self.__to_mails__, self.mail_message.as_bytes())
            self.server.quit()
        except Exception as e:
            print("[ERROR SENDMAIL] => ", str(e))