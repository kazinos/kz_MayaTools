# -*- coding: utf-8 -*-
"""kz_optionVarReader.py

git:https://github.com/kazinos/kz_MayaTools.git

codeing by kazinos
MayaVer Maya2020.4
2022/08/18 kazinos 制作開始
2022/08/22 kazinos make git repository and commit.

plan:
    オプションバーの管理サポートツール
    1.ok オプションバーの一覧を表示
    2.ok iv ,fv ,svで表示内容を指定できるようにする（絞込み機能 narrowing）
    3.ok 索引機能を実装する
    4.ok 選択したoptionVarの内容を確認できるようにする
    5.ok 選択したoptionVarの削除ができるようにする
        
issue:
  
"""
# ------------------------------------------------------------------------------
from __future__ import absolute_import ,division ,generators ,print_function ,unicode_literals
try:
    from future_builtins import *
except:
    pass
import sys
sys.dont_write_bytecode = True
# ------------------------------------------------------------------------------
from maya import cmds
import re
   
def selectListItem():
    """optionVar選択時の処理
    """
    selItem = cmds.textScrollList("optionVerList" ,q=True ,selectItem=True)[0]
    selInfo = cmds.optionVar(q=selItem)
    
    # 変数名 表示処理 
    cmds.textField("optionVerName" ,e=True ,text=selItem)
    
    # 値 表示処理
    if(type(selInfo)==list):
        cmds.textScrollList("selOptionVerInfo" ,e=True ,removeAll=True 
                            ,append="{}".format(selInfo))
        return
    
    cmds.textScrollList("selOptionVerInfo" ,e=True ,removeAll=True ,append=[selInfo])

def deleteItem():
    """選択対象のoptionVarの削除処理
    """
    # 選択されていない場合：return
    if(cmds.textScrollList("optionVerList" ,q=True ,numberOfSelectedItems=True)==0):return
    
    # 選択物がoptionVar内に存在していない場合：return
    if(not cmds.optionVar(exists=cmds.textScrollList("optionVerList" ,q=True ,selectItem=True)[0])):
        cmds.textScrollList("selOptionVerInfo" ,e=True ,removeAll=True 
                            ,append=u"Selection was not found in OptionVar.\nPlease refresh the list.")
        return
    
    # 確認ダイアログ表示
    selItem = cmds.textScrollList("optionVerList" ,q=True ,selectItem=True)[0]
    checklog = cmds.confirmDialog( title=u'確認' 
                                ,message='Do you want to delete optionVar?\n{}'.format(selItem)
                                ,button=['Yes','No'] 
                                ,defaultButton='Yes' 
                                ,cancelButton='No' 
                                ,dismissString='No')
    
    # 削除処理
    if(checklog=="Yes"):
        cmds.optionVar(remove=selItem)
        makeList() 
        cmds.textField("optionVerName" ,e=True ,text=u"")
        cmds.textScrollList("selOptionVerInfo" ,e=True ,removeAll=True ,append=u"")
    
def makeList():
    """optionVar一覧作成処理
    """
    optionVerList = cmds.optionVar(list=True)
    findType = cmds.optionMenu("findType" ,q=True ,value=True)
    findText = cmds.textField("searchField" ,q=True ,text=True)
    
    # 正規表現 "+","*","\" のみの場合のエラー回避処理
    if(findText in ["+","*","\\"]):
        cmds.textScrollList("selOptionVerInfo" ,e=True ,removeAll=True 
                    ,append=u'The + , * , and \\ are special characters.\nThey cannot be used by using them alone.')
        return
    
    # データ型の設定
    seltype=""
    if(not findType=="All"):
        if findType=="string Value":seltype= unicode
        if findType=="int Value"   :seltype= int
        if findType=="float Value" :seltype= float
        if findType=="List Value"  :seltype= list
    
    tmpList=[]
    for tmp in optionVerList:
        # 検索での絞り込み
        if(not re.search(r"{}".format(findText) ,tmp)):continue
        tmpValue = cmds.optionVar(q=tmp)
        
        # typeでの絞り込み
        if(not findType=="All" and not type(tmpValue)==seltype):continue
        tmpList.append(tmp)            
    optionVerList = tmpList
    cmds.textScrollList("optionVerList" ,e=True ,append=optionVerList ,removeAll=True)

# UI設定----------------------------------------------
def makeUI():
    winName="OptionVarReader"
    # ウィンドウが重複した場合の処理
    if cmds.window(winName ,q = True ,ex = True ,resizeToFitChildren=True):
        cmds.deleteUI(winName)
    
    # Window作成
    window = cmds.window(winName ,title=u"OptionVar Reader" 
                         ,s = True ,mxb = False ,mnb = False)
    
    # レイアウト formLayout Ver
    cmds.formLayout("form" ,numberOfDivisions=100)
    cmds.text("titleText" ,label=u"optionVar List" ,w=100 ,h=20) 
    cmds.button("makeListBtn" ,label=u'Create List' 
                ,command=lambda *args:makeList() ,w=100 ,h=30)
    
    # 左側
    # 絞り込み
    cmds.optionMenu("findType" ,label='Find Type' ,w=220)
    cmds.menuItem( label='All' )
    cmds.menuItem( label='string Value')
    cmds.menuItem( label='int Value')
    cmds.menuItem( label='float Value')
    cmds.menuItem( label='List Value')
    
    # 検索
    cmds.text("searchTitle" ,label="search" ,w=56)
    cmds.textField("searchField" ,text="" ,w=116)
    cmds.button("clearSearchField" ,label="clear" ,h=20 
                ,c='cmds.textField("searchField" ,e=True ,text="")')
    
    # optionVar一覧
    cmds.textScrollList("optionVerList" ,w=220 
                        ,allowMultiSelection=False 
                        ,append=[u"Please make a list"] 
                        ,selectCommand = lambda *args:selectListItem())     
    
    # 削除ボタン
    cmds.button("deleleButton" ,label="Delete" ,w=220 ,c=lambda *args:deleteItem())
    
    # 右側
    # 選択optionVarの名前
    cmds.textField("optionVerName" ,h=48 ,text=u"OptionVar Name")   
    
    # 選択optionVarの内容
    cmds.textScrollList("selOptionVerInfo" ,allowMultiSelection=True 
                        ,append=[u"Infomation"])   
    
    # 基準点と配置の設定
    cmds.formLayout("form" ,e=True
                   ,attachForm=[("titleText"        ,'top'   ,5 ) 
                               ,("titleText"        ,'left'  ,5 ) 
                               ,("titleText"        ,'right' ,5 ) 
                               ,("makeListBtn"      ,'top'   ,5 ) 
                               ,("makeListBtn"      ,'left'  ,5 ) 
                               ,("makeListBtn"      ,'right' ,5 ) 
                               ,("findType"         ,'top'   ,5 ) 
                               ,("findType"         ,'top'   ,5 ) 
                               ,("findType"         ,'left'  ,5 ) 
                               ,("searchTitle"      ,'top'   ,5 ) 
                               ,("searchTitle"      ,'left'  ,5 ) 
                               ,("searchField"      ,'top'   ,5 ) 
                               ,("searchField"      ,'left'  ,5 ) 
                               ,("clearSearchField" ,'top'   ,5 ) 
                               ,("clearSearchField" ,'left'  ,5 ) 
                               ,("optionVerList"    ,'top'   ,5 ) 
                               ,("optionVerList"    ,'left'  ,5 ) 
                               ,("deleleButton"     ,'left'  ,5 ) 
                               ,("deleleButton"     ,'bottom',5 ) 
                               ,("optionVerName"    ,'top'   ,5 ) 
                               ,("optionVerName"    ,'right' ,5 ) 
                               ,("selOptionVerInfo" ,'top'   ,5 ) 
                               ,("selOptionVerInfo" ,'bottom',5 ) 
                               ,("selOptionVerInfo" ,'right' ,5 )]
               ,attachControl=[ ("makeListBtn"      ,'top'   ,5 ,"titleText")
                               ,("makeListBtn"      ,'top'   ,5 ,"titleText")
                               ,("findType"         ,'top'   ,5 ,"makeListBtn")
                               ,("searchTitle"      ,'top'   ,5 ,"findType")
                               ,("searchField"      ,'top'   ,5 ,"findType")
                               ,("searchField"      ,'left'  ,5 ,"searchTitle")
                               ,("clearSearchField" ,'top'   ,5 ,"findType")
                               ,("clearSearchField" ,'left'  ,5 ,"searchField")
                               ,("optionVerList"    ,'top'   ,5 ,"searchField")
                               ,("optionVerList"    ,'bottom',5 ,"deleleButton")
                               ,("optionVerName"    ,'top'   ,5 ,"makeListBtn")
                               ,("optionVerName"    ,'left'  ,5 ,"findType")
                               ,("selOptionVerInfo" ,'top'   ,5 ,"optionVerName")
                               ,("selOptionVerInfo" ,'left'  ,5 ,"optionVerList")
                                ])   
    cmds.showWindow(window)
    cmds.window(winName ,e=True ,widthHeight=(400 ,300) ,sizeable=True)

    # 新規シーンかシーンを開いた時にメニューを閉じる
    cmds.scriptJob(event = ['SceneOpened'    ,'cmds.deleteUI("{}")'.format(winName)] ,p = winName)
    cmds.scriptJob(event = ['NewSceneOpened' ,'cmds.deleteUI("{}")'.format(winName)] ,p = winName)

makeUI()