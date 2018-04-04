# -*- coding: utf-8 -*-
# @Time    : 4/2/2018 10:34 AM
# @Author  : Abbott
# @Site    : 
# @File    : MongoHandler.py
# @Software: PyCharm

from omtools.cores.commons import *
#from logsutils import *
import datetime

class MongoFunction:

    def __init__(self, query_data):
        self.source_mongodb = 'test'
        self.commons = commons()

        self.db = query_data['db']
        self.table = query_data['table']
        self.project = query_data['project']
        self.type = query_data['type']
        self.query = query_data['query']

        self.mongodb_execute_conn = self.commons.mongo_conn_collection(self.commons.mongoconf.mongo_conn(self.commons.get_Mongodb_info[self.source_mongodb][self.db]), self.db, self.table)


    def backup_mongodb(self):
        time_now = datetime.datetime.now()
        mongodb_backup_conn = self.commons.mongo_conn_collection(self.commons.mongoconf.mongo_conn(self.commons.get_Mongodb_info[self.source_mongodb]['backup']), self.db, self.table)
        online_data = self.mongodb_execute_conn.find(self.query['condition'])
        online_data_count = self.mongodb_execute_conn.find(self.query['condition']).count()
        backup_insert = []
        for item in online_data:
            item['old_id'] = item['_id']
            item['backupTime'] = time_now
            del item['_id']
            backup_insert.append(item)
        mongodb_backup_conn.insert_many(backup_insert)
        newquery = self.query['condition']
        newquery['backupTime'] = time_now
        backup_data_count = mongodb_backup_conn.find(newquery).count()
        if online_data_count != backup_data_count:
            mongodb_backup_conn.delete_many(self.query['condition'])
            self.backup_mongodb()

    def find_query(self, conn, query):
        try:
            if query['property'] is None:
                result = conn.find(query['condition'])
            else:
                result = conn.find(query['condition'], query['property'])
            return {'status': 200, 'result': result}
        except Exception as e:
            return {'status': 500}

    def update_query(self, conn, query):
        try:
            if query['property'] == True:
                result = conn.update_many(query['condition'], query['set'])
            else:
                result = conn.update(query['condition'], query['set'])

            return {'status': 200, 'result': result}
        except Exception as e:
            return {'status': 500}

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
