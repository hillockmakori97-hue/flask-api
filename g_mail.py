import mailtrap
subject='FLASK-API'
message='Testing mailing'
token='9374bce6e73f8b2a54b983285be37f8f'
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
    response=client.send(mail)
    print('-----------this is mailtrap------')
    print(response)
# email('hillockmakori97@gmail.com','Testing API', 'Testing My API')