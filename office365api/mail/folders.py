from office365api.mail.api import Api
from office365api.model.folder import Folder


class Folders(Api):
    """
    Folder management class.
    """

    FOLDERS_URL = Api.BASE_URL + '/folders'
    FOLDER_URL = FOLDERS_URL + '/{folder_id}'
    SUB_FOLDER_URL = FOLDER_URL + '/childfolders'

    def get_count(self):
        """
        Get count of all folders in mail account.
        :return: Count of folders
        """
        url = self.FOLDERS_URL + '/$count'
        response = self.connection.get(url=url)
        return response.json()

    def get_all_folders(self):
        """
        Get all folders in mail account.
        :return: List of folders
        """
        url = self.FOLDERS_URL
        response = self.connection.get(url=url)
        data = response.json()
        return [Folder.from_dict(value) for value in data.get('value')] if data else []

    def get_sub_folders(self, folder_id):
        """
        Get sub folders in the folder.
        :return: List of folders
        """
        url = self.SUB_FOLDER_URL.format(folder_id=folder_id)
        response = self.connection.get(url=url)
        data = response.json()
        return [Folder.from_dict(value) for value in data.get('value')] if data else []

    def get_folder(self, folder_id):
        """
        Get folder.
        :return: folder
        """
        url = self.FOLDER_URL.format(folder_id=folder_id)
        response = self.connection.get(url=url)
        data = response.json()
        return Folder.from_dict(data) if data else None
