from office365api.model.recipient import Recipient
from office365api.model.item_body import ItemBody
from office365api.model.model import Model


class Message(Model):

    select = ['From', 'Subject', 'Body', 'ToRecipients', 'DateTimeReceived', 'HasAttachments']

    def __init__(self, From, ToRecipients, Subject, Body,
                 HasAttachments=False, Id=None, DateTimeReceived=None):
        self.Id = Id
        self.From = From
        self.ToRecipients = ToRecipients
        self.Subject = Subject
        self.Body = Body
        self.HasAttachments = HasAttachments
        self.DateTimeReceived = DateTimeReceived
        self.Attachments = []
