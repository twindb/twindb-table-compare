class profile::base (
    $user = 'vagrant'
) {

  user { $user:
    ensure => present
  }

  file { "/home/${user}":
    ensure => directory,
    owner  => $user,
    mode   => "0750"
  }

  file { "/home/${user}/.bashrc":
    ensure => present,
    owner  => $user,
    mode   => "0644",
    source => 'puppet:///modules/profile/bashrc',
  }

  file { '/root/.ssh':
    ensure => directory,
    owner => 'root',
    mode => '700'
  }

  file { '/root/.ssh/authorized_keys':
    ensure => present,
    owner => 'root',
    mode => '600',
    source => 'puppet:///modules/profile/id_rsa.pub'
  }

  file { '/root/.ssh/id_rsa':
    ensure => present,
    owner => 'root',
    mode => '600',
    source => 'puppet:///modules/profile/id_rsa'
  }

  file { ["/home/${user}/.my.cnf", "/root/.my.cnf"]:
    ensure => absent,
  }

  package { [
      'make',
      'vim',
      'netcat',
      'net-tools',
      'mysql-client',
      'mysql-server',
      'percona-toolkit',
      'python3-pip',
      'python-is-python3'
  ]:
    ensure => installed,
  }

  service { 'mysql':
    ensure => running,
    enable => true,
    require => Package['mysql-server']
  }

  file { "/home/${user}/mysql_grants.sql":
    ensure => present,
    owner  => $user,
    mode   => "0400",
    source => 'puppet:///modules/profile/mysql_grants.sql',
  }

  exec { 'Create MySQL users':
    path    => '/usr/bin:/usr/sbin',
    command => "mysql -u root -h localhost < /home/$user/mysql_grants.sql",
    require => [
        Service['mysql'],
        File["/home/${user}/mysql_grants.sql"]
    ],
    before => File["/home/${user}/.my.cnf"],
    unless => 'mysql -e "SHOW GRANTS FOR dba@localhost"'
  }

    file { '/usr/bin/pip':
        ensure => link,
        target => '/usr/bin/pip3',
    }

}
