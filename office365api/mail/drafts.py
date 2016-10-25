from office365api.mail.folder import Folder
from office365api.model import Message
from office365api.model.attachment import Attachment


class Drafts(Folder):

    @property
    def folder_name(self):
        return 'Drafts'

    def reply(self, message: Message, comment: str=None, to_all: bool=False):
        """
        Sends reply to sender and other recipients.
        :param message: Message to reply to, only Id is important.
        :param comment: Optional comment.
        :param to_all: If true reply to other recipients as well.
        :return: None
        """
        url = (self.REPLY_ALL_URL if to_all else self.REPLY_URL).format(id=message.Id)
        self.connection.post(url=url, data={'Comment': comment or ''})

    def create_attachment(self, message: Message, attachment: Attachment):
        """

        :param message:
        :param attachment:
        :return:
        """
        self.create_attachment_in_folder(self.folder_name, message=message, attachment=attachment)
