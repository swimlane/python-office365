from office365api.mail.base import Base
from office365api.mail.drafts import Drafts
from office365api.mail.inbox import Inbox
from office365api.mail.folders import Folders


class Mail(Base):
    _inbox = None

    @property
    def inbox(self):
        if not self._inbox:
            self._inbox = Inbox(self.auth)
        return self._inbox

    _drafts = None

    @property
    def drafts(self):
        if not self._drafts:
            self._drafts = Drafts(self.auth)
        return self._drafts

    _folders = None

    @property
    def folders(self):
        if not self._folders:
            self._folders = Folders(self.auth)
        return self._folders
