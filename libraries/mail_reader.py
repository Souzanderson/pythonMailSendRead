#modules
import imaplib
import email
import os

from libraries.mail_config import ConfigMail

class MailReader:
    def __init__(self, config: ConfigMail):
        self.config = config
        self.mail = imaplib.IMAP4_SSL(self.config.host)
        self.mail.login(self.config.user, self.config.key)
        self.selected_mails = None
        self.messages = []
        
    class MailMessage:
        def __init__(self):
            self.subject = None
            self.to = None
            self.fr = None
            self.date = None
            self.text = None
        
        @staticmethod
        def setMessage(email_message):
            try:
                obj = MailReader.MailMessage()
                obj.subject = email_message["subject"]
                obj.to = email_message["to"] 
                obj.fr = email_message["from"] 
                obj.date = email_message["date"]
                return obj
            except Exception as e:
                print(f'[ERROR] => {e}')
                return MailReader.MailMessage()
        
        def toDict(self):
            return{
                "subject": self.subject,
                "to": self.to,
                "from": self.fr,
                "date": self.date,
                "text": self.text,
            }
        
    def readMails(self, locateread="INBOX", type_read="(UNSEEN)"):
        try:
            self.mail.select(locateread)
            _, self.selected_mails = self.mail.search(None, type_read)
            print("[INFO] Mensagens encontradas:" , len(self.selected_mails[0].split()))
            return self
        except Exception as e:
            print(e)
            return self


    def getMessages(self):
        for num in self.selected_mails[0].split():
            try:
                _, data = self.mail.fetch(num , '(RFC822)')
                _, bytes_data = data[0]

                #convert the byte data to message
                email_message = email.message_from_bytes(bytes_data)
                message = MailReader.MailMessage.setMessage(email_message)
                for part in email_message.walk():
                    if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                        message_part = part.get_payload(decode=True)
                        message.text = message_part.decode()
                        self.messages.append(message)
                        break
            except Exception as e:
                print("[ERROR] Erro ao ler mensagem! => ", str(e))
                continue
        return self.messages
    
    
    def getAttachments(self, download_folder=""):
        for num in self.selected_mails[0].split():
            _, data = self.mail.fetch(num , '(RFC822)')
            _, bytes_data = data[0]

            #convert the byte data to message
            email_message = email.message_from_bytes(bytes_data)
            message = MailReader.MailMessage.setMessage(email_message)
            print(email_message)
            for part in email_message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()
                att_path = os.path.join(download_folder, "", filename)

                if not os.path.isfile(att_path):
                    fp = open(att_path, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                    
                    
if __name__ == '__main__':
    rm = MailReader()
    mens = rm.readMails().getMessages()
    print([m.toDict() for m in mens])
    