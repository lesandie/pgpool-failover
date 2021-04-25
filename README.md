
# A Python3 monitorization and management tool for a PostgreSQL 11 multinode cluster (master/slave streaming replication)

# Index

1. [Python3 instalation](#py3install)
2. [Use cases](#usecases)

## Python3 and Psycopg2 install

The python3 instalation shoul be in the node that will execute the python failover app, being the pgpool-II node the logical candidate.

**Python3 installation in Ubuntu 18.04:**

```bash
$sudo apt-get install python3
```

**Python3 installation in CentOS 7:**

```bash
$sudo yum install python3
```

**PsycoPg2 install:**

Psycopg2 is a python library/API compatible with python2 and 3, for interacting with a PostgreSQL database

```bash
$sudo yum/apt install python-psycopg2
```

## Use Cases

In this section we'll explain which use cases and scenarios are available.

### 1 Master down / 2 Slaves up

In this case, we should promote the 2nd node (dbpostgres2) to master and reconfigure the 3rd node (dbpostgres3) to replicate from the new master.

So, we should access the folder */DATA/pgsql_data* at the 2nd node and copy the *postgresql.conf-master* to overwrite the *postgresql.conf*. After this we should remove the *recovery.conf* file, because this node is going to be the new master. Then execute *systemctl restart postgresql* and it should restart the service as the new master.

Next we should reconfigure the 3rd node to replicate from the new master. We should copy the file *recovery.conf-slave* to overwrite the *recovery.conf* file. Execute *systemctl restart postgresql* and it should replicate in a couple of minutes.

Finally, at the pgpool node, we should restart the service with *systemctl restart pgpool*

### 1 Master and 1 slave down / Only 1 slave up

In this scenario we should reconfigure the node and promote it to master, following the above instructions.
