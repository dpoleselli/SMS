from flask import Flask, request
import random
from twilio.twiml.messaging_response import MessagingResponse
import requests
import statistics

app = Flask(__name__)
to_me = []
to_mel = []


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
    elif 'covid' in body:
        if 'us' in body:
            x = requests.get('https://covidtracking.com/api/us')
            if x.status_code == 200:
                val = x.json()
                mes += 'US:\n'
                mes += str(val[0]['positive']) + ' positive cases\n'
                mes += str(val[0]['death']) + ' deaths'
            else:
                mes += 'Sorry, something went wrong: \n'
        elif 'state' in body:
            vals = body.split('-')
            x = requests.get('https://covidtracking.com/api/states?state=' + vals[1].upper())
            val = x.json()
            if x.status_code == 200 and 'error' not in val:
                mes += vals[1].upper() + ':\n'
                mes += str(val['positive']) + ' positive cases\n'
                mes += str(val['death']) + ' deaths'
            else:
                mes += 'Sorry, something went wrong: \n'
                mes += val['message']
        else:
            mes += 'Please specify what data you\'re looking for'
    elif 'to mel' in body:
        vals = body.split('-')
        if len(vals) == 1:
            mes = 'Average red lights to mel: ' + str(statistics.mean(to_mel)) + ' out of 29'
        elif len(vals) == 2:
            to_mel.append(int(vals[1]))
            mes = 'New average red lights to mel: ' + str(statistics.mean(to_mel)) + ' out of 29'
    elif 'to me' in body:
        vals = body.split('-')
        if len(vals) == 1:
            mes = 'Average red lights to me: ' + str(statistics.mean(to_me)) + ' out of 28'
        elif len(vals) == 2:
            to_me.append(int(vals[1]))
            mes = 'New average red lights to me: ' + str(statistics.mean(to_me)) + ' out of 28'
    else:
        mes += 'Que tal mi amigo?'

    resp.message(mes)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
