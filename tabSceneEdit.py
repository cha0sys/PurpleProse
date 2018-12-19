# custom widget for the scene edit tab type
from PyQt5 import QtWidgets, QtCore, QtGui
import pypandoc
import ProjectManager
import logging
logging.basicConfig(filename='PP_runtime.log',level=logging.INFO)

class tabSceneEdit (QtWidgets.QWidget):
    def __init__(self,parent,pjm=ProjectManager.ProjectManager(),sceneid=0):
        super(tabSceneEdit , self).__init__()
        logging.info("Initializing scene tab...")
        self._translate = QtCore.QCoreApplication.translate
        self.parent = parent
        self.pjm = pjm
        self.sceneid = sceneid
        self.type = 'Scene'
        self.textchanged = False
        logging.info("Setting up layout...")
        self.setupUI()
        logging.info("Loading scene %i data..." % sceneid)
        self.OpenScene()
        logging.info("Tab Ready.")

    def setupUI(self):
        self.setObjectName("tabSceneEdit_" + str(self.sceneid))
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(5, -1, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblTitle = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTitle.sizePolicy().hasHeightForWidth())
        self.lblTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.lblTitle.setFont(font)
        self.lblTitle.setWordWrap(True)
        self.lblTitle.setObjectName("lblTitle")
        self.horizontalLayout.addWidget(self.lblTitle)
        self.btnSave = QtWidgets.QCommandLinkButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSave.sizePolicy().hasHeightForWidth())
        self.btnSave.setSizePolicy(sizePolicy)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout.addWidget(self.btnSave)
        self.horizontalLayout.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.txtScene = QtWidgets.QTextEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtScene.sizePolicy().hasHeightForWidth())
        self.txtScene.setSizePolicy(sizePolicy)
        self.txtScene.setObjectName("txtScene")
        self.verticalLayout.addWidget(self.txtScene)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi()

        logging.info("Connecting signals to slots...")
        self.btnSave.clicked.connect(self.SaveScene)
        logging.info("btnSave.clicked() connected.")

        logging.info("Slots connected.")

    def retranslateUi(self):
        self.lblTitle.setText(self._translate("MainFrame", "Title"))
        self.btnSave.setText(self._translate("MainFrame", "Save Scene"))
        self.btnSave.setShortcut(self._translate("MainWindow", "Ctrl+S"))

    def SetFlag(self):
        self.textchanged = True

    def CheckScene(self):
        # Unused until Markdown parsing is implemented
        # if scene has actually been edited, then actually change things.
        # this filters out loading and re-rendering from the signal sources.
        if self.textchanged == True:
            self.UpdateScene()

    def UpdateScene(self):
        # Unused until Markdown parsing is implemented
        contents = str(self.txtScene.toPlainText())
        # convert to HTML from Markdown
        logging.info("Converting from Markdown to HTML...")
        self.textchanged = False
        pdoc_args=['--reference-links','--emoji']
        render = pypandoc.convert_text(contents,'html4',format='md', extra_args=pdoc_args)
        # convert back to plain-text Markdown
        #contents = pypandoc.convert_text(sceneText,'md',format='html')
        self.txtScene.setHtml(render)
        self.textchanged = True

    def SaveScene(self):
        logging.info("Saving scene %i." % self.sceneid)
        contents = str(self.txtScene.toPlainText())
        # convert back to plain-text Markdown
        self.textchanged = False
        #logging.info("Converting to Markdown...")
        #pdoc_args=['--reference-links','--emoji']
        #render = pypandoc.convert_text(contents,'md',format='html',extra_args=pdoc_args)
        logging.info("Sending scene contents to Project Manager.")
        #self.pjm.SaveScene(self.sceneid,render)
        self.pjm.SaveScene(self.sceneid,contents)
        #self.parent.MainWindow.setStatusTip(self._translate("MainWindow", "Saved."))
        logging.info("Scene saved.")
        self.textchanged = True

    def OpenScene(self):
        # only used on tab initialization
        # render = pypandoc.convert_text(contents,'html',format='md')
        self.textchanged = False
        logging.info("Requesting scene contents from Project Manager.")
        contents = self.pjm.OpenScene(self.sceneid)
        data = self.pjm.GetSceneData(self.sceneid)
        #logging.info("Converting from Markdown to HTML...")
        #render = pypandoc.convert_text(contents,'html4',format='md')
        logging.info("Populating textbox.")
        #self.txtScene.setHtml(render)
        self.txtScene.setText(contents)
        logging.info("Scene %i data loaded." % self.sceneid)
        logging.info("Setting title: %s" % data['title'])
        self.lblTitle.setText(QtCore.QCoreApplication.translate("MainFrame", data['title']))
        self.textchanged = True