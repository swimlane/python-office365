from typing import List
from office365api import requests_validated as requests
from office365api.model.attachment import Attachment
from office365api.model.message import Message


class Base(object):

    BASE_URL = 'https://outlook.office365.com/api/v1.0/me/'
    MAILBOX_URL = BASE_URL+'folders/{folder_id}/messages'
    ATTR_URL = BASE_URL+'folders/{folder_id}/messages/{id}/attachments'
    # send_url = 'https://outlook.office365.com/api/v1.0/me/sendmail'
    # draft_url = 'https://outlook.office365.com/api/v1.0/me/folders/{folder_id}/messages'
    # update_url = 'https://outlook.office365.com/api/v1.0/me/messages/{0}'

    def __init__(self, auth):
        self.auth = auth

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

        response = requests.get(url=url, auth=self.auth, params=params)
        data = response.json()
        return [Message.from_dict(value) for value in data.get('value')] if data else []

    def get_attachments(self, folder: str, message: Message)->List[Attachment]:
        """
        Lazy loaded Attachments.
        :return:
        """
        if not message.HasAttachments:
            return []
        response = requests.get(url=self.ATTR_URL.format(id=message.Id, folder_id=folder),
                                auth=self.auth)
        data = response.json()
        message.Attachments = [Attachment.factory(a) for a in data.get('value', [])] \
            if data else []
        return message.Attachments

        #     def send(self):
        #         headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        #
        #         try:
        #             data = {'Message': {'Body': {}}}
        #             data['Message']['Subject'] = self.json['Subject']
        #             data['Message']['Body']['Content'] = self.json['Body']['Content']
        #             data['Message']['Body']['ContentType'] = self.json['Body']['ContentType']
        #             data['Message']['ToRecipients'] = self.json['ToRecipients']
        #             data['Message']['Attachments'] = [att.json for att in self.attachments]
        #             data['SaveToSentItems'] = "false"
        #             data = json.dumps(data)
        #             log.debug(str(data))
        #         except Exception as e:
        #             log.error(str(e))
        #             return False
        #
        #         response = requests.post(self.send_url, data, headers=headers, auth=self.auth)
        #         log.debug('response from server for sending message:' + str(response))
        #
        #         if response.status_code != 202:
        #             return False
        #
        #         return True
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
        #
        #     def getSender(self):
        #         '''get all available information for the sender of the email.'''
        #         return self.json['Sender']
        #
        #     def getSenderEmail(self):
        #         '''get the email address of the sender.'''
        #         return self.json['Sender']['EmailAddress']['Address']
        #
        #     def getSenderName(self):
        #         '''try to get the name of the sender.'''
        #         try:
        #             return self.json['Sender']['EmailAddress']['Name']
        #         except:
        #             return ''
        #
        #     def getSubject(self):
        #         '''get email subject line.'''
        #         return self.json['Subject']
        #
        #     def getBody(self):
        #         '''get email body.'''
        #         return self.json['Body']['Content']
        #
        #     def setRecipients(self, val):
        #         '''
        #         set the recipient list.
        #
        #         val: the one argument this method takes can be very flexible. you can send:
        #             a dictionary: this must to be a dictionary formated as such:
        #                 {"EmailAddress":{"Address":"recipient@example.com"}}
        #                 with other options such ass "Name" with address. but at minimum
        #                 it must have this.
        #             a list: this must to be a list of libraries formatted the way
        #                 specified above, or it can be a list of dictionary objects of
        #                 type Contact or it can be an email address as string. The
        #                 method will sort out the libraries from the contacts.
        #             a string: this is if you just want to throw an email address.
        #             a contact: type Contact from this dictionary.
        #             a group: type Group, which is a list of contacts.
        #         For each of these argument types the appropriate action will be taken
        #         to fit them to the needs of the library.
        #         '''
        #         self.json['ToRecipients'] = []
        #         if isinstance(val, list):
        #             for con in val:
        #                 if isinstance(con, Contact):
        #                     self.addRecipient(con)
        #                 elif isinstance(con, str):
        #                     if '@' in con:
        #                         self.addRecipient(con)
        #                 elif isinstance(con, dict):
        #                     self.json['ToRecipients'].append(con)
        #         elif isinstance(val, dict):
        #             self.json['ToRecipients'] = [val]
        #         elif isinstance(val, str):
        #             if '@' in val:
        #                 self.addRecipient(val)
        #         elif isinstance(val, Contact):
        #             self.addRecipient(val)
        #         elif isinstance(val, Group):
        #             for person in val:
        #                 self.addRecipient(person)
        #         else:
        #             return False
        #         return True
        #
        #     def addRecipient(self, address, name=None):
        #         '''
        #         Adds a recipient to the recipients list.
        #
        #         Arguments:
        #         address -- the email address of the person you are sending to. <<< Important that.
        #             Address can also be of type Contact or type Group.
        #         name -- the name of the person you are sending to. mostly just a decorator. If you
        #             send an email address for the address arg, this will give you the ability
        #             to set the name properly, other wise it uses the email address up to the
        #             at sign for the name. But if you send a type Contact or type Group, this
        #             argument is completely ignored.
        #         '''
        #         if isinstance(address, Contact):
        #             self.json['ToRecipients'].append(address.getFirstEmailAddress())
        #         elif isinstance(address, Group):
        #             for con in address.contacts:
        #                 self.json['ToRecipients'].append(address.getFirstEmailAddress())
        #         else:
        #             if name is None:
        #                 name = address[:address.index('@')]
        #             self.json['ToRecipients'].append({'EmailAddress': {'Address': address, 'Name': name}})
        #
        #     def setSubject(self, val):
        #         '''Sets the subect line of the email.'''
        #         self.json['Subject'] = val
        #
        #     def setBody(self, val):
        #         '''Sets the body content of the email.'''
        #         cont = False
        #
        #         while not cont:
        #             try:
        #                 self.json['Body']['Content'] = val
        #                 self.json['Body']['ContentType'] = 'Text'
        #                 cont = True
        #             except:
        #                 self.json['Body'] = {}
        #
        #     def setBodyHTML(self, val=None):
        #         '''
        #         Sets the body content type to HTML for your pretty emails.
        #
        #         arguments:
        #         val -- Default: None. The content of the body you want set. If you don't pass a
        #             value it is just ignored.
        #         '''
        #         self.json['Body']['ContentType'] = 'HTML'
        #         if val:
        #             self.json['Body']['Content'] = val

