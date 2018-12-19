# -*- coding: utf-8 -*-

# custom widget for the entity edit tab type
from PyQt5 import QtCore, QtWidgets, QtGui
import ProjectManager

import logging
logging.basicConfig(filename='PP_runtime.log',level=logging.INFO)

class tabNewProject (QtWidgets.QWidget):
    def __init__(self,parent,pjm=ProjectManager.ProjectManager(None)):
        super(tabNewProject, self).__init__()
        self.parent = parent
        self.type = 'Scene'
        logging.info("New Project tab opened.")
        self.setupUI()

    def setupUI(self):
        self.widget = QtWidgets.QWidget(self)
        self.widget.setGeometry(QtCore.QRect(10, 10, 611, 376))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblNewProject = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Lucida Sans Unicode")
        font.setPointSize(24)
        self.lblNewProject.setFont(font)
        self.lblNewProject.setAlignment(QtCore.Qt.AlignCenter)
        self.lblNewProject.setObjectName("lblNewProject")
        self.verticalLayout.addWidget(self.lblNewProject)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblPrjTitle = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lblPrjTitle.setFont(font)
        self.lblPrjTitle.setObjectName("lblPrjTitle")
        self.horizontalLayout.addWidget(self.lblPrjTitle)
        self.txtPrjTitle = QtWidgets.QLineEdit(self.widget)
        self.txtPrjTitle.setObjectName("txtPrjTitle")
        self.horizontalLayout.addWidget(self.txtPrjTitle)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.btnPrjCreate = QtWidgets.QCommandLinkButton(self.widget)
        self.btnPrjCreate.setObjectName("btnPrjCreate")
        self.verticalLayout.addWidget(self.btnPrjCreate)

        self.btnPrjCreate.clicked.connect(self.MakeProject)

    def MakeProject(self):
        logging.info("Creating new project.")
        title = str(self.txtPrjTitle.text())
        dbpath = title.replace(' ','_') + '.ppp'
        logging.info("Title: %s" % title)
        logging.info("Project DB filename: %s" % dbpath)
        self.parent.CreateProject(title,dbpath)


