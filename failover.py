import psycopg2
import time
import subprocess
import logging
from ssh_commands import *
# The files in the /DATA directory should be
# postgresql.conf-master, postgresql.conf-slave, 
# recovery.conf-master0, recovery.conf-master1 y recovery.conf-master2
# Based in the pgpool-clusterconfig repo
#
# 1 Master down / 2 Slaves up
# reconfigure slave to master
try:
    # Connect to database
    postgreSQL_pool = psycopg2.connect("dbname=postgres user=postgres password=xxxxxx host=xxx.xxx.xxx.xxx port=xxxx")
    if(postgreSQL_pool):
        print("Connection created successfully")
        a = 0
        condicion = True
        while condicion == True:
            # executes every 5 sec. process_time() returns the current time
            b = time.process_time()
            if b - a > 5 :
                # Open a cursor to perform database operations
                ps_cursor = postgreSQL_pool.cursor()
                ps_cursor.execute("show pool_nodes")
                nodes = ps_cursor.fetchall()
                print("Cluster status:")
                for row in nodes:
                    dictList = dict()
                    info = []
                    for datos in row:
                        info.append(datos)
                    dictList = {
                        'node': info[0],'hostname': info[1],
                        'port': info[2],'status': info[3],
                        'lb_weight': info[4],'role': info[5],
                        'select_cnt': info[6],'load_balance': info[7],
                        'replication_delay': info[8],'last_status_change': info[9]
                    }
                    if dictList.get('status') == "down": 
                        if dictList.get('node') == "0":
                            error1 = new_master_node("1")
                            if error1 == '' :
                                error1 = reconfig_slave("2","1")
                                if error1 == '' :
                                    error1 = reconfig_cluster()
                                else:
                                    raise ValueError(error1)
                            else:
                                raise ValueError(error1)
                        else:
                            raise ValueError(error1)
                        if (dictList.get('node') == "0" and dictList.get('node') == "1"):
                            error1 = new_master_node("2")
                            if error1 == '' :
                                error1 = reconfig_cluster()
                            else:
                                raise ValueError(error1)
                        if (dictList.get('node') == "0" and dictList.get('node') == "2"):
                            error1 = new_master_node("1")
                            if error1 == '' :
                                error1 = reconfig_cluster()
                            else:
                                raise ValueError(error1)
                        condicion = False   
                    else:
                        print(dictList.get('node'),dictList.get('hostname'),
                            dictList.get('role'),dictList.get('status'))
                a = b 
        ps_cursor.close()

except (Exception, psycopg2.DatabaseError) as error :
    print ("Error while connecting to PostgreSQL:\n", error)

except ValueError as ve:
    logger = logging.getLogger(__name__)
    f_handler = logging.FileHandler('/var/log/pgpool/failover.log')
    f_handler.setLevel(logging.ERROR)
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)
    logger.error(ve)

finally:
    #closing database connection.
    postgreSQL_pool.close()
    print("PostgreSQL connection is closed")