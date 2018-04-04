from bson.objectid import ObjectId
import datetime
from pymongo.errors import AutoReconnect
import platform, os, sys
import django
from pymongo import MongoClient
from omtools.cores import redis_handler

if platform.system() == 'Linux':
    sys.path.append('/app/project/AutoDeploy')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoDeploy.settings")
django.setup()

from omtools import models as OMTOOLS_MODELS


class MongodbHandler:
    def __init__(self):

        self.mongo_collection_conn = self.mongo_conn()["test"]["logs"]

    def mongo_conn(self):
        """
        :param kwargs:mongo连接方式字典
        :return: mongo认证后的client，方便使用
        """
        client = MongoClient(host=['10.168.11.54:27018'])
        db_auth = client.admin
        db_auth.authenticate("admin", "admin@)!&")
        return client

    def exec(self):

        result = self.mongo_collection_conn.insert_one({"items": 111})


class MissionHandler:
    def __init__(self):
        pass

    def get_mission_from_db(self, mission_id):
        data_from_db = OMTOOLS_MODELS.MongodbMission.objects.get(id=mission_id)
        return data_from_db

    def post_api(self, mission_obj):
        m_db = mission_obj.database
        m_document = mission_obj.document
        m_find = mission_obj.find
        m_update = mission_obj.update
        m_multi_tag = mission_obj.multi_tag

        query = {
            'condition': m_find,
            'set': m_update,
            'property': {'multi': m_multi_tag},
        }


if __name__ == '__main__':
    redis_queue = redis_handler.RedisQueue('mongodb')
    while True:
        mission_from_redis = redis_queue.get_wait()
        mission_id = int(mission_from_redis[1])
        mission_handler = MissionHandler()
        mission_obj = mission_handler.get_mission_from_db(mission_id)
        mission_handler.post_api(mission_obj)