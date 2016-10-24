import base64
import json
import requests
from office365api.model.model import Model


class Attachment(Model):
    def __init__(self, ContentType: str = None, IsInline: bool = False,
                 DateTimeLastModified: str = None, Name: str = None, Size: int = 0):
        self.ContentType = ContentType
        self.IsInline = IsInline
        self.DateTimeLastModified = DateTimeLastModified
        self.Name = Name
        self.Size = Size


class ItemAttachment(Attachment):
    pass


class FileAttachment(Attachment):
    def __init__(self,
                 ContentBytes: bytearray = None,
                 ContentId: str = None,
                 ContentLocation: str = None,
                 ContentType: str = None,
                 IsInline: bool = False,
                 DateTimeLastModified: str = None,
                 Name: str = None,
                 Size: int = 0):
        super().__init__(ContentType=ContentType,
                         IsInline=IsInline,
                         DateTimeLastModified=DateTimeLastModified,
                         Name=Name,
                         Size=Size)
        self.ContentBytes = ContentBytes
        self.ContentId = ContentId
        self.ContentLocation = ContentLocation
