# custom widget for the entity edit tab type
from PyQt5 import QtCore, QtGui, QtWidgets
import ProjectManager

import logging
logging.basicConfig(filename='PP_runtime.log',level=logging.INFO)

class tabEntityEdit (QtWidgets.QWidget):
    def __init__(self,parent,pjm=ProjectManager.ProjectManager(None),entityid=-1,type=0):
        super(tabEntityEdit , self).__init__()
        self.parent = parent
        self.pjm = pjm
        self.entityid = entityid
        self.type = type
        self.typelabel = self.pjm.GetEntityType(self.type)
        logging.info("Entity Edit tab opened.")
        logging.info("ID: %i" % entityid)
        logging.info("Type: %s" % type)
        logging.info("Building UI...")
        self.setupUI()
        logging.info("Populating fields...")
        if entityid != -1:
            self.OpenEntity()
        logging.info("Tab Ready.")

    def setupUI(self):
        self.setObjectName("tabEntityEdit_"+str(self.entityid))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblName = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblName.setFont(font)
        self.lblName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblName.setObjectName("lblName")
        self.horizontalLayout.addWidget(self.lblName)
        self.txtName = QtWidgets.QLineEdit(self)
        self.txtName.setObjectName("txtName")
        self.horizontalLayout.addWidget(self.txtName)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lblDesc = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDesc.sizePolicy().hasHeightForWidth())
        self.lblDesc.setSizePolicy(sizePolicy)
        self.lblDesc.setObjectName("lblDesc")
        self.verticalLayout_4.addWidget(self.lblDesc)
        self.txtDesc = QtWidgets.QTextEdit(self)
        self.txtDesc.setObjectName("txtDesc")
        self.verticalLayout_4.addWidget(self.txtDesc)
        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.setStretch(1, 1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblAliases = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblAliases.sizePolicy().hasHeightForWidth())
        self.lblAliases.setSizePolicy(sizePolicy)
        self.lblAliases.setObjectName("lblAliases")
        self.verticalLayout.addWidget(self.lblAliases)
        self.txtAliases = QtWidgets.QPlainTextEdit(self)
        self.txtAliases.setObjectName("txtAliases")
        self.verticalLayout.addWidget(self.txtAliases)
        self.lblRelated = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblRelated.sizePolicy().hasHeightForWidth())
        self.lblRelated.setSizePolicy(sizePolicy)
        self.lblRelated.setObjectName("lblRelated")
        self.verticalLayout.addWidget(self.lblRelated)
        self.txtRelated = QtWidgets.QPlainTextEdit(self)
        self.txtRelated.setObjectName("txtRelated")
        self.verticalLayout.addWidget(self.txtRelated)
        self.btnSave = QtWidgets.QCommandLinkButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSave.sizePolicy().hasHeightForWidth())
        self.btnSave.setSizePolicy(sizePolicy)
        self.btnSave.setObjectName("btnSave")
        self.verticalLayout.addWidget(self.btnSave)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(3, 1)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 1)
        logging.info("UI laid out.")

        self.retranslateUi()

        logging.info("Connecting signals to slots...")
        self.btnSave.clicked.connect(self.SaveEntity)
        logging.info("btnSave.clicked() connected.")
        logging.info("Slots connected.")

    def retranslateUi(self):
        logging.info("Labeling controls...")
        _translate = QtCore.QCoreApplication.translate
        self.lblName.setText(_translate("MainWindow", "Name:"))
        self.lblDesc.setText(_translate("MainWindow", "Description:"))
        self.lblAliases.setText(_translate("MainWindow", "Aliases:"))
        self.lblRelated.setText(_translate("MainWindow", "Related:"))
        self.btnSave.setText(_translate("MainWindow", "Save"))
        self.btnSave.setShortcut(_translate("MainWindow", "Ctrl+S"))

    def SaveEntity(self):
        logging.info("Saving entity...")
        ent = {'name': str(self.txtName.text()),
            'aliases': str(self.txtAliases.toPlainText()),
            'related': str(self.txtRelated.toPlainText()),
               'desc': str(self.txtDesc.toPlainText()),
               'type': self.type}
        logging.info(ent)
        if self.entityid != -1:
            self.pjm.SaveEntity(self.entityid,ent)
        else:
            self.entityid = self.pjm.NewEntity(ent)
            self.parent.lastEntity = self.entityid
        #self.parent.MainWindow.setStatusTip(QtCore.QCoreApplication.translate("MainWindow", "Saved."))
        logging.info("Saved!")

    def OpenEntity(self):
        logging.info("Loading entity...")
        ent = self.pjm.OpenEntity(self.entityid)
        logging.info("Entity data returned:")
        logging.info(ent)
        if ent != None:
            self.txtName.setText(ent['name'])
            logging.info("Name set: %s" % ent['name'])
            self.txtDesc.setText(ent['desc'])
            logging.info("Description set.")
            self.type = ent['type']
            logging.info("Type set: %i" % self.type)
            self.typelabel = self.pjm.GetEntityType(self.type)['plural']
            logging.info("Type label set: %s" % self.typelabel)
            try:
                if ent['aliases'] != None:
                    logging.info("Loading aliases...")
                    aliases = ''
                    for a in ent['aliases']:
                        logging.info(a)
                        aliases += a + '\n'
                    self.txtAliases.setPlainText(aliases)
                    logging.info("Aliases set:\n%s" % aliases)
            except Exception as err:
                logging.error("Couldn't load aliases!")
                logging.error(err)
            try:
                if ent['related_names'] != None:
                    logging.info("Loading related entities...")
                    related = ''
                    for r in ent['related_names']:
                        logging.info(r)
                        related += r + '\n'
                    self.txtRelated.setPlainText(related)
                    logging.info("Relations set:\n%s" % related)
            except Exception as err:
                logging.error("Couldn't load relations!")
                logging.error(err)

            logging.info("Loaded!")
        else:
            logging.error("tabEntityEdit: Could not open entity!")
