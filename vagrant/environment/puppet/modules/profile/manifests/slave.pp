class profile::slave {
    include profile::base

    file { '/etc/mysql/mysql.conf.d/mysqld.cnf':
        ensure => present,
        owner => 'mysql',
        source => 'puppet:///modules/profile/my-slave.cnf',
        notify => Service['mysql'],
        require => Package['mysql-server']
    }

    exec { 'Configure replication on slave':
        path    => '/usr/bin:/usr/sbin',
        command => "mysql -u root -e \"STOP SLAVE; CHANGE MASTER TO MASTER_HOST = '192.168.35.250', MASTER_USER = 'repl', MASTER_PASSWORD = 'slavepass', MASTER_AUTO_POSITION = 1; START SLAVE;\"",
        require => Service['mysql']
    }

}
