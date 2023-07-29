# kz_MayaTools
[jp]

Maya用に作った自作ツール
Pythonの学習や、Mayaの学習の為に作成

[en]

(I write using a translation tool.)
Homemade tools made for Maya
Created for learning Python and learning Maya.


## Tool Description
#### kz_optionVerReader.py
https://user-images.githubusercontent.com/55563757/185957323-b74be0ca-fe32-4f9e-b7b4-bbad6a015b76.mp4

[jp]

##### optionVarの一覧作成および削除ツール

ツール作成の効率化の為に作成しました。
ツールを作成する際に、毎回コマンドを入力してoptionVarの内容を確認するのは手間がかかります。
またKeyの名前を変更した際に消し忘れがあると、不要なデータをMayaに残すことになります。
userPrefs.melを開いて確認しても良いのですが、毎回深いフォルダ階層を開く事になりますし、Mayaを閉じないと更新されないという問題もあります。

このツールはそんな悩みから作成しようと思い立ちました。
誰かのツール作成の手伝いになれば幸いです。

[en]

##### OptionVar listing and deletion tool

Created to improve efficiency of tool creation.
When creating a tool, it is time-consuming to enter commands and check the contents of the optionVar each time.
Also, if you forget to delete a key when you rename it, you will leave unnecessary data in Maya.
You could open userPrefs.mel to check, but that would open a deep folder hierarchy each time, and you would have to close Maya to get the updates.

This tool was inspired by such concerns.
I hope it will help someone else to create a tool.

---

#### kz_globalVerReader.py
https://user-images.githubusercontent.com/55563757/196215859-5ab71705-c5c3-4246-becb-478848049457.mp4



[jp]

##### グローバル変数の一覧作成および削除ツール

ツール作成の効率化の為に作成しました。
以外に何が保存されているのか把握しきれていないグローバル変数の中身が気になり制作しました。
・ウインドウの名前
・プリファレンスの設定値
・各種項目のステータス　等
探そうと思うとmelを開いて変数名を探し出してプリントして…と手間ですが、欲しい情報を検索すれば検索の時短になるかと思います。

情報の検索、勉強のお供など、
誰かのツール作成の手伝いになれば幸いです。

[en]

##### global variable listing tool

Created to improve the efficiency of tool creation.
I created it because I was concerned about the contents of global variables, which I could not fully grasp what is stored in other than the following.
Window name
Preference values
The status of various items, etc.
When I want to search, I have to open mel, find the variable name, and print it out... It is time-consuming, but if I search for the information I want, I think it will shorten the time for searching.

Searching for information, study, etc.
I would be happy if I can help someone to create a tool.


#### kz_globalVerReader.py
https://github.com/kazinos/kz_MayaTools/assets/55563757/15c31c0b-7ac9-4922-b24e-b7ef6c5f132f


[jp]

##### joint確認・表示変更ツール

jointのデータ確認の効率化の為に作成しました。
細かい機能をまとめて１つのツールにしました。
出来る事は下記の通りです。
・jointのTranlate,Rotate,Scaleの表示（桁数変更機能付き）
・ラベルの表示・非表示
・軸方向の表示・非表示
・jointの半径　一括変更
・jointの色の変更
・jointのアウトライナー上の色変更

誰かの作業の手伝いになれば幸いです。

[en]

##### global variable listing tool

This tool was created to improve the efficiency of data confirmation for JOINT.
We have combined detailed functions into a single tool.
The following functions are available.
・Display of joint's Tranlate, Rotate, and Scale (with a function to change the number of digits)
・Display/hide labels
・Display/Hide axis direction
・Change the radius of joints at once.
・Change the color of joints.
・Change the color of joints in the outliner.

I would be happy to help someone else's work.
