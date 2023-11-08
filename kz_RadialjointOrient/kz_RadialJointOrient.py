# -*- coding: utf-8 -*-
"""kz_RadialJointOrient.py

git:https://github.com/kazinos/kz_MayaTools.git

codeing by kazinos
MayaVer Maya2020.4
2023/11/03 kazinos 制作開始
2022/11/08 kazinos git commit

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
import math


def RJO_createBasePoint(BasePointLocaterName="RJO_BasePoint_loc"):
    """Create a locator at the center of gravity of the selected joint

    Args:
        BasePointLocaterName (str, optional): Name of the reference locator to be created. Defaults to "RJO_BasePoint_loc".
    """
    worldPosX = 0
    worldPosY = 0
    worldPosZ = 0
    selJnt = cmds.ls(sl=True, type="joint")

    for jnt in selJnt:
        worldPosX += cmds.joint(jnt, q=True, a=True, p=True)[0]
        worldPosY += cmds.joint(jnt, q=True, a=True, p=True)[1]
        worldPosZ += cmds.joint(jnt, q=True, a=True, p=True)[2]
    worldPosX /= len(selJnt)
    worldPosY /= len(selJnt)
    worldPosZ /= len(selJnt)
    if cmds.ls(BasePointLocaterName):
        cmds.delete(BasePointLocaterName)
    loc = cmds.spaceLocator(n=BasePointLocaterName)
    cmds.move(worldPosX, worldPosY, worldPosZ, loc)


def RJO_calcClossProdact(vector01=[1, 0, 0], vector02=[0, 1, 0]):
    """Calculate the closs product

    Calculate a vector in the direction perpendicular to the plane formed by two vectors.
    Args:
        vector01 (list, optional): input Vector1. Defaults to [1, 0, 0].
        vector02 (list, optional): input Vector2. Defaults to [0, 1, 0].

    Returns:
        [float, float, float]: closs product
    """
    resultVector = [0, 0, 0]
    resultVector[0] = vector01[1] * vector02[2] - vector01[2] * vector02[1]
    resultVector[1] = vector01[2] * vector02[0] - vector01[0] * vector02[2]
    resultVector[2] = vector01[0] * vector02[1] - vector01[1] * vector02[0]
    return resultVector


def RJO_calcAngleBetweenTwoVectors(vector01=[1, 0, 0], vector02=[0, 1, 0]):
    """Calculate the angle between two vectors

    Dot product: calculated by transforming vector_A・vector_B = |A||B|cosθ
    cosθ = vector_A・vector_B / |A||B|
    θ = acos(vector_A・vector_B / |A||B|)
    The return value is in radians, so convert to degrees.

    Args:
        vector01 (list, optional): input Vector1. Defaults to [1, 0, 0].
        vector02 (list, optional): input Vector2. Defaults to [0, 1, 0].

    Returns:
        float: Angle between two vectors (digree)
    """
    dot_product = sum(a * b for a, b in zip(vector01, vector02))
    Magnitude01 = math.sqrt(sum(a ** 2 for a in vector01))
    Magnitude02 = math.sqrt(sum(a ** 2 for a in vector02))

    projectionLength = 0
    projectionLength = dot_product / (Magnitude01 * Magnitude02)

    # 不動小数点の誤差で-1～1の範囲を出る事があるので、整える
    if projectionLength <= -1:
        projectionLength = -1
    if projectionLength >= 1:
        projectionLength = 1
    radAngle = math.acos(projectionLength)
    degAngle = math.degrees(radAngle)
    return degAngle


def RJO_convertProjectionVector(inputVector=[1, 0, 0], nomalVector=[1, 0, 0]):
    """Projection of the input vector onto a coordinate plane with nomal vector.

    Args:
        inputVector (list, optional): Vector of conversion source. Defaults to [1,0,0].
        nomalVector (list, optional): normal vector of the surface to be projected. Defaults to [1,0,0].

    Returns:
        [float, float, float]: projection vector
    """
    resultVector = [0, 0, 0]
    dot = nomalVector[0] * inputVector[0] + nomalVector[1] * inputVector[1] + nomalVector[2] * inputVector[2]
    resultVector[0] = inputVector[0] - dot * nomalVector[0]
    resultVector[1] = inputVector[1] - dot * nomalVector[1]
    resultVector[2] = inputVector[2] - dot * nomalVector[2]
    return resultVector


def RJO_checkRotateDirection(vector01=[1, 0, 0], vector02=[0, 1, 0], baseVec=[1, 0, 0]):
    """Check direction of rotation using cross product

    Args:
        vector01 (list, optional): input Vector1. Defaults to [1, 0, 0].
        vector02 (list, optional): input Vector2. Defaults to [0, 1, 0].
        baseVec (list, optional): normal vector. Defaults to [1, 0, 0].

    Returns:
        float: Positive or negative value 1 or -1
    """
    # vec01とvec02の外積を求める
    closs = RJO_calcClossProdact(vector01, vector02)
    if closs == [0.0, 0.0, 0.0]:
        return 1
    if 90 <= RJO_calcAngleBetweenTwoVectors(baseVec, closs):
        return 1
    return -1


def RJO_setAimOrientjoint(primaryAxis="X", secondaryAxis="X", targetJnts=[], aimLoc="RJO_BasePoint_loc"):
    """Process to turn Secondary Axis to aimLoc direction.

    Assuming that the PrimaryAxis is facing the child.

    Args:
        targetJnt (str, optional): Name of the joint whose jointOrient is to be changed. Defaults to "".
        aimLoc (str, optional): Locator name on which the calculation is based. Defaults to "RJO_BasePoint_loc".
    """
    if not targetJnts:
        return
    if primaryAxis == secondaryAxis:
        return
    if not cmds.ls(aimLoc):
        cmds.inViewMessage(amg='<hl>aimtarget not found</hl>', fts=20, pos='midCenter', fade=True)
        return
    for jnt in targetJnts:
        if cmds.listConnections(jnt, type="skinCluster"):
            cmds.inViewMessage(amg='<hl>{} has skinning.</hl>'.format(jnt), fts=20, pos='midCenter', fade=True)
            return
        if not cmds.getAttr("{}.rotate".format(jnt)) == [(0, 0, 0)]:
            cmds.inViewMessage(amg='<hl>joint in rotate</hl>', fts=20, pos='midCenter', fade=True)
            return

    # primalyJointを合わせる為、普通にjointの方向付けをする
    orientSettingDict = {"X": ["xyz", "xup"],
                         "Y": ["yzx", "yup"],
                         "Z": ["zxy", "zup"]}
    AxisDict = {"X": [0, 1, 2],
                "Y": [4, 5, 6],
                "Z": [8, 9, 10]}
    cmds.joint(targetJnts, e=True, oj=orientSettingDict[primaryAxis][0], ch=True, sao=orientSettingDict[primaryAxis][1])

    # 末端jointはjointOrientをゼロに
    for jnt in targetJnts:
        if not cmds.listRelatives(jnt, c=True):
            cmds.joint(jnt, e=True, o=[0, 0, 0])

    for jnt in targetJnts:
        # ベクトルの取得
        jntWorldPos = cmds.xform(jnt, q=True, t=True, ws=True)
        locWorldPos = cmds.xform(aimLoc, q=True, t=True, ws=True)
        JntToLocVector = [locWorldPos[i] - jntWorldPos[i] for i in range(3)]
        primaryVector = [cmds.xform(jnt, q=True, m=True, ws=True)[i] for i in AxisDict[primaryAxis]]
        secondaryVector = [cmds.xform(jnt, q=True, m=True, ws=True)[i] for i in AxisDict[secondaryAxis]]

        # PrimaryAxisをnomalVectorとした平面にJntToLocVectorを射影変換
        projectionVector = RJO_convertProjectionVector(inputVector=JntToLocVector, nomalVector=primaryVector)

        # 2つのベクトル間の角度を計算
        rotateAngle = RJO_calcAngleBetweenTwoVectors(vector01=projectionVector, vector02=secondaryVector)

        # 回転方向（正負）の判定
        rotDirction = RJO_checkRotateDirection(vector01=projectionVector, vector02=secondaryVector, baseVec=primaryVector)
        reverse = 180
        if cmds.optionMenu("SecondaryDirection", q=True, sl=True) == 2:
            reverse = 0
        rotateAngle = rotateAngle * rotDirction + reverse

        # 回転操作
        if primaryAxis == "X":
            cmds.rotate(rotateAngle, 0, 0, jnt, r=True, os=True, fo=True, pcp=True)
        elif primaryAxis == "Y":
            cmds.rotate(0, rotateAngle, 0, jnt, r=True, os=True, fo=True, pcp=True)
        elif primaryAxis == "Z":
            cmds.rotate(0, 0, rotateAngle, jnt, r=True, os=True, fo=True, pcp=True)

    # フリーズ
    cmds.select(targetJnts)
    mel.eval("FreezeTransformations")
    for jnt in targetJnts:
        cmds.rotate(0, 0, 0, jnt, a=True)
    cmds.select(targetJnts)


# -------------------------------------------------------
def RJO_changeSameValueSelected(inputValue="X", changeUIName="PrimaryAxisCollection"):
    """Process to change primaryAxis and secondaryAxis so that they are not the same

    Args:
        inputValue (str, optional): Selected Axis. Defaults to "X".
        changeUIName (str, optional): Changed UI Name. Defaults to "PrimaryAxisCollection".
    """
    setCollectionName = "SecondaryAxisCollection"
    setAttrName = "secondary"

    if changeUIName == "SecondaryAxisCollection":
        setCollectionName = "PrimaryAxisCollection"
        setAttrName = "primary"

    # 選択された軸が同一になるかチェック
    if inputValue != cmds.radioCollection(setCollectionName, q=True, sl=True)[-1]:
        return

    setValue = "X"
    if inputValue == "X":
        setValue = "Y"
    if inputValue == "Y":
        setValue = "Z"
    # 選択の変更
    cmds.radioCollection(setCollectionName, e=True, sl="{}_{}".format(setAttrName, setValue))


def RJO_makeUI():
    toolName = "kz_RadialJointOrient"
    winName = "KRT_win"
    _version = "1.0"
    text_w = 100

    # ウィンドウが重複した場合の処理
    if cmds.window(winName, q=True, ex=True):
        cmds.deleteUI(winName)

    # Window作成
    window = cmds.window(winName, title=u"{} v{}".format(toolName, _version), sizeable=True,
                         maximizeButton=False, minimizeButton=False)
    # レイアウト
    with LayoutManager(cmds.columnLayout(adjustableColumn=True)):
        cmds.text(u"{}".format(toolName))

        cmds.button(l="create BasePoint", c=lambda *args: RJO_createBasePoint())
        cmds.button(l="set Orient",
                    c=lambda *args: RJO_setAimOrientjoint(primaryAxis=cmds.radioCollection("PrimaryAxisCollection", q=True, sl=True)[-1],
                                                          secondaryAxis=cmds.radioCollection("SecondaryAxisCollection", q=True, sl=True)[-1],
                                                          targetJnts=cmds.ls(sl=True, dag=True, type="joint"),
                                                          aimLoc="RJO_BasePoint_loc"))

        # labelの表示・非表示
        with LayoutManager(cmds.frameLayout(l=u"Settings", cll=True, cl=False, mw=20)):
            with LayoutManager(cmds.columnLayout(adj=1)):
                with LayoutManager(cmds.rowLayout(nc=5, adj=1)):
                    cmds.text("Primary Axis", w=text_w, al="left")
                    cmds.radioCollection("PrimaryAxisCollection")
                    cmds.radioButton("primary_X", l="X", sl=True)
                    cmds.radioButton("primary_Y", l="Y")
                    cmds.radioButton("primary_Z", l="Z")
                    cmds.text("", w=54)  # 位置調整用
                with LayoutManager(cmds.rowLayout(nc=6, adj=1)):
                    cmds.text("Secondary Axis", w=text_w, al="left")
                    cmds.radioCollection("SecondaryAxisCollection")
                    cmds.radioButton("secondary_X", l="X")
                    cmds.radioButton("secondary_Y", l="Y", sl=True)
                    cmds.radioButton("secondary_Z", l="Z")
                    cmds.optionMenu("SecondaryDirection")
                    cmds.menuItem(label="+")
                    cmds.menuItem(label="-")
    cmds.showWindow(window)
    cmds.radioButton("primary_X", e=True, onc=lambda *args: RJO_changeSameValueSelected(inputValue="X", changeUIName="PrimaryAxisCollection"))
    cmds.radioButton("primary_Y", e=True, onc=lambda *args: RJO_changeSameValueSelected(inputValue="Y", changeUIName="PrimaryAxisCollection"))
    cmds.radioButton("primary_Z", e=True, onc=lambda *args: RJO_changeSameValueSelected(inputValue="Z", changeUIName="PrimaryAxisCollection"))
    cmds.radioButton("secondary_X", e=True, onc=lambda *args: RJO_changeSameValueSelected(inputValue="X", changeUIName="SecondaryAxisCollection"))
    cmds.radioButton("secondary_Y", e=True, onc=lambda *args: RJO_changeSameValueSelected(inputValue="Y", changeUIName="SecondaryAxisCollection"))
    cmds.radioButton("secondary_Z", e=True, onc=lambda *args: RJO_changeSameValueSelected(inputValue="Z", changeUIName="SecondaryAxisCollection"))

    cmds.window(winName, e=True, widthHeight=(220, 120), sizeable=True)


if __name__ == "__main__":
    RJO_makeUI()
