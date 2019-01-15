import sublime
import sublime_plugin
import os
import subprocess
import re

localFile = remoteFile = ""
localPath = remotePath = ""
ftpServer = ftpUser = ""
bcompare = ""

def settings():
    return sublime.load_settings('RemoteDiff-BCompare.sublime-settings')

def plugin_loaded() -> None:
    global localPath, remotePath
    global ftpServer, ftpUser, bcompare
    localPath = formatPath(settings().get("local_path"))
    remotePath = formatPath(settings().get("remote_path"))
    ftpServer = settings().get("ftp_server")
    ftpUser = settings().get("ftp_user")
    bcompare = settings().get("bcomapre")

def formatPath(path):
    str = os.path.normpath(path)
    return str.replace("\\", "/")

def cmdBuild():
    global localFile
    global remoteFile
    if os.path.exists(localPath) == False:
        sublime.error_message("Could not find local folder:"+localPath)
        return ""
    fileName = re.sub(localPath, "", formatPath(localFile))
    remoteFile = 'ftp://%s@%s/%s%s'%(ftpUser, ftpServer, remotePath, fileName)
    localFile = formatPath(localFile)
    cmd = '%s "%s" "%s"' % (bcompare, localFile, remoteFile)
    return cmd

class RemoteDiffBcompareCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        if os.path.exists(bcompare):
            cmd = cmdBuild()
            subprocess.Popen(cmd)
            return
        else:
            sublime.error_message('Could not find Beyond Compare')
            return

class eventListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        global localFile
        localFile = view.file_name()
