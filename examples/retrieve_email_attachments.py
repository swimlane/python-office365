from office365api import Mail
from dotenv import load_dotenv
from os.path import join, dirname, normpath
from os import environ

dot_env_path = normpath(join(dirname(__file__), '../', '.env'))
load_dotenv(dot_env_path)


def inbox_parameters(auth):
    mail = Mail(auth=auth)
    filters = "HasAttachments eq true" + \
              " and DateTimeReceived gt 2016-01-01T00:00:01Z"
    m = mail.inbox.get_messages(select=['DateTimeSent'],
                                filters=filters,
                                top=1)
    print('inbox_parameters {count}'.format(count=(len(m))))
    for message in m:
        a = mail.inbox.get_attachments(message=message)
        print(a)
    return m


if __name__ == '__main__':
    authorization = (environ.get('OFFICE_USER'), environ.get('OFFICE_USER_PASSWORD'))
    m = inbox_parameters(authorization)
