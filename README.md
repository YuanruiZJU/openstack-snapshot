# openstack-snapshot
该项目主要是向OpenStack中引入libvirt的磁盘外部快照功能。便于虚拟机出现问题、数据损坏时，从外部快照恢复。
适用于openstack的liberty版本。

使用时，用户首先按照官方文档，安装L版本的OpenStack。然后直接将文件的对应的路径覆盖即可，相关命令如下：
```
# cp -r openstack-snapshot/dist-packages/* /usr/lib/python2.7/dist-packages/
# cp -r openstack-snapshot/openstack-dashboard/* /usr/share/openstack-dashboard/
```

* 为了正常使用light-snapshot系统的功能，需要修改数据库中相关表。
  主要是在nova数据库的instances表中增加6列：
```
# mysql -u root -p password

MariaDB [(none)]> use nova

MariaDB [nova]> alter table instances add column light_snapshot_enable tinyint(1);

MariaDB [nova]> alter table instances add column snapshot_committed tinyint(1);

MariaDB [nova]> alter table instances add column snapshot_index int(11);

MariaDB [nova]> alter table instances add column root_index int(11);

MariaDB [nova]> alter table instances add column snapshot_store tinyint(1);

MariaDB [nova]> alter table instances add column snapshot_daily tinyint(1);
```
增加`light_snapshot_enable`，这样，我们可以规定哪些虚拟机可以使用我们的快照系统，哪些不可以或者不用使用我们的快照系统，以便在编码中对虚拟机进行分情况管理。

增加`snapshot_committed`，主要是因为，当虚拟机进行冷迁移、热迁移、resize都操作时，都需要先把全部的snapshot磁盘commit回root disk，最后再次创建虚拟机的时候，可以根据`light_snapshot_enable`和`snapshot_committed`，在开机的时候，判断是否需要做light-snapshot系统的初始化工作。

增加`snapshot_index`，从而能够通过数据库记录当前虚拟机创建了多少个快照，同时我们可以对我们的快照文件避免重复使用文件名，这样，我们就可以将所有删除掉的快照文件，都统一保存到另外一个文件夹中。同时，我们在硬重启的时候，不需要依赖libvirt来获取当前虚拟机的磁盘文件，这样libvirt出现问题时，我们仍然可以正常启动虚拟机。

增加`root_index`, 记录最后一个commit到虚拟机的disk镜像文件的index, 这样我们需要保存所有快照时，首先将原来的快照做硬链接到相应的文件夹，然后commit到根磁盘，然后rm删除快照文件的目录项，最后通过rebase命令和`root_index`更改做硬链接的那个快照文件的base镜像，然后更改数据库中`root_index`

增加`snapshot_store`，表示当前虚拟机是否需要保存。

增加`snapshot_daily`，表示虚拟机是否每天定时打快照


当更改完数据库之后，需要将nova的服务全部重启之后，使更改的数据库有效:
```
在控制节点上：
# service nova-api restart
# service nova-cert restart
# service nova-conductor restart
# service nova-scheduler restart
# service nova-consoleauth restart
# service nova-novncproxy restart

在计算节点上：
# service nova-compute restart
```

* 为了能够正常使用libvirt的相关功能，需要在计算节点上禁用apparmor，操作步骤如下：
```
$ ln -s /etc/apparmor.d/usr.sbin.libvirtd  /etc/apparmor.d/disable/

$ ln -s /etc/apparmor.d/usr.lib.libvirt.virt-aa-helper  /etc/apparmor.d/disable/

$ apparmor_parser -R  /etc/apparmor.d/usr.sbin.libvirtd

$ apparmor_parser -R  /etc/apparmor.d/usr.lib.libvirt.virt-aa-helper
```
然后重启该机器。
