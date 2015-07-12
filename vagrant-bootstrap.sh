#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --force-yes python python-pip python-dev mysql-server mysql-client libmysqlclient-dev

# MySQL config
cat <<EOT >/etc/mysql/conf.d/listen_everywhere.cnf
[mysqld]
bind-address=0.0.0.0
EOT

echo "create database podium_dev;" | mysql -uroot
echo "create database podium_test;" | mysql -uroot
echo "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'password';" |mysql -uroot
mysqladmin -uroot password "password" # Not secure but this is not exposed to the internet, so it's fine
service mysql restart

cd /vagrant
sudo python setup.py develop

# python bcrypt doesn't install correctly...
pip uninstall bcrypt
pip install bcrypt