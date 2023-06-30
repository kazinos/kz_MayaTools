# -*- coding: utf-8 -*-
"""kz_globalVarReader.py

git:https://github.com/kazinos/kz_MayaTools.git

codeing by kazinos
MayaVer Maya2020.4
2022/10/15 kazinos 制作開始
2022/10/17 kazinos make git repository and commit.
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
from maya import cmds, mel
import re


def GVR_selectListItem():
    """optionVar選択時の処理
    """
    selInfo = []
    selItem = cmds.textScrollList("GVR_globalVerList", q=True, selectItem=True)[0]
    if selItem == "Please make a list":
        return

    selInfo = mel.eval("{}={}".format(selItem, selItem))

    # 変数名 表示処理
    cmds.textField("GVR_globalVerName", e=True, text=selItem)

    # info 初期化
    cmds.textScrollList("GVR_selGlobalVerInfo", e=True, removeAll=True)

    # info 表示処理
    if type(selInfo) == "float" or "long":
        cmds.textScrollList("GVR_selGlobalVerInfo", e=True, append=selInfo)

    if type(selInfo) == "unicode":
        cmds.textScrollList("GVR_selGlobalVerInfo", e=True, append="".join(selInfo))

    if type(selInfo) == "list":
        for info in selInfo:
            cmds.textScrollList("GVR_selGlobalVerInfo", e=True, append=info)


def GVR_makeList():
    """globalVar一覧作成処理
    """
    GVR_globalVerList = mel.eval("env")
    # findType = cmds.optionMenu("findType", q=True, value=True)
    findText = cmds.textField("GVR_searchField", q=True, text=True)
    tmpValue = []

    # 正規表現 "+", "*", "\" のみの場合のエラー回避処理
    if findText in ["+", "*", "\\"]:
        cmds.textScrollList("GVR_selGlobalVerInfo", e=True, removeAll=True,
                            append=u'The +,  *,  and \\ are special characters.\nThey cannot be used by using them alone.')
        return

    for tmp in GVR_globalVerList:
        # 検索での絞り込み
        if not re.search(r"{}".format(findText), tmp):
            continue
        tmpValue.append(tmp)

    cmds.textScrollList("GVR_globalVerList", e=True, append=tmpValue, removeAll=True)


# UI設定----------------------------------------------
def GVR_makeUI():
    winName = "GlobalVarReader"
    # ウィンドウが重複した場合の処理
    if cmds.window(winName, q=True, ex=True, resizeToFitChildren=True):
        cmds.deleteUI(winName)

    # Window作成
    window = cmds.window(winName, title=u"global Variable Reader",
                         s=True, mxb=False, mnb=False)

    # レイアウト formLayout Ver
    cmds.formLayout("GVR_form", numberOfDivisions=100)
    cmds.text("GVR_titleText", label=u"global Variable List", w=100, h=20)
    cmds.button("GVR_makeListBtn", label=u'Create List',
                command=lambda *args: GVR_makeList(), w=100, h=30)

    # 左側
    # 検索
    cmds.text("GVR_searchTitle", label="search", w=56)
    cmds.textField("GVR_searchField", text="", w=116)
    cmds.button("GVR_clearSearchField", label="clear", h=20,
                c='cmds.textField("GVR_searchField", e=True, text="")')

    # globalVar一覧
    cmds.textScrollList("GVR_globalVerList", w=220,
                        allowMultiSelection=False,
                        append=[u"Please make a list"],
                        selectCommand=lambda *args: GVR_selectListItem())

    # 右側
    # 選択globalVarの名前
    cmds.textField("GVR_globalVerName", h=48, text=u"GlobalVar Name")

    # 選択globalVarの内容
    cmds.textScrollList("GVR_selGlobalVerInfo", allowMultiSelection=True,
                        append=[u"Infomation"])

    # 基準点と配置の設定
    cmds.formLayout("GVR_form", e=True,
                    attachForm=[("GVR_titleText", 'top', 5),
                                ("GVR_titleText", 'left', 5),
                                ("GVR_titleText", 'right', 5),
                                ("GVR_makeListBtn", 'top', 5),
                                ("GVR_makeListBtn", 'left', 5),
                                ("GVR_makeListBtn", 'right', 5),
                                ("GVR_searchTitle", 'top', 5),
                                ("GVR_searchTitle", 'left', 5),
                                ("GVR_searchField", 'top', 5),
                                ("GVR_searchField", 'left', 5),
                                ("GVR_clearSearchField", 'top', 5),
                                ("GVR_clearSearchField", 'left', 5),
                                ("GVR_globalVerList", 'top', 5),
                                ("GVR_globalVerList", 'left', 5),
                                ("GVR_globalVerList", 'bottom', 5),
                                ("GVR_globalVerName", 'top', 5),
                                ("GVR_globalVerName", 'right', 5),
                                ("GVR_selGlobalVerInfo", 'top', 5),
                                ("GVR_selGlobalVerInfo", 'bottom', 5),
                                ("GVR_selGlobalVerInfo", 'right', 5)],
                    attachControl=[("GVR_makeListBtn", 'top', 5, "GVR_titleText"),
                                   ("GVR_makeListBtn", 'top', 5, "GVR_titleText"),
                                   ("GVR_searchTitle", 'top', 5, "GVR_makeListBtn"),
                                   ("GVR_searchField", 'top', 5, "GVR_makeListBtn"),
                                   ("GVR_searchField", 'left', 5, "GVR_searchTitle"),
                                   ("GVR_clearSearchField", 'top', 5, "GVR_makeListBtn"),
                                   ("GVR_clearSearchField", 'left', 5, "GVR_searchField"),
                                   ("GVR_globalVerList", 'top', 5, "GVR_searchField"),
                                   ("GVR_globalVerName", 'top', 5, "GVR_makeListBtn"),
                                   ("GVR_globalVerName", 'left', 5, "GVR_clearSearchField"),
                                   ("GVR_selGlobalVerInfo", 'top', 5, "GVR_globalVerName"),
                                   ("GVR_selGlobalVerInfo", 'left', 5, "GVR_globalVerList"),
                                   ])
    cmds.showWindow(window)
    cmds.window(winName, e=True, widthHeight=(400, 300), sizeable=True)

    # 新規シーンかシーンを開いた時にメニューを閉じる
    cmds.scriptJob(event=['SceneOpened', 'cmds.deleteUI("{}")'.format(winName)], p=winName)
    cmds.scriptJob(event=['NewSceneOpened', 'cmds.deleteUI("{}")'.format(winName)], p=winName)


if __name__ == "__main__":
    GVR_makeUI()
