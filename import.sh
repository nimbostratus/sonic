#!/bin/sh
mysql -u root -e "drop database sonic"
mysql -u root -e "create database sonic"
rm -rf site_media
./manage.py migrate
./manage.py import
