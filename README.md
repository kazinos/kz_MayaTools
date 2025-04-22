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

---

#### kz_JointDisplaySettings.py
https://github.com/kazinos/kz_MayaTools/assets/55563757/15c31c0b-7ac9-4922-b24e-b7ef6c5f132f

[jp]

##### joint確認・表示変更ツール

jointのデータ確認の効率化の為に作成しました。
細かい機能をまとめて1つのツールにしました。
できる事は下記の通りです。
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

---

#### kz_channelControlSetting.py
https://github.com/kazinos/kz_MayaTools/assets/55563757/78907a6e-ecd3-40e6-98a8-1c88b4fece7b


[jp]

##### アトリビュート編集ツール

Maya標準のChannel Controlの表示を変更しcheckboxで変更できるようにしたものです。

checkBox、Keyableの項目いずれかにチェックが入っていればチャネルボックスに表示されます。

アトリビュート表示部分は上から順に

・標準でチャネルボックスに表示されているもの

・標準で実装されているアトリビュート

・追加アトリビュート

となっており、2段目、3段目はアルファベット順に並び替えています。

誰かの作業の手伝いになれば幸いです。

[en]

##### Attribute Editing Tool

This tool changes the display of Maya's standard Channel Control so that it can be changed in the checkbox.

If either the checkbox or keyable item is checked, it will be displayed in the channel box.

The attributes are displayed in the following order from the top to the bottom

・The attributes that are displayed in the standard channel box.

・Attributes that are implemented by default

・Extra attributes

and the second and third rows are sorted alphabetically.

I hope this helps someone's work.


---


#### kz_RadialjointOrient.py


https://github.com/kazinos/kz_MayaTools/assets/55563757/3e45047b-1a14-464c-b41d-fef52a98246d


[jp]

##### 放射状にjointOrientを設定するツール

secondary軸が基準点を向くようにjointOrientを設定してくれるツールです。

スカートなどの放射状に配置されているjointの軸を設定するのに役に立ちます。

基準点は任意の場所に移動してください。

計算内容は、内積と外積を使って回転角を算出し、jointを回転

その後にフリーズを行っています。

すでにスキニングされているjointの場合は、バインドを解除してから使用してください。

誰かの作業の手伝いになれば幸いです。

[en]

##### A tool that sets the jointOrient radially

This tool sets the jointOrient so that the secondary axis points to the reference point.

This tool is useful for setting the axes of radially placed joints such as skirts.

The reference point can be moved to any location.

The calculation uses the dot product and cross product to calculate the rotation angle, rotate the joint

Freeze is then performed.

If the joint has already been skinned, unbind it before use.

I hope this helps someone's work.
