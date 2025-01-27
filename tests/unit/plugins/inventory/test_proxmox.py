# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jeffrey van Pelt <jeff@vanpelt.one>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# The API responses used in these tests were recorded from PVE version 6.2.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.inventory.data import InventoryData
from ansible_collections.community.general.plugins.inventory.proxmox import InventoryModule


@pytest.fixture(scope="module")
def inventory():
    r = InventoryModule()
    r.inventory = InventoryData()
    return r


def test_verify_file_bad_config(inventory):
    assert inventory.verify_file('foobar.proxmox.yml') is False


def get_auth():
    return True


# NOTE: when updating/adding replies to this function,
# be sure to only add only the _contents_ of the 'data' dict in the API reply
def get_json(url):
    if url == "https://localhost:8006/api2/json/nodes":
        # _get_nodes
        return [{"type": "node",
                 "cpu": 0.01,
                 "maxdisk": 500,
                 "mem": 500,
                 "node": "testnode",
                 "id": "node/testnode",
                 "maxcpu": 1,
                 "status": "online",
                 "ssl_fingerprint": "xx",
                 "disk": 1000,
                 "maxmem": 1000,
                 "uptime": 10000,
                 "level": ""}]
    elif url == "https://localhost:8006/api2/json/pools":
        # _get_pools
        return [{"poolid": "test"}]
    elif url == "https://localhost:8006/api2/json/nodes/testnode/lxc":
        # _get_lxc_per_node
        return [{"cpus": 1,
                 "name": "test-lxc",
                 "cpu": 0.01,
                 "diskwrite": 0,
                 "lock": "",
                 "maxmem": 1000,
                 "template": "",
                 "diskread": 0,
                 "mem": 1000,
                 "swap": 0,
                 "type": "lxc",
                 "maxswap": 0,
                 "maxdisk": "1000",
                 "netout": 1000,
                 "pid": "1000",
                 "netin": 1000,
                 "status": "running",
                 "vmid": "100",
                 "disk": "1000",
                 "uptime": 1000}]
    elif url == "https://localhost:8006/api2/json/nodes/testnode/qemu":
        # _get_qemu_per_node
        return [{"name": "test-qemu",
                 "cpus": 1,
                 "mem": 1000,
                 "template": "",
                 "diskread": 0,
                 "cpu": 0.01,
                 "maxmem": 1000,
                 "diskwrite": 0,
                 "netout": 1000,
                 "pid": "1001",
                 "netin": 1000,
                 "maxdisk": 1000,
                 "vmid": "101",
                 "uptime": 1000,
                 "disk": 0,
                 "status": "running"},
                {"name": "test-qemu-template",
                 "cpus": 1,
                 "mem": 0,
                 "template": 1,
                 "diskread": 0,
                 "cpu": 0,
                 "maxmem": 1000,
                 "diskwrite": 0,
                 "netout": 0,
                 "pid": "1001",
                 "netin": 0,
                 "maxdisk": 1000,
                 "vmid": "9001",
                 "uptime": 0,
                 "disk": 0,
                 "status": "stopped"}]
    elif url == "https://localhost:8006/api2/json/pools/test":
        # _get_members_per_pool
        return {"members": [{"uptime": 1000,
                            "template": 0,
                             "id": "qemu/101",
                             "mem": 1000,
                             "status": "running",
                             "cpu": 0.01,
                             "maxmem": 1000,
                             "diskwrite": 1000,
                             "name": "test-qemu",
                             "netout": 1000,
                             "netin": 1000,
                             "vmid": 101,
                             "node": "testnode",
                             "maxcpu": 1,
                             "type": "qemu",
                             "maxdisk": 1000,
                             "disk": 0,
                             "diskread": 1000}]}
    elif url == "https://localhost:8006/api2/json/nodes/testnode/network":
        # _get_node_ip
        return [{"families": ["inet"],
                 "priority": 3,
                 "active": 1,
                 "cidr": "10.1.1.2/24",
                 "iface": "eth0",
                 "method": "static",
                 "exists": 1,
                 "type": "eth",
                 "netmask": "24",
                 "gateway": "10.1.1.1",
                 "address": "10.1.1.2",
                 "method6": "manual",
                 "autostart": 1},
                {"method6": "manual",
                 "autostart": 1,
                 "type": "OVSPort",
                 "exists": 1,
                 "method": "manual",
                 "iface": "eth1",
                 "ovs_bridge": "vmbr0",
                 "active": 1,
                 "families": ["inet"],
                 "priority": 5,
                 "ovs_type": "OVSPort"},
                {"type": "OVSBridge",
                 "method": "manual",
                 "iface": "vmbr0",
                 "families": ["inet"],
                 "priority": 4,
                 "ovs_ports": "eth1",
                 "ovs_type": "OVSBridge",
                 "method6": "manual",
                 "autostart": 1,
                 "active": 1}]
    elif url == "https://localhost:8006/api2/json/nodes/testnode/lxc/100/config":
        # _get_vm_config (lxc)
        return {
            "console": 1,
            "rootfs": "local-lvm:vm-100-disk-0,size=4G",
            "cmode": "tty",
            "description": "A testnode",
            "cores": 1,
            "hostname": "test-lxc",
            "arch": "amd64",
            "tty": 2,
            "swap": 0,
            "cpulimit": "0",
            "net0": "name=eth0,bridge=vmbr0,gw=10.1.1.1,hwaddr=FF:FF:FF:FF:FF:FF,ip=10.1.1.3/24,type=veth",
            "ostype": "ubuntu",
            "digest": "123456789abcdef0123456789abcdef01234567890",
            "protection": 0,
            "memory": 1000,
            "onboot": 0,
            "cpuunits": 1024,
            "tags": "one, two, three",
        }
    elif url == "https://localhost:8006/api2/json/nodes/testnode/qemu/101/config":
        # _get_vm_config (qemu)
        return {
            "tags": "one, two, three",
            "cores": 1,
            "ide2": "none,media=cdrom",
            "memory": 1000,
            "kvm": 1,
            "digest": "0123456789abcdef0123456789abcdef0123456789",
            "description": "A test qemu",
            "sockets": 1,
            "onboot": 1,
            "vmgenid": "ffffffff-ffff-ffff-ffff-ffffffffffff",
            "numa": 0,
            "bootdisk": "scsi0",
            "cpu": "host",
            "name": "test-qemu",
            "ostype": "l26",
            "hotplug": "network,disk,usb",
            "scsi0": "local-lvm:vm-101-disk-0,size=8G",
            "net0": "virtio=ff:ff:ff:ff:ff:ff,bridge=vmbr0,firewall=1",
            "agent": "1",
            "bios": "seabios",
            "ide0": "local-lvm:vm-101-cloudinit,media=cdrom,size=4M",
            "boot": "cdn",
            "scsihw": "virtio-scsi-pci",
            "smbios1": "uuid=ffffffff-ffff-ffff-ffff-ffffffffffff"
        }
    elif url == "https://localhost:8006/api2/json/nodes/testnode/qemu/101/agent/network-get-interfaces":
        # _get_agent_network_interfaces
        return {"result": [
            {
                "hardware-address": "00:00:00:00:00:00",
                "ip-addresses": [
                    {
                        "prefix": 8,
                        "ip-address-type": "ipv4",
                        "ip-address": "127.0.0.1"
                    },
                    {
                        "ip-address-type": "ipv6",
                        "ip-address": "::1",
                        "prefix": 128
                    }],
                "statistics": {
                    "rx-errs": 0,
                    "rx-bytes": 163244,
                    "rx-packets": 1623,
                    "rx-dropped": 0,
                    "tx-dropped": 0,
                    "tx-packets": 1623,
                    "tx-bytes": 163244,
                    "tx-errs": 0},
                "name": "lo"},
            {
                "statistics": {
                    "rx-packets": 4025,
                    "rx-dropped": 12,
                    "rx-bytes": 324105,
                    "rx-errs": 0,
                    "tx-errs": 0,
                    "tx-bytes": 368860,
                    "tx-packets": 3479,
                    "tx-dropped": 0},
                "name": "eth0",
                "ip-addresses": [
                    {
                        "prefix": 24,
                        "ip-address-type": "ipv4",
                        "ip-address": "10.1.2.3"
                    },
                    {
                        "prefix": 64,
                        "ip-address": "fd8c:4687:e88d:1be3:5b70:7b88:c79c:293",
                        "ip-address-type": "ipv6"
                    }],
                "hardware-address": "ff:ff:ff:ff:ff:ff"
            },
            {
                "hardware-address": "ff:ff:ff:ff:ff:ff",
                "ip-addresses": [
                    {
                        "prefix": 16,
                        "ip-address": "10.10.2.3",
                        "ip-address-type": "ipv4"
                    }],
                "name": "docker0",
                "statistics": {
                    "rx-bytes": 0,
                    "rx-errs": 0,
                    "rx-dropped": 0,
                    "rx-packets": 0,
                    "tx-packets": 0,
                    "tx-dropped": 0,
                    "tx-errs": 0,
                    "tx-bytes": 0
                }}]}


def get_vm_status(node, vmtype, vmid, name):
    return True


def get_option(option):
    if option == 'group_prefix':
        return 'proxmox_'
    if option == 'facts_prefix':
        return 'proxmox_'
    elif option == 'want_facts':
        return True
    else:
        return False


def test_populate(inventory, mocker):
    # module settings
    inventory.proxmox_user = 'root@pam'
    inventory.proxmox_password = 'password'
    inventory.proxmox_url = 'https://localhost:8006'

    # bypass authentication and API fetch calls
    inventory._get_auth = mocker.MagicMock(side_effect=get_auth)
    inventory._get_json = mocker.MagicMock(side_effect=get_json)
    inventory._get_vm_status = mocker.MagicMock(side_effect=get_vm_status)
    inventory.get_option = mocker.MagicMock(side_effect=get_option)
    inventory._populate()

    # get different hosts
    host_qemu = inventory.inventory.get_host('test-qemu')
    host_qemu_template = inventory.inventory.get_host('test-qemu-template')
    host_lxc = inventory.inventory.get_host('test-lxc')
    host_node = inventory.inventory.get_host('testnode')

    # check if qemu-test is in the proxmox_pool_test group
    assert 'proxmox_pool_test' in inventory.inventory.groups
    group_qemu = inventory.inventory.groups['proxmox_pool_test']
    assert group_qemu.hosts == [host_qemu]

    # check if qemu-test has eth0 interface in agent_interfaces fact
    assert 'eth0' in [d['name'] for d in host_qemu.get_vars()['proxmox_agent_interfaces']]

    # check if lxc-test has been discovered correctly
    group_lxc = inventory.inventory.groups['proxmox_all_lxc']
    assert group_lxc.hosts == [host_lxc]

    # check if qemu template is not present
    assert host_qemu_template is None
