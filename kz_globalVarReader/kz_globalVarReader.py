# -*- coding: utf-8 -*-
"""kz_globalVarReader.py

git:https://github.com/kazinos/kz_MayaTools.git

codeing by kazinos
MayaVer Maya2020.4
2022/10/15 kazinos 制作開始
2022/10/17 kazinos make git repository and commit.
2023/06/30 kazinos Change format to linter.

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
from maya import cmds, mel
import re


def selectListItem():
    """optionVar選択時の処理
    """
    selInfo = []
    selItem = cmds.textScrollList("globalVerList", q=True, selectItem=True)[0]
    if selItem == "Please make a list":
        return

    selInfo = mel.eval("{}={}".format(selItem, selItem))

    # 変数名 表示処理
    cmds.textField("globalVerName", e=True, text=selItem)

    # info 初期化
    cmds.textScrollList("selGlobalVerInfo", e=True, removeAll=True)

    # info 表示処理
    if type(selInfo) == "float" or "long":
        cmds.textScrollList("selGlobalVerInfo", e=True, append=selInfo)

    if type(selInfo) == "unicode":
        cmds.textScrollList("selGlobalVerInfo", e=True, append="".join(selInfo))

    if type(selInfo) == "list":
        for info in selInfo:
            cmds.textScrollList("selGlobalVerInfo", e=True, append=info)


def makeList():
    """globalVar一覧作成処理
    """
    globalVerList = mel.eval("env")
    # findType = cmds.optionMenu("findType", q=True, value=True)
    findText = cmds.textField("searchField", q=True, text=True)
    tmpValue = []

    # 正規表現 "+", "*", "\" のみの場合のエラー回避処理
    if findText in ["+", "*", "\\"]:
        cmds.textScrollList("selGlobalVerInfo", e=True, removeAll=True,
                            append=u'The +,  *,  and \\ are special characters.\nThey cannot be used by using them alone.')
        return

    for tmp in globalVerList:
        # 検索での絞り込み
        if not re.search(r"{}".format(findText), tmp):
            continue
        tmpValue.append(tmp)

    cmds.textScrollList("globalVerList", e=True, append=tmpValue, removeAll=True)


# UI設定----------------------------------------------
def makeUI():
    winName = "GlobalVarReader"
    # ウィンドウが重複した場合の処理
    if cmds.window(winName, q=True, ex=True, resizeToFitChildren=True):
        cmds.deleteUI(winName)

    # Window作成
    window = cmds.window(winName, title=u"global Variable Reader",
                         s=True, mxb=False, mnb=False)

    # レイアウト formLayout Ver
    cmds.formLayout("form", numberOfDivisions=100)
    cmds.text("titleText", label=u"global Variable List", w=100, h=20)
    cmds.button("makeListBtn", label=u'Create List',
                command=lambda *args: makeList(), w=100, h=30)

    # 左側
    # 検索
    cmds.text("searchTitle", label="search", w=56)
    cmds.textField("searchField", text="", w=116)
    cmds.button("clearSearchField", label="clear", h=20,
                c='cmds.textField("searchField", e=True, text="")')

    # globalVar一覧
    cmds.textScrollList("globalVerList", w=220,
                        allowMultiSelection=False,
                        append=[u"Please make a list"],
                        selectCommand=lambda *args: selectListItem())

    # 右側
    # 選択globalVarの名前
    cmds.textField("globalVerName", h=48, text=u"GlobalVar Name")

    # 選択globalVarの内容
    cmds.textScrollList("selGlobalVerInfo", allowMultiSelection=True,
                        append=[u"Infomation"])

    # 基準点と配置の設定
    cmds.formLayout("form", e=True,
                    attachForm=[("titleText", 'top'),
                                ("titleText", 'left', 5),
                                ("titleText", 'right', 5),
                                ("makeListBtn", 'top', 5),
                                ("makeListBtn", 'left', 5),
                                ("makeListBtn", 'right', 5),
                                ("searchTitle", 'top', 5),
                                ("searchTitle", 'left', 5),
                                ("searchField", 'top', 5),
                                ("searchField", 'left', 5),
                                ("clearSearchField", 'top', 5),
                                ("clearSearchField", 'left', 5),
                                ("globalVerList", 'top', 5),
                                ("globalVerList", 'left', 5),
                                ("globalVerList", 'bottom', 5),
                                ("globalVerName", 'top', 5),
                                ("globalVerName", 'right', 5),
                                ("selGlobalVerInfo", 'top', 5),
                                ("selGlobalVerInfo", 'bottom', 5),
                                ("selGlobalVerInfo", 'right', 5)],
                    attachControl=[("makeListBtn", 'top', 5, "titleText"),
                                   ("makeListBtn", 'top', 5, "titleTex, 5t"),
                                   ("searchTitle", 'top', 5, "makeListBtn"),
                                   ("searchField", 'top', 5, "makeListBtn"),
                                   ("searchField", 'left', 5, "searchTitle"),
                                   ("clearSearchField", 'top', 5, "makeListBtn"),
                                   ("clearSearchField", 'left', 5, "searchField"),
                                   ("globalVerList", 'top', 5, "searchField"),
                                   ("globalVerName", 'top', 5, "makeListBtn"),
                                   ("globalVerName", 'left', 5, "clearSearchField"),
                                   ("selGlobalVerInfo", 'top', 5, "globalVerName"),
                                   ("selGlobalVerInfo", 'left', 5, "globalVerList"),
                                   ])
    cmds.showWindow(window)
    cmds.window(winName, e=True, widthHeight=(400, 300), sizeable=True)

    # 新規シーンかシーンを開いた時にメニューを閉じる
    cmds.scriptJob(event=['SceneOpened', 'cmds.deleteUI("{}")'.format(winName)], p=winName)
    cmds.scriptJob(event=['NewSceneOpened', 'cmds.deleteUI("{}")'.format(winName)], p=winName)


if __name__ == "__main__":
    makeUI()
