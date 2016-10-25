from os.path import basename
import base64
import json
import requests
from office365api.model.model import Model


class Attachment(Model):

    def __init__(self, ContentType: str = None, IsInline: bool = False,
                 DateTimeLastModified: str = None, Name: str = None, Size: int = 0):
        """
        c-tor
        :param ContentType:
        :param IsInline:
        :param DateTimeLastModified:
        :param Name:
        :param Size:
        """
        self.ContentType = ContentType
        self.IsInline = IsInline
        self.DateTimeLastModified = DateTimeLastModified
        self.Name = Name
        self.Size = Size

    @classmethod
    def factory(cls, data: dict):
        return ItemAttachment.from_dict(data=data) \
            if data.get('@odata.type') == '#Microsoft.OutlookServices.FileAttachment' \
            else FileAttachment.from_dict(data=data)

    @property
    def writable_properties(self):
        raise NameError


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
        """
        c-tor
        :param ContentBytes:
        :param ContentId:
        :param ContentLocation:
        :param ContentType:
        :param IsInline:
        :param DateTimeLastModified:
        :param Name:
        :param Size:
        """
        super().__init__(ContentType=ContentType,
                         IsInline=IsInline,
                         DateTimeLastModified=DateTimeLastModified,
                         Name=Name,
                         Size=Size)
        self.ContentBytes = ContentBytes
        self.ContentId = ContentId
        self.ContentLocation = ContentLocation
        self.__dict__['@odata.type'] = '#Microsoft.OutlookServices.FileAttachment'

    @property
    def writable_properties(self):
        return {
            '@odata.type': '#Microsoft.OutlookServices.FileAttachment',
            'ContentBytes': self.ContentBytes,
            'Name': self.Name
        }

    @classmethod
    def from_file(cls, path: str):
        with open(path, mode='rb') as stream:
            name = basename(path)
            bs = stream.read()
            content_bytes = str(base64.b64encode(bs), 'utf-8')
            return cls(Name=name, ContentBytes=content_bytes)
