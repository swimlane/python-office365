from typing import List
from office365api.connection import Connection
from office365api.model.attachment import Attachment
from office365api.model.message import Message


class Base(object):

    BASE_URL = 'https://outlook.office365.com/api/v1.0/me/'
    MAILBOX_URL = BASE_URL+'folders/{folder_id}/messages'
    ATTACHMENT_URL = BASE_URL + 'folders/{folder_id}/messages/{id}/attachments'
    MESSAGE_URL = BASE_URL + 'messages/{id}'
    SEND_URL = BASE_URL + 'sendmail'
    REPLY_URL = BASE_URL+'messages/{id}/reply'
    REPLY_ALL_URL = BASE_URL+'messages/{id}/replyall'
    # update_url = 'https://outlook.office365.com/api/v1.0/me/messages/{0}'

    def __init__(self, auth):
        self.auth = auth
        self.connection = Connection(auth)

    def get_messages_from_folder(self,
                                 folder: str,
                                 select: List = None,
                                 filters: str = None,
                                 search: str = None,
                                 order_by=None,
                                 top: int=50,
                                 skip: int=0) -> List[Message]:
        """
        Downloads messages to local memory.

        :param skip:  Page results, skip - default 0.

        :param top: Page size, default take first 50 messages.

        :param folder: The folder from where to get messages. [Inbox, Drafts, SentItems,
        DeletedItems]

        :param select: The list of additional fields to retrieve.
        ['Bcc', 'IsDeliveryReceiptRequested']. By default returns only fields required for
        Message class.

        :param filters: Filters for messages OData 4.0 compatible.
        Example: "From/EmailAddress/Address ne 'MicrosoftOffice365@email.office.com'"

        :param search: Search criteria. When supplying string looks in subject, body etc
        if you want to look in a particular field 'from:microsoft'

        :param order_by: Order by field name. Example: 'DateTimeReceived desc'

        :param page: Paging settings.
        """
        url = self.MAILBOX_URL.format(folder_id=folder)

        select = select or []
        select.extend(Message.parameters().keys())
        params = {'$select': (','.join(select)), '$top': top, '$skip': skip}

        def add(key, value):
            if value:
                params[key] = value
        add('$search', search)
        add('$filter', filters)
        add('$orderby', order_by)

        response = self.connection.get(url=url, params=params)
        data = response.json()
        return [Message.from_dict(value) for value in data.get('value')] if data else []

    def get_attachments(self, folder: str, message: Message)->List[Attachment]:
        """
        Lazy loaded Attachments.
        :param message: Message object.
        :param folder: Folder where to perform attachment retrieval.
        :return: Attachment collection. It is also added to message as side effect.
        """
        if not message.HasAttachments:
            return []
        response = self.connection.get(url=self.ATTACHMENT_URL.format(id=message.Id, folder_id=folder))
        data = response.json()
        message.Attachments = [Attachment.factory(a) for a in data.get('value', [])] \
            if data else []
        return message.Attachments

    def send_message(self, message: Message):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data = message.data
        self.connection.post(self.SEND_URL, json=data, headers=headers)

    def delete_message(self, message: Message):
        """
        Deletes message from the server.
        :param message: Message object.
        :return: None
        """
        url = self.MESSAGE_URL.format(id=message.Id)
        self.connection.delete(url=url)

    def create_attachment_in_folder(self, folder_id: str,
                                    message: Message,
                                    attachment: Attachment):
        url = self.ATTACHMENT_URL.format(folder_id=folder_id, id=message.Id)
        self.connection.post(url=url, data=attachment.writable_properties)


        #
        #     def markAsRead(self):
        #         '''marks analogous message as read in the cloud.'''
        #         read = '{"IsRead":true}'
        #         headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        #         try:
        #             response = requests.patch(self.update_url.format(self.json['Id']), read, headers=headers, auth=self.auth)
        #         except:
        #             return False
        #         return True
