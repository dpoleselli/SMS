from flask import Flask, request, redirect
from requests import Response
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    # Get the message the user sent to the Twilio number
    body = request.values.get('Body', None)

    body = body.lower()

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == 'hello':
        resp.message("Hi!")
    elif body == 'bye':
        resp.message("Goodbye")
    else:
        resp.message("Que tal mi amigo?")

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
