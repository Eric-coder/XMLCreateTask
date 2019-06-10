# -*- encoding: utf-8 -*-
import sys
import traceback

from Qss.qss import styleData
sys.path.append("C:/cgteamwork5/bin/lib/pyside")
sys.path.append(r'C:\cgteamwork5\bin\base')
try:
    from PySide import QtGui
    from PySide import QtCore
except ImportError:
    from PySide2 import QtWidgets as QtGui
    from PySide2 import QtCore
ADMIN = [u'吴沐林',u'吕月姣',u'王茜',u'危卓文嘉',u'黄磊',u'肖丹',u'赵姗姗',u'王天祥']

def GetaccountNmae():
    import cgtw
    t_tw = cgtw.tw()
    id = t_tw.sys().get_account_id()
    t_info = t_tw.info_module("public",'account')
    filters = [["account.id",'=',id]]
    t_info.init_with_filter(filters)
    data = t_info.get(["account.name"])
    return [data[0]["account.name"]][0]

def handleError(func):
    def handle(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            title = "error"
            content = traceback.format_exc()
            QtGui.QMessageBox(QtGui.QMessageBox.Critical,
                              title, content).exec_()

    return handle


class Readxml(object):
    def __init__(self, windows):
        import xml.dom.minidom as xml
        import json as json
        import os as os
        import subprocess as subprocess
        import cgtw as cgtw
        import cv2 as cv2

        self._cgtw = cgtw
        self._xml = xml
        self._cv2 = cv2
        self._json = json
        self.t_tw = self._cgtw.tw()
        self._subprocess = subprocess
        self._windows = windows
        self._dialogWindows = DialogWindows()
        path = os.path.abspath(os.path.dirname(__file__))

        self.SHOTINPUTPOINT = "shot.begin_time"
        self.SHOTOUTPUTPOINT = "shot.end_time"
        self.OUTJSDATAPATH = path + "/js.json"

        self.shotInputList = []
        self.shotRenameInputList = []
        self.shotOutputList = []
        self.shotRenameOutputList = []
        self.shotOutputImagePath = []
        self.shotIputTimeCode = []
        self.shotOutputTimeCode = []

    def rootXml(self):
        dom = self._xml.parse(self._windows.lineEdit.text())
        root = dom.documentElement
        return root

    def getClipitemsList(self):  # 获取xml文件中的所有“clipitem”标签
        self.root = self.rootXml()
        clipitemList = self.root.getElementsByTagName("clipitem")
        return clipitemList

    def getClipitems(self, clipitemsName):  # 获取xml文件中name标签的值并分离
        self.clipitemData = clipitemsName.getElementsByTagName("name")[0]
        spliteName = self.clipitemData.firstChild.data.split("_")
        return spliteName

    def getProjectName(self):  # 得到项目名称
        projects = self._windows.lineEdit.text()
        project = projects.split("/")
        return project[-1].split("_")[0]

    def getBlues(self):  # 获取集数信息
        eps = self._windows.lineEdit.text()
        ep = eps.split("/")
        return ep[-1].split("_")[1].split(".")[0]

    def getVideosPath(self):
        path = self._windows.videoslineEite.text()
        return path

    def getImagePath(self):
        imagePath = self._windows.imageEdit.text()
        return imagePath

    def getVideoFrames(self, videosPath):  # 获取所截取视频的总帧数
        vc = self._cv2.VideoCapture(videosPath)  # 读入视频文件
        if vc.isOpened():  # 判断是否正常打开
            print 'Open successful'
        else:
            print 'Open fail'
        frames_num = vc.get(7)  # 获取视频总帧数
        print "The frames of he video is %s" % (frames_num)
        return frames_num

    def compareFrames(self, videsPath):  # 比较视频总帧数与xml入点的大小
        countFrames = self.getVideoFrames(videsPath)
        if countFrames > int(self.shotInputList[0]):
            return True
        else:
            return False

    def compareEndFrames(self, videosPath):
        coutFrames = self.getVideoFrames(videosPath)
        if coutFrames < int(self.shotOutputList[-1]) and coutFrames < int(self.shotRenameOutputList[-1]):
            return False
        else:
            return True

    def setInputFrames(self):  # 设置入点值为1，并且重置入点帧和出点帧
        shotFramesList = []
        clipitemList = self.getClipitemsList()
        for ii in range(len(clipitemList)):
            shotFramesList.append(self.getShotFrames(clipitemList[ii]) - 2)
        for ii in range(len(self.shotInputList)):
            if ii == 0:
                self.shotRenameInputList.append(ii + 1)
            else:
                self.shotRenameInputList.append(
                    (self.shotRenameInputList[-1]) + int(shotFramesList[ii - 1]) + 1)
            if ii == 0:
                self.shotRenameOutputList.append(
                    ii + 1 + int(shotFramesList[ii]))
            else:
                self.shotRenameOutputList.append(
                    self.shotRenameOutputList[-1] + int(shotFramesList[ii]) + 1)

    # filename为xml获取的视频路径，outpath为输出图片保存路径
    def start_thumbnails(self, filePath, savePath, list):
        vc = self._cv2.VideoCapture(filePath)
        if vc.isOpened():
            rval, frame = vc.read()
            print "Open successful!"
        else:
            rval = False
        c = 1
        while rval:
            rval, frame = vc.read()
            for ii in range(len(list)):
                if (c == int(list[ii])):
                    self._cv2.imwrite("%s%s%s%s%s" % (
                        savePath, "/", self.getBlues(), str(list[ii]), ".jpg"), frame)
                    self.shotOutputImagePath.append(
                        "%s%s%s%s%s" % (savePath, "/", self.getBlues(), str(list[ii]), ".jpg"))
                    print 'Save successful'
                    break

            self._windows.progressBar.setValue(
                5 + (75 / float(self.shotInputList[-1])) * c)
            app.processEvents()
            c = c + 1

            self._cv2.waitKey(1)
            if (c == max(list) + 1):
                break
        vc.release()
        print "end"

    # filename为xml获取的视频路径，outpath为输出图片保存路径
    def middle_thumbnails(self, filePath, savePath, listInput, listOutput):
        countFramesList = []
        countRenameList = []
        vc = self._cv2.VideoCapture(filePath)
        if vc.isOpened():
            rval, frame = vc.read()
            print "Open successful!"
        else:
            rval = False
        for each in range(len(listInput)):
            countFramesList.append(
                (int(self.shotInputList[each]) + int(self.shotOutputList[each])) // 2)
            countRenameList.append(
                (int(listInput[each]) + int(listOutput[each])) // 2)
        c = 1
        while rval:
            rval, frame = vc.read()
            for ii in range(len(countRenameList)):

                if (c == countRenameList[ii]):
                    self._cv2.imwrite("%s%s%s%s%s" % (
                        savePath, "/", self.getBlues(), str(countRenameList[ii]), ".jpg"), frame)
                    self.shotOutputImagePath.append(
                        "%s%s%s%s%s" % (savePath, "/", self.getBlues(), str(countRenameList[ii]), ".jpg"))
                    print 'Save successful'
                    break
            self._windows.progressBar.setValue(
                5 + (75 / float(countFramesList[-1])) * c)
            app.processEvents()
            c = c + 1
            self._cv2.waitKey(1)
            if (c == max(countRenameList) + 1):
                break
        vc.release()

    # filename为xml获取的视频路径，outpath为输出图片保存路径
    def end_thumbnails(self, filePath, savePath, list):

        vc = self._cv2.VideoCapture(filePath)
        if vc.isOpened():
            rval, frame = vc.read()
            print "Open successful!"
        else:
            rval = False

        c = 1
        while rval:
            rval, frame = vc.read()
            for ii in range(len(list)):
                if list[ii] == list[-1]:
                    if c == int(list[ii] - 1):
                        self._cv2.imwrite("%s%s%s%s%s" % (
                            savePath, "/", self.getBlues(), str(list[ii]), ".jpg"), frame)
                        self.shotOutputImagePath.append(
                            "%s%s%s%s%s" % (savePath, "/", self.getBlues(), str(list[ii]), ".jpg"))
                        print 'Save successful'
                        break

                elif (c == int(list[ii])):
                    self._cv2.imwrite("%s%s%s%s%s" % (
                        savePath, "/", self.getBlues(), str(list[ii]), ".jpg"), frame)
                    self.shotOutputImagePath.append(
                        "%s%s%s%s%s" % (savePath, "/", self.getBlues(), str(list[ii]), ".jpg"))
                    print 'Save successful'
                    break
            self._windows.progressBar.setValue(
                5 + (75 / float(self.shotOutputList[-1])) * c)
            app.processEvents()
            c = c + 1
            self._cv2.waitKey(1)
            if (c == max(list) + 1):
                break
        vc.release()

        # return "%s%s%s%s%s"%(savePath,"/",self.getBlues(),str(endFrames),".jpg")

    def getFrames(self, clipitemName):  # 获取开始帧
        startFrame = clipitemName.getElementsByTagName("start")[
            0].firstChild.data
        return int(startFrame)

    def getTimeBase(self, clipitemName):  # 获取timeBase的数据
        timeBase = clipitemName.getElementsByTagName("timebase")[
            0].firstChild.data
        return timeBase

    def framesConver(self, frames, clipitemName):  # 将帧数转化为时间码
        timeBase = int(self.getTimeBase(clipitemName))
        if frames == 1:
            frame = frames % timeBase
            if frame < 10:
                frame = str(0) + str(frame)
            second = (frames / timeBase) % 60
            if second < 10:
                second = str(0) + str(second)
            min = ((frames / timeBase) / 60) % 60
            if min < 10:
                min = str(0) + str(min)
            hour = ((frames / timeBase) / 60) / 60
            time = str(hour) + str(min) + str(second) + str(frame)
        else:
            frame = frames % timeBase
            if frame < 10:
                frame = str(0) + str(frame)
            second = (frames / timeBase) % 60
            if second < 10:
                second = str(0) + str(second)
            min = ((frames / timeBase) / 60) % 60
            if min < 10:
                min = str(0) + str(min)
            hour = ((frames / timeBase) / 60) / 60
            time = str(hour) + str(min) + str(second) + str(frame)

        return time.zfill(8)

    def framesConverEnd(self, frames, clipitemName):
        timeBase = int(self.getTimeBase(clipitemName))
        frame = frames % timeBase
        if frame < 10:
            frame = str(0) + str(frame)
        second = (frames / timeBase) % 60
        if second < 10:
            second = str(0) + str(second)
        min = ((frames / timeBase) / 60) % 60
        if min < 10:
            min = str(0) + str(min)
        hour = ((frames / timeBase) / 60) / 60
        time = str(hour) + str(min) + str(second) + str(frame)

        return time.zfill(8)

    def getEndFrames(self, clipitemName):  # 获取结束帧
        endFrame = clipitemName.getElementsByTagName("end")[0].firstChild.data

        return int(endFrame)

    def getShotFrames(self, clipitemName):  # 获取镜头帧数
        startFrames = clipitemName.getElementsByTagName("in")[
            0].firstChild.data
        endFrames = clipitemName.getElementsByTagName("out")[0].firstChild.data
        return (int(endFrames) - int(startFrames) + 1)

    def writeJsonDatas(self):  # 将数据存储到json文件中
        shotNumList = []
        shotFramesList = []
        bluesData = self.getBlues()
        clipitemList = self.getClipitemsList()
        for ii in range(len(clipitemList)):
            self.shotInputList.append(self.getFrames(clipitemList[ii]))
            self.shotOutputList.append(self.getEndFrames(clipitemList[ii]))
            self.shotIputTimeCode.append(self.framesConver(
                self.getFrames(clipitemList[ii]), clipitemList[ii]))
        for jj in range(len(self.shotOutputList)):
            self.shotOutputList[jj] = self.shotOutputList[jj]-1

        for jj in range(len(self.shotOutputList)):
            self.shotOutputTimeCode.append(self.framesConverEnd(
                self.shotOutputList[jj], clipitemList[jj]))
            shotNumList.append(self.getFrames(clipitemList[jj]))
            self._windows.progressBar.setValue(
                0 + (5 / float(len(clipitemList))) * (jj + 1))
            app.processEvents()
        shotFramesList = list(set(shotFramesList))
        for ii in range(len(self.shotOutputList)):
            shotFramesList.append(
                int(self.shotOutputList[ii]) - int(self.shotInputList[ii]) + 1)
        #print self.shotInputList
        #print self.shotOutputList
        #print shotFramesList
        #print self.shotIputTimeCode
        #print self.shotOutputTimeCode
        if self._windows.inputChackBox.isChecked() == True:
            if self.compareFrames(self.setVideoPath) == True:

                self.start_thumbnails(self.getVideosPath(
                ), self.getImagePath(), self.shotInputList)
            else:
                self.setInputFrames()
                self.start_thumbnails(self.getVideosPath(
                ), self.getImagePath(), self.shotRenameInputList)

        if self._windows.middleChackBox.isChecked() == True:
            if self.compareFrames(self.setVideoPath) == True:

                self.middle_thumbnails(self.getVideosPath(), self.getImagePath(), self.shotInputList,
                                       self.shotOutputList)

            else:
                self.setInputFrames()
                if self.compareEndFrames(self.setVideoPath) == False:
                    self._dialogWindows.show()
                else:

                    self.middle_thumbnails(self.getVideosPath(), self.getImagePath(), self.shotRenameInputList,
                                           self.shotRenameOutputList)
        if self._windows.outputChackBox.isChecked() == True:
            if self.compareFrames(self.setVideoPath) == True:
                self.end_thumbnails(self.getVideosPath(),
                                    self.getImagePath(), self.shotOutputList)
            else:
                self.setInputFrames()
                if self.compareEndFrames(self.setVideoPath) == False:
                    self._dialogWindows.show()
                else:
                    self.end_thumbnails(self.getVideosPath(
                    ), self.getImagePath(), self.shotRenameOutputList)

        self.shotNums = self._windows.shotEdit.text()
        self.shotNums = int(self.shotNums)
        for ii in range(len(shotNumList)):
            if ii + self.shotNums <= 9:
                shotNumList[ii] = "%s%s" % ("C000", str(self.shotNums + ii))
            elif ii + self.shotNums > 9 and ii + self.shotNums < 100:
                shotNumList[ii] = "%s%s" % ("C00", str(self.shotNums + ii))
            elif ii + self.shotNums >= 100 and ii + self.shotNums < 1000:
                shotNumList[ii] = "%s%s" % ("C0", str(self.shotNums + ii))
            else:
                shotNumList[ii] = "%s%s" % ("C", str(self.shotNums + ii))
        #print shotNumList
        dict_all = {}
        dirt = {}

        for ii in range(len(shotNumList)):
            dict_all[shotNumList[ii]] = {"shotInput": self.shotIputTimeCode[ii],
                                         "shotOutput": self.shotOutputTimeCode[ii], "shotFrames": shotFramesList[ii],
                                         "shotOutImagePath": self.shotOutputImagePath[ii]}

        dirt["bluesDatas"] = {bluesData: {"shotNum": dict_all}}
        with open(self.OUTJSDATAPATH, "w") as file:
            end = self._json.dumps(dirt, indent=4)
            file.write(end)

    def readJsonDatas(self, jspath):  # 读取json中的数据
        self.writeJsonDatas()

        with open(jspath, "r") as file:
            dict_all = self._json.loads(file.read())

        return dict_all

    def getProjectDatabase(self, project):  # 得到项目的数据库并过滤有用的信息
        t_info = self.t_tw.info_module("public", "project")
        filters = [
            ["project.code", "=", project]
        ]
        t_info.init_with_filter(filters)
        fields = ["project.database"]
		
        database = t_info.get(fields)[0]['project.database']
        return database

    def createShot(self, project, data):  # 创建项目的镜头需要手动创建project

        projectDb = self.getProjectDatabase(project)
        t_info = self.t_tw.info_module(projectDb, "shot")
        t_info.create(data)

    def setImage(self, project, field, shotNum, imagePath):
        projectDb = self.getProjectDatabase(project)

        t_info = self.t_tw.info_module(projectDb, "shot")
        filters = [
            ["eps.eps_name", "=", field],
            ["shot.shot", "=", shotNum]
        ]
        t_info.init_with_filter(filters)

        t_info.set_image("shot.image", imagePath.replace("\\", "/"))

    def submitDatas(self, projectName):
        shoutFrames = []
        shoutinput = []
        shoutOutput = []
        shoutImagesPath = []
        dict_all = self.readJsonDatas(self.OUTJSDATAPATH)
        ep = dict_all["bluesDatas"].keys()[0]
        shoutNum = dict_all["bluesDatas"][ep]["shotNum"].keys()
        for ii in shoutNum:
            shoutFrames.append(dict_all["bluesDatas"]
                               [ep]["shotNum"][ii]["shotFrames"])
            shoutinput.append(dict_all["bluesDatas"]
                              [ep]["shotNum"][ii]["shotInput"])
            shoutOutput.append(dict_all["bluesDatas"]
                               [ep]["shotNum"][ii]["shotOutput"])
            shoutImagesPath.append(
                dict_all["bluesDatas"][ep]["shotNum"][ii]["shotOutImagePath"])

        for jj in range(len(shoutNum)):
            self.createShot(projectName, {"eps.eps_name": ep, "shot.shot": shoutNum[jj], "shot.frame": shoutFrames[jj],
                                          self.SHOTINPUTPOINT: shoutinput[jj], self.SHOTOUTPUTPOINT: shoutOutput[jj]})
            self.setImage(projectName, ep, shoutNum[jj], shoutImagesPath[jj])
            self._windows.progressBar.setValue(
                80 + (20 / float(len(shoutNum))) * (jj + 1))
            app.processEvents()

    @handleError
    def okButton(self):
        self.setProjectName = self._windows.lineEdit.text()
        self.setImagePath = self._windows.imageEdit.text()
        self.setVideoPath = self._windows.videoslineEite.text()
        self.shotNumsEdit = self._windows.shotEdit.text()
        if self.setVideoPath == '':
            name = u"请拖入视频文件"
            QtGui.QMessageBox.warning(self._windows, "Message", name)
            #self.myQMessageBox = MyQMessageBox(name)

        if self.setProjectName == '':
            name = u"请拖入XML文件"
            QtGui.QMessageBox.warning(self._windows, "Message", name)
            #self.myQMessageBox = MyQMessageBox(name)

        if self.setImagePath == '':
            name = u"请拖入缩略图文件夹路径"
            QtGui.QMessageBox.warning(self._windows, "Message", name)
            #self.myQMessageBox = MyQMessageBox(name)

        if self.shotNumsEdit == '':
            name = u"请输入开始镜头号"
            QtGui.QMessageBox.warning(self._windows, "Message", name)
            #self.myQMessageBox = MyQMessageBox(name)

        if self._windows.inputChackBox.isChecked() == False and self._windows.middleChackBox.isChecked() == False and self._windows.outputChackBox.isChecked() == False:
            name = u"请选择截图帧按钮"
            QtGui.QMessageBox.warning(self._windows, "Message", name)
            # self.myQMessageBox = MyQMessageBox(name)
            # self.myQMessageBox.resize(250, 150)

        self.projectName = self.getProjectName()
        self._windows.okBtn.setHidden(True)

        if self._windows.timer.isActive():
            self._windows.timer.stop()
        else:
            self.submitDatas(self.projectName)
            name = u"数据成功上传到cgteamWork"
            QtGui.QMessageBox.about(self._windows, "Message", name)
            #self.myQMessageBox = MyQMessageBox(name)

    def cancleButton(self):
        self._windows.close()
        exit(0)
class Windows(QtGui.QWidget):  # 界面的Class
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self._myLineEdit = MyLineEdit()
        self._mainUi()

    def _mainUi(self):
        self.setWindowTitle(u"cgteamWork上传镜头信息")
        self._center = Pyside_center()
        self.resize(500, 300)

        self.label = QtGui.QLabel(u"xml 文件 路径")
        self.imagelabel = QtGui.QLabel(u"缩略图输出路径")
        self.shotsLabel = QtGui.QLabel(u"开始镜头号输入")
        self.videosName = QtGui.QLabel(u"拖入的视频文件")

        self.videoslineEite = QtGui.QLineEdit()
        self.videoslineEite = MyLineEdit()
        self.lineEdit = QtGui.QLineEdit()
        self.lineEdit = MyLineEdit()
        self.imageEdit = QtGui.QLineEdit()
        self.imageEdit.setDragEnabled(True)
        self.imageEdit = MyLineEdit()
        self.projectEdit = QtGui.QLineEdit()
        self.shotEdit = QtGui.QLineEdit("1")
        self.shotEdit.setValidator(QtGui.QIntValidator())

        self.inputChackBox = QtGui.QRadioButton(u"入点帧图片    ")
        self.middleChackBox = QtGui.QRadioButton(u"中间帧图片   ")
        self.middleChackBox.setChecked(True)
        self.outputChackBox = QtGui.QRadioButton(u"出点帧图片   ")

        self.progressBar = QtGui.QProgressBar()
        #self.progressBar.setTextVisible(False)
        self.progressBar.setValue(0)
        self.progressBar.setMaximumHeight(10)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.timer = QtCore.QBasicTimer()
        self.timer.start(100, self)

        self.okBtn = QtGui.QPushButton(u"确定")
        self.cancleBtn = QtGui.QPushButton(u"取消")

        self.formLayout = QtGui.QFormLayout()
        self.formLayout.addRow(self.videosName, self.videoslineEite)
        self.formLayout.addRow(self.label, self.lineEdit)
        self.formLayout.addRow(self.imagelabel, self.imageEdit)
        self.formLayout.addRow(self.shotsLabel, self.shotEdit)
        self.formLayout.addWidget(self.inputChackBox)
        self.formLayout.addWidget(self.middleChackBox)
        self.formLayout.addWidget(self.outputChackBox)

        self.frameLayout = QtGui.QHBoxLayout()
        self.frameLayout.addWidget(self.inputChackBox)
        self.frameLayout.addWidget(self.middleChackBox)
        self.frameLayout.addWidget(self.outputChackBox)

        self.progressBarLayout = QtGui.QHBoxLayout()
        self.progressBarLayout.addWidget(self.progressBar)

        self.BtnLayout = QtGui.QHBoxLayout()
        self.BtnLayout.addWidget(self.okBtn)
        self.BtnLayout.addWidget(self.cancleBtn)

        self.laterLayout = QtGui.QVBoxLayout()
        self.laterLayout.addLayout(self.formLayout)
        self.laterLayout.addLayout(self.BtnLayout)
        self.laterLayout.addLayout(self.progressBarLayout)

        ############################类的实例化##############################
        self._readxml = Readxml(self)
        ############################创建信号连接#############################
        self.okBtn.clicked.connect(self._readxml.okButton)
        self.timer = QtCore.QBasicTimer()
        self.step = 0
        self.cancleBtn.clicked.connect(self._readxml.cancleButton)

        self.setLayout(self.laterLayout)


class Dialog(QtGui.QWidget):
    def __init__(self, a, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.name = a
        self.setWindowTitle(u'信息弹窗')
        self._center = Pyside_center()
        self.resize(250, 150)

        self.label = QtGui.QLabel()
        self.label.setText(u"警告!!!\n"+self.name)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLayout = QtGui.QHBoxLayout()
        self.labelLayout.addWidget(self.label)

        self.setLayout(self.labelLayout)


class DialogSuccess(QtGui.QWidget):
    def __init__(self, a, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.name = a
        self.setWindowTitle(u'信息弹窗')
        #self._center = Pyside_center()
        #self._center = Parent_center()
        self.resize(250, 150)
        self.label = QtGui.QLabel()
        self.label.setText(self.name)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLayout = QtGui.QHBoxLayout()
        self.labelLayout.addWidget(self.label)

        self.setLayout(self.labelLayout)


class DialogWindows(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setWindowTitle(u'信息弹窗')
        self.label = QtGui.QLabel()
        self.label.setText(u"警告\n"+u"视频帧数太少请拖如正确视频")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLayout = QtGui.QHBoxLayout()
        self.labelLayout.addWidget(self.label)
        self.setLayout(self.labelLayout)


class Pyside_center(QtGui.QWidget):
    def __init__(self):
        super(Pyside_center, self).__init__()
        self.initUI()

    def initUI(self):
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class MyLineEdit(QtGui.QLineEdit):
    def __init__(self, parent=None):
        super(MyLineEdit, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        st = str(event.mimeData().urls())
        st = st.replace('[PySide.QtCore.QUrl', "")
        st = st.replace("'), ", ",")
        st = st.replace("('file:///", "")
        st = st.replace("')]", "")
        self.setText(st)


class MyQMessageBox(QtGui.QMessageBox):
    def __init__(self, name, parent=None):
        QtGui.QMessageBox.__init__(self, parent)
        self.name = name
        self._windows = Windows(self)
        self.initUi()

    def initUi(self):
        self.resize(200, 300)
        self.showAbout()

    def showAbout(self):

        QtGui.QMessageBox.about(self._windows, "Message", self.name)


if __name__ == "__main__":
    app = QtGui.QApplication.instance()
    if app == None:
        app = QtGui.QApplication(sys.argv)
    if GetaccountNmae() not in ADMIN:
        admin = QtGui.QMessageBox
        msg_box = admin(admin.Warning, u"提示!", u"您没有权限!", admin.Yes)
        msg_box.exec_()
    else:
        windows = Windows()
        windows.setStyleSheet(styleData)
        windows.show()
        app.exec_()
