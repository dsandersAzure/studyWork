from notifications import app, api
import sqlite3

port_number = 5000

def check_key(key=None):
    if key==None:
        return False

    database_name = 'datavol/notifications.db'
    try:
        return_data = ''
        database_opened = False
        updated_data = False

        db_connection = sqlite3.connect(database_name)
        db_cursor = db_connection.cursor()
        database_opened = True
        db_cursor.execute(
            'select value from configuration where key = ?',
            (key,) \
        )

        db_records = db_cursor.fetchone()

        db_cursor.close()
        db_connection.close()

        if db_records == None:
            return True # Default to a locked state if database is empty!

        if db_records[0].upper() == 'TRUE':
            return True;
        else:
            return False;
    except Exception as e:
        raise Exception('Something went wrong!')

