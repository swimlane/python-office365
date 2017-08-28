from os.path import basename
import base64

from office365api.model.model import Model


class Attachment(Model):
    def __init__(self, Id=None, ContentType=None, IsInline=False,
                 DateTimeLastModified=None, Name=None, Size=0):
        """
        c-tor
        :param Id: Attachment Id.
        :param ContentType:
        :param IsInline:
        :param DateTimeLastModified:
        :param Name:
        :param Size:
        """
        self.Id = Id
        self.ContentType = ContentType
        self.IsInline = IsInline
        self.DateTimeLastModified = DateTimeLastModified
        self.Name = Name
        self.Size = Size

    @classmethod
    def factory(cls, data):
        return ItemAttachment.from_dict(data=data) \
            if data.get('@odata.type') != '#Microsoft.OutlookServices.FileAttachment' \
            else FileAttachment.from_dict(data=data)

    @property
    def writable_properties(self):
        raise NameError


class ItemAttachment(Attachment):
    def __init__(self,
                 Id=None,
                 Item=None,
                 ContentType=None,
                 IsInline=False,
                 DateTimeLastModified=None,
                 Name=None,
                 Size=0):
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
        super(ItemAttachment, self).__init__(Id=Id,
                                             ContentType=ContentType,
                                             IsInline=IsInline,
                                             DateTimeLastModified=DateTimeLastModified,
                                             Name=Name,
                                             Size=Size)
        self.Item = Item
        self.__dict__['@odata.type'] = '#Microsoft.OutlookServices.ItemAttachment'


class FileAttachment(Attachment):
    def __init__(self,
                 Id=None,
                 ContentBytes=None,
                 ContentId=None,
                 ContentLocation=None,
                 ContentType=None,
                 IsInline=False,
                 DateTimeLastModified=None,
                 Name=None,
                 Size=0):
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
        super(FileAttachment, self).__init__(Id=Id,
                                             ContentType=ContentType,
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
    def from_file(cls, path):
        with open(path, mode='rb') as stream:
            name = basename(path)
            content_bytes = base64.b64encode(stream.read()).decode()
            return cls(Name=name, ContentBytes=content_bytes)
