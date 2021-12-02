from json.decoder import JSONDecodeError
import sys
import json
import collections #容器的資料型態
import argparse #解析參數
import jsonpy
import os
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
try:
    from PyQt5.QtCore import QstringList
except ImportError:
    QstringList = list

class JsonItem(QtWidgets.QMainWindow):
    def __init__(self):
        super(JsonItem,self).__init__()
        self.ui = jsonpy.Ui_MainWindow()
        self.ui.setupUi(self)
        filenames = QstringList()
        self.filenames = filenames#儲存list用
        #self.ui.treeWidget.header().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        #selfmodel = self.ui.treeWidget.selectionModel()
        #selfmodel.selectionChanged.connect()
        self.ui.open.clicked.connect(self.open_file)#定義 buttons
        self.ui.save.clicked.connect(self.save_file)
        self.ui.saveas.clicked.connect(self.save_as)
        self.ui.reset.clicked.connect(self.reset)
        self.ui.findbt.clicked.connect(self.find_data)
        self.ui.find.returnPressed.connect(self.find_data)
        

    def open_file(self):
        #files = QtWidgets.QFileDialog()
        #files.setFileMode(QtWidgets.QFileDialog.AnyFile)
        #if files.exec_():
            #filename = files.selectedFiles()
        try:
                filename=QtWidgets.QFileDialog.getOpenFileName(self,'Open file','./','JSON(*.json)')
                with open(filename[0],'r') as file:
                    data = json.load(file)
                    data1 = json.dumps(data, sort_keys=True,indent=3)#sort_key:是否排序，indent:格式編排等級
                    self.ui.textEdit.setText(data1)
                    #jfile = open(filename[0])
                    #jdata = json.load(jfile,object_pairs_hook=collections.OrderedDict)#有順序的傳遞函數
                    #root = QtWidgets.QTreeWidgetItem(['root'])
        except json.decoder.JSONDecodeError:
                QtWidgets.QMessageBox.warning(self,'Hint','Not json format file.',QtWidgets.QMessageBox.Yes)

        except Exception as e :
                print(e)
                QtWidgets.QMessageBox.warning(self,'Hint','Error open.',QtWidgets.QMessageBox.Yes)

    def save_file(self):
        filename = self.filenames
        update = self.ui.textEdit.toPlainText()
        try:
            data = json.loads(update)
            with open(str(filename[0]),'w') as file: #w：寫入
                file.write(update)
                file.close()
                QtWidgets.QMessageBox.information(self,'Success','File saved.',QtWidgets.QMessageBox.Yes)
        except IndexError:
            QtWidgets.QMessageBox.warning(self,'Hint','Click save as first.',QtWidgets.QMessageBox.Yes)
        except json.decoder.JSONDecodeError:
            QtWidgets.QMessageBox.warning(self,'Hint','Wrong json format.',QtWidgets.QMessageBox.Yes)
        except Exception as e:
            print(e)
            QtWidgets.QMessageBox.warning(self,'Hint','Error',QtWidgets.QMessageBox.Yes)

    def save_as(self):
        try:
            text = self.ui.textEdit.toPlainText()
            data = json.loads(text)
            name = QtWidgets.QFileDialog.getSaveFileName(self,'Save file','','JSON(*.json)')
            filename = str(name[0])
            file = open(filename,'w')
            file.write(text)
            file.close()
            QtWidgets.QMessageBox.information(self,'Success','File saved!',QtWidgets.QMessageBox.Yes)
        except json.decoder.JSONDecodeError:
            QtWidgets.QMessageBox.warning(self,'Hint','Wrong json format.',QtWidgets.QMessageBox.Yes)
        
        except Exception as e:
            print(e)
            QtWidgets.QMessageBox.warning(self,'Hint','Error.',QtWidgets.QMessageBox.Yes)

    def reset(self):
        QtCore.QCoreApplication.quit()                              #sys.executable返回python,當前系統的路徑
        status = QtCore.QProcess.startDetached(sys.executable,sys.argv)#sys.argv傳遞到python參數列表
    
    def recurse_jdata(self,jdata,treewidget):
        if isinstance(jdata, dict):#isinstance判斷jdata是否為dict
            for key, val in jdata.items():
                self.tree_and_row(key,val,treewidget)
        elif isinstance(jdata,list):
            for i ,val in enumerate(jdata):
                key = str(i)
                self.tree_and_row(key,val,treewidget)

    def tree_and_row(self,key,val,treewidget):
        if isinstance(val,dict) or isinstance(val,list):
            row_item = QtWidgets.QTreeWidgetItem([key])
            self.recurse_jdata(val, row_item)
        else:
            row_item = QtWidgets.QTreeWidgetItem([key,str(val)])
        treewidget.addChild(row_item)#新增在tree上

    def find_data(self):
        find_str = self.ui.find.text()

        if find_str == '':
            return #結束函式，回傳一None值
        items = self.ui.textEdit(find_str,QtCore.Qt.MatchExactly)
        if find_str != self.find_str:
            self.find_str = find_str





class JsonView(QtWidgets.QMainWindow):
    def __init__(self):
        super(JsonView,self).__init__()
        jsonview = JsonItem()
        self.setCentralWidget(jsonview)
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    jsonviewer = JsonView()
    sys.exit(app.exec_())