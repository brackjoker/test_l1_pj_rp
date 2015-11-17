from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
from ryu.lib import ofctl_v1_0


class FlowTester(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(FlowTester, self).__init__(*args, **kwargs)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        print('## Switch Features: dpid=%d' % datapath.id)
        self.add_flow(datapath)

    def add_flow(self, datapath):
        dpid = datapath.id
        print('## New switch is joined: %s' % dpid)

        dut_vlan_vid = 200
        wire_id = 101

        # forward #########################################

        # default
        deny_any_flow = {
            'match': {
                # match any
            },
            'actions': [
                # empty : action DROP
            ],
            'priority': 0
        }

        # host1 -> host5
        s1_wire15_flow = {
            'match': {
                'in_port': 2,
                'dl_src': "0a:00:00:00:00:01"
            },
            'actions': [
                {
                    'type': 'SET_VLAN_VID',
                    'vlan_vid': wire_id
                },
                {
                    'type': 'OUTPUT',
                    'port': 1
                }
            ]
        }
        s2_wire15_flow = {
            'match': {
                'in_port': 1,
                'dl_src': "0a:00:00:00:00:01",
                'dl_vlan': wire_id
            },
            'actions': [
                {
                    'type': 'SET_VLAN_VID',
                    'vlan_vid': dut_vlan_vid
                },
                {
                    'type': 'OUTPUT',
                    'port': 2
                }
            ]
        }

        # host2 -> host5
        s1_wire25_flow = {
            'match': {
                'in_port': 3,
                'dl_src': "0a:00:00:00:00:02"
            },
            'actions': [
                {
                    'type': 'SET_VLAN_VID',
                    'vlan_vid': wire_id
                },
                {
                    'type': 'OUTPUT',
                    'port': 1
                }
            ]
        }
        s2_wire25_flow = {
            'match': {
                'in_port': 1,
                'dl_src': "0a:00:00:00:00:02",
                'dl_vlan': wire_id
            },
            'actions': [
                {
                    'type': 'SET_VLAN_VID',
                    'vlan_vid': dut_vlan_vid
                },
                {
                    'type': 'OUTPUT',
                    'port': 2
                }
            ]
        }

        # backward ########################################

        # host5 -> host1
        s2_wire51_flow = {
            'match': {
                'in_port': 2,
                'dl_dst': "0a:00:00:00:00:01",
                'dl_vlan': dut_vlan_vid
            },
            'actions': [
                {
                    'type': 'SET_VLAN_VID',
                    'vlan_vid': wire_id
                },
                {
                    'type': 'OUTPUT',
                    'port': 1
                }
            ]
        }
        s1_wire51_flow = {
            'match': {
                'in_port': 1,
                'dl_dst': "0a:00:00:00:00:01",
                'dl_vlan': wire_id
            },
            'actions': [
                {
                    'type': 'STRIP_VLAN',
                },
                {
                    'type': 'OUTPUT',
                    'port': 2
                }
            ]
        }

        # host5 -> host2
        s2_wire52_flow = {
            'match': {
                'in_port': 2,
                'dl_dst': "0a:00:00:00:00:02",
                'dl_vlan': dut_vlan_vid
            },
            'actions': [
                {
                    'type': 'SET_VLAN_VID',
                    'vlan_vid': wire_id
                },
                {
                    'type': 'OUTPUT',
                    'port': 1
                }
            ]
        }
        s1_wire52_flow = {
            'match': {
                'in_port': 1,
                'dl_dst': "0a:00:00:00:00:02",
                'dl_vlan': wire_id
            },
            'actions': [
                {
                    'type': 'STRIP_VLAN',
                },
                {
                    'type': 'OUTPUT',
                    'port': 3
                }
            ]
        }

        # broadcast for wiregroup1
        s2_wg1_flow_bc = {
            'match': {
                'in_port': 2,
                'dl_dst': "ff:ff:ff:ff:ff:ff",
                'dl_vlan': dut_vlan_vid
            },
            'actions': [
                {
                    'type': 'SET_VLAN_VID',
                    'vlan_vid': wire_id
                },
                {
                    'type': 'OUTPUT',
                    'port': 1
                }
            ]
        }
        s1_wg1_flow_bc = {
            'match': {
                'in_port': 1,
                'dl_dst': "ff:ff:ff:ff:ff:ff",
                'dl_vlan': wire_id
            },
            'actions': [
                {
                    'type': 'STRIP_VLAN'
                },
                {
                    'type': 'OUTPUT',
                    'port': 2
                },
                {
                    'type': 'OUTPUT',
                    'port': 3
                }
            ]
        }

        s1_flows = [
            deny_any_flow,
            s1_wire15_flow, s1_wire25_flow, s1_wire51_flow, s1_wire52_flow,
            s1_wg1_flow_bc
        ]
        s2_flows = [
            deny_any_flow,
            s2_wire15_flow, s2_wire25_flow, s2_wire51_flow, s2_wire52_flow,
            s2_wg1_flow_bc
        ]

        if dpid == 0x1:
            # for switch1 (s1)
            for flow in s1_flows:
                ofctl_v1_0.mod_flow_entry(datapath, flow, ofproto_v1_0.OFPFC_ADD)
        elif dpid == 0x2:
            # for switch2 (s2)
            for flow in s2_flows:
                ofctl_v1_0.mod_flow_entry(datapath, flow, ofproto_v1_0.OFPFC_ADD)
