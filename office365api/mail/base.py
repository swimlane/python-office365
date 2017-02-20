from typing import List

from office365api.mail.api import Api
from office365api.model import Recipient
from office365api.model.attachment import Attachment
from office365api.model.message import Message


class Base(Api):
    """
    Messages base.
    """

    def get_messages_from_folder(self,
                                 folder: str,
                                 select: List = None,
                                 filters: str = None,
                                 search: str = None,
                                 order_by=None,
                                 top: int=100,
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

        # search override
        if search:
            for key in ['$skip', '$filter', '$orderby']:
                params.pop(key, None)

        response = self.connection.get(url=url, params=params)
        data = response.json()
        return [Message.from_dict(value) for value in data.get('value')] if data else []

    def get_attachments(self, message: Message)->List[Attachment]:
        """
        Lazy loaded Attachments.
        :param message: Message object.
        :return: Attachment collection. It is also added to message as side effect.
        """
        if not message.HasAttachments:
            return []
        response = self.connection.get(url=self.ATTACHMENT_URL.format(id=message.Id))
        data = response.json()
        message.Attachments = [Attachment.factory(a) for a in data.get('value', [])] \
            if data else []
        return message.Attachments

    def send_message(self, message: Message):
        """
        Immediately sends the message.
        :param message: Message.
        :return: None
        """
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data = message.data
        self.connection.post(self.SEND_URL, json=data, headers=headers)

    def reply(self, message: Message, comment: str=None, to_all: bool=False):
        """
        Sends reply to sender and other recipients.
        :param message: Message to reply to, only Id is important.
        :param comment: Optional comment.
        :param to_all: If true reply to other recipients as well.
        :return: None
        """
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        url = (self.REPLY_ALL_URL if to_all else self.REPLY_URL).format(id=message.Id)
        data = {'Comment': (comment or '')}
        self.connection.post(url=url, json=data, headers=headers)

    def forward(self, message: Message, recipients: List[Recipient], comment: str=None):
        """
        Sends reply to sender and other recipients.
        :param recipients: Recipients to forward it too.
        :param message: Message to reply to, only Id is important.
        :param comment: Optional comment.
        :return: None
        """
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        url = self.FORWARD_URL.format(id=message.Id)
        data = {'Comment': (comment or ''), 'ToRecipients': [dict(r) for r in recipients]}
        self.connection.post(url=url, json=data, headers=headers)

    def delete_message(self, message: Message):
        """
        Deletes message from the server.
        :param message: Message object.
        :return: None
        """
        self.delete_message_id(message_id=message.Id)

    def delete_message_id(self, message_id: str):
        """
        Deletes message from the server.
        :param message_id: Message id
        :return: None
        """
        url = self.MESSAGE_URL.format(id=message_id)
        self.connection.delete(url=url)

    def update_message(self, message: Message, fields: dict):
        """
        Deletes message from the server.
        :param fields: Fields needed updating.
        :param message: Message object.
        :return: None
        """
        url = self.MESSAGE_URL.format(id=message.Id)
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        self.connection.patch(url=url, data=fields, headers=headers)

    def create_attachment(self, message: Message, attachment: Attachment):
        """
        Adds an attachment to draft message before sending.
        :param message: The draft message.
        :param attachment: Attachment.
        :return: None
        """
        url = self.ATTACHMENT_URL.format(id=message.Id)
        self.connection.post(url=url, data=attachment.writable_properties)

    def delete_attachment(self, message: Message, attachment: Attachment):
        """
        Deletes attachment from message.
        :param message: The message.
        :param attachment: The attachment.
        :return:
        """
        url = self.ATTACHMENT_URL.format(id=message.Id) + '/' + attachment.Id
        self.connection.delete(url=url)

    def mark_read(self, message: Message):
        """
        Marks messages read.
        :param message: Message to mark.
        :return:
        """
        read = {"IsRead": True}
        self.update_message(message=message, fields=read)


    def mark_read_id(self, id: str):
        """
        Marks messages read.
        :param id: The id of the message to mark.
        :return:
        """
        fields = {"IsRead": True}
        url = self.MESSAGE_URL.format(id=id)
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        self.connection.patch(url=url, data=fields, headers=headers)
