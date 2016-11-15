from office365api.mail.mailbox import MailBox


class Inbox(MailBox):
    """
    Inbox mailbox methods.
    """

    @property
    def folder_name(self):
        return 'Inbox'
