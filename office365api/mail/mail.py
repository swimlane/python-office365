from office365api.mail.base import Base
from office365api.mail.drafts import Drafts
from office365api.mail.inbox import Inbox


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
