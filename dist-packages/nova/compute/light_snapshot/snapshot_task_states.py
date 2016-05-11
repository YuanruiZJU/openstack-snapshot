# Copyright 2010 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Possible task states for instances when instances is create snapshot using
   the function libvirt supports.
"""


# added by Yuanrui Fan. To Use the snapshot function of libvirt in new version
# we add snapshot function for openstack. Here is the task states for this function
VM_SNAPSHOT_PENDING = "light_snapshot_pending"
VM_SNAPSHOT = "light_snapshot"
VM_SNAPSHOT_COMMIT = "commit_last_snapshot"

VM_COMMIT_START = "commit_start"
VM_COMMITING = "committing"

VM_DELETE_SNAPSHOT = "vm_delete_snapshot"

VM_RECOVER_START = "recover_start"
VM_RECOVER_FROM_SNAPSHOT = "recovering"

DISABLE_SNAPSHOT = "disabling_light_snapshot"
ENABLE_SNAPSHOT = "enabling_light_snapshot"
