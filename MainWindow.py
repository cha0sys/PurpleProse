# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
# Initially created by: PyQt5 UI code generator 5.11.3


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import ProjectManager
import tabSceneEdit
import tabEntityEdit
import tabNewProject
import LinkDialog
import logging
logging.basicConfig(filename='PP_runtime.log',level=logging.INFO)

class Ui_MainWindow(object):
    pjm = None
    lastTarget = None
    lastEntity = None

    def __init__(self,MainWindow):
        super(Ui_MainWindow, self).__init__()
        logging.info("Initializing...")
        self.pjm = ProjectManager.ProjectManager(self)
        self.MainWindow = MainWindow
        logging.info("ProjectManager created.")

    def setupUi(self):
        logging.info("Creating main window...")
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(1120, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainWindow.sizePolicy().hasHeightForWidth())
        self.MainWindow.setSizePolicy(sizePolicy)
        self.MainWindow.setMinimumSize(QtCore.QSize(1120, 480))
        self.MainWindow.setBaseSize(QtCore.QSize(1280, 1024))
        self.MainWindow.setWindowTitle("CarrionP13")
        logging.info("Creating central widget...")
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        logging.info("Creating left sidebar...")
        self.pnlLeft = QtWidgets.QHBoxLayout()
        self.pnlLeft.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.pnlLeft.setObjectName("pnlLeft")
        logging.info("Creating project tree view...")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setMinimumSize(QtCore.QSize(180, 0))
        self.treeWidget.setDragEnabled(True)
        self.treeWidget.setDropIndicatorShown(True)
        self.treeWidget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.treeWidget.setWordWrap(True)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        logging.info("Adding defaults to tree...")

        self.treeWidget.itemProject = QtWidgets.QTreeWidgetItem(self.treeWidget)
        self.treeWidget.itemProject.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        self.treeWidget.itemProject.setData(1,QtCore.Qt.WhatsThisRole,'Project')
        self.treeWidget.itemProject.setExpanded(True)

        self.treeWidget.itemBooks = QtWidgets.QTreeWidgetItem(self.treeWidget.itemProject)
        self.treeWidget.itemBooks.setData(1,QtCore.Qt.WhatsThisRole,'Book Root')
        self.treeWidget.itemBooks.setExpanded(True)


        self.treeWidget.itemEntities = QtWidgets.QTreeWidgetItem(self.treeWidget.itemProject)
        self.treeWidget.itemEntities.setData(1,QtCore.Qt.WhatsThisRole,'Metadata Root')
        self.treeWidget.itemEntities.setExpanded(True)

        logging.info("Tree items added.")
        self.treeWidget.header().setHighlightSections(True)

        self.pnlLeft.addWidget(self.treeWidget, 0, QtCore.Qt.AlignLeft)
        self.gridLayout.addLayout(self.pnlLeft, 0, 0, 1, 1)
        logging.info("Left panel complete.")
        logging.info("Creating middle panel...")
        self.pnlMid = QtWidgets.QGridLayout()
        self.pnlMid.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.pnlMid.setObjectName("pnlMid")
        logging.info("Creating tab viewport...")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(600, 200))
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        logging.info("Adding default tab...")
        self.tabNew = tabNewProject.tabNewProject(self,self.pjm)
        self.tabNew.setObjectName("tabNew")
        self.tabWidget.addTab(self.tabNew, "New Project")
        self.pnlMid.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.pnlMid, 0, 1, 1, 1)
        logging.info("Middle panel complete.")
        logging.info("Creating right panel...")
        self.pnlRight = QtWidgets.QHBoxLayout()
        self.pnlRight.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.pnlRight.setObjectName("pnlRight")
        logging.info("Creating info tollbox view...")
        self.toolBox = QtWidgets.QToolBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setMinimumSize(QtCore.QSize(200, 0))
        self.toolBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolBox.setObjectName("toolBox")
        logging.info("Adding views to toolbox...")
        """
        logging.info("Adding project info view...")
        self.pgProjectInfo = QtWidgets.QWidget()
        self.pgProjectInfo.setGeometry(QtCore.QRect(0, 0, 200, 365))
        self.pgProjectInfo.setObjectName("pgProjectInfo")
        self.lblPrjInfo = QtWidgets.QLabel(self.pgProjectInfo)
        self.lblPrjInfo.setGeometry(QtCore.QRect(5, -5, 146, 36))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lblPrjInfo.setFont(font)
        self.lblPrjInfo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblPrjInfo.setObjectName("lblPrjInfo")
        self.toolBox.addItem(self.pgProjectInfo, "")
        self.toolBox.setItemEnabled(0,False)
        logging.info("Project info view added.")
        """
        logging.info("Adding scene info view...")
        self.pgSceneInfo = QtWidgets.QWidget()
        self.pgSceneInfo.setGeometry(QtCore.QRect(0, 0, 200, 365))
        self.pgSceneInfo.setObjectName("pgSceneInfo")
        self.lblScnInfo = QtWidgets.QLabel(self.pgSceneInfo)
        self.lblScnInfo.setGeometry(QtCore.QRect(5, -5, 151, 36))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lblScnInfo.setFont(font)
        self.lblScnInfo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblScnInfo.setObjectName("lblScnInfo")
        self.linkList = QtWidgets.QListWidget(self.pgSceneInfo)
        self.linkList.setObjectName("linkList")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.linkList.sizePolicy().hasHeightForWidth())
        self.linkList.setSizePolicy(sizePolicy)
        self.linkList.setGeometry(QtCore.QRect(0, 40, 180, 320))
        self.linkList.setMinimumSize(QtCore.QSize(175, 0))
        self.linkList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.linkList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.linkList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.toolBox.addItem(self.pgSceneInfo, "")
        logging.info("Scene info view added.")
        self.pnlRight.addWidget(self.toolBox, 0, QtCore.Qt.AlignRight)
        self.gridLayout.addLayout(self.pnlRight, 0, 2, 1, 1)
        logging.info("Right panel complete.")
        self.MainWindow.setCentralWidget(self.centralwidget)
        logging.info("Building menu bar...")
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1100, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.MainWindow.setMenuBar(self.menubar)
        logging.info("Menu bar complete.")
        logging.info("Creating status bar...")
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)
        logging.info("Status bar created.")

        logging.info("Preparing actions...")
        # menu bar actions
        logging.info("Preparing menu bar actions...")
        self.actionNew = QtWidgets.QAction(self.MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(self.MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(self.MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionImport = QtWidgets.QAction(self.MainWindow)
        self.actionImport.setEnabled(False)
        self.actionImport.setObjectName("actionImport")
        self.actionExport = QtWidgets.QAction(self.MainWindow)
        self.actionExport.setEnabled(False)
        self.actionExport.setObjectName("actionExport")
        self.actionProgram_Settings = QtWidgets.QAction(self.MainWindow)
        self.actionProgram_Settings.setVisible(False)
        self.actionProgram_Settings.setEnabled(False)
        self.actionProgram_Settings.setObjectName("actionProgram_Settings")
        self.actionQuit = QtWidgets.QAction(self.MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionClose_Project = QtWidgets.QAction(self.MainWindow)
        self.actionClose_Project.setObjectName("actionClose_Project")
        self.actionCut = QtWidgets.QAction(self.MainWindow)
        self.actionCut.setObjectName("actionCut")
        self.actionCut.setEnabled(False)
        self.actionCopy = QtWidgets.QAction(self.MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionCopy.setEnabled(False)
        self.actionPaste = QtWidgets.QAction(self.MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionPaste.setEnabled(False)
        self.actionFind = QtWidgets.QAction(self.MainWindow)
        self.actionFind.setObjectName("actionFind")
        self.actionFind.setEnabled(False)
        self.actionReplace = QtWidgets.QAction(self.MainWindow)
        self.actionReplace.setObjectName("actionReplace")
        self.actionReplace.setEnabled(False)
        self.actionAbout = QtWidgets.QAction(self.MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.setEnabled(False)
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionProgram_Settings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose_Project)
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionFind)
        self.menuEdit.addAction(self.actionReplace)
        self.menuEdit.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        logging.info("Menu bar actions prepared.")
        self.linkList.actionLLlink = QtWidgets.QAction(self.MainWindow)
        self.linkList.actionLLlink.setObjectName("actionLLlink")
        # tree context-menu actions
        logging.info("Preparing non-custom tree context actions...")
        self.treeWidget.actionRenameProject = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionRenameProject.setObjectName("actionRenameProject")
        # entity actions
        self.treeWidget.actionNewEntity = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionNewEntity.setObjectName("actionNewEntity")
        self.treeWidget.actionNewEntityType = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionNewEntityType.setObjectName("actionNewEntityType")
        self.treeWidget.actionDelEntity = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionDelEntity.setObjectName("actionDelEntity")
        self.treeWidget.actionDelEntityType = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionDelEntityType.setObjectName("actionDelEntityType")
        self.treeWidget.actionRenEntity = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionRenEntity.setObjectName("actionRenEntity")
        self.treeWidget.actionRenEntityType = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionRenEntityType.setObjectName("actionRenEntityType")
        self.treeWidget.actionLinkEntity = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionLinkEntity.setObjectName("actionLinkEntity")
        self.treeWidget.actionMoveEntity = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionMoveEntity.setObjectName("actionMoveEntity")

        # scene actions
        self.treeWidget.actionNewScene = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionNewScene.setObjectName("actionNewScene")
        self.treeWidget.actionNewChapter = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionNewChapter.setObjectName("actionNewChapter")
        self.treeWidget.actionNewBook = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionNewBook.setObjectName("actionNewBook")
        self.treeWidget.actionDelScene = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionDelScene.setObjectName("actionDelScene")
        self.treeWidget.actionDelChapter = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionDelChapter.setObjectName("actionDelChapter")
        self.treeWidget.actionDelBook = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionDelBook.setObjectName("actionDelBook")
        self.treeWidget.actionRenScene = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionRenScene.setObjectName("actionRenScene")
        self.treeWidget.actionRenChapter = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionRenChapter.setObjectName("actionRenChapter")
        self.treeWidget.actionRenBook = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionRenBook.setObjectName("actionRenBook")
        self.treeWidget.actionMoveScene = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionMoveScene.setObjectName("actionMoveScene")
        self.treeWidget.actionMoveChapter = QtWidgets.QAction(self.treeWidget)
        self.treeWidget.actionMoveChapter.setObjectName("actionMoveChapter")
        logging.info("Tree actions prepared.")

        logging.info("Setting UI text...")
        self.retranslateUi(self.MainWindow)
        logging.info("UI text set.")
        logging.info("Setting default indeces for tab and toolbox panes...")
        self.tabWidget.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(0)
        logging.info("Set.")

        logging.info("Connecting signals to slots...")
        logging.info("Menu bar action signals...")
        self.actionNew.triggered.connect(self.NewProject)
        self.actionOpen.triggered.connect(self.OpenProject)
        self.actionSave.triggered.connect(self.SaveProject)
        self.actionClose_Project.triggered.connect(self.CloseProject)

        logging.info("Tree-view signals...")
        # change this to set tab focus on selected item id
        self.treeWidget.itemActivated['QTreeWidgetItem*','int'].connect(self.treeItemActivated)
        self.treeWidget.itemChanged['QTreeWidgetItem*','int'].connect(self.UpdateName)
        self.treeWidget.customContextMenuRequested['QPoint'].connect(self.treeContextMenu)
        self.linkList.customContextMenuRequested['QPoint'].connect(self.linkListContextMenu)

        # tree context-menu actions
        # Project-level(-ish)
        self.treeWidget.actionRenameProject.triggered.connect(self.treeActionRenameProject)
        self.treeWidget.actionNewBook.triggered.connect(self.treeActionNewBook)
        self.treeWidget.actionNewEntityType.triggered.connect(self.treeActionNewEntityType)

        # EntityType-level
        #self.treeWidget.actionNewEntityType.triggered.connect(self.treeActionNewEntityType)
        self.treeWidget.actionNewEntity.triggered.connect(self.treeActionNewEntity)
        self.treeWidget.actionDelEntityType.triggered.connect(self.treeActionDelEntityType)
        self.treeWidget.actionRenEntityType.triggered.connect(self.treeActionRenEntityType)

        # Entity-level
        self.treeWidget.actionRenEntity.triggered.connect(self.treeActionRenEntity)
        self.treeWidget.actionDelEntity.triggered.connect(self.treeActionDelEntity)
        self.treeWidget.actionLinkEntity.triggered.connect(self.treeActionLinkEntity)
        self.treeWidget.actionMoveEntity.triggered.connect(self.treeActionMoveEntity)

        # scene actions
        self.treeWidget.actionNewScene.triggered.connect(self.treeActionNewScene)
        self.treeWidget.actionNewChapter.triggered.connect(self.treeActionNewChapter)
        self.treeWidget.actionDelScene.triggered.connect(self.treeActionDelScene)
        self.treeWidget.actionDelChapter.triggered.connect(self.treeActionDelChapter)
        self.treeWidget.actionDelBook.triggered.connect(self.treeActionDelBook)
        self.treeWidget.actionRenScene.triggered.connect(self.treeActionRenScene)
        self.treeWidget.actionRenChapter.triggered.connect(self.treeActionRenChapter)
        self.treeWidget.actionRenBook.triggered.connect(self.treeActionRenBook)
        self.treeWidget.actionMoveChapter.triggered.connect(self.treeActionMoveChapter)

        logging.info("Other signals...")
        self.tabWidget.tabCloseRequested.connect(self.CloseTab)
        self.tabWidget.currentChanged.connect(self.UpdateLinkList)
        self.linkList.actionLLlink.triggered.connect(self.LLLink)
        self.linkList.itemDoubleClicked['QListWidgetItem*'].connect(self.llItemActivated)
        logging.info("Signals connected.")
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        logging.info("Status bar...")
        MainWindow.setStatusTip(_translate("MainWindow", "Ready"))
        logging.info("Tree-view panel...")
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.headerItem().setHidden(True)
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        logging.info("Tree branches...")
        self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "Project"))
        logging.info("+ Project.")
        self.treeWidget.topLevelItem(0).child(1).setText(0, _translate("MainWindow", "Metadata"))
        logging.info("-+ Metadata.")
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("MainWindow", "Books"))
        logging.info("-+ Books")
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        logging.info("Tree branches set.")
        logging.info("Default tab...")
        self.tabNew.lblNewProject.setText(_translate("MainWindow", "New Project"))
        self.tabNew.lblPrjTitle.setText(_translate("MainWindow", "Title:"))
        self.tabNew.btnPrjCreate.setText(_translate("MainWindow", "Create Project"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabNew), _translate("MainWindow", "New Project"))
        logging.info("Info panel...")
        #self.lblPrjInfo.setText(_translate("MainWindow", "Project Info"))
        #self.toolBox.setItemText(self.toolBox.indexOf(self.pgProjectInfo), _translate("MainWindow", "Project"))
        self.lblScnInfo.setText(_translate("MainWindow", "Scene Info"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.pgSceneInfo), _translate("MainWindow", "Scene"))
        logging.info("Menu bar...")
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save Project"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionImport.setText(_translate("MainWindow", "Import"))
        self.actionImport.setShortcut(_translate("MainWindow", "Ctrl+Shift+I"))
        self.actionExport.setText(_translate("MainWindow", "Export"))
        self.actionExport.setShortcut(_translate("MainWindow", "Ctrl+Shift+E"))
        self.actionProgram_Settings.setText(_translate("MainWindow", "Program Settings"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionClose_Project.setText(_translate("MainWindow", "Close Project"))
        self.actionClose_Project.setShortcut(_translate("MainWindow", "Ctrl+Shift+C"))
        self.actionCut.setText(_translate("MainWindow", "Cut"))
        self.actionCut.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actionFind.setText(_translate("MainWindow", "Find"))
        self.actionFind.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.actionReplace.setText(_translate("MainWindow", "Replace"))
        self.actionReplace.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actionAbout.setText(_translate("MainWindow", "About..."))
        # tree context-menu actions
        self.linkList.actionLLlink.setText(_translate("MainWindow", "Link Metadata Entry to Active Scene"))
        logging.info("Tree context-menu:")
        self.treeWidget.actionRenameProject.setText(_translate("treeWidget","Rename Project"))
        # entity actions
        logging.info("Entity actions...")
        self.treeWidget.actionNewEntity.setText(_translate("treeWidget","New Metadata Entry"))
        self.treeWidget.actionNewEntityType.setText(_translate("treeWidget","New Metadata Type"))
        self.treeWidget.actionDelEntity.setText(_translate("treeWidget","Delete Metadata Entry"))
        self.treeWidget.actionDelEntityType.setText(_translate("treeWidget","Delete Metadata Type"))
        self.treeWidget.actionRenEntity.setText(_translate("treeWidget","Rename Metadata Entry"))
        self.treeWidget.actionRenEntityType.setText(_translate("treeWidget","Rename Metadata Type"))
        self.treeWidget.actionLinkEntity.setText(_translate("treeWidget","Link Metadata Entry"))
        self.treeWidget.actionMoveEntity.setText(_translate("treeWidget","Move Metadata Entry"))

        # scene actions
        logging.info("Scene actions...")
        self.treeWidget.actionNewScene.setText(_translate("treeWidget","New Scene"))
        self.treeWidget.actionNewChapter.setText(_translate("treeWidget","New Chapter"))
        self.treeWidget.actionNewBook.setText(_translate("treeWidget","New Book"))
        self.treeWidget.actionDelScene.setText(_translate("treeWidget","Delete Scene"))
        self.treeWidget.actionDelChapter.setText(_translate("treeWidget","Delete Chapter"))
        self.treeWidget.actionDelBook.setText(_translate("treeWidget","Delete Book"))
        self.treeWidget.actionRenScene.setText(_translate("treeWidget","Rename Scene"))
        self.treeWidget.actionRenChapter.setText(_translate("treeWidget","Rename Chapter"))
        self.treeWidget.actionRenBook.setText(_translate("treeWidget","Rename Book"))
        self.treeWidget.actionMoveScene.setText(_translate("treeWidget","Move Scene"))
        self.treeWidget.actionMoveChapter.setText(_translate("treeWidget","Move Chapter"))
        logging.info("All text set.")

    def CloseTab(self,index):
        # close tab with index i
        # simple handler for the tabCloseRequest signal
        self.tabWidget.removeTab(index)

    def FindTab(self,title):
        # returns the index of a tab given its title
        # self.tabWidget.tabText(i)
        ret = None
        logging.info("Finding tab index...")
        for i in range(self.tabWidget.count()):
            t = self.tabWidget.tabText(i)
            if t == title:
                ret = i
                break
        logging.info(ret)
        return ret

    def UpdateLinkList(self):
        # updates the Scene link list to reflect the currently active tab
        logging.info("Updating scene linked list...")
        if self.tabWidget.currentIndex() != -1:
            logging.info(self.tabWidget.currentWidget().type)
            if self.tabWidget.currentWidget().type == 'Scene':
                logging.info(self.tabWidget.currentWidget().sceneid)
                self.RebuildLinkList(self.tabWidget.currentWidget().sceneid)
            else:
                logging.info("Not a scene-type tab. Clearing list...")
                self.ClearLinkList()
        else:
            logging.warning("No active tab.")

    def ClearLinkList(self):
        # clears the link list on the right panel
        logging.info("Link List count: %i" % self.linkList.count())
        if self.linkList.count() > 0:
            logging.info("Clearing old link list contents...")
            try:
                self.linkList.clear()
                """
                for r in range(self.linkList.count()):
                    logging.info(self.linkList.item(0))
                    self.linkList.takeItem(0)
                    logging.info("Removed item %i." % r)
                """
            except Exception as err:
                logging.error("Couldn't clear Link List!")
                logging.error(err)
            logging.info("Link list cleared.")


    def RebuildLinkList(self,sceneid):
        # repopulates the link list when a scene tab is made active
        self.ClearLinkList()
        rl = self.pjm.GetSceneData(sceneid)['rel_ids']
        if rl != None:
            for rid in rl:
                logging.info("Adding link id %i" % rid)
                rn = self.pjm.GetEntityData(rid)['name']
                logging.info("Adding %s to Link List." % rn)
                self.linkList.addItem(rn)
            logging.info("Link list repopulated.")
        else:
            logging.info("No related entities for the list.")

    def llItemActivated(self,item):
        logging.info("Link List item double-clicked")
        logging.info(str(item.text()))
        eid = self.pjm.GetEntID(str(item.text()))
        if eid != None:
            self.OpenEntity(eid)

    def treeItemActivated(self, item, col):
        # determines what to do when something in the tree is double-clicked
        # we only care about the 'Scene' and 'Metadata Entry' types.
        # 'col' is expected to be 0, since column 1 is hidden.
        # that said, we don't actually care about column 0,
        # since the type tag and scene/entity id are in column 1
        # where it doesn't clutter the UI.
        #check:unverified
        itemType = str(item.data(1,QtCore.Qt.WhatsThisRole))
        itemID = item.data(1,QtCore.Qt.UserRole)
        if itemType == 'Scene':
            # open the scene in a new tab
            logging.info("Scene %i requested." % itemID)
            self.OpenScene(itemID)
        elif itemType == 'Metadata Entry':
            # open the entity in a new tab
            logging.info("Entity %i requested." % itemID)
            self.OpenEntity(itemID)
        else:
            # ignore it
            logging.info("Category-type item %s activated." % str(item.text()[0]))

    def UpdateName(self,target,col):
        # handler for in-tree renaming events
        # target is the item whose name changed
        # col is the column in which the data changed
        newname = str(target.data(0,QtCore.Qt.DisplayRole))
        itemid = int(target.data(1,QtCore.Qt.UserRole))
        itemtype = str(target.data(1,QtCore.Qt.WhatIsRole))
        # depending on itemtype, call the appropriate rename handler
        if itemtype == 'Book':
            self.pjm.RenameBook(itemid,newname)
        elif itemtype == 'Chapter':
            self.pjm.RenameChapter(itemid,newname)
        elif itemtype == 'Scene':
            self.pjm.RenameScene(itemid,newname)
        elif itemtype == 'Metadata Type':
            self.pjm.RenameEntityType(itemid,newname)
        elif itemtype == 'Metadata Entry':
            self.pjm.RenameEntity(itemid,newname)
        elif itemtype == 'Project':
            self.pjm.RenameProject(itemid,newname)
        else:
            logging.warning("Invalid type on in-tree rename operation!")
            logging.warning("Name: %s\tType: %s\tID:%i" % newname,itemtype,itemid)

    def treeActionRenameProject(self):
        # rename the project
        # pops a dialog to get new name from user
        # should reimplement with in-place
        # self.lastTarget is what got right-clicked.
        logging.info("Project rename requested.")
        pname = self.GetString('Rename Project','New Title of Project:')
        if pname != None:
            logging.info("Rename entry for project: %s" % pname)
            logging.info("Old name: %s" % str(self.lastTarget.text(0)))
            self.pjm.RenameProject(pname)
            logging.info("Regenerating tree...")
            self.RegenProjectTree()
            logging.info("Project renamed.")
        else:
            logging.info("Operation canceled.")

    def NewProject(self):
        # open the New Project tab
        #check:ok
        logging.info("New Project tab requested.")
        self.tabNew = tabNewProject.tabNewProject(self,self.pjm)
        self.tabNew.setObjectName("tabNew")
        idx = self.tabWidget.addTab(self.tabNew, "New Project")
        self.tabWidget.setCurrentIndex(idx)

    def CreateProject(self,title,dbpath):
        # calls the project manager to create the project,
        # then opens the first scene.
        #check:ok
        logging.info("Requesting new project from Project Manager.")
        self.pjm.NewProject(title,dbpath)
        logging.info("Project created. Swapping tabs...")
        self.OpenScene(0)
        self.RegenProjectTree()
        self.tabWidget.removeTab(self.FindTab('New Project'))

    def SaveProject(self):
        # save the currently-open project
        logging.info("Requesting Project Manager save the current project.")
        self.pjm.SaveProject()

    #def SaveProjectAs(self):
        # ask the user what to save this new project as

    def CloseProject(self):
        # close the currently-open project
        logging.info("Requesting Project Manager save and close the current project.")
        if self.GetYN("Save project?") == QtWidgets.QMessageBox.Yes:
            self.pjm.SaveProject()
        self.pjm.CloseProject()

    def QuitProgram(self):
        logging.info("Quitting program.")
        self.CloseProject()
        QtWidgets.qApp.quit()

    def OpenProject(self):
        # pops a browse dialog for file selection
        # then calls the project manager to load it
        logging.info("Requesting Project Manager open an existing project.")
        prjpath = self.OpenFileBrowser()
        lid = self.pjm.OpenProject(prjpath)
        self.OpenScene(lid)
        self.RegenProjectTree()
        self.tabWidget.removeTab(self.FindTab("New Project"))

    def RegenProjectTree(self):
        # rebuilds the project tree from the DB
        #check:ok
        # A/N: I can't believe this nonsense actually worked first time through!
        _translate = QtCore.QCoreApplication.translate
        # clear default tree
        logging.info("Trimming default Books subtree...")
        self.treeWidget.topLevelItem(0).child(0).removeChild(self.treeWidget.topLevelItem(0).child(0).child(0))
        logging.info("Trimming default Metadata subtree...")
        self.treeWidget.topLevelItem(0).removeChild(self.treeWidget.topLevelItem(0).child(1))
        logging.info("Subtrees trimmed.")

        # populate tree
        # books
        # keys: id, title, order, type
        logging.info("Growing Books subtree...")
        booktree = self.pjm.GetBookTree()
        logging.info("Retrieved.")
        logging.info("Books...")
        self.treeWidget.itemBookList = {}
        for b in booktree['Books']:
            try:
                logging.info(b)
                self.treeWidget.itemBookList[b['id']] = QtWidgets.QTreeWidgetItem()
                logging.info("Entry created.")
                logging.info(self.treeWidget.itemBookList[b['id']])
                self.treeWidget.itemBookList[b['id']].setData(1,QtCore.Qt.WhatsThisRole,b['type'])# breaks here
                logging.info("Entry type set: %s" % b['type'])
                self.treeWidget.itemBookList[b['id']].setData(1,QtCore.Qt.InitialSortOrderRole,b['order'])
                logging.info("Entry sort order set: %i" % b['order'])
                self.treeWidget.itemBookList[b['id']].setData(1,QtCore.Qt.UserRole,b['id'])
                logging.info("Entry ID set: %i" % b['id'])
                self.treeWidget.itemBookList[b['id']].setExpanded(True)
                self.treeWidget.itemBookList[b['id']].setText(0, _translate("MainWindow", b['title']))
                logging.info("Entry title set: %s" % b['title'])
                self.treeWidget.itemBooks.insertChild((int(b['order']) - 1),self.treeWidget.itemBookList[b['id']])
                logging.info("Node inserted at index %i." % (int(b['order']) - 1))
            except Exception as e:
                logging.error("Could not add tree entry %i!" % b['id'])
                logging.error(e)
        logging.info(self.treeWidget.itemBookList.keys())

        # + 'book' key
        logging.info("Chapters...")
        self.treeWidget.itemChapterList = {}
        for c in booktree['Chapters']:
            try:
                logging.info(c)
                self.treeWidget.itemChapterList[c['id']] = QtWidgets.QTreeWidgetItem()
                self.treeWidget.itemChapterList[c['id']].setData(1,QtCore.Qt.WhatsThisRole,c['type'])
                self.treeWidget.itemChapterList[c['id']].setData(1,QtCore.Qt.InitialSortOrderRole,c['order'])
                self.treeWidget.itemChapterList[c['id']].setData(1,QtCore.Qt.UserRole,c['id'])
                self.treeWidget.itemChapterList[c['id']].setExpanded(True)
                self.treeWidget.itemChapterList[c['id']].setText(0, _translate("MainWindow", c['title']))
                self.treeWidget.itemChapterList[c['id']].setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsEnabled)
                self.treeWidget.itemBookList[c['book']].insertChild(c['order']-1,self.treeWidget.itemChapterList[c['id']])
            except Exception as e:
                logging.error("Could not add tree entry %i!" % c['id'])
                logging.error(e)
        logging.info(self.treeWidget.itemChapterList.keys())

        # + 'chapter' key
        logging.info("Scenes...")
        self.treeWidget.itemSceneList = {}
        for s in booktree['Scenes']:
            try:
                logging.info(s)
                self.treeWidget.itemSceneList[s['id']] = QtWidgets.QTreeWidgetItem()
                self.treeWidget.itemSceneList[s['id']].setData(1,QtCore.Qt.WhatsThisRole,s['type'])
                self.treeWidget.itemSceneList[s['id']].setData(1,QtCore.Qt.InitialSortOrderRole,s['order'])
                self.treeWidget.itemSceneList[s['id']].setData(1,QtCore.Qt.UserRole,s['id'])
                self.treeWidget.itemSceneList[s['id']].setExpanded(True)
                self.treeWidget.itemSceneList[s['id']].setText(0, _translate("MainWindow", s['title']))
                self.treeWidget.itemSceneList[s['id']].setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsEnabled)
                self.treeWidget.itemChapterList[s['chapter']].insertChild(c['order']-1,self.treeWidget.itemSceneList[s['id']])
            except Exception as e:
                logging.error("Could not add tree entry %i!" % s['id'])
                logging.error(e)
        logging.info(self.treeWidget.itemSceneList.keys())

        # metadata
        logging.info("Growing Metadata subtree...")
        metatree = self.pjm.GetMetaTree()

        # set root category
        logging.info("Metadata Root...")
        self.treeWidget.itemTypeList = {}
        logging.info(metatree['Types'][0])
        try:
            self.treeWidget.itemTypeList[metatree['Types'][0]['id']] = QtWidgets.QTreeWidgetItem()
            self.treeWidget.itemTypeList[metatree['Types'][0]['id']].setData(1,QtCore.Qt.WhatsThisRole,metatree['Types'][0]['type'])
            self.treeWidget.itemTypeList[metatree['Types'][0]['id']].setData(1,QtCore.Qt.UserRole,metatree['Types'][0]['id'])
            self.treeWidget.itemTypeList[metatree['Types'][0]['id']].setExpanded(True)
            self.treeWidget.itemTypeList[metatree['Types'][0]['id']].setText(0, _translate("MainWindow", metatree['Types'][0]['label']))
            self.treeWidget.itemProject.addChild(self.treeWidget.itemTypeList[metatree['Types'][0]['id']])
        except Exception as e:
            logging.error("Could not add tree entry %i!" % metatree['Types'][0]['id'])
            logging.error(e)
        logging.info(self.treeWidget.itemTypeList.keys())

        # set child categories
        # keys: id, parent, label, type
        logging.info("Metadata Types...")
        for t in metatree['Types'][1:]:
            try:
                logging.info(t)
                self.treeWidget.itemTypeList[t['id']] = QtWidgets.QTreeWidgetItem()
                self.treeWidget.itemTypeList[t['id']].setData(1,QtCore.Qt.WhatsThisRole,t['type'])
                self.treeWidget.itemTypeList[t['id']].setData(1,QtCore.Qt.UserRole,t['id'])
                self.treeWidget.itemTypeList[t['id']].setExpanded(True)
                self.treeWidget.itemTypeList[t['id']].setText(0, _translate("MainWindow", t['label']))
                self.treeWidget.itemTypeList[t['id']].setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsEnabled)
                self.treeWidget.itemTypeList[t['parent']].addChild(self.treeWidget.itemTypeList[t['id']])
            except Exception as e:
                logging.error("Could not add tree entry %i!" % t['id'])
                logging.error(e)
        logging.info(self.treeWidget.itemTypeList.keys())

        # set metadata entries
        # keys: id, name, cat_id, type
        logging.info("Metadata Entries...")
        self.treeWidget.itemEntryList = {}
        for e in metatree['Entries']:
            try:
                logging.info(e)
                self.treeWidget.itemEntryList[e['id']] = QtWidgets.QTreeWidgetItem()
                self.treeWidget.itemEntryList[e['id']].setData(1,QtCore.Qt.WhatsThisRole,e['type'])
                self.treeWidget.itemEntryList[e['id']].setData(1,QtCore.Qt.UserRole,e['id'])
                self.treeWidget.itemEntryList[e['id']].setExpanded(True)
                self.treeWidget.itemEntryList[e['id']].setText(0, _translate("MainWindow", e['name']))
                self.treeWidget.itemEntryList[e['id']].setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsEnabled)
                self.treeWidget.itemTypeList[e['cat_id']].addChild(self.treeWidget.itemEntryList[e['id']])
            except Exception as err:
                logging.error("Could not add tree entry %i!" % t['id'])
                logging.error(err)
        logging.info(self.treeWidget.itemEntryList.keys())
        logging.info("Tree regrown.")

    def treeActionNewBook(self):
        # self.lastTarget is what got right-clicked.
        _translate = QtCore.QCoreApplication.translate
        bname = self.GetString('New Book',"Name of New Book:")
        if bname != None:
            logging.info("Creating entry for new book:", bname)
            newBook = QtWidgets.QTreeWidgetItem(self.lastTarget)
            newBook.setData(1,QtCore.Qt.WhatsThisRole,'Book')
            newBook.setText(0, _translate("MainWindow", bname))
            newBook.setData(1,QtCore.Qt.UserRole, self.pjm.NewBook(bname))
        else:
            logging.info("Operation canceled.")

    def treeActionRenBook(self):
        # pops a dialog to get new name from user
        # should reimplement with in-place
        # self.lastTarget is what got right-clicked.
        logging.info("Book rename requested.")
        bname = self.GetString('Rename Book','New Title of Book:')
        if bname != None:
            logging.info("Rename entry for book: %s" % bname)
            logging.info("Old name: %s" % str(self.lastTarget.text(0)))
            bid = int(self.lastTarget.data(1,QtCore.Qt.UserRole))
            logging.info(bid)
            self.pjm.RenameBook(bid, bname)
            logging.info("Regenerating tree...")
            self.RegenProjectTree()
            # TODO should update tab title if open
            logging.info("Book renamed.")
        else:
            logging.info("Operation canceled.")

    def treeActionDelBook(self):
        # deletes all child entries and then the right-clicked category.
        logging.info("Book deletion requested.")
        bname = str(self.lastTarget.text(0))
        if self.GetYN("Delete book %s?" % bname):
            self.DeleteBook(self.lastTarget)
            logging.info("Deletion complete.")
        else:
            logging.info("Operation canceled.")

    def DeleteBook(self,node):
        # walks through subtree and calls the Project Manager to delete each node
        nodetype = str(node.data(1,QtCore.Qt.WhatsThisRole))
        nodeid = int(node.data(1,QtCore.Qt.UserRole))
        nodename = str(node.text(0))
        logging.info("Node:")
        logging.info(nodeid)
        logging.info(nodename)
        logging.info(nodetype)
        if nodetype == 'Scene':
            # entries have no children; ok to delete
            self.DeleteScene(nodeid)
        elif nodetype == 'Chapter':
            if node.childCount <= 0:
                # no children; ok to delete
                self.pjm.DeleteChapter(nodeid)
            else:
                # traverse first child branch
                self.DeleteChapter(node.child(0))
                # retraverse from this node to check next branch
                self.DeleteChapter(node)
        elif nodetype == 'Book':
            if node.childCount <= 0:
                # no children; ok to delete
                self.pjm.DeleteBook(nodeid)
            else:
                # traverse first child branch
                self.DeleteBook(node.child(0))
                # retraverse from this node to check next branch
                self.DeleteBook(node)
        else:
            logging.warning("Attempt to delete non-Scene, non-Chapter, or non-Book node!")

    def treeActionNewChapter(self):
        # self.lastTarget is what got right-clicked.
        _translate = QtCore.QCoreApplication.translate
        cname = self.GetString('New Chapter',"Name of New Chapter:")
        if cname != None:
            logging.info("Creating entry for new chapter:", cname)
            newCh = QtWidgets.QTreeWidgetItem(self.lastTarget)
            newCh.setData(1,QtCore.Qt.WhatsThisRole,'Chapter')
            newCh.setText(0, _translate("MainWindow", cname))
            newCh.setData(1,QtCore.Qt.UserRole, self.pjm.NewChapter(cname, \
                newCh.parent().data(1,QtCore.Qt.UserRole)))
            newCh.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsEnabled)
        else:
            logging.info("Operation canceled.")

    def treeActionRenChapter(self):
        # pops a dialog to get new name from user
        # should reimplement with in-place
        # self.lastTarget is what got right-clicked.
        logging.info("Chapter rename requested.")
        cname = self.GetString('Rename Chapter','New Title of Chapter:')
        if cname != None:
            logging.info("Rename entry for chapter: %s" % cname)
            logging.info("Old name: %s" % str(self.lastTarget.text(0)))
            cid = int(self.lastTarget.data(1,QtCore.Qt.UserRole))
            logging.info(cid)
            self.pjm.RenameChapter(cid, cname)
            logging.info("Regenerating tree...")
            self.RegenProjectTree()
            logging.info("Chapter renamed.")
        else:
            logging.info("Operation canceled.")

    def treeActionDelChapter(self):
        # deletes all child entries and then the right-clicked category.
        logging.info("Chapter deletion requested.")
        cname = str(self.lastTarget.text(0))
        if self.GetYN("Delete chapter %s?" % cname):
            self.DeleteChapter(self.lastTarget)
            logging.info("Deletion complete.")
        else:
            logging.info("Operation canceled.")

    def DeleteChapter(self,node):
        # walks through subtree and calls the Project Manager to delete each node
        nodetype = str(node.data(1,QtCore.Qt.WhatsThisRole))
        nodeid = int(node.data(1,QtCore.Qt.UserRole))
        nodename = str(node.text(0))
        logging.info("Node:")
        logging.info(nodeid)
        logging.info(nodename)
        logging.info(nodetype)
        if nodetype == 'Scene':
            # entries have no children; ok to delete
            self.DeleteScene(nodeid)
        elif nodetype == 'Chapter':
            if node.childCount <= 0:
                # no children; ok to delete
                self.pjm.DeleteChapter(nodeid)
            else:
                # traverse first child branch
                self.DeleteChapter(node.child(0))
                # retraverse from this node to check next branch
                self.DeleteChapter(node)
        else:
            logging.warning("Attempt to delete non-Scene or non-Chapter node!")

    def treeActionMoveChapter(self):
        self.NotImplemented()

    def treeActionNewScene(self):
        # sets up the tree item for the requested scene
        # self.lastTarget is what got right-clicked.
        #check:ok
        logging.info("New Scene requested.")
        _translate = QtCore.QCoreApplication.translate
        sname = self.GetString('New Scene','Name of New Scene:')
        if sname != None:
            logging.info("Creating entry for new scene: %s" % sname)
            logging.info(str(self.lastTarget.text(0)))
            chapter = int(self.lastTarget.data(1,QtCore.Qt.UserRole))
            logging.info(chapter)
            book = int(self.lastTarget.parent().data(1,QtCore.Qt.UserRole))
            logging.info(book)
            logging.info("Creating new tree item for scene...")
            newScene = QtWidgets.QTreeWidgetItem()
            newScene.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsEnabled)
            logging.info("Setting role to 'Scene'")
            newScene.setData(1,QtCore.Qt.WhatsThisRole,'Scene')
            logging.info("Setting tree item title to %s." % sname)
            newScene.setText(0, _translate("MainWindow", sname))

            # once tree item is ready, create the DB entry
            logging.info("Starting DB entry process...")
            sid = self.NewScene(sname, chapter, book)
            logging.info("Scene created with id: ",sid)
            newScene.setData(1,QtCore.Qt.UserRole, sid)
            self.lastTarget.addChild(newScene)
            logging.info("New scene '%s' ready." % sname)
        else:
            logging.info("Operation canceled.")

    def NewScene(self,sname,bookid,chapterid):
        # ask user for scene's name, then make it and open it
        #check:ok
        logging.info("Requesting new Scene from Project Manager.")
        logging.info("sname: %s, bookid: %i, chapterid: %i", sname, bookid, chapterid)
        sid = self.pjm.NewScene(sname,bookid,chapterid) # make the scene in DB
        self.OpenScene(sid) # make it active
        return sid

    def OpenScene(self,sceneid):
        # open a tab with the given scene and give it focus
        #check:ok
        logging.info("Requesting Project Manager open existing scene %i." % sceneid)
        sceneData = self.pjm.GetSceneData(sceneid)
        logging.info(sceneData)
        idx = self.FindTab(sceneData['title'])
        if idx == None:
            scnTab = tabSceneEdit.tabSceneEdit(self,self.pjm,sceneid)
            logging.info("Loading scene into new tab.")
            idx = self.tabWidget.addTab(scnTab, sceneData['title'])
            logging.info("Scene loaded into tab %i." % idx)
        self.tabWidget.setCurrentIndex(idx)
        logging.info("Active tab switched to %i." % idx)

    def treeActionRenScene(self):
        # pops a dialog to get new name from user
        # should reimplement with in-place
        # self.lastTarget is what got right-clicked.
        logging.info("Scene rename requested.")
        try:
            sname = self.GetString('Rename Scene','New Title of Scene:')
            if sname != None:
                logging.info("Rename entry for scene: %s" % sname)
                oldname = str(self.lastTarget.text(0))
                logging.info("Old name: %s" % oldname)
                sid = int(self.lastTarget.data(1,QtCore.Qt.UserRole))
                logging.info(sid)
                self.pjm.RenameScene(sid, sname)
                logging.info("Scene renamed.")
                logging.info("Regenerating tree...")
                self.RegenProjectTree()
                logging.info("Reopening tab...")
                idx = self.FindTab(oldname)
                curr = self.tabWidget.currentIndex()
                logging.info(idx)
                if idx != None:
                    self.CloseTab(idx)
                    if idx == curr:
                        self.OpenScene(sid)
            else:
                logging.info("Operation canceled.")
        except Exception as err:
            logging.error("Couldn't rename scene!")
            logging.error(err)


    def treeActionDelScene(self):
        self.DeleteScene(self.lastTarget)

    def DeleteScene(self,node):
        # pops a dialog for user to confirm deletion
        # self.lastTarget is what got right-clicked.
        logging.info("Scene deletion requested.")
        sname = str(node.text(0))
        if self.GetYN("Delete scene %s?" % sname):
            sid = int(node.data(1,QtCore.Qt.UserRole))
            logging.info(sname)
            logging.info(sid)
            if self.pjm.DeleteScene(sid):
                # update project tree
                self.tabWidget.removeTab(self.FindTab(sname))
                self.lastTarget.parent().removeChild(node)
                logging.info("Scene deleted.")
            else:
                logging.error("Could not delete scene.")
                self.ErrorMsg("Could not delete scene:\n%s" % sname)
        else:
            logging.info("Operation canceled.")

    def treeActionMoveScene(self):
        self.NotImplemented()

    def treeActionNewEntityType(self):
        # self.lastTarget is what got right-clicked.
        _translate = QtCore.QCoreApplication.translate
        logging.info("New metadata type requested.")
        sname = self.GetString('New Metadata Category',"Name of New Metadata Category (singular form):")
        if sname != None:
            pname = self.GetString('New Metadata Category',"Name of New Metadata Category (plural form):")
            if pname != None:
                logging.info("Creating entry for new entity category: %s (%s)" % (sname,pname))
                newET = QtWidgets.QTreeWidgetItem(self.lastTarget)
                newET.setData(1,QtCore.Qt.WhatsThisRole,'Metadata Type')
                newET.setText(0, _translate("MainWindow", pname))
                newET.setData(1,QtCore.Qt.UserRole, self.pjm.NewEntityType(sname, pname, \
                        newET.parent().data(1,QtCore.Qt.UserRole)))
                newET.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsEnabled)
            else:
                logging.info("Operation canceled.")
        else:
            logging.info("Operation canceled.")

    def treeActionDelEntityType(self):
        # deletes all child entries and then the right-clicked category.
        logging.info("Category deletion requested.")
        etname = str(self.lastTarget.text(0))
        if self.GetYN("Delete category %s?" % etname):
            self.DeleteEntityType(self.lastTarget)
            logging.info("Deletion complete.")
        else:
            logging.info("Operation canceled.")

    def DeleteEntityType(self,node):
        # walks through subtree and calls the Project Manager to delete each node
        nodetype = str(node.data(1,QtCore.Qt.WhatsThisRole))
        nodeid = int(node.data(1,QtCore.Qt.UserRole))
        nodename = str(node.text(0))
        logging.info("Node:")
        logging.info(nodeid)
        logging.info(nodename)
        logging.info(nodetype)
        if nodetype == 'Metadata Entry':
            # entries have no children; ok to delete
            self.DeleteEntity(nodeid)
        elif nodetype == 'Metadata Type':
            if node.childCount <= 0:
                # no children; ok to delete
                self.pjm.DeleteEntityType(nodeid)
            else:
                # traverse first child branch
                self.DeleteEntityType(node.child(0))
                # retraverse from this node to check next branch
                self.DeleteEntityType(node)
        else:
            logging.warning("Attempt to delete non-Entity or non-Entity Type node!")

    def treeActionRenEntityType(self):
        # renames a metadata category
        # TODO reimplement with in-place editing on tree
        logging.info("Category rename requested.")
        ncn = self.GetString("Rename Category","New name for Category:")
        if ncn != None:
            etid = int(self.lastTarget.data(1,QtCore.Qt.UserRole))
            self.pjm.RenameEntityType(etid,ncn)
            logging.info("Regenerating tree...")
            self.RegenProjectTree()
            logging.info("Category renamed.")
        else:
            logging.info("Operation canceled.")

    def treeActionNewEntity(self):
        # self.lastTarget is what got right-clicked.
        _translate = QtCore.QCoreApplication.translate
        logging.info("New metadata entry requested.")
        ename = self.GetString('New Metadata Entry',"Name of New Metadata Entry:")
        logging.info("Name retrieved:")
        logging.info(ename)
        if ename != None:
            etype = self.lastTarget.data(1,QtCore.Qt.UserRole)
            ent = {'name':ename,'desc':'','type':etype,'related':'','aliases':''}
            logging.info(ent)
            logging.info("Requesting new entity from the Project Manager...")
            eid = self.pjm.NewEntity(ent)
            if eid != None:
                logging.info("Creating tree entry for new entity: %s" % ename)
                newEntity = QtWidgets.QTreeWidgetItem()
                logging.info("Setting data...")
                newEntity.setData(1, QtCore.Qt.WhatsThisRole,'Metadata Entry')
                newEntity.setData(1, QtCore.Qt.UserRole, eid)
                newEntity.setText(0, _translate("MainWindow", ename))
                logging.info("Setting flags...")
                newEntity.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsEnabled)
                logging.info("Adding to parent category subtree...")
                self.lastTarget.addChild(newEntity)
                logging.info("New entity created. Opening it for editing...")
                self.OpenEntity(eid)
            else:
                logging.warning("Could not create new entity!")
                self.ErrorMsg("Could not create new metadata entry!")
        else:
            logging.info("Operation canceled.")

    def OpenEntity(self,entityid):
        # open a tab with the given entity and give it focus
        logging.info("Requesting Project Manager open an existing entity.")
        ent = self.pjm.GetEntityData(entityid)
        if ent != None:
            logging.info(ent['name'])
            idx = self.FindTab(ent['name'])
            if idx == None:
                idx = self.tabWidget.addTab(tabEntityEdit.tabEntityEdit(self.MainWindow,self.pjm,entityid,ent['type']), ent['name'])
            logging.info("Tab index: %i" % idx)
            self.tabWidget.setCurrentIndex(idx)
        else:
            logging.warning("Could not open entity %i!" % entityid)
            self.ErrorMsg("Could not open entity %i!" % entityid)

    def treeActionRenEntity(self):
        # rename a metadata entry
        # TODO reimplement with editing in-place on tree
        # self.lastTarget is what was right-clicked.
        logging.info("Requesting entity rename")
        ename = self.GetString("Rename Metadata Entry","New Name of Metadata Entry:")
        if ename != None:
            eid = int(self.lastTarget.data(1,QtCore.Qt.UserRole))
            logging.info(ename)
            logging.info(eid)
            self.pjm.RenameEntity(eid,ename)
            logging.info("Regenerating tree...")
            self.RegenProjectTree()
            logging.info("Entity renamed.")
        else:
            logging.info("Operation canceled.")

    def treeActionDelEntity(self):
        # process metadata entry deletion request
        # self.lastTarget is what was right-clicked.
        self.DeleteEntity(self.lastTarget)

    def DeleteEntity(self,entity):
        # delete a metadata entry
        logging.info("Requesting entity deletion")
        ename = entity.text(0)
        logging.info(ename)
        if self.GetYN("Confirm Deletion","Really delete %s?" % ename):
            eid = int(entity.data(1,QtCore.Qt.UserRole))
            logging.info(eid)
            if self.pjm.DeleteEntity(eid):
                self.tabWidget.removeTab(self.FindTab(ename))
                entity.parent().removeChild(entity)
                logging.info("Entity deleted.")
            else:
                logging.error("Could not delete %s!" % ename)
                self.ErrorMsg("Could not delete:\n%s" % ename)
        else:
            logging.info("Operation canceled.")

    def treeActionLinkEntity(self):
        # links the right-clicked entity to either a scene or another entity
        # self.lastTarget is what was right-clicked.
        logging.info("Entity Link operation started.")
        ename = str(self.lastTarget.text(0))
        self.LinkDialog(self.lastTarget.data(1,QtCore.Qt.UserRole),self.lastTarget.whatsThis(1),"Link %s to:" % ename)
        logging.info("Entity Link operation complete.")

    def treeActionMoveEntity(self):
        self.NotImplemented()

    def OpenFileBrowser(self):
        logging.info("Open-File routine start")
        try:
            logging.info("Opening file picker dialog")
            fd = QtWidgets.QFileDialog()
            # getOpenFileName returns a tuple with [0] = path to the selected file
            # and [1] = the selection filter for the dialog. So we strip out all but [0].
            fname = str(fd.getOpenFileName(fd,'Open File...','~/','Project Files (*.ppp)')[0])
            logging.info(fname)
            return fname
        except IOError as e:
            self.ErrorMsg(e)
        logging.info("Open-File routine end")

    def ErrorMsg(self, e):
        logging.warning("Error: %s" % e)
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(e)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.setWindowTitle("Error")
        msg.buttonClicked.connect(msg.close)
        msg.exec_()

    def GetYN(self,prompt):
        # returns either QtWidgets.QMessageBox.Yes or QtWidgets.QMessageBox.No
        logging.info("Asking user (Y/N): %s" % prompt)
        dlg = QtWidgets.QMessageBox()
        dlg.setIcon(QtWidgets.QMessageBox.Question)
        dlg.setText(prompt)
        dlg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        dlg.setDefaultButton(QtWidgets.QMessageBox.Yes)
        dlg.setWindowTitle("Question")
        rt = dlg.exec_()
        return rt

    def GetString(self,title,prompt):
        logging.info("Creating dialog...")
        try:
            val, ok = QtWidgets.QInputDialog.getText(self.centralwidget,title,prompt)
        except:
            logging.error("Error opening QInputDialog:",sys.exc_info()[0])
        finally:
            if ok and val !='':
                logging.info(val)
                return val
            else:
                logging.info("None.")
                return None

    def InfoMsg(self, message):
        logging.info("Message:",message)
        logging.info("Creating MessageBox widget...")
        msg = QtWidgets.QMessageBox()
        logging.info("Setting icon...")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        logging.info("Setting text...")
        msg.setText(message)
        logging.info("Adding OK button...")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        logging.info("Setting dialog title...")
        msg.setWindowTitle("Message")
        logging.info("Connecting signals...")
        msg.buttonClicked.connect(msg.close)
        logging.info("Popping dialog...")
        msg.exec_()
        logging.info("Complete.")

    def NotImplemented(self):
        logging.info("Action from context menu triggered.")
        self.InfoMsg("Not implemented yet!")
        logging.info("User alerted.")

    def LinkDialog(self,target,targettype, prompt):
        # shows a tree view where user can link an entity to a scene or another entity
        # LinkDialog.LinkDialog(target,title,prompt,pjm=ProjectManager.ProjectManager(),parent=None)
        logging.info("Launching Link dialog...")
        linker = LinkDialog.LinkDialog(targettype, "Link Entry", prompt, self.MainWindow, self.pjm)
        linkid = linker.exec_()
        if linkid > 900000:
            # yes, I know this is a bad idea long-term. But for a proof-of-concept it's fine.
            # TODO for next revision, find a better way to pass type with the id from the dialog.
            linkid -= 900000
            linktype = 'Metadata Entry'
        else:
            linktype = 'Scene'
        if targettype != 'Scene':
            if self.pjm.LinkEntity(target,linktype,linkid):
                logging.info("Entity Link successful.")
            else:
                logging.error("Entity Link failed.")
        else:
            if self.pjm.LinkEntity(linkid,linktype,target):
                logging.info("Entity Link successful.")
            else:
                logging.error("Entity Link failed.")

    def LLLink(self):
        # link active scene to entities
        logging.info("Entity Link operation started.")
        currid = self.tabWidget.currentWidget().sceneid
        sname = self.pjm.GetSceneData(currid)['title']
        self.LinkDialog(currid,'Scene',"Link %s to:" % sname)
        logging.info("Entity Link operation complete.")

    def treeContextMenu(self,event):
        logging.info("Building context menu.")
        logging.info("Getting right-click location...")
        logging.info(event)
        self.lastTarget = self.treeWidget.itemAt(event)
        self.lastTarget.setSelected(True)
        logging.info(str(self.lastTarget.text(0)))
        ttype = str(self.lastTarget.data(1,QtCore.Qt.WhatsThisRole))
        logging.info(ttype)
        logging.info("Creating menu widget...")
        treeMenu = QtWidgets.QMenu(self.treeWidget)
        logging.info("Making sure it's empty...")
        treeMenu.clear()

        logging.info("Adding actions to context menu...")
        if ttype == 'Project':
            logging.info("Project-level.")
            treeMenu.addAction(self.treeWidget.actionRenameProject)
        elif ttype == 'Metadata Root':
            logging.info("Metadata Root level.")
            treeMenu.addAction(self.treeWidget.actionNewEntityType)
        elif ttype == 'Metadata Type':
            logging.info("EntityTypes-level.")
            treeMenu.addAction(self.treeWidget.actionNewEntity)
            logging.info("New Entity option added.")
            treeMenu.addAction(self.treeWidget.actionRenEntityType)
            logging.info("Rename Entity Type option added.")
            treeMenu.addAction(self.treeWidget.actionDelEntityType)
            logging.info("Delete Entity Type option added.")
        elif ttype == 'Metadata Entry':
            logging.info("Entities-level.")
            treeMenu.addAction(self.treeWidget.actionRenEntity)
            treeMenu.addAction(self.treeWidget.actionDelEntity)
            treeMenu.addAction(self.treeWidget.actionLinkEntity)
        elif ttype == 'Book Root':
            logging.info("Book Root level.")
            treeMenu.addAction(self.treeWidget.actionNewBook)
        elif ttype == 'Book':
            logging.info("Book-level.")
            treeMenu.addAction(self.treeWidget.actionRenBook)
            treeMenu.addAction(self.treeWidget.actionDelBook)
            treeMenu.addAction(self.treeWidget.actionNewChapter)
        elif ttype == 'Chapter':
            logging.info("Chapter-level.")
            treeMenu.addAction(self.treeWidget.actionRenChapter)
            treeMenu.addAction(self.treeWidget.actionDelChapter)
            treeMenu.addAction(self.treeWidget.actionNewScene)
        elif ttype == 'Scene':
            logging.info("Scene-level.")
            treeMenu.addAction(self.treeWidget.actionRenScene)
            treeMenu.addAction(self.treeWidget.actionDelScene)
        else:
            logging.warning("WARNING: Invalid context.")
            return

        logging.info("Actions added.")

        # the action's triggered() signal handles the actual action.
        # self.__lastTarget holds the tree item actually right-clicked
        # so the slot mapped to the action's triggered() signal can
        # know which item to operate on.
        action = treeMenu.exec_(QtGui.QCursor.pos())
        logging.info(action)
        if action != None:
            logging.info("Menu option triggered: %s " % str(action.text()))
        else:
            logging.info("Menu canceled.")

    def linkListContextMenu(self,event):
        logging.info("Building context menu.")
        logging.info("Getting right-click location...")
        logging.info(event)

        logging.info("Creating menu widget...")
        llMenu = QtWidgets.QMenu(self.linkList)
        logging.info("Making sure it's empty...")
        llMenu.clear()

        logging.info("Adding actions to context menu...")
        llMenu.addAction(self.linkList.actionLLlink)

        logging.info("Actions added.")

        # the action's triggered() signal handles the actual action.
        # self.__lastTarget holds the tree item actually right-clicked
        # so the slot mapped to the action's triggered() signal can
        # know which item to operate on.
        action = llMenu.exec_(QtGui.QCursor.pos())
        logging.info(action)
        if action != None:
            logging.info("Menu option triggered: %s " % str(action.text()))
        else:
            logging.info("Menu canceled.")