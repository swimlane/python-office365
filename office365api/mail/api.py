from office365api.connection import Connection


class Api(object):
    BASE_URL = 'https://outlook.office365.com/api/v1.0/me'
    SEND_URL = BASE_URL + '/sendmail'
    MAILBOX_URL = BASE_URL + '/folders/{folder_id}/messages'
    MESSAGE_URL = BASE_URL + '/messages/{id}'

    ATTACHMENT_URL = MESSAGE_URL + '/attachments?$expand=Microsoft.OutlookServices.ItemAttachment/Item'
    REPLY_URL = MESSAGE_URL+'/reply'
    REPLY_ALL_URL = MESSAGE_URL+'/replyall'
    FORWARD_URL = MESSAGE_URL+'/forward'

    def __init__(self, auth):
        self.auth = auth
        self.connection = Connection(auth)