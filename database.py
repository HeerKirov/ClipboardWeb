import pymongo
import config


client = pymongo.MongoClient("mongodb://%s:%s/" % (config.mongodb['host'], config.mongodb['port']))
db = client[config.mongodb['name']]

record_col = db['record']
option_col = db['option']


class Record(object):
    mongo_id = None
    id = None
    content = None
    content_type = None
    sign = None
    password = None
    file_name = None
    file_type = None
    create_time = None
    create_ip = None

    def __init__(self, **kwargs):
        self.mongo_id = kwargs.get('_id', None)
        self.id = kwargs.get('id')
        self.content = kwargs.get('content', '')
        self.content_type = kwargs.get('content_type')
        self.sign = kwargs.get('sign', None)
        self.password = kwargs.get('password', None)
        self.file_name = kwargs.get('file_name', None)
        self.file_type = kwargs.get('file_type', None)
        self.create_time = kwargs.get('create_time')
        self.create_ip = kwargs.get('create_ip')

    def to_json(self, no_mongo_id=False):
        ret = {
            'id': self.id,
            'content': self.content,
            'content_type': self.content_type,
            'create_time': self.create_time,
            'create_ip': self.create_ip
        }
        if self.mongo_id is not None and not no_mongo_id:
            ret['_id'] = self.mongo_id
        if self.password is not None:
            ret['password'] = self.password
        if self.sign is not None:
            ret['sign'] = self.sign
        if self.file_name is not None:
            ret['file_name'] = self.file_name
        if self.file_type is not None:
            ret['file_type'] = self.file_type
        return ret

    @staticmethod
    def create(**kwargs):
        record = Record(**kwargs)
        record.mongo_id = record_col.insert_one(record.to_json())
        return record

    @staticmethod
    def update(record):
        if isinstance(record, Record) and record.mongo_id is not None:
            record_col.update_one({'_id': record.mongo_id}, {'$set': record.to_json(no_mongo_id=True)})
            return record
        else:
            raise Exception('Record object is not illegal.')

    @staticmethod
    def delete(record):
        if isinstance(record, Record) and record.mongo_id is not None:
            record_col.delete_one({'_id': record.mongo_id})
            return record
        else:
            raise Exception('Record object is not illegal.')

    @staticmethod
    def retrieve(record_id):
        return record_col.find_one({'id': record_id})


class Option(object):
    mongo_id = None
    record_count = None

    def __init__(self, **kwargs):
        self.mongo_id = kwargs.get('_id', None)
        self.record_count = kwargs.get('record_count', 0)

    def to_json(self, no_mongo_id=False):
        ret = {
            'record_count': self.record_count
        }
        if self.mongo_id is not None and not no_mongo_id:
            ret['_id'] = self.mongo_id
        return ret

    @staticmethod
    def get():
        results = option_col.find()
        if results.count() <= 0:
            option_col.insert_one({'record_count': 0})
            results = option_col.find()
        result = results[0]
        return Option(**result)

    @staticmethod
    def update(option):
        if isinstance(option, Option) and option.mongo_id is not None:
            ret = option_col.update_one({'_id': option.mongo_id}, {'$set': option.to_json(no_mongo_id=True)})
            return option
        else:
            raise Exception('Option object is not illegal.')
