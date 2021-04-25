import subprocess

# The files in the /DATA directory should be
# postgresql.conf-master, postgresql.conf-slave, 
# recovery.conf-master0, recovery.conf-master1 y recovery.conf-master2
# Based in the pgpool-clusterconfig repo
#
# 1 Master down / 2 Slaves up
# reconfigure slave to master

def new_master_node(node_number):
    result = subprocess.run(["ssh", "root@dbpostgres" + str(int(node_number)+1) + ".xx.xx.com", 
                "/usr/bin/cp -a /DATA/pgsql_data/postgresql.conf-master /DATA/pgsql_data/postgresql.conf;/usr/bin/rm -f /DATA/pgsql_data/recovery.conf;systemctl restart postgresql-11"],
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False)
    return(result.stderr.decode())

#reconfigure slave to replicate from the new master
def reconfig_slave(node_number, node_master_number):
    result = subprocess.run(["ssh", "root@dbpostgres" + str(int(node_number)+1) + ".xx.xx.com", 
                "/usr/bin/cp -a /DATA/pgsql_data/recovery.conf-master" + node_master_number + " /DATA/pgsql_data/recovery.conf;systemctl restart postgresql-11"],
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False)
    return(result.stderr.decode())

#promote node to master
def reconfig_cluster():    
    result = subprocess.run(["ssh", "root@dbpostgres-balancer.xx.xx.com", 
                "systemctl stop pgpool;sleep 30;/usr/bin/rm -f /var/log/pgpool/pgpool_status;systemctl start pgpool"],
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False)
    return(result.stderr.decode())