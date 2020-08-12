import dropbox
from .config import API_TOKEN

dbx_object = dropbox.Dropbox(API_TOKEN)


def upload(dbx_object, name, data_to_save, overwrite=True):
    path = '/binary_data_storage/' + name
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    data = data_to_save
    print(data)
    res = dbx_object.files_upload(
        data, path, mode,
        mute=True)
    return res


def download(dbx_object, name):
    path = '/binary_data_storage/' + name
    md, res = dbx_object.files_download(path)
    data = res.content
    return data
