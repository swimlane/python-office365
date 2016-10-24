from office365api.mail.folder import Folder


class Inbox(Folder):

    @property
    def folder_name(self):
        return 'Inbox'
