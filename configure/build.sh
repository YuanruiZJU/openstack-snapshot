#!/bin/bash
cp -r ../dist-packages/* /usr/lib/python2.7/dist-packages/

service nova-api restart
service nova-conductor restart
service nova-scheduler restart
service nova-compute restart

