from office365api.model.model import Model


# noinspection PyPep8Naming
class Folder(Model):
    """
    The folder info.
    """

    def __init__(self,
                 Id: str,
                 ParentFolderId: str,
                 DisplayName: str,
                 ChildFolderCount: int,
                 TotalItemCount: int=0,
                 UnreadItemCount: int=0,
                 ):
        """
        c-tor
        :param Id: The folder's unique identifier.
        :param ParentFolderId: The unique identifier for the folder's parent folder.
        :param DisplayName: The folder's display name.
        :param ChildFolderCount: The number of folders in the folder.
        :param TotalItemCount: The number of items in the folder.
        :param UnreadItemCount: The number of items in the folder marked as unread.
        """
        self.TotalItemCount = TotalItemCount
        self.UnreadItemCount = UnreadItemCount
        self.DisplayName = DisplayName
        self.ChildFolderCount = ChildFolderCount
        self.Id = Id
        self.ParentFolderId = ParentFolderId
