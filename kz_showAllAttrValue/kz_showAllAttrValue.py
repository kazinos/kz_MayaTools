"""showAllAttrValue.py

Returns:
    _type_: _description_
"""

from maya import cmds
from maya.common.ui import LayoutManager


def getAllAttrName(node):
    def __recursiveGetMultAttrName(attr, attrList=[]):
        try:
            if cmds.getAttr(attr, mi=True):
                for i in cmds.getAttr(attr, mi=True):
                    if type(i) == int:
                        __recursiveGetMultAttrName("{}[{}]".format(attr, i), attrList)
                    else:
                        __recursiveGetMultAttrName("{}.{}".format(attr, i), attrList)
            attrList.append(attr)
            return attrList
        except:
            return None

    allAttrList = []
    for attr in cmds.listAttr(node):
        result = __recursiveGetMultAttrName("{}.{}".format(node, attr), attrList=[])
        if result:
            allAttrList = allAttrList + result
    return allAttrList





def SAV_makeList():
    selObj = cmds.ls(sl=True)
    if not selObj:
        return
    attrList = getAllAttrName(selObj[0])
    cmds.textScrollList("SAV_attrList",e=True,ra=True)
    if not attrList:
        return
    cmds.textScrollList("SAV_attrList",e=True,a=attrList)



def SAV_selectListItem():
    selAttrName = cmds.textScrollList("SAV_attrList",q=True,si=True)
    selAttrValue = "None"
    if cmds.getAttr(selAttrName,type=True) == "message":
        selAttrType = "message"
        selAttrValue = "None"
    elif cmds.getAttr(selAttrName,mi=True):
        selAttrValue = "mult Attr"
    else:
        selAttrType = cmds.getAttr(selAttrName,type=True)
        selAttrValue = ""
        if not selAttrType in ["double3","double4","float3","float2","TdataCompound"]:
            selAttrValue = cmds.getAttr(selAttrName)
        print(selAttrType)
        print(selAttrValue)
    cmds.textField("SAV_dataTypeFld",e=True,tx=selAttrType)
    cmds.textScrollList("SAV_valueList", e=True, ra=True,append=selAttrValue)



def SAV_makeUI():
    winName = "showAllAttrValue"
    # ウィンドウが重複した場合の処理
    if cmds.window(winName, q=True, ex=True, resizeToFitChildren=True):
        cmds.deleteUI(winName)

    # Window作成
    window = cmds.window(winName, title="Show All Attr Value", s=True, mxb=False, mnb=False)

    # レイアウト formLayout Ver
    cmds.formLayout("SAV_form", numberOfDivisions=100)
    cmds.text("SAV_titleText", label="Show All Attr Value", w=100, h=20)
    cmds.button("SAV_execBtn", l="Make attr list", c=lambda *args: SAV_makeList())
    cmds.paneLayout("SAV_attrPaneLayout", configuration="vertical2")

    # 左側
    cmds.textScrollList("SAV_attrList", w=150, allowMultiSelection=False, append=["Please make a list"], selectCommand=lambda *args: SAV_selectListItem())

    # 右側
    cmds.textScrollList("SAV_valueList", allowMultiSelection=True, append=["attr value"])
    cmds.setParent("..")
    cmds.text("SAV_typeLabel", l="Data Type:")
    cmds.textField("SAV_dataTypeFld")


    # # 基準点と配置の設定
    cmds.formLayout(
        "SAV_form",
        e=True,
        attachForm=[
            ("SAV_titleText", "top", 5),
            ("SAV_titleText", "left", 5),
            ("SAV_titleText", "right", 5),
            ("SAV_execBtn", "top", 5),
            ("SAV_execBtn", "left", 5),
            ("SAV_execBtn", "right", 5),
            ("SAV_typeLabel", "top", 5),
            ("SAV_typeLabel", "left", 5),
            # ("SAV_typeLabel", "right", 5),
            ("SAV_dataTypeFld", "top", 5),
            ("SAV_dataTypeFld", "left", 5),
            ("SAV_dataTypeFld", "right", 5),
            ("SAV_attrPaneLayout", "top", 5),
            ("SAV_attrPaneLayout", "left", 5),
            ("SAV_attrPaneLayout", "right", 5),
            ("SAV_attrPaneLayout", "bottom", 5),
        ],
        attachControl=[
            ("SAV_execBtn", "top", 5, "SAV_titleText"),
            ("SAV_typeLabel", "top", 5, "SAV_execBtn"),
            ("SAV_dataTypeFld", "top", 5, "SAV_execBtn"),
            ("SAV_dataTypeFld", "left", 5, "SAV_typeLabel"),
            ("SAV_attrPaneLayout", "top", 5, "SAV_typeLabel"),
        ],
    )
    cmds.showWindow(window)
    cmds.window(winName, e=True, widthHeight=(400, 300), sizeable=True)

    # 新規シーンかシーンを開いた時にメニューを閉じる
    cmds.scriptJob(event=["SceneOpened", 'cmds.deleteUI("{}")'.format(winName)], p=winName)
    cmds.scriptJob(event=["NewSceneOpened", 'cmds.deleteUI("{}")'.format(winName)], p=winName)


if __name__ == "__main__":
    SAV_makeUI()
