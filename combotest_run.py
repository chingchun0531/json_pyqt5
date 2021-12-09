import json
from json.decoder import JSONDecodeError
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.sip import delete

from widgetwindow import *

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.openbtn.clicked.connect(self.Openfile)
        self.ui.g1.activated.connect(self.g1_changed)
        self.ui.num.activated.connect(self.num_changed)
        self.ui.g2.activated.connect(self.g2_changed)#listwidget
        self.ui.g3.activated.connect(self.g3_changed)#listwidget
        self.ui.g4.activated.connect(self.g4_changed)#listwidget
        self.ui.num1.activated.connect(self.num1_changed)
        self.ui.g5.activated.connect(self.g5_changed)#listwidget
        self.ui.num2.activated.connect(self.num2_changed)
        self.ui.newbtn.clicked.connect(self.new_reset)
        self.ui.savebtn.clicked.connect(self.save_changed)
        self.ui.g2.installEventFilter(self)
        self.ui.g4.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.ContextMenu and source is self.ui.g2:
            menu = QtWidgets.QMenu()
            add1 = menu.addAction('Addtext')
            add2 = menu.addAction('Addlist')
            add3 = menu.addAction('AddInt')
            copy = menu.addAction('Copy')
            dele = menu.addAction('Delete')
            action = menu.exec_(self.mapToGlobal(event.pos()))#鼠標的位置
            if action == add1:
                k1,n1 = QtWidgets.QInputDialog.getText(self,'Input','Add key:')
                v1,n2 = QtWidgets.QInputDialog.getText(self,'Input','Add val:')
                if n1 and n2:
                    data = {k1:v1}
                    self.data[self.ui.g1.currentItem().text()][int(self.ui.num.currentText())].update(data)
                    update = json.dumps(self.data,indent=3)
                    filename = self.filenames
                    with open(filename[0],'w') as file:#write寫入filename[0]:儲存位置
                        file.write(update)
                        file.close()
                        self.ui.textEdit.setText(update)
                        self.ui.g2.addItem(k1)
            elif action == add2:
                k2,n3 = QtWidgets.QInputDialog.getText(self,'Input','Add key:')
                v2,n4 = QtWidgets.QInputDialog.getText(self,'Input','Add val:')
                if n3 and n4:
                    tv2 = list(eval(v2))
                    data1 = {k2:tv2}
                    self.data[self.ui.g1.currentItem().text()][int(self.ui.num.currentText())].update(data1)
                    update = json.dumps(self.data,indent=3)
                    filename = self.filenames
                    with open(filename[0],'w') as file:#write寫入filename[0]:儲存位置
                        file.write(update)
                        file.close()
                        self.ui.textEdit.setText(update)
            elif action == dele:
                del self.data[self.ui.g1.currentItem().text()][int(self.ui.num.currentText())][self.ui.g2.currentItem().text()]
                item_index = self.ui.g2.currentRow()
                self.ui.g2.takeItem(item_index)
                self.ui.t2.clear()
                update = json.dumps(self.data,indent=3)
                filename = self.filenames
                with open(filename[0],'w') as file:#write寫入filename[0]:儲存位置
                        file.write(update)
                        file.close()
                        self.ui.textEdit.setText(update)

        return super().eventFilter(source, event)

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
            self.ui.g1.addItem(key)#顯示config_set&switch
            self.ui.textEdit.setText(json.dumps(data,indent=3))
        
    
    def g1_changed(self,g1_index):
        self.ui.g2.clear()
        self.ui.g3.clear()
        self.ui.g4.clear()
        self.ui.g5.clear()
        self.ui.num.clear()
        self.ui.num1.clear()
        self.ui.num2.clear()
        self.ui.t1.setText('')
        self.ui.t2.setText('')
        self.ui.t3.setText('')
        self.ui.t4.setText('')
        try:
            if type(self.data[self.ui.g1.item(g1_index.row()).text()]) != list and type(self.data[self.ui.g1.item(g1_index.row()).text()])!= dict:
               self.ui.t1.setText(self.data[self.ui.g1.item(g1_index.row()).text()])
            else:
                for i,j in enumerate(self.data[self.ui.g1.currentItem().text()]):
                    self.ui.num.addItem(str(i))
                    self.g1_index = self.data[self.ui.g1.item(g1_index.row()).text()][int(self.ui.num.currentText())]#list

        except Exception as e:
            print('Error:',e)

    def num_changed(self):
        self.ui.g2.clear()
        self.ui.g3.clear()
        self.ui.g4.clear()
        self.ui.g5.clear()
        self.ui.num1.clear()
        self.ui.num2.clear()
        self.ui.t2.setText('')
        self.ui.t3.setText('')
        self.ui.t4.setText('')
        for key,val in self.data[self.ui.g1.currentItem().text()][int(self.ui.num.currentText())].items():
              self.ui.g2.addItem(key)
              self.g1_index = self.data[self.ui.g1.currentItem().text()][int(self.ui.num.currentText())]

    def g2_changed(self,g2_index):#選項AI_features
        self.ui.g3.clear()
        self.ui.g4.clear()
        self.ui.g5.clear()
        self.ui.num1.clear()
        self.ui.num2.clear()
        self.ui.t2.setText('')
        self.ui.t3.setText('')
        self.ui.t4.setText('')            
        #QtWidgets.QMessageBox.information(self,'Hint','choose:'+self.ui.listWidget.item(g2_index.row()).text())
        try:
            if type(self.g1_index[self.ui.g2.item(g2_index.row()).text()]) != list and type(self.g1_index[self.ui.g2.item(g2_index.row()).text()])!= dict:
                self.ui.t2.setText(str(self.g1_index[self.ui.g2.item(g2_index.row()).text()]))
            else:
              for key,val in self.g1_index[self.ui.g2.item(g2_index.row()).text()].items():
                self.ui.g3.addItem(key)
                self.g2_index = self.g1_index[self.ui.g2.item(g2_index.row()).text()]
        except Exception as e:
            print('Error:',e)

    def g3_changed(self,g3_index):#選項HD
        self.ui.g4.clear()
        self.ui.g5.clear()
        self.ui.num1.clear()
        self.ui.num2.clear()
        self.ui.t4.setText('')
        try:
          for key,val in self.g2_index[self.ui.g3.currentItem().text()].items():
            self.ui.g4.addItem(key)
            self.g3_index = self.g2_index[self.ui.g3.currentItem().text()]
        except Exception as e:
            print('Error:',e)

    def g4_changed(self,g4_index):#顯示ROI再底下(可能有list[]要再拆解)
        self.ui.num1.clear()
        self.ui.g5.clear()
        self.ui.num2.clear()
        self.ui.t3.setText('')
        self.ui.t4.setText('')
        try:
            if type(self.g3_index[self.ui.g4.currentItem().text()]) != list and type(self.g3_index[self.ui.g4.currentItem().text()]) != dict:
                self.ui.t3.setText(str(self.g3_index[self.ui.g4.item(g4_index.row()).text()]))
                self.g4_index = self.g3_index[self.ui.g4.item(g4_index.row()).text()]
            elif type(self.g3_index[self.ui.g4.currentItem().text()]) == list:
              for i,j in enumerate(self.g3_index[self.ui.g4.currentItem().text()]):
                self.ui.num1.addItem(str(i))
                self.g4_index = self.g3_index[self.ui.g4.currentItem().text()][int(self.ui.num1.currentText())]
            else:#dict
               for key,val in self.g3_index[self.ui.g4.currentItem().text()].items():#type:dict_item,不能為list
                  self.ui.g5.addItem(key)
                  self.g4_index = self.g3_index[self.ui.g4.currentItem().text()]
            print(self.g4_index)
        except Exception as e:
            print('Error:',e)

    def num1_changed(self):
        self.ui.g5.clear()
        self.ui.num2.clear()
        self.ui.t3.setText('')
        self.ui.t4.setText('')
        if type(self.g3_index[self.ui.g4.currentItem().text()][int(self.ui.num1.currentText())])!= list:
            for key,val in self.g4_index.items():#type:dict_item,不能為list
                self.ui.g5.addItem(key)
        else:
                self.ui.t3.setText(json.dumps(self.g3_index[self.ui.g4.currentItem().text()][int(self.ui.num1.currentText())]))

    def g5_changed(self,g5_index):
        self.ui.num2.clear()
        self.ui.t4.setText('')
        if type(self.g4_index[self.ui.g5.currentItem().text()]) != list and type(self.g4_index[self.ui.g5.currentItem().text()]) != dict:
         self.ui.t4.setText(self.g4_index[self.ui.g5.currentItem().text()])
        else:
            for i,j in enumerate(self.g4_index[self.ui.g5.currentItem().text()]):
                self.ui.num2.addItem(str(i))
                self.g5_index = self.g4_index[self.ui.g5.currentItem().text()]
            self.ui.t4.setText(json.dumps(self.g4_index[self.ui.g5.currentItem().text()],indent=3))

    def num2_changed(self):
        if type(self.g4_index[self.ui.g5.currentItem().text()][int(self.ui.num2.currentText())])==list:
            self.ui.t4.setText(json.dumps(self.g4_index[self.ui.g5.currentItem().text()][int(self.ui.num2.currentText())]))
        else:
            self.ui.t4.setText(str(self.g4_index[self.ui.g5.currentItem().text()][int(self.ui.num2.currentText())]))


    def save_changed(self):
        try:
            for key,val in self.data.items():#config_set
                if key == self.ui.g1.currentItem().text() and self.ui.t1.text()!= '' :
                    self.data[key] = self.ui.t1.text()
                    update = json.dumps(self.data,indent=3)
                    filename = self.filenames
                    with open(filename[0],'w') as file:#write寫入filename[0]:儲存位置
                        file.write(update)
                        file.close()
                        self.ui.textEdit.setText(update)
                        QtWidgets.QMessageBox.information(self,'Success','Saved Successfully.',QtWidgets.QMessageBox.Yes)

            for k1,v1 in self.g1_index.items():#AI_features
                if k1 == self.ui.g2.currentItem().text() and self.ui.t2.toPlainText() != '':
                    if type(v1) == str:
                        self.g1_index[k1] = self.ui.t2.toPlainText()
                    elif type(v1) == int:
                        self.g1_index[k1] = int(self.ui.t2.toPlainText())
                    self.data[self.ui.g1.currentItem().text()][int(self.ui.num.currentText())].update(self.g1_index)
                    update = json.dumps(self.data,indent=3)
                    filename = self.filenames
                    with open(filename[0],'w') as file:#write寫入filename[0]:儲存位置
                        file.write(update)
                        file.close()
                        self.ui.textEdit.setText(update)
                        QtWidgets.QMessageBox.information(self,'Success','Saved Successfully.',QtWidgets.QMessageBox.Yes)

            for k2,v2 in self.g3_index.items():#HD->ROI
                if k2 == self.ui.g4.currentItem().text() and self.ui.t3.toPlainText() != '':
                    if type(v2) != list:
                        if type(v2) == str:
                            self.g3_index[k2] = self.ui.t3.toPlainText()
                        elif type(v2) == int:
                            self.g3_index[k2] = int(self.ui.t3.toPlainText())
                        self.data[self.ui.g1.currentItem().text()][int(self.ui.num.currentText())][self.ui.g2.currentItem().text()][self.ui.g3.currentItem().text()].update(self.g3_index)
                    else:
                        self.g3_index[k2][int(self.ui.num1.currentText())] = list(eval(self.ui.t3.toPlainText()))
                        self.data[self.ui.g1.currentItem().text()][int(self.ui.num.currentText())][self.ui.g2.currentItem().text()][self.ui.g3.currentItem().text()].update(self.g3_index)
                    update = json.dumps(self.data,indent=3)
                    filename = self.filenames
                    with open(filename[0],'w') as file:#write寫入filename[0]:儲存位置
                        file.write(update)
                        file.close()
                        self.ui.textEdit.setText(update)
                        QtWidgets.QMessageBox.information(self,'Success','Saved Successfully.',QtWidgets.QMessageBox.Yes)

            for k3,v3 in self.g4_index.items():#ROINAME
                if k3 == self.ui.g5.currentItem().text() and self.ui.t4.toPlainText() != '':
                    if type(v3)!=list:
                        if type(v3) == str:
                            self.g4_index[k3] = self.ui.t4.toPlainText()
                        elif type(v3) == int:
                            self.g4_index[k3] = int(self.ui.t4.toPlainText())
                        self.data[self.ui.g1.currentItem().text()][int(self.ui.num.currentText())][self.ui.g2.currentItem().text()][self.ui.g3.currentItem().text()][self.ui.g4.currentItem().text()][int(self.ui.num1.currentText())].update(self.g4_index)       
                    else:
                        if type(self.g4_index[k3][int(self.ui.num2.currentText())])==list:
                            self.g4_index[k3][int(self.ui.num2.currentText())] = eval(self.ui.t4.toPlainText())
                            self.data[self.ui.g1.currentItem().text()][int(self.ui.num.currentText())][self.ui.g2.currentItem().text()][self.ui.g3.currentItem().text()][self.ui.g4.currentItem().text()][int(self.ui.num1.currentText())].update(self.g4_index)
                        else:
                            self.g4_index[k3][int(self.ui.num2.currentText())]  = float(self.ui.t4.toPlainText())
                            self.data[self.ui.g1.currentItem().text()][int(self.ui.num.currentText())][self.ui.g2.currentItem().text()][self.ui.g3.currentItem().text()][self.ui.g4.currentItem().text()].update(self.g4_index)

                    update = json.dumps(self.data,indent=3)
                    filename = self.filenames
                    with open(filename[0],'w') as file:
                        file.write(update)
                        file.close()
                        self.ui.textEdit.setText(update)
                        QtWidgets.QMessageBox.information(self,'Success','Saved Successfully.',QtWidgets.QMessageBox.Yes)

        except IndexError:
            QtWidgets.QMessageBox.warning(self,'Hint','Index error.',QtWidgets.QMessageBox.Yes)
        except JSONDecodeError:
            QtWidgets.QMessageBox.warning(self,'Hint','Not json format.',QtWidgets.QMessageBox.Yes)
        except NameError:
            QtWidgets.QMessageBox.warning(self,'Hint','Error',QtWidgets.QMessageBox.Yes)
        except SyntaxError:#語法錯誤
            QtWidgets.QMessageBox.warning(self,'Hint','Wrong input.',QtWidgets.QMessageBox.Yes)
        except ValueError:
            QtWidgets.QMessageBox.warning(self,'Hint','Value error.',QtWidgets.QMessageBox.Yes)
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