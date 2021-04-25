import psycopg2
from psycopg2 import pool
try:
    postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 2,user = "postgres",
                                              password = "xxxxx",
                                              host = "xx.xx.xx.xx",
                                              port = "xxxx",
                                              database = "postgres")
    if(postgreSQL_pool):
        print("Connection pool created successfully")
    # Use getconn() method to Get Connection from connection pool
    ps_connection  = postgreSQL_pool.getconn()
    if(ps_connection):
        print("successfully recived connection from connection pool ")
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute("show pool_nodes")
        nodes = ps_cursor.fetchall()
        print ("Cluster status:")
        for row in nodes:
            print (row)
        ps_cursor.close()
        #Use this method to release the connection object and send back ti connection pool
        postgreSQL_pool.putconn(ps_connection)
        print("Put away a PostgreSQL connection")
except (Exception, psycopg2.DatabaseError) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
    # use closeall method to close all the active connection if you want to turn of the application
    if (postgreSQL_pool):
        postgreSQL_pool.closeall
    print("PostgreSQL connection pool is closed")