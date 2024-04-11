import OpenOPC
import Tableview
import testaddchart3
import choseProject
import maintest
import pywintypes
import sys
import os
import glob
import numpy as np
from PIL import Image
from QlabelDrag import DraggableLabel_1
from compent import CustomComponent
from maintest import Ui_MainWindow
from collections import deque
from random import randint
import pyqtgraph  as pg
import win32timezone
from PyQt5 import QtWidgets,uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
from PyQt5.QtWidgets import QApplication, QDialog,QTableWidget,QTableWidgetItem,QGridLayout,QSizePolicy,QVBoxLayout, QTextEdit,QHBoxLayout,QLabel,QWidget
from PyQt5.QtCore import QTimer,QTime,Qt,QPoint,pyqtSignal,QEvent,QMimeData,QByteArray,QBuffer
from PyQt5.QtGui import QPixmap,QDrag,QImage,QMouseEvent
#opc服务器连接
opc = OpenOPC.client()
opcserv = 'Matrikon.OPC.Simulation.1'
opc.connect(opcserv)
#print(opc.info())

TAG1 = ['simulated_1.TAG1']
TAG2 = ['simulated_1.TAG2']
TAGS = [TAG1,TAG2]
data_list = []
time_list = []
name_list = []
que_list = []
data_item=[]
name_item=[]
que_item = []
time_item = []
#下面两个是图像的数组
x_list = []
y_list = []
#y_deque =  deque(maxlen=50)#使用deque方法，设置最大长度为50
#标志位定义
#current_str = ""
class MainDialog(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(MainDialog,self).__init__(parent)
        self.ui = maintest.Ui_MainWindow()
        self.ui.setupUi(self)
        #形参在这里定义
        self.current_str = ""
        self.y_deque = deque(maxlen=50)  # 使用deque方法，设置最大长度为50
        self.log_flag = None
        #实例化，不想重新在ui界面中写槽函数就直接这里实例化
        self.ui.radioButton.toggled.connect(lambda:self.radiobutton(self.ui.radioButton))
        self.layout = QVBoxLayout(self.ui.tab)
        self.textEdit = QTextEdit(self.ui.tab)#实例化一个textedit来实现日志功能
        self.layout.addWidget(self.textEdit)
        self.ui.tabWidget.setTabText(0,"Log日志")
        self.ui.tabWidget.setTabText(1,"位号数据图")
        #实例化一个widget里面的label来存放拉过来的image
        self.textLabel = QLabel(self)
        self.textLabel.setPixmap(QPixmap())  # 初始化为空图
        self.textLabel.hide()  # 初始隐藏标签
        self.drag_start_position = QPoint()
        self.drag_position = QPoint()
        self.dragging = False
        self.setAcceptDrops(True)
        #实例化多个label
        self.labels = []
        #拖拽实例化，设置一个组件来试试
        '''
        self.layout_image = QVBoxLayout(self.ui.widget)
        self.image_path = "tiaojiefa.png"
        self.custom_component = CustomComponent(self.image_path)
        self.layout_image.addWidget(self.custom_component)
        self.drag_position = QPoint()
        self.setAcceptDrops(True)
        '''
        '''使用PlotWiget来绘画失败
        loade = QUiLoader()
        loade.registerCustomWidget(pg.PlotWidget)  # 注册PlotWidget类

        self.x = list(range(50))
        self.y = list(range(50))#设置x，y
        self.ui.graphicsView.setStyleSheet("background-color: rgb(255, 255, 255);")
        #self.ui.graphicsView.setLabel('bottom', '时间', **styles)
        self.ui.graphicsView.setWindowTitle("选中当前Flag值")
        #self.ui.graphicsView.plot(x,y)
        #self.ui.graphicsView.setLabel('left', '值', **styles)  # 设置左边Y的标签名字为功率
        #self.ui.graphicsView.showGrid(x=True, y=True)  # X轴和Y轴的网格显示
        #self.my_line = self.ui.graphicsView.
        '''#接下来使用pg来画图
        pg.setConfigOption('background','#f0f0f0')
        pg.setConfigOption('foreground', 'black')#坐标轴变黑
        self.pic = pg.PlotWidget()
        #self.curve = self.pic.plot(pen='r', symbol='o',title="当前Flag的值")
        pen = pg.mkPen(color='r', width=3)  # 红色，线宽3
        self.curve = self.pic.plot(pen=pen, title="当前Flag的值")  # 返回一条曲线
        self.pic.setXRange(0, 50)
        self.pic.setYRange(0, 100)
        self.pic.setWindowTitle("测试图")

        #self.layout = QGridLayout(self.ui.widget)
        self.layout = QGridLayout(self.ui.tab_2)
        #self.layout = QGridLayout(self.ui.graphicsView)
        self.layout.addWidget(self.pic)
        self.pic.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        #self.layout.addWidget(self.pic)
        self.set_timer()
        print("界面初始化成功")
    def radiobutton(self,button):
        if button.isChecked():
            print("LOG日志已打开")
            self.log_flag = True
            self.textEdit.append("LOG日志已打开")
        else:
            print("LOG日志已关闭")
            self.log_flag = False
            self.textEdit.append("LOG日志已关闭")
    def set_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.draw)
        self.timer.start(500)  # 这里是毫秒，2s触发一次

    def draw(self):
        #print(self.ui.comboBox.currentIndexChanged)
        self.str = self.ui.comboBox.currentText()
        if self.str != self.current_str:
            self.y_deque.clear()
            #for item in self.pic.items():
                #self.pic.removeItem(item)
            self.current_str = self.str
            print("不同")
            #print(self.current_str)
        self.y,self.quality,self.x = opc.read(self.str)
        #y_list.append(self.y)
        if self.str == "":
            print("请选择Flag")
        else:
            self.y_deque.append(self.y)
            x_list.append(self.x)
            '''这样写有弊端，这样在i==50时候，找不到；可以换成y_list = y_list[1:51]来进行列表切片，但是这样占内存，使用deque方法
            if len(y_list)>50:
                for i in range(0,51):
                    y_list[i] = y_list[i+1]
            '''
            y_list = list(self.y_deque)
            #print(y_list)
            y_array = np.array(y_list, dtype=float)
            y_finite = y_array[np.isfinite(y_array)]  # 检查数组中是否有非有限值（例如，NaN 或无穷大）
            print(y_finite)
            self.curve.setData(y_finite)
            self.pic.update()
        #x = opc[]
        #self.curve.setData(y)  # 曲线设置数据
    def queryTag(self):
        j=0
        i=0
        print("已经进入查询函数")
        #print(data_list[0])
        #for i in range(len(data_list)-1):
            #data_item[i].setText(str(data_list[i]))
        for i in range(len(data_list)):
            #data_item[i].QtWidgets.QTableWidgetItem(str(data_list[i]))
            data_item.append(QtWidgets.QTableWidgetItem(str(data_list[i])))
            name_item.append(QtWidgets.QTableWidgetItem(str(name_list[i])))
            que_item.append(QtWidgets.QTableWidgetItem(str(que_list[i])))
            time_item.append(QtWidgets.QTableWidgetItem(str(time_list[i])))
            if self.log_flag == True:
                text_to_display = f"位号为{name_list[i]}，值为{data_list[i]}，质量{que_list[i]}于{time_list[i]}添加成功"
                self.textEdit.append(text_to_display)

        for j in range(2):
            self.ui.comboBox.addItem(name_list[j])
            if self.log_flag == True:
                self.textEdit.append("Flag已加入目录")
            self.current_str = name_list[0]
            #current_str = name_list[0]
            #print(current_str)
            self.ui.tableWidget.setItem(j,0,name_item[j])
            self.ui.tableWidget.setItem(j,1,data_item[j])
            self.ui.tableWidget.setItem(j,2,que_item[j])
            self.ui.tableWidget.setItem(j,3,time_item[j])
            if self.log_flag == True:
                self.textEdit.append("表格更新成功")
            #print(j)
    def clearText(self):
        row = self.ui.tableWidget.rowCount()
        m = 0
        column = self.ui.tableWidget.columnCount()
        for m in range(0,row):
            for n in range(0,column):
                self.ui.tableWidget.takeItem(m,n)
        if self.log_flag == True:
            self.textEdit.append("界面清除成功")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.textLabel.geometry().contains(event.pos()):
                self.dragging = True
                self.drag_start_position = event.pos() - self.textLabel.pos()
                #self.drag_start_position = event.pos()
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging and event.buttons() & Qt.LeftButton:
            # 计算新的位置并移动textLabel
            new_pos = event.pos() - self.drag_start_position
            self.textLabel.move(new_pos)
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def choseproject(self):
        chose_window.show()
    def dropEvent(self, event):
        print(f'event.mimeData().hasImage()的值是{event.mimeData().hasImage()}')
        if event.mimeData().hasImage():
            # 获取图像数据并处理
            image = QImage.fromData(event.mimeData().imageData())
            pixmap = QPixmap.fromImage(image)
            # 将 pixmap 添加到 widget 中，设置 QLabel 的 pixmap
            #self.label.setPixmap(pixmap)

            # self.textLabel.setPixmap(pixmap)
            # self.textLabel.resize(pixmap.size())
            # self.textLabel.move(event.pos() - self.drag_start_position)
            # self.textLabel.show()
            # event.acceptProposedAction()

            #label = QLabel(self)
            label = DraggableLabel_1(self)
            label.setPixmap(pixmap)
            label.resize(pixmap.size())
            label.move(event.pos() - self.drag_start_position)
            label.show()
            self.labels.append(label)

            event.acceptProposedAction()

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.acceptProposedAction()
    def dragMoveEvent(self, event):
        if event.mimeData().hasImage():
            event.acceptProposedAction()
    def clearproject(self):
        print("已进入删除控件状态")
        for label in self.labels:
            if label.is_selected:
                label.hide()
                label.is_selected = False  # 清除选中状态
i=0
#创造一个来拖拽已经放入到mainwindows的类
class DraggableLabel(QLabel):
    def __init__(self, parent=None):
        super(DraggableLabel, self).__init__(parent)
        self.setAcceptDrops(True)
        self.drag_start_position = QPoint()
        image = QImage.fromData(event.mimeData().imageData())
        pixmap = QPixmap.fromImage(image)
        # 设置label的图像
        #pixmap = QPixmap(image_path)
        self.setPixmap(pixmap)
        self.resize(pixmap.size())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        delta = event.pos() - self.drag_start_position
        new_pos = self.pos() + delta
        self.move(new_pos)
class ChoseDialog(QDialog):
    image_selected = pyqtSignal(str)  # 定义一个信号，用于发送图片路径
    def __init__(self, parent=None):
        super(ChoseDialog, self).__init__(parent)
        self.uidia = choseProject.Ui_Dialog()
        self.uidia.setupUi(self)
        #进行各个控件对象实例化
        self.image_folder_path_1 = ".\Process Icons\Process Icons\Columns_1"
        self.image_folder_path_2 = ".\Process Icons\Process Icons\Heat Exchange_1"
        self.image_folder_path_3 = ".\Process Icons\Process Icons\Pumps_1"
        self.image_folder_path_4 = ".\Process Icons\Process Icons\Compressors_1"
        self.image_folder_path_5 = ".\Process Icons\Process Icons\Reactors_1"
        self.image_folder_path_6 = ".\Process Icons\Process Icons\Pipes and Fittings_1"
        self.image_folder_path_7 = ".\Process Icons\Process Icons\LNG"
        self.image_path = glob.glob(os.path.join(self.image_folder_path_1, "*.png"))
        self.image_paths = self.image_path
        #self.image_paths = glob.glob(os.path.join(self.image_folder_path_1, "*.png"))
        #self.image_paths = [".\Process Icons\Process Icons\Columns\Absorber-1.png","tiaojiefa.png","tiaojiefa.png","tiaojiefa.png","tiaojiefa.png","tiaojiefa.png"]
        self.creatLable()
        #self.labels = []#用于储存后面的Qlabel实例
    def choseproject_1(self):
        self.image_paths = glob.glob(os.path.join(self.image_folder_path_1, "*.png"))
        self.refreshImageLabels(self.image_paths)
        #self.creatLable()
    def choseproject_2(self):
        #self.image_path.clear()
        self.image_paths = glob.glob(os.path.join(self.image_folder_path_2, "*.png"))
        self.refreshImageLabels(self.image_paths)
    def choseproject_3(self):
        self.image_paths = glob.glob(os.path.join(self.image_folder_path_3, "*.png"))
        self.refreshImageLabels(self.image_paths)
        #self.creatLable()
    def choseproject_4(self):
        self.image_paths = glob.glob(os.path.join(self.image_folder_path_4, "*.png"))
        self.refreshImageLabels(self.image_paths)
        #self.creatLable()
    def choseproject_5(self):
        self.image_paths = glob.glob(os.path.join(self.image_folder_path_5, "*.png"))
        self.refreshImageLabels(self.image_paths)
        #self.creatLable()
    def choseproject_6(self):
        self.image_paths = glob.glob(os.path.join(self.image_folder_path_6, "*.png"))
        self.refreshImageLabels(self.image_paths)
        #self.creatLable()
    def choseproject_7(self):
        self.image_paths = glob.glob(os.path.join(self.image_folder_path_7, "*.png"))
        self.refreshImageLabels(self.image_paths)
        #self.creatLable()
    def creatLable(self):
        #self.layout = QGridLayout(self.uidia.widget)
        #self.layout = QGridLayout(self.uidia.scrollArea)
        self.uidia.scrollArea.setWidgetResizable(True)
        widget = QWidget()
        self.uidia.scrollArea.setWidget(widget)
        self.layout = QGridLayout(widget)
        row = 0
        col = 0
        for image_path in self.image_paths:
            image_label = QLabel()
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(100,100,Qt.KeepAspectRatio)
            #scaled_pixmap = pixmap.scaled(100,100)
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(image_label,row,col)
            image_label.setMouseTracking(True)  # 启用鼠标追踪
            #image_label.clicked.connect(lambda checked, path=image_path: self.on_image_clicked(path))  # 双击事件
            image_label.installEventFilter(self)  # 安装事件过滤器以捕获拖动事件
            #self.labels.append(image_label)
            col += 1
            if col >= 3:
                row += 1
                col = 0
        widget.adjustSize()
        #self.uidia.scrollArea.setMinimumSize(self.layout.sizeHint())
        #self.uidia.scrollArea.adjustSize()
        #self.setMinimumSize(scaled_pixmap.size())
        #self.uidia.widget.setMinimumSize(self.layout.sizeHint())
        #self.uidia.widget.adjustSize()
    def refreshImageLabels(self, new_image_paths):
        # 清除布局中的所有控件
        for i in reversed(range(self.layout.count())):
            item = self.layout.takeAt(i)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

                # 初始化行和列计数器
        row = 0
        col = 0

        # 根据新的图片路径列表重新创建QLabel
        for image_path in new_image_paths:
            image_label = QLabel()
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setMouseTracking(True)
            image_label.installEventFilter(self)

            # 将QLabel添加到布局中
            self.layout.addWidget(image_label, row, col)

            # 更新列和行计数器
            col += 1
            if col >= 4:
                row += 1
                col = 0

                # 调整布局和窗口大小以适应新的控件
        widget.adjustSize()
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self.drag_start_position = event.pos()
                return True
        elif event.type() == QEvent.MouseMove:
            if not (event.buttons() & Qt.LeftButton):
                return False
            if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
                return False
            #在此之前创造一个buffer来储存图片
            # 创建一个 QBuffer 并设置其为写模式，将 QPixmap 转换为 QImage 并保存到 QBuffer，并且从 QBuffer 中获取 QByteArray
            buffer = QBuffer()
            buffer.open(QBuffer.WriteOnly)
            image = obj.pixmap().toImage()
            image.save(buffer, "PNG")
            byte_array = buffer.data()

            # 创建 QMimeData 对象，并设置要传输的数据
            mime_data = QMimeData()
            mime_data.setImageData(byte_array)

            # 创建 QDrag 对象并设置 MimeData
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setPixmap(obj.pixmap())  # 设置拖放时的图标
            drag.setHotSpot(event.pos())  # 设置鼠标热点的位置

            # 执行拖放操作
            if drag.exec_(Qt.CopyAction | Qt.MoveAction) == Qt.MoveAction:
                # 如果操作是移动，则可以从界面上移除 QLabel
                # 这里可以添加移除 QLabel 的逻辑
                pass

            return True
        return super(ChoseDialog, self).eventFilter(obj, event)

    def on_image_clicked(self, path):
        self.image_selected.emit(path)  # 发送图片路径信号
if __name__ == '__main__':
    #while(True):
        #value_1,que_1,time_1 = opc.read(TAG1, group='Group0', update=10)
        #value_2,que_2,time_2 = opc.read(TAG2, group='Group0', update=10)
        #data_list.append(value_1),data_list.append(value_2)
        #que_list.append(que_1),que_list.append(que_2)
    for name, value, quality, time in opc.iread(['simulated_1.TAG1', 'simulated_1.TAG2']):
        name_list.append(name)
        data_list.append(value)
        que_list.append(quality)
        time_list.append(time)
    #print(data_list)
    #print(name_list)
    #print(que_list)
    #print(time_list)
    app = QApplication(sys.argv)
    window = MainDialog()#实例化Form
    chose_window = ChoseDialog()
    '''
    while (True):
        if ui.comboBox.currentText() != current_str:
            y_deque.clear()
            for item in pic.items():
                pic.removeItem(item)
    '''
    window.show()
    #app.exec()
    sys.exit(app.exec_())
