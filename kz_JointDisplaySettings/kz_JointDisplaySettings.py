# -*- coding: utf-8 -*-
"""kz_jointDisplaySettings.py

git:https://github.com/kazinos/kz_MayaTools.git

codeing by kazinos
MayaVer Maya2020.4
2023/07/23 kazinos 制作開始

issue:

"""
from maya import cmds, mel
from maya.common.ui import LayoutManager


def JDS_showJointLabel(_target=[], _setBool=False):
    # エラー回避処理
    if not _target:
        cmds.inViewMessage(amg='<hl>Please select joint</hl>', fts=20, pos='midCenter', fade=True)

    # 設定
    for _jnt in _target:
        cmds.setAttr("{}.drawLabel".format(_jnt), _setBool)


def JDS_showAxis(_target=[], _setBool=False):
    # エラー回避処理
    if not _target:
        cmds.inViewMessage(amg='<hl>Please select joint</hl>', fts=20, pos='midCenter', fade=True)

    # 設定
    for _jnt in _target:
        cmds.setAttr("{}.displayLocalAxis".format(_jnt), _setBool)


def JDS_setJointColor(_target=[], _rgb=[0, 0, 0], _setBool=False):
    # エラー回避処理
    if not _target:
        cmds.inViewMessage(amg='<hl>Please select joint</hl>', fts=20, pos='midCenter', fade=True)

    # リセット処理
    if not _setBool:
        for _jnt in _target:
            cmds.setAttr("{}.overrideColorR".format(_jnt), 0)
            cmds.setAttr("{}.overrideColorG".format(_jnt), 0)
            cmds.setAttr("{}.overrideColorB".format(_jnt), 0)
            cmds.setAttr("{}.overrideColor".format(_jnt), 0)
            cmds.setAttr("{}.overrideRGBColors".format(_jnt), False)
            cmds.setAttr("{}.overrideEnabled".format(_jnt), False)
        return

    # 設定
    for _jnt in _target:
        cmds.setAttr("{}.overrideEnabled".format(_jnt), True)
        cmds.setAttr("{}.overrideRGBColors".format(_jnt), True)
        cmds.setAttr("{}.overrideColorR".format(_jnt), _rgb[0])
        cmds.setAttr("{}.overrideColorG".format(_jnt), _rgb[1])
        cmds.setAttr("{}.overrideColorB".format(_jnt), _rgb[2])


def JDS_setJointRadius(_target=[], _setValue=0.5):
    # エラー回避処理
    if not _target:
        cmds.inViewMessage(amg='<hl>Please select joint</hl>', fts=20, pos='midCenter', fade=True)

    for _jnt in _target:
        cmds.setAttr("{}.radius".format(_jnt), _setValue)


def JDS_setJointOutlinerColor(_setBool=False):
    _jnts = cmds.ls(type="joint")
    _ArrayCount = cmds.intField("JDS_colorCount", q=True, value=True)

    # reset処理
    if (not _setBool):
        for _jnt in _jnts:
            cmds.setAttr("{}.outlinerColorR".format(_jnt), 0)
            cmds.setAttr("{}.outlinerColorG".format(_jnt), 0)
            cmds.setAttr("{}.outlinerColorB".format(_jnt), 0)
            cmds.setAttr("{}.useOutlinerColor".format(_jnt), False)
        return

    # 色設定
    for i in range(_ArrayCount):
        _tex = cmds.textField("JDS_findName_{}".format(i), q=True, text=True)
        _col = cmds.colorSliderGrp("JDS_olColor_{}".format(i), q=True, rgb=True)
        if _tex == "":
            continue
        for _jnt in _jnts:
            if ("{}".format(_tex) in _jnt):
                cmds.setAttr("{}.useOutlinerColor".format(_jnt), True)
                cmds.setAttr("{}.outlinerColorR".format(_jnt), _col[0])
                cmds.setAttr("{}.outlinerColorG".format(_jnt), _col[1])
                cmds.setAttr("{}.outlinerColorB".format(_jnt), _col[2])
    # tmp = cmds.ls(sl=True)
    # cmds.select(cl=True)
    # cmds.select(tmp)
    cmds.setFocus("")


# -------------------------------------------------------
def JDS_makeOutlinerUI():
    """joint Outliner Color内のUI作成

    Returns:
        columnLayout: countにあわせたレイアウト
    """
    _ArrayCount = cmds.intField("JDS_colorCount", q=True, value=True)
    outlinerInfoList = []

    # 既にあれば消す
    if cmds.columnLayout("outlinerUILayout", ex=True):
        # 消す前に情報を一時的にoutlinerInfoListに記憶
        for i in range(_ArrayCount):
            if not cmds.textField("JDS_findName_{}".format(i), ex=True):
                break
            outlinerInfoList.append([cmds.textField("JDS_findName_{}".format(i), q=True, text=True),
                                    cmds.colorSliderGrp("JDS_olColor_{}".format(i), q=True, rgb=True)])
        # 消す
        cmds.deleteUI("outlinerUILayout", lay=True)

    # UI作成
    with LayoutManager(cmds.columnLayout("outlinerUILayout", p="outlinerLayout", adj=True)):
        with LayoutManager(cmds.rowLayout(nc=2, adj=1)):
            cmds.text(l="Search Name", al="left", w=150)
            cmds.text(l="Color", al="left")
        for i in range(_ArrayCount):
            with LayoutManager(cmds.rowLayout(nc=2, adj=1)):
                cmds.textField("JDS_findName_{}".format(i), w=100)
                cmds.colorSliderGrp("JDS_olColor_{}".format(i), rgb=(0, 0, 0), cw2=[50, 100])

    # outlinerInfoListがあれば値を反映
    if outlinerInfoList:
        for i in range(len(outlinerInfoList)):
            cmds.textField("JDS_findName_{}".format(i), e=True, text=outlinerInfoList[i][0])
            cmds.colorSliderGrp("JDS_olColor_{}".format(i), e=True, rgb=outlinerInfoList[i][1])

    return cmds.columnLayout("outlinerUILayout", q=True)


def JDS_makeUI():
    winName = "JDS_win"
    # text_w = 200
    # input_w = 100
    btn_w = 100
    # アウトライナUIの管理用リスト
    # outlinerUI = None

    # ウィンドウが重複した場合の処理
    if cmds.window(winName, q=True, ex=True):
        cmds.deleteUI(winName)

    # Window作成
    window = cmds.window(winName, title=u"kz_JointDisplaySettings", sizeable=True,
                         maximizeButton=False, minimizeButton=False)
    # レイアウト
    with LayoutManager(cmds.columnLayout(adjustableColumn=True)):
        cmds.text(u"Joint display settings")

        # labelの表示・非表示
        with LayoutManager(cmds.frameLayout(l=u"Label Display", cll=True, cl=True, mw=20)):
            with LayoutManager(cmds.rowLayout(nc=3, adj=3)):
                cmds.button(l="Select ON", w=btn_w, c=lambda *args: JDS_showJointLabel(cmds.ls(sl=True, typ="joint"), True))
                cmds.button(l="Select OFF", w=btn_w, c=lambda *args: JDS_showJointLabel(cmds.ls(sl=True, typ="joint"), False))
                cmds.text(l="")  # 調整用
            with LayoutManager(cmds.rowLayout(nc=3, adj=3)):
                cmds.button(l="Hierarchy ON", w=btn_w, c=lambda *args: JDS_showJointLabel(cmds.ls(sl=True, dag=True, typ="joint"), True))
                cmds.button(l="Hierarchy OFF", w=btn_w, c=lambda *args: JDS_showJointLabel(cmds.ls(sl=True, dag=True, typ="joint"), False))
                cmds.text(l="")  # 調整用
            with LayoutManager(cmds.rowLayout(nc=3, adj=3)):
                cmds.button(l="All ON", w=btn_w, c=lambda *args: JDS_showJointLabel(cmds.ls(typ="joint"), True))
                cmds.button(l="All OFF", w=btn_w, c=lambda *args: JDS_showJointLabel(cmds.ls(typ="joint"), False))
                cmds.text(l="")  # 調整用

        # 軸の表示・非表示
        with LayoutManager(cmds.frameLayout(l=u"Axis Display", cll=True, cl=True, mw=20)):
            with LayoutManager(cmds.rowLayout(nc=3, adj=3)):
                cmds.button(l="Select ON", w=btn_w, c=lambda *args: JDS_showAxis(cmds.ls(sl=True, typ="joint"), True))
                cmds.button(l="Select OFF", w=btn_w, c=lambda *args: JDS_showAxis(cmds.ls(sl=True, typ="joint"), False))
                cmds.text(l="")  # 調整用
            with LayoutManager(cmds.rowLayout(nc=3, adj=3)):
                cmds.button(l="Hierarchy ON", w=btn_w, c=lambda *args: JDS_showAxis(cmds.ls(sl=True, dag=True, typ="joint"), True))
                cmds.button(l="Hierarchy OFF", w=btn_w, c=lambda *args: JDS_showAxis(cmds.ls(sl=True, dag=True, typ="joint"), False))
                cmds.text(l="")  # 調整用
            with LayoutManager(cmds.rowLayout(nc=3, adj=3)):
                cmds.button(l="All ON", w=btn_w, c=lambda *args: JDS_showAxis(cmds.ls(typ="joint"), True))
                cmds.button(l="All OFF", w=btn_w, c=lambda *args: JDS_showAxis(cmds.ls(typ="joint"), False))
                cmds.text(l="")  # 調整用

        # jointRadiusの設定
        with LayoutManager(cmds.frameLayout(l=u"Joint Radius", cll=True, cl=True, mw=20)):
            with LayoutManager(cmds.rowLayout(nc=1, adj=1)):
                cmds.floatField("JDS_radiusfloat", value=0.5)
            with LayoutManager(cmds.rowLayout(nc=4, adj=4)):
                cmds.button(l="Select", w=btn_w * 0.66, c=lambda *args: JDS_setJointRadius(cmds.ls(sl=True, type="joint"),
                                                                                           cmds.floatField("JDS_radiusfloat", q=True, value=True)))
                cmds.button(l="Hierarchy", w=btn_w * 0.66, c=lambda *args: JDS_setJointRadius(cmds.ls(sl=True, dag=True, type="joint"),
                                                                                              cmds.floatField("JDS_radiusfloat", q=True, value=True)))
                cmds.button(l="ALL", w=btn_w * 0.66, c=lambda *args: JDS_setJointRadius(cmds.ls(type="joint"),
                                                                                        cmds.floatField("JDS_radiusfloat", q=True, value=True)))
                cmds.text(l="")  # 調整用

        # jointColorの設定
        with LayoutManager(cmds.frameLayout(l=u"Joint Color", cll=True, cl=True, mw=20)):
            with LayoutManager(cmds.rowLayout(nc=1, adj=1)):
                cmds.colorSliderGrp("JDS_jointColor", rgb=(0, 0, 0))
            with LayoutManager(cmds.rowLayout(nc=3, adj=3)):
                cmds.button(l="Set", w=btn_w, c=lambda *args: JDS_setJointColor(cmds.ls(sl=True, type="joint"),
                                                                                cmds.colorSliderGrp("JDS_jointColor", q=True, rgb=True),
                                                                                _setBool=True))
                cmds.button(l="Reset", w=btn_w, c=lambda *args: JDS_setJointColor(cmds.ls(sl=True, dag=True, type="joint"),
                                                                                  _setBool=False))
                cmds.text(l="")  # 調整用
            with LayoutManager(cmds.rowLayout(nc=2, adj=2)):
                cmds.button(l="ALL Reset", w=btn_w * 2, c=lambda *args: JDS_setJointColor(cmds.ls(type="joint"),
                                                                                          _setBool=False))

        # outlinerColorの設定
        with LayoutManager(cmds.frameLayout(l=u"Joint Outliner Color", cll=True, cl=True, mw=20)):
            with LayoutManager(cmds.rowLayout(nc=2, adj=2)):
                cmds.text("Count:")
                cmds.intField("JDS_colorCount", value=4, cc=lambda *args: JDS_makeOutlinerUI())

            # 可変UIここから-----
            with LayoutManager(cmds.columnLayout("outlinerLayout", adj=True)):
                JDS_makeOutlinerUI()
            # 可変UIここまで-----
            cmds.text("tips:Second half is priority")
            with LayoutManager(cmds.rowLayout(nc=3, adj=3)):
                cmds.button(l="Set", w=btn_w, c=lambda *args: JDS_setJointOutlinerColor(True))
                cmds.button(l="Reset", w=btn_w, c=lambda *args: JDS_setJointOutlinerColor(False))
                cmds.text(l="")  # 調整用

    cmds.showWindow(window)
    cmds.window(winName, e=True, widthHeight=(220, 136), sizeable=True)

    # 新規シーンかシーンを開いた時にメニューを閉じる
    cmds.scriptJob(event=['SceneOpened', 'cmds.deleteUI("{}")'.format(winName)], p=winName)
    cmds.scriptJob(event=['NewSceneOpened', 'cmds.deleteUI("{}")'.format(winName)], p=winName)


if __name__ == "__main__":
    JDS_makeUI()
