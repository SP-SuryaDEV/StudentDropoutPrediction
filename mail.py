import smtplib
import pandas as pd
from email.message import EmailMessage

class Emailer:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def send(self, recipient, subject, body):
        msg = EmailMessage()
        msg['From'] = self.email
        msg['To'] = recipient
        msg['Subject'] = subject  
        msg.set_content(body)

        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(self.email, self.password)
        smtp_server.send_message(msg)
        smtp_server.quit()


class SendEmail:

    def __init__(self, email):
        self.emailer = Emailer('sosexamplemessage@gmail.com', 'jrpd befe utpa mxxp')
        self.receiver = email
        self.subject = 'Weekly PassWord Update!'


    def MessageUpdate(self, name, password):
       
       message = f'''This Will be Your Password for this week to Access the Student Success Portal\n
                General Login Credentials:

                    Username : Test
                    Password : pass23

                Personal Login Credentials:

                    Student Name: {name}
                    Student Password: {password}

            NOTE : Make Sure to Check the The Portal daily for periodic updates from Your Advisors !!!
            '''
    
       self.emailer.send(self.receiver, self.subject, message)
