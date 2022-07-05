'''
####################################################################################
############# INSTRUÇÕES PARA UTILIZAÇÃO DO EMAIL SENDER/RECEIVER ################## 
####################################################################################
#                                                                                  #
#   - Coloque o arquivo ./library/mail_sender em uma pasta em seu projeto;         #
#   - Coloque o arquivo ./library/mail_sender em uma pasta em seu projeto;         #
#   - Coloque o arquivo ./library/mail_config em uma pasta em seu projeto;         #
#   - Siga o exemplo de utilização abaixo;                                         #
#                                                                                  #
####################################################################################
####################################################################################

'''


from libraries.mail_config import ConfigMail
from libraries.mail_reader import MailReader
from libraries.mail_sender import MailSender


sm = MailSender(ConfigMail())
sm.setHeader(["teste@teste.com"],"teste de envio automático", "1"
    ).setMessageText("Olá!")
sm.sendMail()

rm = MailReader(ConfigMail())
mens = rm.readMails().getMessages()
print([m.toDict() for m in mens])

