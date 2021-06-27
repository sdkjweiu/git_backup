import pymysql
conn = pymysql.connect(host='192.168.182.128', port=3306, user='mysqlID', passwd='mysqlPW', database='flasky')
cur = conn.cursor()

cur.execute('alter table user drop index username_index')
cur.execute('drop table user')
cur.execute('drop table role')
# cur.execute('create database flasky')
# cur.close()     #명령 끝
# conn.close()    #접속 끝

# conn = pymysql.connect(host='192.168.182.128', port=3306, user='mysqlID', passwd='mysqlPW', database='flasky')
# cur = conn.cursor()
cur.execute('create table role (id int primary key auto_increment, name varchar(64) unique)')
cur.execute('create table user (id int primary key auto_increment, username varchar(64) unique, role_id int, foreign key(role_id) references role(id) )')
cur.execute('create index username_index on user(username)')
cur.close()
conn.close()