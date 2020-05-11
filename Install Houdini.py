# -*- coling: utf-8 -*-
import os,sys
from Deadline.Scripting import *
import DeadlineUI.Controls.Scripting.DeadlineScriptDialog  as D
import DeadlineUI

H18Dir = "Z:/Learn_houdini/houdini18.0/"
CopyExe = r"""
Execute cmd /c C:/"Program Files"/Thinkbox/Deadline7/bin/dpython.exe -c "import os;zf = open('{exe}','rb');wf = open(os.path.join(os.getenv('TEMP').replace('\\','/') +'/'+'{name}'),'wb');wf.write(zf.read());zf.close();wf.close()"
"""
InstallCMD = r"""
Execute cmd /c %TEMP%/{name} /S /MainApp=Yes /InstallDir='C:\Program Files\Side Effects Software\Houdini {versions}\' /AcceptEula=yes /ApprenticeLicensing=Yes /DesktopIcon=Yes /FileAssociations=No /HoudiniServer=Yes /HQueueServer=No /EngineMaya=No /HQueueClient=No /IndustryFileAssociations=No /LicenseServer= 130server-PC /Registry=No /StartMenu=Side Effects Software
"""
copyDLL = r"""
Execute cmd /c C:/"Program Files"/Thinkbox/Deadline7/bin/dpython.exe -c "import os;zf = open('z:/Learn_houdini/houdini18.0/H18CarkDLL/zlib1.dll','rb');zf1 = open('z:/Learn_houdini/houdini18.0/H18CarkDLL/zlib1_zzz.dll','rb');wf = open('C:/Program Files/Side Effects Software/Houdini {versions}/bin/zlib1.dll','wb');wf1 = open('C:/Program Files/Side Effects Software/Houdini {versions}/bin/zlib1_zzz.dll','wb');wf.write(zf.read());wf1.write(zf1.read());zf.close();wf.close();zf1.close();wf1.close()"
"""

text = []


Command = None
scriptDialog = None
def __main__():
    exe,name = getHouAPK(H18Dir)
    showMessage("Do you install {} ?".format(exe[0]))

def getHouAPK(path):
    houApkPath = []
    name =[]
    for fileName in os.listdir(path):
        if fileName[-3:] == "exe" and "houdini" in fileName:
            houApkPath.append(os.path.join(path,fileName))
            name.append(fileName)
    return houApkPath , name

def showMessage(text = None):
    global scriptDialog
    scriptDialog = D.DeadlineScriptDialog() 
    scriptDialog.SetSize( 450, 68 )
    scriptDialog.AllowResizingDialog( False )
    scriptDialog.SetTitle(r"Selecte The Houdini Installation package")
    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid( "NameLabel", "LabelControl",text, 0, 0, "The name of the Windows Service to start or stop.", False )
    scriptDialog.EndGrid()
    scriptDialog.AddGrid()
    scriptDialog.AddHorizontalSpacerToGrid( "DummyLabel", 0, 0 )
    ok = scriptDialog.AddControlToGrid('ok',"ButtonControl",'Yes',0,1,'Install')
    ok.ValueModified.connect(OkButtonPressed)
    cancel = scriptDialog.AddControlToGrid("Cancel", "ButtonControl", "Cancel", 0, 2,"Not Install" )
    cancel.ValueModified.connect(cancelButtonPressed)
    shooes = scriptDialog.AddControlToGrid("Other", "ButtonControl", "Other", 0, 3,"Selecte Other" )
    shooes.ValueModified.connect(seleteFile)
    scriptDialog.EndGrid()
    scriptDialog.ShowDialog( True )
 
def seleteFile( *args ):
    global scriptDialog
    exe = scriptDialog.ShowOpenFileBrowser(H18Dir,"App File (houdini*.exe*)")
    name = exe.split('/')[-1]
    scriptDialog.ShowMessageBox( "install {}".format(name),'ok')
    execSlave(path = exe,name = name)

def OkButtonPressed():
    exe,name = getHouAPK(H18Dir)
    execSlave(path = exe[0],name = name[0])

def cancelButtonPressed( *args ):
    global scriptDialog
    scriptDialog.CloseDialog()

def execSlave( **args ):
    global scriptDialog
    exe = args['path']
    name = args['name']
    slaves = SlaveUtils.GetSelectedSlaveNames()
    for slave in slaves:
        SlaveUtils.SendRemoteCommandWithResults(slave,CopyExe.format(exe = exe , name = name))
        SlaveUtils.SendRemoteCommandWithResults(slave,InstallCMD.format(name = name , versions = name.split('-')[1]))
        if name.split('-')[1].split('.')[0]+'.'+name.split('-')[1].split('.')[1] == "18.0":
            SlaveUtils.SendRemoteCommandWithResults(slave,copyDLL.format(versions = name.split('-')[1]))
        SlaveUtils.SendRemoteCommandWithResults(slave,"Execute cmd /c C:\Windows\System32\hserver.exe -S 130server-PC")
    scriptDialog.CloseDialog()
