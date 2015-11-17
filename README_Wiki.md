##	L1patch環境のセットアップ
本書では一般的なソフトウェアのインストール方法は扱わない。  
今回実装したL1patchツール各種は下記の条件を満たすLinux OS上で動作する  
(PoCではUbuntu serverを使用)。

* Mininet2.2.22以降
* Ryu3.24以降
* Open vSwitch 2.0以降
* Python2.7系

※なお、Mininetを動作させるサーバは、2個以上のネットワークインタフェースを持つ必要がある。L1patchとしてMininetOVSにインタフェースを組み込む必要があるが、OVSへ組み込むと、サーバに対するリモートアクセスやOFCとの通信(OFCを別ホストに用意する場合)のためには使用できなくなるためである。

##  各種設定ファイルの作成
下記に本スクリプトで使用する設定ファイルのサンプルと書き方を示す。  
※設定ファイル内の「#」で始まる行は説明文となるため、設定する際には除いて設定を作成すること
1. テスト用ネットワークの設定ファイル作成
テスト対象ネットワークの情報と、テストしたい事をもとに、Lßpatchの設定情報を作成する。
 * 物理環境情報 (nodeinfo.json)  
   L1patchを使用してテスト環境を定義するための物理環境定義ファイルを示す。基本的には、最終的にL1patch動作ルール(OFSへ設定するフロールール)を生成するために必要な、テスト用ノード、接続先DUTのポート設定である。  
```
{
#テスト用ノード(Mininet Host)の情報定義。
"test-hosts": {  
"test-hosts": {
    "h1": {  
      "port-index": {  
        "h1-eth0": {  
#L1patch動作のために生成するフロールールは、テスト用ノードのMACアドレスをキーにするため、テスト用ノード設定ではMACアドレス指定が必須となる。
          "mac-addr": "0a:00:00:00:00:01",  
#IPアドレスとデフォルトゲートウェイについてはオプショナル。
          "ip-addr": "192.168.2.11/24",  
          "gateway": "192.168.2.254"  
{
#テスト用ノード(Mininet Host)の情報定義。
 "test-hosts": {
  "test-hosts": {
    "h1": {
      "port-index": {
        "h1-eth0": {
#L1patch動作のために生成するフロールールは、テスト用ノードのMACアドレスをキーにするため、テスト用ノード設定ではMACアドレス指定が必須となる。
          "mac-addr": "0a:00:00:00:00:01",
#IPアドレスとデフォルトゲートウェイについてはオプショナル。
          "ip-addr": "192.168.2.11/24",
          "gateway": "192.168.2.254"
        }
      }
    },
    "h2": {
      "port-index": {
        "h2-eth0": {
          "mac-addr": "0a:00:00:00:00:02",
          "ip-addr": "192.168.2.12/24",
          "gateway": "192.168.2.254"
        }
      }
    },
    "h3": {
      "port-index": {
        "h3-eth0": {
          "mac-addr": "0a:00:00:00:00:03",
          "ip-addr": "192.168.2.13/24",
          "gateway": "192.168.2.254"
        }
      }
    },
    "h4": {
      "port-index": {
        "h4-eth0": {
          "mac-addr": "0a:00:00:00:00:04",
          "ip-addr": "192.168.2.14/24",
          "gateway": "192.168.2.254"
        }
      }
    },
    "h5": {
      "port-index": {
        "h5-eth0": {
          "mac-addr": "0a:00:00:00:00:05",
          "ip-addr": "192.168.2.15/24"
        }
      }
    }
  },
#Dispatcher = L1patchとして動作するOpenFlow Switchの情報定義
 "dispatchers": {
#スイッチ"s1"はMininetが起動し、テスト用ノードが接続されるOFSである。PoC上は"s1/dpid:1"をテスト用ノードが接続されるデフォルトのスイッチとして仮定しているので注意。
   "s1": {
#OFC Datapath ID (10進数で指定する点に注意)
     "datapath-id": 1,
#コメント
     "description": "host edge switch",
#OFSのポート一覧(使うもの)
     "port-index": {
#ポート名
       "s1-eth1": {
#ポート番号(フロールール中で指定するOFSポート番号)
         "number": 1
       },
       "s1-eth2": {
         "number": 2
       },
       "s1-eth3": {
         "number": 3
       },
       "s1-eth4": {
         "number": 4
       },
       "s1-eth5": {
         "number": 5
       }
     }
   },
   "s2": {
     "datapath-id": 2,
     "description": "inter switch",
     "port-index": {
       "s2-eth1": {
         "number": 1
       },
       "s2-eth2": {
         "number": 2
       },
       "s2-eth3": {
         "number": 3
       },
       "s2-eth4": {
         "number": 4
       }
     }
   },
   "s3": {
     "datapath-id": 3,
     "description": "DUT edge switch",
     "port-index": {
       "s3-eth1": {
         "number": 1
       },
       "s3-eth2": {
         "number": 2
       },
       "s3-eth3": {
         "number": 3
       },
       "s3-eth4": {
         "number": 4
       },
       "s3-eth5": {
         "number": 5
       }
     }
   }
 },
 #物理トポロジ(どのポートからどのポートに対して物理リンクが張られているか)の情報。L1patchで接続するテスト用ノード・OFS(dispatcher)・DUTポートについて、物理リンクで直接結線されているポートのペアで定義。(ポート間対応、接続バリデーションなどで使用)
 "link-list": [
   [["h1", "h1-eth0"], ["s1", "s1-eth2"]],
   [["h2", "h2-eth0"], ["s1", "s1-eth3"]],
   [["h3", "h3-eth0"], ["s1", "s1-eth4"]],
   [["h4", "h4-eth0"], ["s1", "s1-eth5"]],
   [["h5", "h5-eth0"], ["s2", "s2-eth4"]],
   [["s1", "s1-eth1"], ["s2", "s2-eth1"]],
   [["s2", "s2-eth2"], ["s3", "s3-eth1"]],
   [["s2", "s2-eth3"], ["s3", "s3-eth2"]],
   [["h6", "h6-eth0.200"], ["s3", "s3-eth3"]],
   [["h7", "h7-eth0"], ["s3", "s3-eth4"]],
   [["h8", "h8-eth0"], ["s3", "s3-eth5"]]
 ]
}
```
DUT側ポートのVLAN指定について、ひとつの物理ポートで複数のVLANを利用するTrunkポートでは下記のように定義する。  
```
"dut-hosts": {
    "L2SW1": {
      "port-index": {
        "gi1/0/2.2013": {
          "vlan-tagged": true,
          "vlan-id": 2013
        },
        "gi1/0/2.2015": {
          "vlan-tagged": true,
          "vlan-id": 2015
        },
        "gi1/0/2.2016": {
          "vlan-tagged": true,
          "vlan-id": 2016
        },
#(省略)
      }
    },
```
 *	論理環境情報 (wireinfo.json)  
 テスト用ノードを、どのDUTポートへワイヤで接続するかを決める。  
```
{
 "wire-index" : {
#論理接続(ワイヤ)の定義
   "wire1": {
#コメント
     "description": "wire between host1(h1) and h6",
#ワイヤ動作モードの設定(共有モード)
     "mode": "shared",
#接続元(テスト用ノード側)の端点
     "test-host-port": ["h1", "h1-eth0"],
#接続先(テスト対象機器/DUT)側の端点
     "dut-host-port": ["h6", "h6-eth0.200"],
#端点～端点を結ぶときに通過するOFSのポート(現在は自動検出ではなく手動設定)。共有モードワイヤなので、同じ物理ポートを複数のワイヤ(wire2～wire4)で使用する。
     "path": [
       ["s1", "s1-eth2"],
       ["s1", "s1-eth1"],
       ["s2", "s2-eth1"],
       ["s2", "s2-eth2"],
       ["s3", "s3-eth1"],
       ["s3", "s3-eth3"]
     ]
   },
   "wire2": {
     "description": "wire between host2(h2) and h6",
     "mode": "shared",
     "test-host-port": ["h2", "h2-eth0"],
     "dut-host-port": ["h6", "h6-eth0.200"],
     "path": [
       ["s1", "s1-eth3"],
       ["s1", "s1-eth1"],
       ["s2", "s2-eth1"],
       ["s2", "s2-eth2"],
       ["s3", "s3-eth1"],
       ["s3", "s3-eth3"]
     ]
   },
   "wire3": {
     "description": "wire between host3(h3) and h7",
     "mode": "shared",
     "test-host-port": ["h3", "h3-eth0"],
     "dut-host-port": ["h7", "h7-eth0"],
     "path": [
       ["s1", "s1-eth4"],
       ["s1", "s1-eth1"],
       ["s2", "s2-eth1"],
       ["s2", "s2-eth2"],
       ["s3", "s3-eth1"],
       ["s3", "s3-eth4"]
     ]
   },
   "wire4": {
     "description": "wire between host4(h4) and h7",
     "mode": "shared",
     "test-host-port": ["h4", "h4-eth0"],
     "dut-host-port": ["h7", "h7-eth0"],
    "path": [
       ["s1", "s1-eth5"],
       ["s1", "s1-eth1"],
       ["s2", "s2-eth1"],
       ["s2", "s2-eth2"],
       ["s3", "s3-eth1"],
       ["s3", "s3-eth4"]
     ]
   },
   "wire5": {
     "description": "wire between host5(h5) and h8",
#専有モードワイヤ
     "mode": "exclusive",
#専有モードワイヤ端点の定義
     "test-host-port": ["h5", "h5-eth0"],
     "dut-host-port": ["h8", "h8-eth0"],
     "path": [
       ["s2", "s2-eth4"],
       ["s2", "s2-eth3"],
       ["s3", "s3-eth2"],
       ["s3", "s3-eth5"]
     ]
   }
 },
#ワイヤグループは、共有モードワイヤのL2 broadcast domain設定。
#ひとつのDUTポートに複数のwireを付ける場合、どのwireが同じセグメントに所属しているwireなのかを別途指定する必要があるため。
 "wire-group-index": {
   "wiregroup1":{
     "description": "DUT:h6, PORT:s6-eth6.200(vlan 200)",
#"id"(wire group id)の実装については5.3節参照。
     "id": 101,
#wiregroup1はDUT h6/h6-eth6.200 に接続されるふたつのワイヤを含むグループ
     "wires": ["wire1", "wire2"]
   },
   "wiregroup2": {
     "description": "DUT:h7, PORT:h7-eth0",
     "id": 102,
     "wires": ["wire3", "wire4"]
   }
 }
}
```


2. テストシナリオの設定ファイル作成  
設定したテスト対象ネットワーク、テスト用ノード配置をもとに、どのノードからどのノードに対して通信を行うかを定義する
 * テストパターン定義(scenario_pattern.json)  
```
{
 "params": {
   "@h1@": "192.168.2.11",
   "@h2@": "192.168.2.12",
   "@h3@": "192.168.2.13",
   "@h4@": "192.168.2.14",
   "@h5@": "192.168.2.15",
   "@h6@": "192.168.2.106",
   "@h7@": "192.168.2.107",
   "@h8@": "192.168.2.108"
 },
 "scenarios": {
   "test-node to dut": {
     "shared-wire-to-h6(SUCCESS)": [
       ["h1", "h2"],
       ["@h6@"]
     ],
     "shared-wire-to-h7(SUCCESS)": [
       ["h3", "h4"],
       ["@h7@"]
     ],
     "exclusive-wire-to-h8(SUCCESS)": [
       ["h5"],
       ["@h8@"]
     ]
   },
   "dut to test-node": {
     "shared-wire-to-h1_h2(SUCCESS)": [
       ["h6"],
       ["@h1@", "@h2@"]
     ],
     "shared-wire-to-h3_h4(SUCCESS)": [
       ["h7"],
       ["@h3@", "@h4@"]
     ],
     "exclusive-wire-to-h5(SUCCESS)": [
       ["h8"],
       ["@h5@"]
     ]
   }
 }
}
```
3. テスト定義ファイルの作成  
テスト環境やテストシナリオの定義ファイルをもとに、テスト自動実行のための定義ファイルを作成する。
 * テスト自動実行定義(testdefs.json)

 ```
#L1patchの設定情報
 "l1patch-defs": {
#L1patch物理構成定義ファイル(read)
   "physical-info-file": "nodeinfo_topo2.json",
#L1patch論理構成定義ファイル(read)
   "logical-info-file": "wireinfo_topo2.json",
#専有モードワイヤ用のフロールールを保存するファイル(write)
   "exclusive-wire-flows-file": "flows_exclusive_topo2.json",
#共有モードワイヤ用のフロールールを保存するファイル(write)
   "shared-wire-flows-file": "flows_shared_topo2.json",
#専有モードワイヤ用のフロールールを生成するためのコマンド
   "generate-exclusive-wire-flows-command": "python run_l1patch.py -p @physical-info@ -l @logical-info@ -m exclusive > @exclusive-wire-flows@",
#共有モードワイヤ 用のフロールールを生成するためのコマンド
   "generate-shared-wire-flows-command": "python run_l1patch.py -p @physical-info@ -l @logical-info@ -m shared > @shared-wire-flows@",
#専有モードワイヤ用のフロールールをOFCにPUTするコマンド
   "put-exclusive-wire-flows-command": "cat @exclusive-wire-flows@ | python patch_ofc_rest_knocker.py -m put",
#共有モードワイヤ用 のフロールールをOFCにPUTするコマンド
   "put-shared-wire-flows-command": "cat @shared-wire-flows@ |  python patch_ofc_rest_knocker.py -m put",
#専有モードワイヤ用のフロールールをOFCにDELETEするコマンド
   "delete-exclusive-wire-flows-command": "cat @exclusive-wire-flows@ | python patch_ofc_rest_knocker.py -m delete",
#共有モードワイヤ用のフロールールをOFCにDELETEするコマンド
   "delete-shared-wire-flows-command": "cat @shared-wire-flows@ |  python patch_ofc_rest_knocker.py -m delete"
 },
#テスト実行環境のパラメータ定義
 “test-env-params”: {
#L1patchを構成するOFSで使われるOpenFlow Version ("OpenFlow10" or "OpenFlow13")
   "ofs-openflow-version": "OpenFlow10",
#Mininetサーバが外部ネットワークと接続するために使うインタフェース名(複数設定可能)
   "mininet-external-interfaces": []
 },
# シナリオテストのパラメータ定義
 "ping-test-params": {
#ping テストで使うコマンド(コマンドオプション指定注意)
   "ping-command": "ping -i 0.2 -c 5",
 }
}
 ```

##  OpenFlowコントローラの起動
※サンプルのOFCのREST API URLはlocalhost:8080

> **#OpenFlow Controllerの起動**  
> hoge@prjexp01:~/PycharmProjects/l1patch-dev$ ryu-manager --verbose patch_ofc.py  

> **#以下画面表示**  
> loading app patch_ofc.py
> loading app ryu.controller.ofp_handler  
> (省略)  
>  (24249) wsgi starting up on http://0.0.0.0:8080/

##  L1patch設定の確認

L1patch物理情報定義(nodeinfo.json)作成にあたって、OFSのポート番号が必要になる。Mininetは通常ノード接続順にポートが指定されるが、あらかじめ内容を確認しておく必要がある。そのため、まず自動実行スクリプトをCLIモードで実行してMininet側の情報確認を行う。  

> hoge@prjexp01:~/PycharmProjects/l1patch-dev$ sudo python run_scenario_test.py -f testdefs_topo2.json --manual

* 手動テスト実行 (--manual)  
* Layerオプション指定なし: L1patchの設定は行われない  

> **#フローデータの生成。データ生成はおこなうがOFSへの投入は行われない。**  
> INFO - exec command: python run_l1patch.py -p nodeinfo_topo2.json -l wireinfo_topo2.json -m exclusive > flows_exclusive_topo2.json  
> **#シナリオファイルの生成。データ生成はおこなうがCLIモードでは使わない。**  
> INFO - exec command: python scenario_generator.py -f scenario_pattern_topo2_simple.json > scenario_topo2.json  
> **#-fオプションで指定されたテスト定義ファイル内のパラメータとして、"test-scenario-defs" - "class"指定がある場合は、指定されたclassで再読込する 。**  
> INFO - reload runner class: scenario_pinger_topo2.ScenarioPingerTopo2  
> INFO - exec command: python run_l1patch.py -p nodeinfo_topo2.json -l wireinfo_topo2.json -m exclusive > flows_exclusive_topo2.json  
> INFO - exec command: python run_l1patch.py -p nodeinfo_topo2.json -l wireinfo_topo2.json -m shared > flows_shared_topo2.json  
> INFO - exec command: python scenario_generator.py -f scenario_pattern_topo2_simple.json > scenario_topo2.json  
> **#テストを行う test-runner classを確認**  
> INFO - run scenario test with runner-class: ScenarioPingerTopo2  
> **#テスト用ノードを生成**  
> INFO - Start run_test()  
> INFO - build test host: test host h1[h1-eth0] = MAC:0a:00:00:00:00:01, IP:192.168.2.11/24, Gateway:192.168.2.254  
> INFO - build test host: test host h2[h2-eth0] = MAC:0a:00:00:00:00:02, IP:192.168.2.12/24, Gateway:192.168.2.254  
> INFO - build test host: test host h3[h3-eth0] = MAC:0a:00:00:00:00:03, IP:192.168.2.13/24, Gateway:192.168.2.254  
> INFO - build test host: test host h4[h4-eth0] = MAC:0a:00:00:00:00:04, IP:192.168.2.14/24, Gateway:192.168.2.254  
> INFO - build test host: test host h5[h5-eth0] = MAC:0a:00:00:00:00:05, IP:192.168.2.15/24, Gateway:None  
> **#CLIモードに入る**  
> mininet>   
> **#mininet topology を確認する(狙った順序でmininet ovsに接続されているかどうか)**  
> mininet> net  
> h1 h1-eth0:s1-eth3  
> h2 h2-eth0:s1-eth4  
> h3 h3-eth0:s1-eth5  
> h4 h4-eth0:s1-eth6  
> h5 h5-eth0:s1-eth7  
> h6 h6-eth0.200:s3-eth2  
> h7 h7-eth0:s3-eth3  
> h8 h8-eth0:s2-eth4  
> s1 lo:  s1-eth1:s2-eth1 s1-eth2:s2-eth2 s1-eth3:h1-eth0 s1-eth4:h2-eth0 s1-eth5:h3-eth0 s1-eth6:h4-eth0  s1-eth7:h5-eth0  
> s2 lo:  s2-eth1:s1-eth1 s2-eth2:s1-eth2 s2-eth3:s3-eth1 s2-eth4:h8-eth0  
> s3 lo:  s3-eth1:s2-eth3 s3-eth2:h6-eth0.200 s3-eth3:h7-eth0  
> c0  
> mininet>  
> **#OVSのポート番号を確認する**  
> **#外部ネットワーク(実機のテスト象NW)でテストを実行する場合は、外部接続用のインタフェースが含まれることを確認すること**  
> mininet> dpctl show

## 手動テスト実行
物理構成の確認ができたら、生成されるフロールールをOFCに投入し、テスト対象ネットワークを構成して手作業で動作を確認する。  
※外部の実機環境をテストする場合は、フロールールを設定してDUT間接続が成立してはじめて、テスト対象ネットワークの物理構成や簡単な通信テストが行えるようになる。  

> hoge@prjexp01:~/PycharmProjects/l1patch-dev$ sudo python run_scenario_test.py -f testdefs_topo2.json --manual --all-layers

* --manual 手動テスト実行  
* --all-layers すべてのワイヤを設定  

> **#フロールール生成・テストシナリオ生成を行う。**  
> **#(省略)**  
> INFO - reload runner class: scenario_pinger_topo2.ScenarioPingerTopo2  
> INFO - exec command: python run_l1patch.py -p nodeinfo_topo2.json -l wireinfo_topo2.json -m exclusive > flows_exclusive_topo2.json  
> INFO - exec command: python run_l1patch.py -p nodeinfo_topo2.json -l wireinfo_topo2.json -m shared > flows_shared_topo2.json  
> INFO - exec command: python scenario_generator.py -f scenario_pattern_topo2_simple.json > scenario_topo2.json  
> INFO - run scenario test with runner-class: ScenarioPingerTopo2  
> **#テスト用ノードを生成**  
> INFO - Start run_test()  
> INFO - build test host: test host h1[h1-eth0] = MAC:0a:00:00:00:00:01, IP:192.168.2.11/24, Gateway:192.168.2.254  
> INFO - build test host: test host h2[h2-eth0] = MAC:0a:00:00:00:00:02, IP:192.168.2.12/24, Gateway:192.168.2.254  
> INFO - build test host: test host h3[h3-eth0] = MAC:0a:00:00:00:00:03, IP:192.168.2.13/24, Gateway:192.168.2.254  
> INFO - build test host: test host h4[h4-eth0] = MAC:0a:00:00:00:00:04, IP:192.168.2.14/24,Gateway:192.168.2.254  
> INFO - build test host: test host h5[h5-eth0] = MAC:0a:00:00:00:00:05, IP:192.168.2.15/24, Gateway:None  
> **#生成したフロールールをOFC REST　APIに設定する**  
> INFO - put exclusive-wire-flow-rules  
> INFO - exec command: cat flows_exclusive_topo2.json | python patch_ofc_rest_knocker.py -m put  
> INFO - Set API URL: http://localhost:8080/patch/flow  
> INFO - Send PUT: node:s2, rule:{"priority": 65535, "outport": 4, "inport": 2, "dpid": 2}  
> INFO - Response: {'date': 'Tue, 27 Oct 2015 11:59:29 GMT', 'status': '200', 'content-length': '0', 'content-type': 'text/html; charset=UTF-8'}  
> INFO - Content:  
> **#(省略)**  
> **#設定し終わったらCLIモードに入る**  
> mininet>  
> **#L1patch定義に問題がなければ、テスト用ノードの生成とDUTへの配置が行われ、手作業でテストが可能になる。**  
> mininet> h6 ping -c3 h1  
> PING 192.168.2.11 (192.168.2.11) 56(84) bytes of data.  
> 64 bytes from 192.168.2.11: icmp_seq=1 ttl=64 time=0.498 ms  
> 64 bytes from 192.168.2.11: icmp_seq=2 ttl=64 time=0.059 ms  
> 64 bytes from 192.168.2.11: icmp_seq=3 ttl=64 time=0.057 ms  
>  
> --- 192.168.2.11 ping statistics ---  
> 3 packets transmitted, 3 received, 0% packet loss, time 1998ms  
> rtt min/avg/max/mdev = 0.057/0.204/0.498/0.208 ms  
> mininet>  

## テスト自動実行
> hoge@prjexp01:~/PycharmProjects/l1patch-dev$ sudo python run_scenario_test.py -f testdefs_topo2.json --all-layers

* ユースケースオプション指定なしでテスト自動実行
* --all-layers すべてのワイヤを設定
