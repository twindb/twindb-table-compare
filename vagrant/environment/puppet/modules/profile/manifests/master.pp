class profile::master {
    include profile::base

    file { '/etc/my.cnf':
        ensure => present,
        owner => 'mysql',
        source => 'puppet:///modules/profile/my-master.cnf',
        notify => Service['mysql']
    }
}
