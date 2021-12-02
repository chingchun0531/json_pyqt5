import json
from json.decoder import JSONDecodeError
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from combotest import *

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.openbtn.clicked.connect(self.Openfile)
        self.ui.g1.activated.connect(self.g1_changed)
        self.ui.num.activated.connect(self.num_changed)
        self.ui.g2.activated.connect(self.g2_changed)
        self.ui.g3.activated.connect(self.g3_changed)
        self.ui.g4.activated.connect(self.g4_changed)
        self.ui.num1.activated.connect(self.num1_changed)
        self.ui.g5.activated.connect(self.g5_changed)
        self.ui.newbtn.clicked.connect(self.new_reset)
        self.ui.savebtn.clicked.connect(self.save_changed)

    def Openfile(self):
        try:
            filename = QtWidgets.QFileDialog.getOpenFileName(self,'Open file','','JSON(*.json)')
            self.filenames = filename
            with open(filename[0],'r') as f:
                data = json.load(f)
                data1 = json.dumps(data)
                self.data = data
        except JSONDecodeError:
            QtWidgets.QMessageBox.warning(self,'Hint','Not json format.',QtWidgets.QMessageBox.Yes)
        except Exception as e:
            print(e)
            QtWidgets.QMessageBox.warning(self,'Hint','Error.',QtWidgets.QMessageBox.Yes)
        
        for key,val in data.items():
            self.ui.g1.addItem(key,val)#顯示config_set&switch
            self.ui.textEdit.setText(json.dumps(data,indent=3))
        
    
    def g1_changed(self,g1_index):
        self.ui.g2.clear()
        self.ui.g3.clear()
        self.ui.g4.clear()
        self.ui.g5.clear()
        self.ui.num.clear()
        self.ui.num1.clear()
        self.ui.textEdit.setText('')
        self.ui.t1.setText('')
        self.ui.t2.setText('')
        self.ui.t3.setText('')
        self.ui.t4.setText('')
        try:
            if type(self.ui.g1.itemData(g1_index)) != list and type(self.ui.g1.itemData(g1_index))!= dict:
               self.ui.t1.setText(self.ui.g1.itemData(g1_index))
            else:
                for i,j in enumerate(self.data[self.ui.g1.currentText()]):
                    self.ui.num.addItem(str(i))
                    self.g1_index = self.ui.g1.itemData(g1_index)[int(self.ui.num.currentText())]#list
        except Exception as e:
            print('Error:',e)

    def num_changed(self):
        self.ui.g2.clear()
        self.ui.g3.clear()
        self.ui.g4.clear()
        self.ui.g5.clear()
        self.ui.num1.clear()
        self.ui.textEdit.setText('')
        self.ui.t2.setText('')
        self.ui.t3.setText('')
        self.ui.t4.setText('')
        for key,val in self.data[self.ui.g1.currentText()][int(self.ui.num.currentText())].items():
              self.ui.g2.addItem(key,val)
              self.ui.textEdit.setText(json.dumps(self.data[self.ui.g1.currentText()][int(self.ui.num.currentText())],indent=3))


    def g2_changed(self,g2_index):#選項AI_features
        self.ui.g3.clear()
        self.ui.g4.clear()
        self.ui.g5.clear()
        self.ui.num1.clear()
        self.ui.textEdit.setText('')
        self.ui.t2.setText('')
        self.ui.t3.setText('')
        self.ui.t4.setText('')
        try:
            if type(self.ui.g2.itemData(g2_index)) != list and type(self.ui.g2.itemData(g2_index))!= dict:
                self.ui.t2.setText(str(self.ui.g2.itemData(g2_index)))
            else:
              for key,val in self.g1_index[self.ui.g2.currentText()].items():
                self.ui.g3.addItem(key,val)
                self.g2_index = self.ui.g2.itemData(g2_index)
                self.ui.textEdit.setText(json.dumps(self.ui.g2.itemData(g2_index),indent=3))
        except Exception as e:
            print('Error:',e)

    def g3_changed(self,g3_index):#選項HD
        self.ui.g4.clear()
        self.ui.g5.clear()
        self.ui.textEdit.setText('')
        self.ui.t4.setText('')
        try:
          for key,val in self.g2_index[self.ui.g3.currentText()].items():
            self.ui.g4.addItem(key,val)
            self.ui.textEdit.setText(json.dumps(self.g2_index[self.ui.g3.currentText()],indent=3))
            self.g3_index = self.g2_index[self.ui.g3.currentText()]
            #print(self.g2_index[self.ui.g3.currentText()])
        except Exception as e:
            print('Error:',e)

    def g4_changed(self,g4_index):#顯示ROI再底下(可能有array[]要再拆解)
        self.ui.num1.clear()
        self.ui.g5.clear()
        self.ui.textEdit.setText('')
        self.ui.t3.setText('')
        self.ui.t4.setText('')
        try:
            if type(self.ui.g4.itemData(g4_index)) != list and type(self.ui.g4.itemData(g4_index)) != dict:
                self.ui.t3.setText(str(self.ui.g4.itemData(g4_index)))
            elif type(self.ui.g4.itemData(g4_index)) == list:
              for i,j in enumerate(self.g3_index[self.ui.g4.currentText()]):#type:dict_item,不能為list
                self.ui.num1.addItem(str(i))
                self.ui.textEdit.setText(json.dumps(self.ui.g4.itemData(g4_index),indent=3))
            else:
               for key,val in self.g3_index[self.ui.g4.currentText()].items():#type:dict_item,不能為list
                self.ui.g5.addItem(key,val)
                self.ui.textEdit.setText(self.g3_index[self.ui.g4.currentText()])
            self.g4_index = self.ui.g4.itemData(g4_index)[int(self.ui.num1.currentText())]
        except Exception as e:
            print('Error:',e)

    def num1_changed(self):
        self.ui.g5.clear()
        self.ui.textEdit.setText('')
        self.ui.t3.setText('')
        self.ui.t4.setText('')
        if type(self.g3_index[self.ui.g4.currentText()][int(self.ui.num1.currentText())])!= list:
            for key,val in self.g4_index.items():#type:dict_item,不能為list
                self.ui.g5.addItem(key,val)
                self.ui.textEdit.setText(json.dumps(self.g4_index, indent=3))
        else:
                self.ui.t3.setText(json.dumps(self.g3_index[self.ui.g4.currentText()][int(self.ui.num1.currentText())]))

    def g5_changed(self,g5_index):
        if type(self.ui.g5.itemData(g5_index)) != list and type(self.ui.g5.itemData(g5_index)) != dict:
         self.ui.t4.setText(self.ui.g5.itemData(g5_index))
        else:
            self.ui.t4.setText(json.dumps(self.ui.g5.itemData(g5_index),indent=3))

    def save_changed(self):
        try:
            for key,val in self.data.items():
                if key == self.ui.g1.currentText() and self.ui.t1.text()!= '' :
                    self.data[key] = self.ui.t1.text()
                    update = json.dumps(self.data,indent=3)
                    filename = self.filenames
                    with open(filename[0],'w') as file:#write寫入filename[0]:儲存位置
                        file.write(update)
                        file.close()
                        QtWidgets.QMessageBox.information(self,'Success','Saved Successfully.',QtWidgets.QMessageBox.Yes)
            for k1,v1 in self.g1_index.items():
                if k1 == self.ui.g2.currentText() and self.ui.t2.text() != '':
                    self.g1_index[k1] = self.ui.t2.text()
                    self.data[self.ui.g1.currentText()][int(self.ui.num.currentText())].update(self.g1_index)
                    update = json.dumps(self.data,indent=3)
                    filename = self.filenames
                    with open(filename[0],'w') as file:#write寫入filename[0]:儲存位置
                        file.write(update)
                        file.close()
                        QtWidgets.QMessageBox.information(self,'Success','Saved Successfully.',QtWidgets.QMessageBox.Yes)

            for k2,v2 in self.g3_index.items():
                if k2 == self.ui.g4.currentText() and self.ui.t3.text() != '':
                    self.g3_index[k2] = self.ui.t3.text()
                    self.data[self.ui.g1.currentText()][int(self.ui.num.currentText())][self.ui.g2.currentText()].update(self.g3_index)
                    update = json.dumps(self.data,indent=3)
                    filename = self.filenames
                    with open(filename[0],'w') as file:#write寫入filename[0]:儲存位置
                        file.write(update)
                        file.close()
                        QtWidgets.QMessageBox.information(self,'Success','Saved Successfully.',QtWidgets.QMessageBox.Yes)

            for k3,v3 in self.g4_index.items():
                if k3 == self.ui.g5.currentText() and self.ui.t4.text() != '':
                    self.g4_index[k3] = self.ui.t4.text()
                    self.data[self.ui.g1.currentText()][int(self.ui.num.currentText())][self.ui.g2.currentText()][self.ui.g3.currentText()][self.ui.g4.currentText()][int(self.ui.num1.currentText())].update(self.g4_index)       
                    update = json.dumps(self.data,indent=3)
                    filename = self.filenames
                    with open(filename[0],'w') as file:
                        file.write(update)
                        file.close()
                        QtWidgets.QMessageBox.information(self,'Success','Saved Successfully.',QtWidgets.QMessageBox.Yes)     

        except JSONDecodeError:
            QtWidgets.QMessageBox.warning(self,'Hint','Not json format.',QtWidgets.QMessageBox.Yes)
        except Exception as e:
            print(e)



    def new_reset(self):
        QtCore.QCoreApplication.quit()#關閉                    #sys.executable返回python,當前系統的路徑
        QtCore.QProcess.startDetached(sys.executable,sys.argv)#重啟#sys.argv傳遞到python參數列表



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())