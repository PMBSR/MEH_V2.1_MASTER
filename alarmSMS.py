from SMS import SendSms

Sender = 'Estufas'
indicativo ='351'
Mobilenr = input('Your Phone Number:')
Smstext = 'SERVICES OKAY!'

SendSms(Sender,Mobilenr,Smstext)
print('Message Sended!')
