#!/usr/bin/env bash

# Ensure root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Add pgRouting launchpad repository
sudo apt-add-repository -y ppa:ubuntugis/ppa
sudo apt-add-repository -y ppa:georepublic/pgrouting
sudo apt-get update

# Install pgRouting package (for Ubuntu 14.04)
sudo apt-get --yes --force-yes install postgresql-9.3-pgrouting postgresql-server-dev-9.3  python-psycopg2 pv

# Install osm2pgrouting package
sudo apt-get --yes --force-yes install osm2pgrouting

# set postgress user password
cd /tmp; echo  "ALTER USER postgres with encrypted password 'postgres';" | /usr/bin/sudo -u postgres psql template1; cd -

# enable password login
echo "host    replication     postgres        127.0.0.1/32            md5" >> /etc/postgresql/9.3/main/pg_hba.conf

#restart server
service postgresql restart


SQL="
-- create tabel if not exist
DROP DATABASE IF EXISTS pgrouting;
CREATE DATABASE pgrouting
OWNER = postgres;"

cd /tmp; echo "$SQL" | /usr/bin/sudo -u postgres psql template1; cd -

SQL="
-- Enable PostGIS (includes raster)
CREATE EXTENSION postgis;
-- Enable Topology
CREATE EXTENSION postgis_topology;
-- fuzzy matching needed for Tiger
CREATE EXTENSION fuzzystrmatch;
-- Enable US Tiger Geocoder
CREATE EXTENSION postgis_tiger_geocoder;
-- add pgRouting core functions
CREATE EXTENSION pgrouting;"

cd /tmp; echo "$SQL" | /usr/bin/sudo -u postgres psql pgrouting; cd -


# install lighthttpd (remember to attach the server to a security group with http
# access enabled ie launch-wizard-1 )
# also some other packages
apt-get install --yes --force-yes lighttpd python-pip git-core
pip install flup  flask

cd ${0%/*}
mv /var/www/ /tmp/
mkdir /var/www
#git clone https://github.com/gisgroup/soeingisdingdemo.git www
cp -R ../* /var/www/
cd /var/
chown postgres:www-data /var/www -Rf

pv /var/www/dump.sql.bz2 | bunzip2 | PGPASSWORD=postgres psql -U postgres -h localhost pgrouting

# set lighttpd config files
cp /var/www/server_config/lighttpd.conf /etc/lighttpd/lighttpd.conf
cp /var/www/server_config/10-fastcgi.conf /etc/lighttpd/conf-available/10-fastcgi.conf
ln -s /etc/lighttpd/conf-available/10-fastcgi.conf /etc/lighttpd/conf-enabled

# lighttpd now runs as postgres
chmod g+rwx /var/log/lighttpd -Rf
chown postgres:www-data /var/www -Rf

service lighttpd restart
