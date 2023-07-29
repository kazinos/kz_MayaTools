# -*- coding: utf-8 -*-
"""kz_jointDisplaySettings.py

git:https://github.com/kazinos/kz_MayaTools.git

codeing by kazinos
MayaVer Maya2020.4
2023/07/23 kazinos 制作開始
2023/07/27 kazinos formLayout開閉時のWindowサイズ変更処理の実装
2023/07/29 kazinos 選択されているjointのTRS値を桁数を指定して表示する機能の実装

issue:
outlinerColor count変更時のWindowリサイズ処理
outlinerColor 実行後、描画更新処理の実装

"""
from maya import cmds
from maya.common.ui import LayoutManager


def JDS_setJointTRS():
    unit = cmds.intField("unitNum", q=True, v=True)
    selobj = cmds.ls(sl=True, type="joint")
    objTranslate = [0, 0, 0]
    objRotate = [0, 0, 0]
    objScale = [0, 0, 0]
    if selobj:
        objTranslate = cmds.xform(selobj[0], q=True, t=True)
        objRotate = cmds.xform(selobj[0], q=True, ro=True)
        objScale = cmds.xform(selobj[0], q=True, s=True, r=True)

    cmds.floatField("view_tx", e=True, pre=unit, v=objTranslate[0])
    cmds.floatField("view_ty", e=True, pre=unit, v=objTranslate[1])
    cmds.floatField("view_tz", e=True, pre=unit, v=objTranslate[2])
    cmds.floatField("view_rx", e=True, pre=unit, v=objRotate[0])
    cmds.floatField("view_ry", e=True, pre=unit, v=objRotate[1])
    cmds.floatField("view_rz", e=True, pre=unit, v=objRotate[2])
    cmds.floatField("view_sx", e=True, pre=unit, v=objScale[0])
    cmds.floatField("view_sy", e=True, pre=unit, v=objScale[1])
    cmds.floatField("view_sz", e=True, pre=unit, v=objScale[2])


def JDS_showJointLabel(target=[], setBool=False):
    # エラー回避処理
    if not target:
        cmds.inViewMessage(amg='<hl>Please select joint</hl>', fts=20, pos='midCenter', fade=True)
    # 設定
    for jnt in target:
        cmds.setAttr("{}.drawLabel".format(jnt), setBool)


def JDS_showAxis(target=[], setBool=False):
    # エラー回避処理
    if not target:
        cmds.inViewMessage(amg='<hl>Please select joint</hl>', fts=20, pos='midCenter', fade=True)
    # 設定
    for jnt in target:
        cmds.setAttr("{}.displayLocalAxis".format(jnt), setBool)


def JDS_setJointColor(target=[], rgb=[0, 0, 0], setBool=False):
    # エラー回避処理
    if not target:
        cmds.inViewMessage(amg='<hl>Please select joint</hl>', fts=20, pos='midCenter', fade=True)
    # リセット処理
    if not setBool:
        for jnt in target:
            cmds.setAttr("{}.overrideColorR".format(jnt), 0)
            cmds.setAttr("{}.overrideColorG".format(jnt), 0)
            cmds.setAttr("{}.overrideColorB".format(jnt), 0)
            cmds.setAttr("{}.overrideColor".format(jnt), 0)
            cmds.setAttr("{}.overrideRGBColors".format(jnt), False)
            cmds.setAttr("{}.overrideEnabled".format(jnt), False)
        return
    # 設定
    for jnt in target:
        cmds.setAttr("{}.overrideEnabled".format(jnt), True)
        cmds.setAttr("{}.overrideRGBColors".format(jnt), True)
        cmds.setAttr("{}.overrideColorR".format(jnt), rgb[0])
        cmds.setAttr("{}.overrideColorG".format(jnt), rgb[1])
        cmds.setAttr("{}.overrideColorB".format(jnt), rgb[2])


def JDS_setJointRadius(target=[], setValue=0.5):
    # エラー回避処理
    if not target:
        cmds.inViewMessage(amg='<hl>Please select joint</hl>', fts=20, pos='midCenter', fade=True)

    # 設定
    for jnt in target:
        cmds.setAttr("{}.radius".format(jnt), setValue)


def JDS_setJointOutlinerColor(setBool=False):
    jnts = cmds.ls(type="joint")
    arrayCount = cmds.intField("JDScolorCount", q=True, value=True)

    # reset処理
    if not setBool:
        for jnt in jnts:
            cmds.setAttr("{}.outlinerColorR".format(jnt), 0)
            cmds.setAttr("{}.outlinerColorG".format(jnt), 0)
            cmds.setAttr("{}.outlinerColorB".format(jnt), 0)
            cmds.setAttr("{}.useOutlinerColor".format(jnt), False)
        return

    # 色設定
    for i in range(arrayCount):
        tex = cmds.textField("JDS_findName_{}".format(i), q=True, text=True)
        col = cmds.colorSliderGrp("JDS_olColor_{}".format(i), q=True, rgb=True)
        if tex == "":
            continue
        for jnt in jnts:
            if ("{}".format(tex) in jnt):
                cmds.setAttr("{}.useOutlinerColor".format(jnt), True)
                cmds.setAttr("{}.outlinerColorR".format(jnt), col[0])
                cmds.setAttr("{}.outlinerColorG".format(jnt), col[1])
                cmds.setAttr("{}.outlinerColorB".format(jnt), col[2])
    cmds.setFocus("")


# -------------------------------------------------------
def resizeUIHight(winaName, layoutName):
    """frameLayout開閉時のWindowサイズ変更処理

    Args:
        winaName (str): リサイズを行うウインドウの名前
        layoutName (str): 変更を行うLayoutの名前
    """
    WinHight = cmds.window(winaName, q=True, h=True)
    layoutHight = cmds.frameLayout(layoutName, q=True, h=True)
    cmds.window(winaName, e=True, h=WinHight - layoutHight + 24)


def JDS_makeOutlinerUI():
    """joint Outliner Color内のUI作成

    Returns:
        columnLayout: countにあわせたレイアウト
    """
    arrayCount = cmds.intField("JDScolorCount", q=True, value=True)
    outlinerInfoList = []

    # 既にあれば消す
    if cmds.columnLayout("JDS_outlinerUILayout", ex=True):
        # 一時的に情報をoutlinerInfoListに記憶
        for i in range(arrayCount):
            if not cmds.textField("JDS_findName_{}".format(i), ex=True):
                break
            outlinerInfoList.append([cmds.textField("JDS_findName_{}".format(i), q=True, text=True),
                                    cmds.colorSliderGrp("JDS_olColor_{}".format(i), q=True, rgb=True)])
        # 消す
        cmds.deleteUI("JDS_outlinerUILayout", lay=True)

    # UI作成
    with LayoutManager(cmds.columnLayout("JDS_outlinerUILayout", p="outlinerLayout", adj=True)):
        with LayoutManager(cmds.rowLayout(nc=2, adj=1)):
            cmds.text(l="Search Name", al="left", w=150)
            cmds.text(l="Color", al="left")
        for i in range(arrayCount):
            with LayoutManager(cmds.rowLayout(nc=2, adj=1)):
                cmds.textField("JDS_findName_{}".format(i), w=100)
                cmds.colorSliderGrp("JDS_olColor_{}".format(i), rgb=(0, 0, 0), cw2=[50, 100])

    # outlinerInfoListがあれば値を反映
    if outlinerInfoList:
        for i in range(len(outlinerInfoList)):
            cmds.textField("JDS_findName_{}".format(i), e=True, text=outlinerInfoList[i][0])
            cmds.colorSliderGrp("JDS_olColor_{}".format(i), e=True, rgb=outlinerInfoList[i][1])

    return cmds.columnLayout("JDS_outlinerUILayout", q=True)


def JDS_makeUI():
    """mainUI
    """
    winName = "kz_JointDisplaySettings"
    btn_w = 120

    # ウィンドウが重複した場合の処理
    if cmds.window(winName, q=True, ex=True):
        cmds.deleteUI(winName)

    # Window作成
    window = cmds.window(winName, title=u"kz_JointDisplaySettings", sizeable=True,
                         maximizeButton=False, minimizeButton=False)
    # レイアウト
    with LayoutManager(cmds.columnLayout(adjustableColumn=True)):
        cmds.text(u"Joint display settings")
        trsTitle_w = 80
        trsFloatFld_w = 80
        with LayoutManager(cmds.rowLayout(nc=8, adj=8)):
            cmds.text("unit", w=trsTitle_w)
            cmds.intField("unitNum", w=trsFloatFld_w, v=3,
                          cc=lambda *args: JDS_setJointTRS())

        with LayoutManager(cmds.rowLayout(nc=8, adj=8)):
            cmds.text("translate", w=trsTitle_w)
            cmds.text("X")
            cmds.floatField("view_tx", w=trsFloatFld_w)
            cmds.text("Y")
            cmds.floatField("view_ty", w=trsFloatFld_w)
            cmds.text("Z")
            cmds.floatField("view_tz", w=trsFloatFld_w)
            cmds.text("")
        with LayoutManager(cmds.rowLayout(nc=8, adj=8)):
            cmds.text("rotate", w=trsTitle_w)
            cmds.text("X")
            cmds.floatField("view_rx", w=trsFloatFld_w)
            cmds.text("Y")
            cmds.floatField("view_ry", w=trsFloatFld_w)
            cmds.text("Z")
            cmds.floatField("view_rz", w=trsFloatFld_w)
            cmds.text("")
        with LayoutManager(cmds.rowLayout(nc=8, adj=8)):
            cmds.text("Scale", w=trsTitle_w)
            cmds.text("X")
            cmds.floatField("view_sx", w=trsFloatFld_w)
            cmds.text("Y")
            cmds.floatField("view_sy", w=trsFloatFld_w)
            cmds.text("Z")
            cmds.floatField("view_sz", w=trsFloatFld_w)
            cmds.text("")

        # labelの表示・非表示
        with LayoutManager(cmds.frameLayout("JDS_FrameLayout1", l=u"Label Display", cll=True, cl=True, mw=20,
                                            cc=lambda *args: resizeUIHight(winName, "JDS_FrameLayout1"))):
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
        with LayoutManager(cmds.frameLayout("JDS_FrameLayout2", l=u"Axis Display", cll=True, cl=True, mw=20,
                                            cc=lambda *args: resizeUIHight(winName, "JDS_FrameLayout2"))):
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
        with LayoutManager(cmds.frameLayout("JDS_FrameLayout3", l=u"Joint Radius", cll=True, cl=True, mw=20,
                                            cc=lambda *args: resizeUIHight(winName, "JDS_FrameLayout3"))):
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
        with LayoutManager(cmds.frameLayout("JDS_FrameLayout4", l=u"Joint Color", cll=True, cl=True, mw=20,
                                            cc=lambda *args: resizeUIHight(winName, "JDS_FrameLayout4"))):
            with LayoutManager(cmds.rowLayout(nc=1, adj=1)):
                cmds.colorSliderGrp("JDS_jointColor", rgb=(0, 0, 0))
            with LayoutManager(cmds.rowLayout(nc=4, adj=4)):
                cmds.button(l="Set", w=btn_w * 0.66, c=lambda *args: JDS_setJointColor(cmds.ls(sl=True, type="joint"),
                                                                                       cmds.colorSliderGrp("JDS_jointColor", q=True, rgb=True),
                                                                                       setBool=True))
                cmds.button(l="Reset", w=btn_w * 0.66, c=lambda *args: JDS_setJointColor(cmds.ls(sl=True, dag=True, type="joint"),
                                                                                         setBool=False))
                cmds.button(l="ALL Reset", w=btn_w * 0.66, c=lambda *args: JDS_setJointColor(cmds.ls(type="joint"),
                                                                                             setBool=False))
                cmds.text(l="")  # 調整用

        # outlinerColorの設定
        with LayoutManager(cmds.frameLayout("JDS_FrameLayout5", l=u"Joint Outliner Color", cll=True, cl=True, mw=20,
                                            cc=lambda *args: resizeUIHight(winName, "JDS_FrameLayout5"))):
            with LayoutManager(cmds.rowLayout(nc=2, adj=2)):
                cmds.text("Count:")
                cmds.intField("JDScolorCount", value=4, cc=lambda *args: JDS_makeOutlinerUI())

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
    # ジョイントの選択変更イベントを登録
    script_job_id = cmds.scriptJob(event=["SelectionChanged", JDS_setJointTRS], parent="MayaWindow")

    cmds.window(winName, e=True, widthHeight=(312, 136), sizeable=True,
                cc="cmds.scriptJob(kill={})".format(script_job_id))


if __name__ == "__main__":
    JDS_makeUI()
