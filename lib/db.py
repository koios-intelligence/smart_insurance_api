from pymongo import MongoClient
import json


class DataBase(object):

    def __init__(self):
        with open('config.json') as json_data_file:
            config = json.load(json_data_file)

        db_name = config['db']['name']
        db_uri = config['db']['uri']
        self.db = MongoClient(db_uri)[db_name]

    def update_db(self, table_name, key, field, value):
        """
        Update the value(s) of a(many) field(s) in a specific
        table
        :param table_name:
            String
        :param key:
            Primary key (field, value) pair
        :param field:
            Name of the field(s) you wish to
            update, String, list or dict
            if dictionary, all the information is
            in the field variable and value is
            set to None
        :param value:
            New value(s) for the field
        :return:
            Boolean
        """
        table = self.db[table_name]
        if isinstance(field, dict):
            assert value is None
            update_results = table.update_one(key,
                                              {
                                                  '$set': field
                                              })
        elif isinstance(field, list):
            assert len(field) == len(value)
            update_results = table.update_one(key,
                             {
                                 '$set': {
                                     field[i]: value[i] for i in range(len(field))
                                 }
                             })

        else:
            update_results = table.update_one(key,
                             {
                                 '$set': {
                                     field: value
                                 }
                             })

        if update_results.matched_count == 0:
            return False
        else:
            return True

    def find(self, table_name, key):
        """
        Find object in a table
        :param table_name:
            String
        :param key:
            (field, value) pair
        :return:
            object or None
        """
        table = self.db[table_name]

        return table.find_one(key)

    def insert(self, table_name, field, value):
        """

        Insert the value(s) of a(many) field(s) in a specific
        table
        :param table_name:
            String
        :param field:
            Name of the field(s) you wish to
            update, String
        :param value:
            New value(s) for the field(s)
        :return:
            True
        """
        table = self.db[table_name]

        if isinstance(field, list):
            assert len(field) == len(value)
            insert_results = table.insert_one({
                field[i]: value[i] for i in range(len(field))
            })

        else:
            insert_results = table.insert_one({field: value})

        return True