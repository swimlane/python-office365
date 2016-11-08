import base64
import inspect
from copy import copy
from os.path import basename


class Model(object):

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __iter__(self):
        """
        Convert objects back to dictionary.
        :return: Dictionary representation.
        """
        for k, v in self.__dict__.items():
            if v is not None:
                yield k,  Model.get_value(v)

    @staticmethod
    def get_value(value):
        """
        Convert objects back to dictionary.
        :param value:
        :return:
        """
        if isinstance(value, list):
            return [Model.get_value(v) for v in value]
        if issubclass(type(value), Model):
            return dict(value)
        return value

    @classmethod
    def parameters(cls):
        parameters = copy(inspect.getargspec(cls.__init__).args)
        parameters.remove('self')
        return parameters

    @classmethod
    def from_dict(cls, data):
        kwargs = {}
        for arg in cls.parameters():
            kwargs[arg] = Model.get_data(data.pop(arg))
        model = cls(**kwargs)
        model.__dict__.update(data)
        return model

    @staticmethod
    def get_data(value):
        if isinstance(value, list):
            return [Model.get_data(v) for v in value]
        # Got damn 2.7 and no annotations
        if hasattr(value, 'keys'):
            key_name = value.keys()[0]
            for klass in [Recipient, Message, EmailAddress, ItemBody, Attachment]:
                if key_name == klass.__name__:
                    return klass.from_dict(value[key_name])
        return value

    @property
    def data(self):
        return {self.__class__.__name__(self)}


class ItemBody(Model):

    def __init__(self, Content=None, ContentType='Text'):
        """
        Body is a complex type in Office365
        :param ContentType: Can be Text or HTML
        :param Content: Body Content.
        """
        self.ContentType = ContentType
        self.Content = Content


class Recipient(Model):
    """
    Represents information about a user in the sending or receiving end of an event or message.
    """

    # noinspection PyShadowingNames
    def __init__(self, EmailAddress=None):
        """
        c-tor
        :param EmailAddress: The recipient's email address.
        """
        self.EmailAddress = EmailAddress

    @classmethod
    def from_email(cls, email):
        name, _ = email.split('@')
        return cls(EmailAddress=EmailAddress(Name=name, Address=email))


class EmailAddress(Model):
    """
    The name and email address of a contact or message recipient.
    """

    def __init__(self, Name, Address):
        """
        c-tor
        :param Name:  The display name of the person or entity.
        :param Address: The email address of the person or entity.
        """
        self.Name = Name
        self.Address = Address


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
            if data.get('@odata.type') == '#Microsoft.OutlookServices.FileAttachment' \
            else FileAttachment.from_dict(data=data)

    @property
    def writable_properties(self):
        raise NameError


class ItemAttachment(Attachment):
    pass


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
            bs = stream.read()
            content_bytes = str(base64.b64encode(bs))
            return cls(Name=name, ContentBytes=content_bytes)
