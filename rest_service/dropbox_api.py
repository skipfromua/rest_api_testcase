import dropbox
from config import API_TOKEN, CACHING_ON
from local_storage_mongo import unloaded_data, cached_data
from requests.exceptions import ConnectionError

dbx_object = dropbox.Dropbox(API_TOKEN)


def upload(dbx_object, key_value, data_to_save):
    path, mode = _standart_variables(key_value)
    try:
        _send_previously_unloaded_data(mode)
        res = dbx_object.files_upload(data_to_save, path, mode, mute=True)
        return res
    except ConnectionError:
        _caching_failure_uploaded_data(key_value, data_to_save)
        return '200 OK'


def download(dbx_object, key_value):
    path, mode = _standart_variables(key_value)
    try:
        _send_previously_unloaded_data(mode)
        md, res = dbx_object.files_download(path)
        data = res.content
        if CACHING_ON:
            _caching_downloaded_data(key_value, data)
        return data
    except ConnectionError:
        data = _find_by_key_value_from_database(key_value)
        if data:
            return 'Resource is temporary unavailable, returned from cache {}'.format(data.get('data')).encode()
        return 'Resource is temporary unavailable'.encode()


def _caching_downloaded_data(key_value, data):
    key_value_already_in_database = cached_data.find_one({'key_value': key_value})
    if key_value_already_in_database:
        cached_data.delete_one(key_value_already_in_database)
    cached_data.insert_one({'key_value': key_value, 'data': data})


def _find_by_key_value_from_database(key_value):
    return cached_data.find_one({'key_value': key_value})


def _send_previously_unloaded_data(mode):
    for one_of_unloaded_data in unloaded_data.find():
        path = '/binary_data_storage/{}'.format(one_of_unloaded_data.get('key_value'))
        dbx_object.files_upload(one_of_unloaded_data.get('data'), path, mode, mute=True)
        unloaded_data.delete_one(one_of_unloaded_data)


def _caching_failure_uploaded_data(key_value, data):
    already_in = unloaded_data.find_one({'key_value': key_value})
    if already_in:
        unloaded_data.delete_one(already_in)
    unloaded_data.insert({'key_value': key_value, 'data': data})


def _standart_variables(key_value):
    return '/binary_data_storage/{}'.format(key_value), dropbox.files.WriteMode.overwrite
