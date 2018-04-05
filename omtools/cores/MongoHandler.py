# -*- coding: utf-8 -*-
# @Time    : 4/2/2018 10:34 AM
# @Author  : Abbott
# @Site    : 
# @File    : MongoHandler.py
# @Software: PyCharm

from omtools.cores.commons import *
from omtools.cores.logsutils import *
import datetime

class MongoFunction:

    def __init__(self, query_data):
        self.source_mongodb = 'test'

        self.commons = commons()

        self.logfile = ''
        self.LoggingConf = CommonLogging(self.logfile)
        self.time_now = datetime.datetime.now()

        msg = 'task_time: {0}, task_info: {1}'.format(self.time_now, query_data)
        self.LoggingConf.logging_info(msg)

        self.db = query_data['db']
        self.table = query_data['table']
        self.project = query_data['project']
        self.type = query_data['type']
        self.query = query_data['query']
        self.taskId = query_data['task_id']

        self.mongodb_execute_conn = self.commons.mongo_conn_collection(self.commons.mongoconf.mongo_conn(self.commons.get_Mongodb_info[self.source_mongodb][self.db]), self.db, self.table)


    def backup_mongodb(self):

        mongodb_backup_conn = self.commons.mongo_conn_collection(self.commons.mongoconf.mongo_conn(self.commons.get_Mongodb_info[self.source_mongodb]['backup']), self.db, self.table)
        online_data = self.mongodb_execute_conn.find(self.query['condition'])
        online_data_count = self.mongodb_execute_conn.find(self.query['condition']).count()
        backup_insert = []
        for item in online_data:
            item['old_id'] = item['_id']
            item['backupTime'] = self.time_now
            del item['_id']
            backup_insert.append(item)
        mongodb_backup_conn.insert_many(backup_insert)
        newquery = self.query['condition']
        newquery['backupTime'] = self.time_now
        backup_data_count = mongodb_backup_conn.find(newquery).count()
        msg = 'task_id: {0}, online_data_count: {1}, backup_data_count: {2}'.format(self.taskId, online_data_count, backup_data_count)
        self.LoggingConf.logging_info(msg)
        if online_data_count != backup_data_count:
            msg = 'task_id: {0}, backup failed, delete backup first, backup again.'.format(self.taskId, online_data_count,
                                                                                        backup_data_count)
            self.LoggingConf.logging_info(msg)
            mongodb_backup_conn.delete_many(newquery)
            self.backup_mongodb()

    def find_query(self, conn, query):
        status = 200
        try:
            if query['property'] is None:
                result = conn.find(query['condition'])
            else:
                result = conn.find(query['condition'], query['property'])
            msg = 'task_id: {0}, status: {1}, result: {2}'.format(self.taskId, status, result)
            self.LoggingConf.logging_info(msg)
            return {'status': status, 'result': result}
        except Exception as e:
            status = 500
            msg = 'task_id: {0}, status: {1}'.format(self.taskId, status)
            self.LoggingConf.logging_error(msg)
            return {'status': status}

    def update_query(self, conn, query):
        status = 200
        try:
            if query['property'] == True:
                result = conn.update_many(query['condition'], query['set'])
            else:
                result = conn.update(query['condition'], query['set'])

            msg = 'task_id: {0}, status: {1}, result: {2}'.format(self.taskId, status, result[0])
            self.LoggingConf.logging_info(msg)
            return {'status': status, 'result': result}
        except Exception as e:
            msg = 'task_id: {0}, status: {1}'.format(self.taskId, status)
            self.LoggingConf.logging_error(msg)
            status = 500
            return {'status': status}

    def insert_query(self, conn, query):
        conn.insert(query['condition'])

    def delete_query(self, conn, query):
        conn.delete(query['condition'])

    def execute_mongodb(self):
        if self.type == "update":
            self.backup_mongodb()
            result = self.update_query(self.mongodb_execute_conn, self.query)
            return result
        elif self.type == "find":
            result = self.find_query(self.mongodb_execute_conn, self.query)
            return result
        elif self.type == "insert":
            pass
        else:
            pass

if __name__ == '__main__':
    query = {'db': 'logsdb', 'table': 'proposal', 'project': '', 'type': 'update',
             'query': {'condition': {'a': {'$in': ['1']}}, 'set': {'$set': {'b': '1'}}, 'property': True}}

    # query = {'db': 'logsdb', 'table': 'proposal', 'project': '', 'type': 'find',
    #          'query': {'condition': {'a': {'$in': ['1']}}, 'set': None, 'property': None}}
    MongoFunction(query).execute_mongodb()
