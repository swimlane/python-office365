from office365api import Mail
from dotenv import load_dotenv
from os.path import join, dirname, normpath
from os import environ

dot_env_path = normpath(join(dirname(__file__), '../', '.env'))
load_dotenv(dot_env_path)


def simplest(auth):
    mail = Mail(auth=auth)

    c = mail.folders.get_count()
    print('Folder count {0}'.format(c))

    m = mail.folders.get_all_folders()
    print('Folder names.')
    for folder in m:
        print("    {id} {name}".format(id=folder.Id, name=folder.DisplayName))

    for folder in (f for f in m if f.ChildFolderCount > 0):
        f_info = mail.folders.get_folder(folder_id=folder.Id)
        print('Subfolders of {name}'.format(name=folder.DisplayName))
        sf = mail.folders.get_sub_folders(folder.Id)
        for f in sf:
            print("    {id} {name}".format(id=f.Id, name=f.DisplayName))


if __name__ == '__main__':
    authorization = (environ.get('OFFICE_USER'), environ.get('OFFICE_USER_PASSWORD'))
    simplest(authorization)


