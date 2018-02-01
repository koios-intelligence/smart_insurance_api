from passlib.apps import custom_app_context as pwd_context
from lib.db import DataBase


# TODO: Fix this function
def check_pw(password):
    """
    Check whether the password
    string entered is in concordance
    with some specified standards

    :param password:
        String
    :return:
        Boolean
    """

    return True


class User(object):

    def __init__(self):
        self.db = DataBase()

    def store_password(self, password, username):
        """
        Store hashed password in the DB
        :param password:
            String
        :param username:
            String
        :return:
            Boolean
        """

        # check if username already exists
        db_response = self.db.find(table_name='users',
                                   key={'username': username})

        if db_response is None:

            password_hash = pwd_context.encrypt(password)
            self.db.insert(table_name='users',
                           field=['username', 'password'],
                           value=[username, password_hash]
                           )
            return True
        else:
            return False

    def verify_password(self, password, username):
        """
        Verify if the password entered match the
        one store in DB
        :param password:
            String
        :param username:
            String
        :return:
            Boolean
        """
        db_response = self.db.find(table_name='users',
                                   key={'username': username})
        try:
            if db_response is not None:
                password_hash = db_response['password']
                return pwd_context.verify(password, password_hash)
            else:
                return NotImplementedError
        except ValueError:
            return False
