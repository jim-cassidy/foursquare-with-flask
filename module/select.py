import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn
 
 
def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
   # cur.execute("PRAGMA table_info(students)")
    #cur.execute("INSERT INTO list ( names ) VALUES ( 10 )")
    cur.execute("SELECT id, names FROM list")
  #  cur.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';")

    print ("executed..")

    rows = cur.fetchall()
  #  print ( rows )
    for row in rows:
        print( str(row[1]) + " " + str(row[0]))
 
 
def select_task_by_priority(conn, priority):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM list", (priority,))
 
  
    rows = cur.fetchall()
 
    for row in rows:
        print(row)
 
 
def main():
    database = r"saved.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
         
 
        print("1. Select all tasks")
        select_all_tasks(conn)
 
 
if __name__ == '__main__':
    main()
