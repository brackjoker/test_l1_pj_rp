# L1patchPJ

## 概要

(このプロジェクトってこういうものです。)

## ドキュメント

(このページに細かい使い方があるよ)
* PoCレポート(リンク)
  * PoCレポートにはこういうことを書いてあるよ。
* 技術レポート(リンク)
  * 技術レポートにはこういうことを書いてあるよ。

# L1patchをつかってみる
## 最低限の使い方
この後説明するものが何をしようとしているのか。Readmeは簡潔にどういう風に動かすものかというのだけ見せられれば良いと思います。
* 机上テスト(topo2)の実行
  * 机上テストとは何か?
  * そのために必要なものは何か?
  * 机上テストを行うと何がわかるのか?

topo2で作る構成の図はドキュメントにあるはずなのでそれを張り付けるとよいかも。机上テスト(topo2)ではホスト間でこういうワイヤを作りますよ、という図。

##	L1patch環境のセットアップ
今回、こういうツールでテストをしています、という情報。
PoCレポートにある使ってるもの一覧のテーブルをコピーしてしまうのが早いかな…。topo2のはなしであればnovamanで使ったソフトウェアの話だけでよいでしょう。
* Mininet2.2.22以降
* Ryu3.24以降
* Open vSwitch 2.0以降
* Python2.7系

##  各種設定ファイルの準備
使うファイルの紹介。リポジトリに挙げると、github URLでファイルへのリンク指定できるので、それを使う。ファイルの中身の詳細については"技術レポート"読んでね。
* 物理情報の定義(`nodeinfo_topo2.json`, リンク)
  * ここではどういうものを定義しているのか(概要)
* 論理情報の定義(`wireinfo_topo2.json`, リンク)
  * ここではどういうものを定義しているのか(概要)
* テストシナリオの定義(`scenario_pattern_topo2_simple.json`, リンク)
  * ここではどういうものを定義しているのか(概要)
* テスト自動実行定義(`testdefs_topo2.json`, リンク)
  * ここではどういうものを定義しているのか(概要)

##  OpenFlowコントローラの起動
※サンプルのOFCのREST API URLはlocalhost:8080

    hoge@prjexp01:~/l1patch-dev$ ryu-manager --verbose patch_ofc.py  

##  L1patchの実行(手動操作モード)

    hoge@prjexp01:~/l1patch-dev$ sudo python run_scenario_test.py -f testdefs_topo2.json --all-layers --manual

Mininet CLIに入るので、コマンドを実行してどうなっているのか確認してみてください。
- `h1 ping h6` etc
- `pingall`
- `dpctl dump-flows`

pingallするとこういうのが出てきて、図で示した「ワイヤ」接続ができているというのがわかりますよね、くらいはあってもいいかな…

## L1patchの実行(自動実行モード)

    hoge@prjexp01:~/l1patch-dev$ sudo python run_scenario_test.py -f testdefs_topo2.json --all-layers

実行が終わったら結果(test_result_topo2.md)が生成されているはずなので確認してみてください。

## ちょっと複雑なテストの実行

テスト定義の中で指定するテストシナリオファイルを `scenario_pattern_topo2.json`(リンク張る) に変えてみるとどうなるか。
