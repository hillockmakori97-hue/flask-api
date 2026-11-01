import mailtrap
import os
from dotenv import load_dotenv
load_dotenv()
subject='FLASK-API'
message='Testing mailing'
token=os.getenv('mailtrap_api_key')
def email(to,subject,message):
    mail=mailtrap.Mail(
        sender=mailtrap.Address(email="hello@demomailtrap.co",name="FLASK_API"),
        to=[mailtrap.Address(email=to)],
        subject=subject,
        text=message,
        category="mailtrap integration test"
    )
    client=mailtrap.MailtrapClient(token)
    print('this is mailtrap----------------')
    # response=client.send(mail)
    # print('-----------this is mailtrap------')
    # print(response)
# email('hillockmakori97@gmail.com','Testing API', 'Testing My API')