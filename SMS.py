import nexmo

def SendSms(sender,to,text):
    client = nexmo.Client(key='863ebd62', secret='grwxupG0M9yPJfcP')    # credencias do serviço nexmo - consultadas em Vonage API Dashboard
    indicativo ='351'   # indicativo do país
    Mobilenr = to       # número do destinatário
    to = indicativo+Mobilenr

    client.send_message({
        'from': sender,
        'to': to,
        'text': text,
    })
