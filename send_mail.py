from flask import Flask, request
from flask_mail import Mail, Message
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)

app.config.from_object('env')
mail = Mail(app)


class Mailer(Resource):
    def get(self):
        msg = Message(
            subject='Test Mailer',
            body='This is a Test Mail.')

        return self._send_mail(msg)

    def post(self):
        data_receive = request.json

        msg = Message(
            subject=data_receive['subject'],
            body=data_receive['body_plain'],
            html=data_receive['body_html'])

        return self._send_mail(msg)

    def _send_mail(self, msg):
        with mail.connect() as connect:
            msg.sender = app.config['SENDER']
            msg.recipients = app.config['RECIPIENTS']

            connect.send(msg)
            return {
                'mensagem': 'E-mail enviado com sucesso!',
                'sucesso': 1}, 200


api.add_resource(Mailer, '/mailer')
if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=6969)
