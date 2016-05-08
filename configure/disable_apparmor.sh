#!/bin/bash

ln -s /etc/apparmor.d/usr.sbin.libvirtd  /etc/apparmor.d/disable/

ln -s /etc/apparmor.d/usr.lib.libvirt.virt-aa-helper  /etc/apparmor.d/disable/

apparmor_parser -R  /etc/apparmor.d/usr.sbin.libvirtd

apparmor_parser -R  /etc/apparmor.d/usr.lib.libvirt.virt-aa-helper

