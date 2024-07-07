# airwork_automation
求人サイトのエアワークへの募集作成を自動化するRPA
作成中の募集データを見つけると、そのデータをテンプレートとして、勤務地の数分自動で作成する。

exeファイル作成化手順

vscodeを開く
各ファイルをローカルPC(いま開いているPC)のフォルダに保存する。
ctrl + @でTERMINALを開く
+ボタンの隣の下向き矢印をクリックする
cmdをクリックする。
以下二つのコマンドをcmdにコピペしてエンターキーを押す
- pip install -r requirements.txt
- pip install --upgrade -r requirements.txt
次に以下をcmdにコピペしてエンターキーを押す
make_binary.bat
exeファイルができるのでダブルクリックで実行する。