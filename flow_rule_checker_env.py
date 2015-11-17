from functools import partial
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import Link
from mininet.node import RemoteController, OVSSwitch, Host


class VLANHost(Host):
    def config(self, vlan_id, **params):
        r = super(VLANHost, self).config(**params)
        intf = self.defaultIntf()

        vlan_intf = '%s.%d' % (intf, vlan_id)
        self.cmd('ip addr del %s dev %s' % (params['ip'], intf))
        self.cmd('ip link add link %s name %s type vlan id %d' % (
            intf, vlan_intf, vlan_id
        ))
        self.cmd('ip addr add %s brd 10.255.255.255 dev %s' % (
            params['ip'], vlan_intf
        ))
        self.cmd('ip link set dev %s up' % (vlan_intf))

        intf.name = vlan_intf
        self.nameToIntf[vlan_intf] = intf

        return r


if '__main__' == __name__:
    switch = partial(OVSSwitch, protocols='OpenFlow10')
    net = Mininet(switch=switch)

    c0 = RemoteController('c0')
    net.addController(c0)

    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h5 = net.addHost('h5', cls=VLANHost, vlan_id=200)

    Link(s1, s2, intfName1="s1-eth1", intfName2="s2-eth1")

    Link(h1, s1)
    Link(h2, s1)
    Link(h5, s2)

    net.build()

    h1.intf('h1-eth0').setMAC('0a:00:00:00:00:01')
    h2.intf('h2-eth0').setMAC('0a:00:00:00:00:02')
    h5.intf('h5-eth0').setMAC('0a:00:00:00:00:05')

    net.start()
    CLI(net)
    net.stop()
