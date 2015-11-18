# L1patch応用NWテストシステムプロジェクト サンプルプログラム

## このプロジェクトについて
従来、ネットワークの試験を実施する際には、大量の物理的な機材・配線を用意して、物理配線や疎通試験の作業を人手で行う必要があり、問題となっておりました。本プロジェクトでは、SDNの技術を使うことでこれらの問題の解決を目指し、上記の各社からネットワーク試験の経験と技術を持つ技術者が協力し、課題を共有、議論することで研究を進めてまいりました。

## 本プロジェクトの成果物について
現在、沖縄オープンラボラトリのホームページにてプロジェクトの成果物を公開予定です。
https://www.okinawaopenlabs.org/

プロジェクトの内容にご興味のある方はこちらまでお問い合わせください。
＜本件に関するお問い合わせ＞
一般社団法人沖縄オープンラボラトリ
L1Patch応用NWテストシステムPJ 担当
Mail: 

# L1patchの使用方法
この後説明するものが何をしようとしているのか。Readmeは簡潔にどういう風に動かすものかというのだけ見せられれば良いと思います。
* 机上テスト(topo2)の実行
  * 机上テストとは何か?
  * そのために必要なものは何か?
  * 机上テストを行うと何がわかるのか?

topo2で作る構成の図はドキュメントにあるはずなのでそれを張り付けるとよいかも。机上テスト(topo2)ではホスト間でこういうワイヤを作りますよ、という図。

##	L1patch環境のセットアップ
今回のサンプルにて使用しているソフトウェアとバージョンは下記の通りです。

* Mininet2.2.22以降
* Ryu3.24以降
* Open vSwitch 2.0以降
* Python2.7系

##  各種設定ファイルの準備
このサンプルプログラムでは下記の４つのファイルを作成する必要がある

* 物理情報の定義(`nodeinfo_topo2.json`, [リンク](nodeinfo_topo2.json))  
  このファイルでは実際に物理的に接続されている機器の情報と接続するMininetのノードの情報を定義しているファイルです。  
  ファイル内でMininetで生成される試験ノードのIPや物理的に接続している接続しているWhiteboxスイッチのポート情報、物理的に接続されている機器の接続情報を定義する。  

* 論理情報の定義(`wireinfo_topo2.json`, [リンク](wireinfo_topo2.json))  
  L1Patchで作成する論理接続の情報を定義しているファイルです。  
  各ネットワーク機器と試験ノードのデータプレーンの接続構成を設定ファイルで定義します。  


* テストシナリオの定義(`scenario_pattern_topo2_simple.json`, [リンク](scenario_pattern_topo2_simple.json))  
  試験ノード間のどこからどこにトラフィック(Ping)を流すのかを設定する定義ファイル。
  各試験ノード設定とトラフィック(Ping)を流す始点と終点の設定、想定される結果を設定する。

* テスト自動実行定義(`testdefs_topo2.json`, [リンク](testdefs_topo2.json))  
  試験の自動実行を行うための定義ファイル。
  実行する試験でどの設定ファイルを使って試験をするかやテスト環境のOpenFlowのバージョン、シナリオで使用する試験用のコマンドを定義する。

##  OpenFlowコントローラの起動
※サンプルのOFCのREST API URLはlocalhost:8080

    hoge@prjexp01:~/l1patch-dev$ ryu-manager --verbose patch_ofc.py  

##  L1patchの実行(手動操作モード)

    hoge@prjexp01:~/l1patch-dev$ sudo python run_scenario_test.py -f testdefs_topo2.json --all-layers --manual

上記を実行するとMininet CLIに入るので、コマンドを実行してどうなっているのか確認してみてください。
- `h1 ping h6` etc
- `pingall`
- `dpctl dump-flows`

pingallするとこういうのが出てきて、図で示した「ワイヤ」接続ができているというのがわかりますよね、くらいはあってもいいかな…

## L1patchの実行(自動実行モード)

    hoge@prjexp01:~/l1patch-dev$ sudo python run_scenario_test.py -f testdefs_topo2.json --all-layers

実行が終わったら結果(test_result_topo2.md)が生成されているはずなので確認してみてください。

## ちょっと複雑なテストの実行



テスト定義の中で指定するテストシナリオファイルを `scenario_pattern_topo2.json`(リンク張る) に変えてみるとどうなるか。
