from office365api import Mail
from dotenv import load_dotenv
from os.path import join, dirname, normpath
from os import environ
from office365api.model import Recipient, ItemBody
from office365api import Message

dot_env_path = normpath(join(dirname(__file__), '../', '.env'))
load_dotenv(dot_env_path)


def send_email(auth):
    mail = Mail(auth=auth)
    recipient = Recipient.from_email(auth[0])
    message = Message(Body=ItemBody(Content='Test body'),
                      Subject='Test from office365api', From=recipient,
                      ToRecipients=[recipient])
    mail.inbox.send_message(message)

    filters = "Subject eq '{subject}'".format(subject=message.Subject)
    m = mail.inbox.get_messages(filters=filters)

    print('inbox_parameters {count}'.format(count=(len(m))))

    for message in m:
        mail.delete_message(message=message)


if __name__ == '__main__':
    authorization = (environ.get('OFFICE_USER'), environ.get('OFFICE_USER_PASSWORD'))
    send_email(authorization)

