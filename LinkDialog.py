# -*- coding: utf-8 -*-
# Dialog for linking entities
# Initial form implementation generated from reading ui file 'LinkDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3

import ProjectManager as pm
from PyQt5 import QtCore, QtGui, QtWidgets
import logging
logging.basicConfig(filename='PP_runtime.log',level=logging.INFO)

class LinkDialog(QtWidgets.QDialog):
    def __init__(self,targettype,title,prompt,parent=None,pjm=pm.ProjectManager()):
        logging.info("Initializing Link dialog...")
        super(LinkDialog,self).__init__(parent)
        self.type = targettype
        self.pjm = pjm
        logging.info("Building UI...")
        self.setupUi(title,prompt)

    def setupUi(self, title, prompt):
        self.setObjectName("LinkDialog")
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.resize(410, 503)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.setFont(font)
        self.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(310, 35, 81, 461))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 10, 106, 16))
        self.label.setObjectName("label")
        self.treeWidget = QtWidgets.QTreeWidget(self)
        self.treeWidget.setGeometry(QtCore.QRect(10, 35, 286, 456))
        self.treeWidget.setObjectName("treeWidget")
        logging.info("Adding defaults to tree...")
        try:
            self.treeWidget.itemProject = QtWidgets.QTreeWidgetItem(self.treeWidget)
            self.treeWidget.itemProject.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
            self.treeWidget.itemProject.setData(1,QtCore.Qt.WhatsThisRole,'Project')
            self.treeWidget.itemProject.setExpanded(True)
            self.treeWidget.itemBooks = QtWidgets.QTreeWidgetItem(self.treeWidget.itemProject)
            self.treeWidget.itemBooks.setData(1,QtCore.Qt.WhatsThisRole,'Book Root')
            self.treeWidget.itemBooks.setExpanded(True)
            logging.info("Tree items added.")
        except Exception as e:
            logging.error(e)
        self.treeWidget.header().setHighlightSections(True)
        logging.info("Setting UI text...")
        self.retranslateUi(title, prompt)
        logging.info("Populating tree...")
        self.RegenProjectTree()
        logging.info("Connecting signals to slots...")
        self.treeWidget.itemClicked['QTreeWidgetItem*','int'].connect(self.UpdateEndpoint)
        self.buttonBox.accepted.connect(self.LinkSelected)
        self.buttonBox.rejected.connect(self.reject)
        logging.info("Connected.")
        QtCore.QMetaObject.connectSlotsByName(self)
        logging.info("Meta-object registered.")

    def retranslateUi(self, title, prompt):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("LinkDialog", title))
        self.label.setText(_translate("LinkDialog", prompt))
        self.treeWidget.headerItem().setHidden(True)
        try:
            logging.info("Tree branches...")
            self.treeWidget.topLevelItem(0).setText(0, _translate("LinkDialog", "Project"))
            logging.info("+ Project.")
            self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("LinkDialog", "Books"))
            logging.info("-+ Books")
        except Exception as e:
            logging.error(e)

    def UpdateEndpoint(self,e,col):
        self.endpoint = e
        logging.info("Endpoint changed.")
        logging.info(e)

    def LinkSelected(self):
        # handle the selection
        logging.info("Link target selected.")
        try:
            logging.info(self.endpoint)
            linktype = self.endpoint.whatsThis(1)
            logging.info("Type: %s" % linktype)
            linkid = self.endpoint.data(1,QtCore.Qt.UserRole)
            logging.info("Target ID: %i" % linkid)
            if linktype == 'Scene' or linktype == 'Metadata Entry':
                if linktype == 'Metadata Entry':
                    linkid += 900000
                self.done(linkid)
        except Exception as e:
            logging.error(e)

    def RegenProjectTree(self):
        # rebuilds the project tree from the DB
        #check:ok
        # A/N: this is downright excessive but it works
        _translate = QtCore.QCoreApplication.translate
        # populate tree
        # books
        # keys: id, title, order, type
        if self.type != 'Scene':
            logging.info("Growing Books subtree...")
            booktree = self.pjm.GetBookTree()
            logging.info("Retrieved.")
            logging.info("Books...")
            self.treeWidget.itemBookList = {}
            for b in booktree['Books']:
                logging.info(b)
                self.treeWidget.itemBookList[b['id']] = QtWidgets.QTreeWidgetItem(self.treeWidget.itemBooks)
                self.treeWidget.itemBookList[b['id']].setData(1,QtCore.Qt.WhatsThisRole,b['type'])
                self.treeWidget.itemBookList[b['id']].setData(1,QtCore.Qt.InitialSortOrderRole,b['order'])
                self.treeWidget.itemBookList[b['id']].setData(1,QtCore.Qt.UserRole,b['id'])
                self.treeWidget.itemBookList[b['id']].setExpanded(True)
                self.treeWidget.itemBookList[b['id']].setText(0, _translate("LinkDialog", b['title']))
            logging.info(self.treeWidget.itemBookList.keys())

            # + 'book' key
            logging.info("Chapters...")
            self.treeWidget.itemChapterList = {}
            for c in booktree['Chapters']:
                logging.info(c)
                self.treeWidget.itemChapterList[c['id']] = QtWidgets.QTreeWidgetItem(self.treeWidget.itemBookList[c['book']])
                self.treeWidget.itemChapterList[c['id']].setData(1,QtCore.Qt.WhatsThisRole,c['type'])
                self.treeWidget.itemChapterList[c['id']].setData(1,QtCore.Qt.InitialSortOrderRole,c['order'])
                self.treeWidget.itemChapterList[c['id']].setData(1,QtCore.Qt.UserRole,c['id'])
                self.treeWidget.itemChapterList[c['id']].setExpanded(True)
                self.treeWidget.itemChapterList[c['id']].setText(0, _translate("LinkDialog", c['title']))
                self.treeWidget.itemChapterList[c['id']].setFlags(QtCore.Qt.ItemIsEnabled)
            logging.info(self.treeWidget.itemChapterList.keys())

            # + 'chapter' key
            logging.info("Scenes...")
            self.treeWidget.itemSceneList = {}
            for s in booktree['Scenes']:
                logging.info(s)
                self.treeWidget.itemSceneList[s['id']] = QtWidgets.QTreeWidgetItem(self.treeWidget.itemChapterList[s['chapter']])
                self.treeWidget.itemSceneList[s['id']].setData(1,QtCore.Qt.WhatsThisRole,s['type'])
                self.treeWidget.itemSceneList[s['id']].setData(1,QtCore.Qt.InitialSortOrderRole,s['order'])
                self.treeWidget.itemSceneList[s['id']].setData(1,QtCore.Qt.UserRole,s['id'])
                self.treeWidget.itemSceneList[s['id']].setExpanded(True)
                self.treeWidget.itemSceneList[s['id']].setText(0, _translate("LinkDialog", s['title']))
                self.treeWidget.itemSceneList[s['id']].setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
            logging.info(self.treeWidget.itemSceneList.keys())
        else:
            logging.info("Scene-type origin. Skipping Book subtree...")
        # metadata
        logging.info("Growing Metadata subtree...")
        metatree = self.pjm.GetMetaTree()

        # set root category
        logging.info("Metadata Root...")
        self.treeWidget.itemTypeList = {}
        logging.info(metatree['Types'][0])
        self.treeWidget.itemTypeList[metatree['Types'][0]['id']] = QtWidgets.QTreeWidgetItem(self.treeWidget.itemProject)
        self.treeWidget.itemTypeList[metatree['Types'][0]['id']].setData(1,QtCore.Qt.WhatsThisRole,metatree['Types'][0]['type'])
        self.treeWidget.itemTypeList[metatree['Types'][0]['id']].setData(1,QtCore.Qt.UserRole,metatree['Types'][0]['id'])
        self.treeWidget.itemTypeList[metatree['Types'][0]['id']].setExpanded(True)
        self.treeWidget.itemTypeList[metatree['Types'][0]['id']].setText(0, _translate("LinkDialog", metatree['Types'][0]['label']))
        logging.info(self.treeWidget.itemTypeList.keys())

        # set child categories
        # keys: id, parent, label, type
        logging.info("Metadata Types...")
        for t in metatree['Types'][1:]:
            logging.info(t)
            self.treeWidget.itemTypeList[t['id']] = QtWidgets.QTreeWidgetItem(self.treeWidget.itemTypeList[t['parent']])
            self.treeWidget.itemTypeList[t['id']].setData(1,QtCore.Qt.WhatsThisRole,t['type'])
            self.treeWidget.itemTypeList[t['id']].setData(1,QtCore.Qt.UserRole,t['id'])
            self.treeWidget.itemTypeList[t['id']].setExpanded(True)
            self.treeWidget.itemTypeList[t['id']].setText(0, _translate("LinkDialog", t['label']))
            self.treeWidget.itemTypeList[t['id']].setFlags(QtCore.Qt.ItemIsEnabled)
        logging.info(self.treeWidget.itemTypeList.keys())

        # set metadata entries
        # keys: id, name, cat_id, type
        logging.info("Metadata Entries...")
        self.treeWidget.itemEntryList = {}
        for e in metatree['Entries']:
            logging.info(e)
            self.treeWidget.itemEntryList[e['id']] = QtWidgets.QTreeWidgetItem(self.treeWidget.itemTypeList[e['cat_id']])
            self.treeWidget.itemEntryList[e['id']].setData(1,QtCore.Qt.WhatsThisRole,e['type'])
            self.treeWidget.itemEntryList[e['id']].setData(1,QtCore.Qt.UserRole,e['id'])
            self.treeWidget.itemEntryList[e['id']].setExpanded(True)
            self.treeWidget.itemEntryList[e['id']].setText(0, _translate("LinkDialog", e['name']))
            self.treeWidget.itemEntryList[e['id']].setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        logging.info(self.treeWidget.itemEntryList.keys())
        logging.info("Tree regrown.")