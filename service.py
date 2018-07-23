import database
from datetime import datetime
import config
import os
import sys

CONTENT_TYPE = (
    ('txt', 'Text'),
    ('md', 'Markdown'),
    ('auto', 'Auto language'),
    ('c', 'C/C++'),
    ('java', 'Java'),
    ('js', 'Javascript'),
    ('xml', 'XML/HTML'),
    ('go', 'Golang')
)


def is_std_type(type_name):
    for (k, v) in CONTENT_TYPE:
        if k == type_name:
            return True
    return False


def get_file_type(filename):
    ext = filename.rsplit('.', 1)[1]


def get_file_real_path(record_id=None):
    if record_id is None:
        if config.file_uploads['path'][0] == '/':
            return os.path.join(config.file_uploads['path'])
        else:
            return os.path.join(sys.path[0], config.file_uploads['path'])
    else:
        if config.file_uploads['path'][0] == '/':
            return os.path.join(config.file_uploads['path'], '%s.upload' % (record_id,))
        else:
            return os.path.join(sys.path[0], config.file_uploads['path'], '%s.upload' % (record_id,))


class RecordService(object):
    @staticmethod
    def add(content, content_type, create_ip, sign=None, password=None, file=None):
        if not is_std_type(content_type):
            return None
        file_name = file.filename if file is not None else None
        file_type = get_file_type(file.filename) if file is not None else None
        option = database.Option.get()
        record_id = int(option.record_count) + 1
        result = database.Record.create(content=content, content_type=content_type,
                                        sign=sign, password=password,
                                        create_time=datetime.now(), create_ip=create_ip,
                                        file_name=file_name, file_type=file_type,
                                        id=record_id)
        if file is not None:
            file_path = get_file_real_path(record_id)
            file.save(file_path)
        option.record_count += 1
        database.Option.update(option)
        return result

    @staticmethod
    def get(record_id):
        return database.Record.retrieve(record_id)


class ServiceException(Exception):
    def __init__(self, msg):
        super(ServiceException, self).__init__(msg)

