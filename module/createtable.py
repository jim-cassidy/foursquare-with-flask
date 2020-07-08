import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn
 
 
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
     #   c.execute(create_table_sql)
    except Error as e:
        print(e)
 
 
def main():
    database = r"saved.db"
 
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS list (
                                        names VARCHAR(20) , id VARCHAR(30)) """

  #  sql_deletetable = """ DROP TABLE scores  """


    sql_create_projects_table2 = """ CREATE TABLE IF NOT EXISTS scores (
                                        id integer NOT NULL,
                                        satdate date NOT NULL,
                                        score integer NOT NULL
                                    ); """

   
 
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute(sql_create_projects_table)
    print ("executed!!!")
 
    # create a database connection
  #  conn = create_connection(database)
      
   # conn.execute(sql_deletetable)
    # create tables
    if conn is not None:
        # create projects table
     #   create_table(conn, sql_create_projects_table)
	create_table(conn, sql_create_projects_table)
        print ("created")
        c = conn.cursor()
        c.execute(sql_create_projects_table)



    else:
        print("Error! cannot create the database connection.")
 
 
if __name__ == '__main__':
    main()
