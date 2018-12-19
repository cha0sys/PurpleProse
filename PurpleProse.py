# Purple Prose: A world-building metadata management app 
# geared specifically toward fiction writing.
# Requirements: Python3.7, PyQT5.11, SQLite (Python3.7 built-in is fine), PyPandoc (any)

"""
* = done
/ = partially done
TODO:
-[/] implement sidebars
    -[/] left sidebar tree
        -[*] per-element-type context menu
        -[ ] element dragging/reorder
            -[ ] need QTreeWidget subclass reimplementing drag/drop event handlers
        -[*] element addition/deletion
        -[*] dynamic element creation from DB entries
        -[*] context menu actions
    -[ ] project stats view
    -[ ] scene stats
    -[/] scene linked entities
        -[*] add/remove entity links from tree
        -[*] add/remove entity links from right sidebar
        -[ ] add/remove entity links from entity tab
        -[*] correct link display in right sidebar
-[/] implement menubar options
-[*] finish implementing ProjectManager
"""

import sys
from PyQt5 import QtWidgets
import MainWindow
import logging
logging.basicConfig(filename='PP_runtime.log',level=logging.INFO, filemode='w')

# Main segment - PyQT5
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    frmMain = QtWidgets.QMainWindow()
    ui = MainWindow.Ui_MainWindow(frmMain)
    logging.info("UI initalized.")
    ui.setupUi()
    logging.info("UI assembled.")
    frmMain.show()
    sys.exit(app.exec_())

