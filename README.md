# openstack-snapshot
该项目主要是向OpenStack中引入libvirt的磁盘外部快照功能。便于虚拟机出现问题、数据损坏时，从外部快照恢复。
适用于openstack的liberty版本。
使用时，只要直接将文件的对应的路径覆盖即可。

为了正常使用light-snapshot系统的功能，需要修改数据库中相关表。

主要是在nova数据库的instances表中增加一列：

```
mysql -u root -p password

use nova

alter table instances add column light_snapshot_enable tinyint(1);

```

这样，在创建虚拟机时，可以规定哪些虚拟机可以使用我们的快照系统，哪些不可以或者不用使用我们的快照系统，以便
在编码中对虚拟机进行分情况处理。
