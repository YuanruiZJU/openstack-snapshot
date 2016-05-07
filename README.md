# openstack-snapshot
该项目主要是向OpenStack中引入libvirt的磁盘外部快照功能。便于虚拟机出现问题、数据损坏时，从外部快照恢复。
适用于openstack的liberty版本。
使用时，只要直接将文件的对应的路径覆盖即可。

为了正常使用light-snapshot系统的功能，需要修改数据库中相关表。

主要是在nova数据库的instances表中增加两列：

```
mysql -u root -p password

use nova

alter table instances add column light_snapshot_enable tinyint(1);

alter table instances add column snapshot_committed tinyint(1);

```

增加`light_snapshot_enable`，这样，我们可以规定哪些虚拟机可以使用我们的快照系统，哪些不可以或者不用使用我们的快照系统，以便在编码中对虚拟机进行分情况管理。

增加`snapshot_committed`，主要是因为，用户可能有在关机的情况下将全部snapshot都commit到root disk的需要，另外，当虚拟机进行冷迁移、热迁移、resize都操作时，都需要先把全部的snapshot磁盘commit回root disk，最后再次创建虚拟机的时候，可以根据`light_snapshot_enable`和`snapshot_committed`，在开机的时候，判断是否需要做light-snapshot系统的初始化工作。

当更改完数据库之后，需要将nova的服务全部重启之后，使更改的数据库有效。
