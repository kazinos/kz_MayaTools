# -*- coding: utf-8 -*-
"""kz_optionVarReader.py

git:https://github.com/kazinos/kz_MayaTools.git

codeing by kazinos
MayaVer Maya2020.4
2022/08/18 kazinos 制作開始
2022/08/22 kazinos make git repository and commit.
2023/06/30 kazinos Change format to linter.
                   Add prefix to UI name and method name.

issue:

"""
# ------------------------------------------------------------------------------
from __future__ import absolute_import, division, generators, print_function, unicode_literals
try:
    from future_builtins import *  # noqa
except BaseException:
    pass
import sys
sys.dont_write_bytecode = True
# ------------------------------------------------------------------------------
from maya import cmds
import re


def OVR_selectListItem():
    """optionVar選択時の処理
    """
    selItem = cmds.textScrollList("OVR_optionVerList", q=True, selectItem=True)[0]
    selInfo = cmds.optionVar(q=selItem)

    # 変数名 表示処理
    cmds.textField("OVR_optionVerName", e=True, text=selItem)

    # 値 表示処理
    if type(selInfo) == list:
        cmds.textScrollList("OVR_selOptionVerInfo", e=True, removeAll=True,
                            append="{}".format(selInfo))
        return

    cmds.textScrollList("OVR_selOptionVerInfo", e=True, removeAll=True, append=[selInfo])


def OVR_deleteItem():
    """選択対象のoptionVarの削除処理
    """
    # 選択されていない場合：return
    if cmds.textScrollList("OVR_optionVerList", q=True, numberOfSelectedItems=True) == 0:
        return

    # 選択物がoptionVar内に存在していない場合：return
    if not cmds.optionVar(exists=cmds.textScrollList("OVR_optionVerList", q=True, selectItem=True)[0]):
        cmds.textScrollList("OVR_selOptionVerInfo", e=True, removeAll=True,
                            append=u"Selection was not found in OptionVar.\nPlease refresh the list.")
        return

    # 確認ダイアログ表示
    selItem = cmds.textScrollList("OVR_optionVerList", q=True, selectItem=True)[0]
    checklog = cmds.confirmDialog(title=u'check',
                                  message='Do you want to delete optionVar?\n{}'.format(selItem),
                                  button=['Yes', 'No'],
                                  defaultButton='Yes',
                                  cancelButton='No',
                                  dismissString='No')

    # 削除処理
    if checklog == "Yes":
        cmds.optionVar(remove=selItem)
        OVR_makeList()
        cmds.textField("OVR_optionVerName", e=True, text=u"")
        cmds.textScrollList("OVR_selOptionVerInfo", e=True, removeAll=True, append=u"")


def OVR_makeList():
    """optionVar一覧作成処理
    """
    OVR_optionVerList = cmds.optionVar(list=True)
    OVR_findType = cmds.optionMenu("OVR_findType", q=True, value=True)
    findText = cmds.textField("OVR_searchField", q=True, text=True)

    # 正規表現 "+", "*", "\" のみの場合のエラー回避処理
    if findText in ["+", "*", "\\"]:
        cmds.textScrollList("OVR_selOptionVerInfo", e=True, removeAll=True,
                            append=u'The +, *, and \\ are special characters.\nThey cannot be used by using them alone.')
        return

    # データ型の設定
    seltype = ""
    if not OVR_findType == "All":
        if OVR_findType == "string Value":
            seltype = unicode
        if OVR_findType == "int Value":
            seltype = int
        if OVR_findType == "float Value":
            seltype = float
        if OVR_findType == "List Value":
            seltype = list

    tmpList = []
    for tmp in OVR_optionVerList:
        # 検索での絞り込み
        if not re.search(r"{}".format(findText), tmp):
            continue
        tmpValue = cmds.optionVar(q=tmp)

        # typeでの絞り込み
        if not OVR_findType == "All" and not type(tmpValue) == seltype:
            continue
        tmpList.append(tmp)
    OVR_optionVerList = tmpList
    cmds.textScrollList("OVR_optionVerList", e=True, append=OVR_optionVerList, removeAll=True)


# UI設定----------------------------------------------
def OVR_makeUI():
    winName = "OptionVarReader"
    # ウィンドウが重複した場合の処理
    if cmds.window(winName, q=True, ex=True, resizeToFitChildren=True):
        cmds.deleteUI(winName)

    # Window作成
    window = cmds.window(winName, title=u"OptionVar Reader",
                         s=True, mxb=False, mnb=False)

    # レイアウト formLayout Ver
    cmds.formLayout("OVR_form", numberOfDivisions=100)
    cmds.text("OVR_titleText", label=u"optionVar List", w=100, h=20)
    cmds.button("OVR_makeListBtn", label=u'Create List', w=100, h=30,
                command=lambda *args: OVR_makeList())

    # 左側
    # 絞り込み
    cmds.optionMenu("OVR_findType", label='Find Type', w=220)
    cmds.menuItem(label='All')
    cmds.menuItem(label='string Value')
    cmds.menuItem(label='int Value')
    cmds.menuItem(label='float Value')
    cmds.menuItem(label='List Value')

    # 検索
    cmds.text("OVR_searchTitle", label="search", w=56)
    cmds.textField("OVR_searchField", text="", w=116)
    cmds.button("OVR_clearsearchField", label="clear", h=20,
                c='cmds.textField("OVR_searchField", e=True, text="")')

    # optionVar一覧
    cmds.textScrollList("OVR_optionVerList", w=220,
                        allowMultiSelection=False,
                        append=[u"Please make a list"],
                        selectCommand=lambda *args: OVR_selectListItem())

    # 削除ボタン
    cmds.button("OVR_deleleButton", label="Delete", w=220, c=lambda *args: OVR_deleteItem())

    # 右側
    # 選択optionVarの名前
    cmds.textField("OVR_optionVerName", h=48, text=u"OptionVar Name")

    # 選択optionVarの内容
    cmds.textScrollList("OVR_selOptionVerInfo", allowMultiSelection=True,
                        append=[u"Infomation"])

    # 基準点と配置の設定
    cmds.formLayout("OVR_form", e=True,
                    attachForm=[("OVR_titleText", 'top', 5),
                                ("OVR_titleText", 'left', 5),
                                ("OVR_titleText", 'right', 5),
                                ("OVR_makeListBtn", 'top', 5),
                                ("OVR_makeListBtn", 'left', 5),
                                ("OVR_makeListBtn", 'right', 5),
                                ("OVR_findType", 'top', 5),
                                ("OVR_findType", 'top', 5),
                                ("OVR_findType", 'left', 5),
                                ("OVR_searchTitle", 'top', 5),
                                ("OVR_searchTitle", 'left', 5),
                                ("OVR_searchField", 'top', 5),
                                ("OVR_searchField", 'left', 5),
                                ("OVR_clearsearchField", 'top', 5),
                                ("OVR_clearsearchField", 'left', 5),
                                ("OVR_optionVerList", 'top', 5),
                                ("OVR_optionVerList", 'left', 5),
                                ("OVR_deleleButton", 'left', 5),
                                ("OVR_deleleButton", 'bottom', 5),
                                ("OVR_optionVerName", 'top', 5),
                                ("OVR_optionVerName", 'right', 5),
                                ("OVR_selOptionVerInfo", 'top', 5),
                                ("OVR_selOptionVerInfo", 'bottom', 5),
                                ("OVR_selOptionVerInfo", 'right', 5)],
                    attachControl=[("OVR_makeListBtn", 'top', 5, "OVR_titleText"),
                                   ("OVR_makeListBtn", 'top', 5, "OVR_titleText"),
                                   ("OVR_findType", 'top', 5, "OVR_makeListBtn"),
                                   ("OVR_searchTitle", 'top', 5, "OVR_findType"),
                                   ("OVR_searchField", 'top', 5, "OVR_findType"),
                                   ("OVR_searchField", 'left', 5, "OVR_searchTitle"),
                                   ("OVR_clearsearchField", 'top', 5, "OVR_findType"),
                                   ("OVR_clearsearchField", 'left', 5, "OVR_searchField"),
                                   ("OVR_optionVerList", 'top', 5, "OVR_searchField"),
                                   ("OVR_optionVerList", 'bottom', 5, "OVR_deleleButton"),
                                   ("OVR_optionVerName", 'top', 5, "OVR_makeListBtn"),
                                   ("OVR_optionVerName", 'left', 5, "OVR_findType"),
                                   ("OVR_selOptionVerInfo", 'top', 5, "OVR_optionVerName"),
                                   ("OVR_selOptionVerInfo", 'left', 5, "OVR_optionVerList"),
                                   ])
    cmds.showWindow(window)
    cmds.window(winName, e=True, widthHeight=(400, 300), sizeable=True)

    # 新規シーンかシーンを開いた時にメニューを閉じる
    cmds.scriptJob(event=['SceneOpened', 'cmds.deleteUI("{}")'.format(winName)], p=winName)
    cmds.scriptJob(event=['NewSceneOpened', 'cmds.deleteUI("{}")'.format(winName)], p=winName)


if __name__ == "__main__":
    OVR_makeUI()
