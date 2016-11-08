from office365api.model.email_address import EmailAddress
from office365api.model.model import Model


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
