from office365api.mail.folder import Folder
from office365api.model import Message


class Inbox(Folder):

    @property
    def folder_name(self):
        return 'Inbox'
