from office365api.model.recipient import Recipient
from office365api.model.item_body import ItemBody
from office365api.model.model import Model


class Message(Model):

    def __init__(self, From: Recipient, ToRecipients: [Recipient], Subject: str, Body: ItemBody,
                 HasAttachments: bool=False, Id: str=None, DateTimeReceived=None):
        self.Id = Id
        self.From = From
        self.ToRecipients = ToRecipients
        self.Subject = Subject
        self.Body = Body
        self.HasAttachments = HasAttachments
        self.DateTimeReceived = DateTimeReceived
        self.Attachments = []

    def __iter__(self):
        """
        Convert objects back to dictionary.
        :return: Dictionary representation.
        """
        for k, v in self.__dict__.items():
            if v is not None and k != 'HasAttachments':
                yield k, Model.get_value(v)
