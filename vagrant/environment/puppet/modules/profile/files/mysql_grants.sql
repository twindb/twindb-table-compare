CREATE USER IF NOT EXISTS 'dba'@'%' IDENTIFIED BY 'qwerty';
CREATE USER IF NOT EXISTS 'dba'@'localhost' IDENTIFIED BY 'qwerty';
CREATE USER IF NOT EXISTS 'repl'@'%' IDENTIFIED WITH mysql_native_password BY 'slavepass';

GRANT ALL ON *.* TO 'dba'@'%';
GRANT ALL ON *.* TO 'dba'@'localhost';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';
