class profile::master {
    include profile::base

    file { '/etc/mysql/mysql.conf.d/mysqld.cnf':
        ensure => present,
        owner => 'mysql',
        source => 'puppet:///modules/profile/my-master.cnf',
        notify => Service['mysql'],
        require => Package['mysql-server']
    }

    exec { 'Create table for checksumming':
        path    => '/usr/bin:/usr/sbin',
        command => "mysql -e 'CREATE DATABASE IF NOT EXISTS test;
        CREATE TABLE test.t1(id int not null primary key auto_increment, name varchar(255));
        INSERT INTO test.t1(name) SELECT RAND()*100;
        INSERT INTO test.t1(name) SELECT name FROM test.t1;
        INSERT INTO test.t1(name) SELECT name FROM test.t1;
        INSERT INTO test.t1(name) SELECT name FROM test.t1;
        INSERT INTO test.t1(name) SELECT name FROM test.t1;
        INSERT INTO test.t1(name) SELECT name FROM test.t1;
        INSERT INTO test.t1(name) SELECT name FROM test.t1;
        INSERT INTO test.t1(name) SELECT name FROM test.t1;
        INSERT INTO test.t1(name) SELECT name FROM test.t1;
        INSERT INTO test.t1(name) SELECT name FROM test.t1;
        INSERT INTO test.t1(name) SELECT name FROM test.t1;
        INSERT INTO test.t1(name) SELECT name FROM test.t1;
        INSERT INTO test.t1(name) SELECT name FROM test.t1;
        INSERT INTO test.t1(name) SELECT name FROM test.t1;
        INSERT INTO test.t1(name) SELECT name FROM test.t1;
        INSERT INTO test.t1(name) SELECT name FROM test.t1;
        INSERT INTO test.t1(name) SELECT name FROM test.t1;
        INSERT INTO test.t1(name) SELECT name FROM test.t1;
        INSERT INTO test.t1(name) SELECT name FROM test.t1;'",
        require => [ Service['mysql'] ],
        unless => 'mysql -e "DESC test.t1"'
    }

    exec { 'Run pt-tc':
        path    => '/usr/bin:/usr/sbin',
        command => "pt-table-checksum",
        require => [
            Service['mysql'],
            Exec['Create table for checksumming'],
            Package['percona-toolkit'],
        ],
        unless => 'mysql -e "SHOW TABLES FROM percona"',
        returns => [16, 8]
    }
}
