from office365api.model.message import Message
from office365api.model.attachment import Attachment
from office365api.mail.api import Api


class Base(Api):

    def get_messages_from_folder(self,
                                 folder,
                                 select=None,
                                 filters=None,
                                 search=None,
                                 order_by=None,
                                 top=100,
                                 skip=0):
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
        select.extend(Message.parameters())
        params = {'$select': (','.join(select)), '$top': top, '$skip': skip}

        def add(k, v):
            if v:
                params[k] = v

        # Search must be surrounded by quotes
        add('$search', '"{}"'.format(search) if search else None)
        add('$filter', filters)
        add('$orderby', order_by)

        # search override
        if search:
            for key in ['$skip', '$filter', '$orderby']:
                params.pop(key, None)

        response = self.connection.get(url=url, params=params)
        data = response.json()
        return [Message.from_dict(value) for value in data.get('value')] if data else []

    def get_attachments(self, message):
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

    def send_message(self, message):
        """
        Immediately sends the message.
        :param message: Message.
        :return: None
        """
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data = message.data
        self.connection.post(self.SEND_URL, json=data, headers=headers)

    def reply(self, message, comment=None, to_all=False):
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

    def forward(self, message, recipients, comment=None):
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

    def delete_message(self, message):
        """
        Deletes message from the server.
        :param message: Message object.
        :return: None
        """
        self.delete_message_id(message_id=message.Id)

    def delete_message_id(self, message_id):
        """
        Deletes message from the server.
        :param message_id: Message id
        :return: None
        """
        url = self.MESSAGE_URL.format(id=message_id)
        self.connection.delete(url=url)

    def update_message(self, message, fields):
        """
        Updates a message on the server.
        :param fields: Fields needed updating.
        :param message: Message object.
        :return: None
        """
        self.update_message_id(message.Id, fields)

    def update_message_id(self, msg_id, fields):
        """
        Deletes message from the server.
        :param fields: Fields needed updating.
        :param msg_id: ID of a message
        :return: None
        """
        url = self.MESSAGE_URL.format(id=msg_id)
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        self.connection.patch(url=url, data=fields, headers=headers)

    def create_attachment(self, message, attachment):
        """
        Adds an attachment to draft message before sending.
        :param message: The draft message.
        :param attachment: Attachment.
        :return: None
        """
        url = self.ATTACHMENT_URL.format(id=message.Id)
        self.connection.post(url=url, data=attachment.writable_properties)

    def delete_attachment(self, message, attachment):
        """
        Deletes attachment from message.
        :param message: The message.
        :param attachment: The attachment.
        :return:
        """
        url = self.ATTACHMENT_URL.format(id=message.Id) + '/' + attachment.Id
        self.connection.delete(url=url)

    def mark_read(self, message):
        """
        Marks messages read.
        :param message: Message to mark.
        :return:
        """
        self.mark_read_id(message.Id)

    def mark_read_id(self, msg_id):
        """
        Marks messages read.
        :param msg_id: The id of the message to mark.
        :return:
        """
        read = "{'IsRead': true}"
        self.update_message_id(msg_id, read)
