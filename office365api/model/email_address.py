from office365api.model.model import Model


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