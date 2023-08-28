# -*- coding: utf-8 -*-
"""kz_channelControlSetting.py

git:https://github.com/kazinos/kz_MayaTools.git

coding by kazinos
MayaVer Maya2020.4
2023/08/29 v1.0 kz_channelControlSettingの作成

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
from maya.common.ui import LayoutManager


def CCS_changeAttr(ctrlName="", AttrName="", changeGroup=""):
    """Attribute change process

    UI display changes at the same time

    Args:
        ctrlName (str, optional): Name of the control to be changed. Defaults to "".
        AttrName (str, optional): Name of the attribute to be changed. Defaults to "".
        changeGroup (str, optional): Name of the group to be changed.Choose one of "base" "default" or "extra". Defaults to "".
    """
    # ctrlNameからどのパネルの項目が選択されたか判断
    index = ctrlName.split("_")[-1]
    boxType = "base"
    if "default" in ctrlName:
        boxType = "default"
    if "extra" in ctrlName:
        boxType = "extra"

    # アトリビュートの変更
    if changeGroup == "channelBox":
        cmds.setAttr(AttrName, cb=cmds.checkBox(ctrlName, q=True, value=True))
    if changeGroup == "keyable":
        cmds.setAttr(AttrName, k=cmds.checkBox(ctrlName, q=True, value=True))
    if changeGroup == "lock":
        cmds.setAttr(AttrName, lock=cmds.checkBox(ctrlName, q=True, value=True))

    # UIの更新
    cmds.checkBox("{}ChannelBox_{}".format(boxType, index), e=True, value=cmds.getAttr(AttrName, cb=True))
    cmds.checkBox("{}Keyable_{}".format(boxType, index), e=True, value=cmds.getAttr(AttrName, keyable=True))
    cmds.checkBox("{}Lock_{}".format(boxType, index), e=True, value=cmds.getAttr(AttrName, lock=True))


def CCS_SelectionChangedCommand():
    """Processing when object selection is changed

    Retrieve attributes of selected objects and reconstruct UI
    """
    label_w = 100
    checkBox_w = 40
    baseScrollName, baseColumnName, defaultScrollName, defaultColumnName, extraScrollName, extraColumnName, baseAttrList = CCS_getUIName()

    # UIの初期化
    if cmds.columnLayout(baseColumnName, q=True, childArray=True):
        for i in cmds.columnLayout(baseColumnName, q=True, childArray=True):
            cmds.deleteUI(i)

    if cmds.columnLayout(defaultColumnName, q=True, childArray=True):
        for i in cmds.columnLayout(defaultColumnName, q=True, childArray=True):
            cmds.deleteUI(i)

    if cmds.columnLayout(extraColumnName, q=True, childArray=True):
        for i in cmds.columnLayout(extraColumnName, q=True, childArray=True):
            cmds.deleteUI(i)

    # 選択されたobjectの取得
    selobj = cmds.ls(sl=True, type="transform")

    # 選択がない場合の処理
    cmds.textField("selectObjectField", e=True, text="None")
    if not selobj:
        with LayoutManager(cmds.columnLayout(baseColumnName, e=True, parent=baseScrollName)):
            cmds.text("defaultNonSelectedText", l="There is nothing selected.", parent=baseColumnName)
        with LayoutManager(cmds.columnLayout(defaultColumnName, e=True, parent=defaultScrollName)):
            cmds.text("defaultNonSelectedText", l="There is nothing selected.", parent=defaultColumnName)
        with LayoutManager(cmds.columnLayout(extraColumnName, e=True, parent=extraScrollName)):
            cmds.text("extraNonSelectedText", l="There is nothing selected.", parent=extraColumnName)
        return

    # 選択されているオブジェクト名のUI表示
    cmds.textField("selectObjectField", e=True, text=selobj[0])

    # アトリビュートの取得
    extraAttrs = cmds.listAttr(selobj[0], userDefined=True)
    defaultAttrs = cmds.listAttr(selobj[0])
    defaultAttrs = cmds.sortCaseInsensitive(list(set(defaultAttrs) - set(baseAttrList)))
    if extraAttrs:
        defaultAttrs = cmds.sortCaseInsensitive(list(set(defaultAttrs) - set(extraAttrs)))

    # 正常に取得できないアトリビュートは除外対象とする
    ignoreList = ["message", "TdataCompound", "rotationInterpolation", "publishedNodeInfo"]

    # よく使うアトリビュート更新部
    with LayoutManager(cmds.columnLayout(baseColumnName, e=True, parent=baseScrollName)):
        for i, attr in enumerate(baseAttrList):
            # 除外リスト及び配列型のものは除外
            if attr in ignoreList or "." in attr:
                continue

            # トリビュートの取得
            isHidden = cmds.getAttr("{}.{}".format(selobj[0], attr), channelBox=True)
            isKeyable = cmds.getAttr("{}.{}".format(selobj[0], attr), keyable=True)
            isLock = cmds.getAttr("{}.{}".format(selobj[0], attr), lock=True)

            # UIの作成
            with LayoutManager(cmds.rowLayout(nc=5, adj=1, parent=baseColumnName)):
                cmds.text("{}".format(attr), al="left", w=label_w)
                cmds.checkBox("baseChannelBox_{}".format(i), l=" ", value=isHidden, w=checkBox_w,
                              cc="CCS_changeAttr('baseChannelBox_{}', '{}.{}', 'channelBox')".format(i, selobj[0], attr))
                cmds.checkBox("baseKeyable_{}".format(i), l=" ", value=isKeyable, w=checkBox_w,
                              cc="CCS_changeAttr('baseKeyable_{}', '{}.{}', 'keyable')".format(i, selobj[0], attr))
                cmds.checkBox("baseLock_{}".format(i), l=" ", value=isLock, w=checkBox_w,
                              cc="CCS_changeAttr('baseLock_{}', '{}.{}', 'lock')".format(i, selobj[0], attr))

    # 標準アトリビュート更新部
    with LayoutManager(cmds.columnLayout(defaultColumnName, e=True, parent=defaultScrollName)):
        for i, attr in enumerate(defaultAttrs):
            # 除外リスト及び配列型のものは除外
            if attr in ignoreList or "." in attr:
                continue

            # トリビュートの取得
            isHidden = cmds.getAttr("{}.{}".format(selobj[0], attr), channelBox=True)
            isKeyable = cmds.getAttr("{}.{}".format(selobj[0], attr), keyable=True)
            isLock = cmds.getAttr("{}.{}".format(selobj[0], attr), lock=True)

            # UIの作成
            with LayoutManager(cmds.rowLayout(nc=5, adj=1, parent=defaultColumnName)):
                cmds.text("{}".format(attr), al="left", w=label_w)
                cmds.checkBox("defaultChannelBox_{}".format(i), l=" ", value=isHidden, w=checkBox_w,
                              cc="CCS_changeAttr('defaultChannelBox_{}', '{}.{}', 'channelBox')".format(i, selobj[0], attr))
                cmds.checkBox("defaultKeyable_{}".format(i), l=" ", value=isKeyable, w=checkBox_w,
                              cc="CCS_changeAttr('defaultKeyable_{}', '{}.{}', 'keyable')".format(i, selobj[0], attr))
                cmds.checkBox("defaultLock_{}".format(i), l=" ", value=isLock, w=checkBox_w,
                              cc="CCS_changeAttr('extraLock_{}', '{}.{}', 'lock')".format(i, selobj[0], attr))

    # 追加アトリビュート更新部
    with LayoutManager(cmds.columnLayout(extraColumnName, e=True, parent=extraScrollName)):
        # 追加アトリビュートが存在しなかった場合のUI作成　選択更新時、deleteUIをする都合上何かしら作成する必要がある
        if not extraAttrs:
            cmds.text("extraNonSelectedText", l="No additional attributes found", parent=extraColumnName)
            return

        for i, attr in enumerate(extraAttrs):
            # 除外リスト及び配列型のものは除外
            if attr in ignoreList or "." in attr:
                continue

            # トリビュートの取得
            isHidden = cmds.getAttr("{}.{}".format(selobj[0], attr), channelBox=True)
            isKeyable = cmds.getAttr("{}.{}".format(selobj[0], attr), keyable=True)
            isLock = cmds.getAttr("{}.{}".format(selobj[0], attr), lock=True)

            # UIの作成
            with LayoutManager(cmds.rowLayout(nc=4, adj=1, parent=extraColumnName)):
                cmds.text("{}".format(attr), al="left", w=label_w)
                cmds.checkBox("extraChannelBox_{}".format(i), l=" ", value=isHidden, w=checkBox_w,
                              cc="CCS_changeAttr('extraChannelBox_{}', '{}.{}', 'channelBox')".format(i, selobj[0], attr))
                cmds.checkBox("extraKeyable_{}".format(i), l=" ", value=isKeyable, w=checkBox_w,
                              cc="CCS_changeAttr('extraKeyable_{}', '{}.{}', 'keyable')".format(i, selobj[0], attr))
                cmds.checkBox("extraLock_{}".format(i), l=" ", value=isLock, w=checkBox_w,
                              cc="CCS_changeAttr('extraLock_{}', '{}.{}', 'lock')".format(i, selobj[0], attr))


# UI設定----------------------------------------------
def callAttrSettingWindow(callType=1):
    mel.eval("AttributeEditor;")
    print("callType =", callType)
    if callType == 1:
        mel.eval("showAddAttrWin")
    if callType == 2:
        mel.eval("showDeleteAttrWin")
    if callType == 3:
        mel.eval("showRenameAttrWin")


def CCS_getUIName():
    """Methods for managing UI names and values

    Returns:
        str: Base ScrollLayout Name
        str: Base ColimnLayout Name
        str: default ScrollLayout Name
        str: default ColimnLayout Name
        str: extra ScrollLayout Name
        str: extra ColimnLayout Name
        str[]: Attribute Name List for show in Base ScrollLayout

    """
    baseScrollName = "CCS_baseAttrListScroll"
    baseColumnName = "CCS_baseAttrsListScrollChildren"
    defaultScrollName = "CCS_defaultAttrListScroll"
    defaultColumnName = "CCS_defaultAttrsListScrollChildren"
    extraScrollName = "CCS_extraAttrListScroll"
    extraColumnName = "CCS_extraAttrsListScrollChildren"
    baseAttrList = ["translateX", "translateY", "translateZ",
                    "rotateX", "rotateY", "rotateZ",
                    "scaleX", "scaleY", "scaleZ",
                    "visibility"]
    return baseScrollName, baseColumnName, defaultScrollName, defaultColumnName, extraScrollName, extraColumnName, baseAttrList


def CCS_makeUI():
    """Create main UI
    """
    winName = "CCS_win"
    _version = "1.0"
    label_w = 100
    checkBox_w = 40
    baseScrollName, baseColumnName, defaultScrollName, defaultColumnName, extraScrollName, extraColumnName, baseAttrList = CCS_getUIName()

    # ウィンドウが重複した場合の処理
    if cmds.window(winName, q=True, ex=True):
        cmds.deleteUI(winName)

    # Window作成
    window = cmds.window(winName, title=u"Kz_channelControlSetting v{}".format(_version), sizeable=True,
                         maximizeButton=False, minimizeButton=False)

    # レイアウト formLayout Ver
    cmds.formLayout("CCS_form", numberOfDivisions=100)
    cmds.text("CCS_title", l=u"Kz_channelControlSetting")

    # 選択オブジェクト表示部
    with LayoutManager(cmds.rowLayout("CCS_selectObjectLayout", numberOfColumns=2, adj=2)):
        cmds.text("Select object:")
        cmds.textField("selectObjectField", text="", editable=False)

    # タイトル表示部
    with LayoutManager(cmds.rowLayout("CCS_topicLayout", numberOfColumns=5, adj=1)):
        cmds.text("Name", w=label_w, al="left")
        cmds.text("channel\nBox", w=56, al="center")
        cmds.text("Keyable", w=56, al="left")
        cmds.text("Lock", w=56, al="left")

    # 一覧表示部分
    with LayoutManager(cmds.paneLayout("CCS_panel", configuration='horizontal3', paneSize=[[1, 100, 50], [2, 100, 30]])):
        # よく使うアトリビュート表示部
        with LayoutManager(cmds.scrollLayout(baseScrollName, borderVisible=True, childResizable=True, hst=0, vst=16, vsb=True)):
            with LayoutManager(cmds.columnLayout(baseColumnName, adj=True)):
                for baseAttr in baseAttrList:
                    with LayoutManager(cmds.rowLayout(numberOfColumns=5, adj=1)):
                        cmds.text("{}".format(baseAttr), al="left", w=label_w)
                        cmds.checkBox("extraChannelBox_{}".format(baseAttr), l=" ", value=False, w=checkBox_w)
                        cmds.checkBox("extraKeyable_{}".format(baseAttr), l=" ", value=False, w=checkBox_w)
                        cmds.checkBox("extraLock_{}".format(baseAttr), l=" ", value=False, w=checkBox_w)

        # 標準アトリビュート表示部
        with LayoutManager(cmds.scrollLayout(defaultScrollName, borderVisible=True, childResizable=True, hst=0, vst=16, vsb=True)):
            with LayoutManager(cmds.columnLayout(defaultColumnName, adj=True)):
                cmds.text("defaultNonSelectedText", l="There is nothing selected.")

        # 追加アトリビュート表示部
        with LayoutManager(cmds.scrollLayout(extraScrollName, borderVisible=True, childResizable=True, hst=0, vst=16, vsb=True)):
            with LayoutManager(cmds.columnLayout(extraColumnName, adj=True)):
                cmds.text("extraNonSelectedText", l="There is nothing selected.")

    # 標準機能呼び出しボタン
    with LayoutManager(cmds.rowLayout("CCS_showBtnLayout", numberOfColumns=3, adj=1)):
        cmds.button("CCS_showAddAttrWindowBtn", l="Add Attr", w=88, c=lambda *args: callAttrSettingWindow(callType=1))
        cmds.button("CCS_showDeleteAttrWindowBtn", l="Delete Attr", w=88, c=lambda *args: callAttrSettingWindow(callType=2))
        cmds.button("CCS_showEditAttrWindowBtn", l="Edit Attr", w=88, c=lambda *args: callAttrSettingWindow(callType=3))

    # Tipsの表示
    cmds.text("Tipstext", l="Tips:Uncheck the Channel box and Kyeable to hide it")

    # 基準点と配置の設定
    cmds.formLayout("CCS_form", e=True,
                    attachForm=[("CCS_title", 'top', 5),
                                ("CCS_title", 'left', 5),
                                ("CCS_title", 'right', 5),
                                ("CCS_selectObjectLayout", 'top', 5),
                                ("CCS_selectObjectLayout", 'left', 5),
                                ("CCS_selectObjectLayout", 'right', 5),
                                ("CCS_topicLayout", 'top', 5),
                                ("CCS_topicLayout", 'left', 5),
                                ("CCS_topicLayout", 'right', 5),
                                ("CCS_panel", 'top', 5),
                                ("CCS_panel", 'left', 5),
                                ("CCS_panel", 'right', 5),
                                ("CCS_showBtnLayout", 'left', 5),
                                ("CCS_showBtnLayout", 'right', 5),
                                ("CCS_showBtnLayout", 'bottom', 5),
                                ("Tipstext", 'left', 5),
                                ("Tipstext", 'right', 5),
                                ("Tipstext", 'bottom', 5),
                                ],
                    attachControl=[("CCS_selectObjectLayout", 'top', 5, "CCS_title"),
                                   ("CCS_topicLayout", 'top', 5, "CCS_selectObjectLayout"),
                                   ("CCS_panel", 'top', 5, "CCS_topicLayout"),
                                   ("CCS_panel", 'bottom', 5, "CCS_showBtnLayout"),
                                   ("CCS_showBtnLayout", 'bottom', 5, "Tipstext"),
                                   ])
    cmds.setParent("..")  # for close formLayout

    # windowの描画
    cmds.showWindow(window)

    # 新規シーンかシーンを開いた時にメニューを閉じる
    cmds.scriptJob(event=['SceneOpened', 'cmds.deleteUI("{}")'.format(winName)], p=winName)
    cmds.scriptJob(event=['NewSceneOpened', 'cmds.deleteUI("{}")'.format(winName)], p=winName)

    # 選択変更時のイベントを登録
    scriptJobId = cmds.scriptJob(event=["SelectionChanged", CCS_SelectionChangedCommand], parent="MayaWindow")

    # ウインドウを閉じた際にscriptJpbを破棄する
    cmds.window(winName, e=True, widthHeight=(360, 600), sizeable=True,
                cc="cmds.scriptJob(kill={})".format(scriptJobId))

    # UIの更新
    CCS_SelectionChangedCommand()


if __name__ == "__main__":
    CCS_makeUI()
