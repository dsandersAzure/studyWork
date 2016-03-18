import sqlite3, os

class Notification_Service_Database(object):
    __db_name = None
    __db_conn = None
    __db_cursor = None

    def __init__(self,
                 port_number='5000',
                 server_name='localhsot'
    ):
        self.__server_name = server_name
        self.__port_number = port_number

        self.__db_name = 'datavolume/'+server_name+'-'+str(port_number)+\
            '-notifications.db'

        self.__db_conn = None
        self.__db_cursor = None

        self.__validate_notification_table()


    def __open_db(self):
        try:
            self.__db_conn = sqlite3.connect(self.__db_name)
            self.__db_cursor = self.__db_conn.cursor()
        except Exception as e:
            print(repr(e))
            if not self.__db_cursor == None:
                self.__db_cursor.close()
            if not self.__db_conn == None:
                self.__db_conn.close()


    def __validate_notification_table(self):
        _returned = None

        try:
            self.__open_db()
            self.__db_exec('select * from notifications')
        except sqlite3.OperationalError as oe:
            print(str(oe))
            self.__db_cursor.execute(
                    'CREATE TABLE notifications( '+\
                    '  id integer primary key autoincrement, '+\
                    '  sender string not null, '+\
                    '  recipient string not null,' +\
                    '  notification string not null, '+\
                    '  action string not null, '+\
                    '  event_date string not null '+\
                    ')'
                )
        except Exception as e:
            print(repr(e))
            raise
        finally:
            self.__close_db()


    def __db_exec(self, sql_statement=None, sql_parameters=()):
        if sql_statement == None:
            return None

        _returned = None

        try:
            if self.__db_cursor == None:
                raise Exception('Cursor does not exist!')
            self.__db_cursor.execute(sql_statement, sql_parameters)
        except Exception as e:
            print(repr(e))
            raise


    def __close_db(self):
        if not self.__db_cursor == None:
            self.__db_cursor.close()
        if not self.__db_conn == None:
            self.__db_conn.close()
        self.__db_cursor = None
        self.__db_conn = None


    def get_notifications(
        self,
        recipient=None
    ):
        if recipient == None:
            return []

        returned = None
        try:
            self.__open_db()
            self.__db_exec('select * from notifications '+\
                           'where recipient = ?',
                           (recipient,))
            returned = self.__db_cursor.fetchall()
            self.__db_conn.commit()
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()

        return returned


    def clear_notification(
        self,
        identifier=None
    ):
        if identifier == None:
            return []

        returned = True
        try:
            self.__open_db()
            self.__db_exec('delete from notifications '+\
                           'where id = ?',
                           (identifier,))
            self.__db_conn.commit()
        except Exception as e:
            returned = False
            print(repr(e))
        finally:
            self.__close_db()

        return returned


    def clear_notifications(
        self,
        recipient=None
    ):
        if recipient == None:
            return []

        returned = True
        try:
            self.__open_db()
            self.__db_exec('delete from notifications '+\
                           'where recipient = ?',
                           (recipient,))
            self.__db_conn.commit()
        except Exception as e:
            returned = False
            print(repr(e))
        finally:
            self.__close_db()

        return returned


    def save_notification(
        self,
        sender=None,
        recipient=None,
        text=None,
        action=None,
        event_date=None
    ):
        returned = None
        try:
            self.__open_db()
            self.__db_exec('insert into notifications ('+\
                           ' sender, '+\
                           ' recipient, '+\
                           ' notification, '+\
                           ' action, '+\
                           ' event_date) '+\
                           'values (?,?,?,?,?)',
                           (sender, recipient, text, action, event_date))
            self.__db_conn.commit()
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()

        return True


