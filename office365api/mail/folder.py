from typing import List
from office365api.mail.base import Base


class Folder(Base):
    @property
    def folder_name(self):
        raise NotImplementedError('This class cannot be used without inheritance.')

    def get_messages(self, select: List = None,
                     filters: str = None,
                     search: str = None,
                     order_by=None,
                     top: int = 50,
                     skip: int = 0):
        """
        Downloads messages to local memory.

        :param skip:  Page results, skip - default 0.

        :param top: Page size, default take first 50 messages.

        :param select: The list of additional fields to retrieve.
        ['Bcc', 'IsDeliveryReceiptRequested']. By default returns only fields required for
        Message class.

        :param filters: Filters for messages OData 4.0 compatible.
        Example: "From/EmailAddress/Address ne 'MicrosoftOffice365@email.office.com'"

        :param search: Search criteria. When supplying string looks in subject, body etc
        if you want to look in a particular field 'from:microsoft'

        :param order_by: Order by field name. Example: 'DateTimeReceived desc'

        :param page: Paging settings.
        """
        return self.get_messages_from_folder(folder=self.folder_name,
                                             select=select,
                                             filters=filters,
                                             search=search,
                                             order_by=order_by,
                                             top=top, skip=skip)
