from flask import Flask, request
import random
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    # Get the message the user sent to the Twilio number
    body = request.values.get('Body', None)

    body = body.lower()

    # Start our TwiML response
    resp = MessagingResponse()

    mes = '-\n'
    # Determine the right reply for this message
    if body == 'hello':
        mes += 'Hi!'
    elif body == 'bye':
        mes += 'Goodbye!'
    elif 'joke' in body:
        lines = open('static/shortjokes.csv').read().splitlines()
        mes += random.choice(lines).split(',')[1].strip('"')
    else:
        mes += 'Que tal mi amigo?'

    resp.message(mes)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
