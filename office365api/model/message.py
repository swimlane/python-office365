from office365api.model import Recipient
from office365api.model.model import Model


class Message(Model):

    select = ['From', 'Subject', 'Body', 'ToRecipients', 'DateTimeReceived', 'HasAttachments']

    def __init__(self, From: Recipient, ToRecipients: [Recipient], Subject: str, Body: str,
                 HasAttachments: bool=False, Id: str=None, DateTimeReceived=None):
        self.Id = Id
        self.From = From
        self.ToRecipients = ToRecipients
        self.Subject = Subject
        self.Body = Body
        self.HasAttachments = HasAttachments
        self.DateTimeReceived = DateTimeReceived
        self.Attachments = []
