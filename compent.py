from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout,QHBoxLayout
from PyQt5.QtGui import QPixmap,QDrag
from PyQt5.QtCore import Qt,QPoint
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QMimeData

class CustomComponent(QWidget):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.initUI(image_path)

    def initUI(self, image_path):
        # 创建一个布局
        layout = QHBoxLayout(self)

        # 创建一个标签用于显示图片
        self.image_label = QLabel(self)
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(100,100)
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        # 将标签添加到布局中
        layout.addWidget(self.image_label)

        # 设置组件大小与图片大小相同
        self.setFixedSize(scaled_pixmap.size())

        # 启用鼠标跟踪
        self.setMouseTracking(True)
        self.drag_position = QPoint()

    def mousePressEvent(self, event):
        # 鼠标按下事件，记录开始位置
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
            # 计算部件应该移动到的位置
        delta = event.pos() - self.drag_position
        new_pos = self.pos() + delta
        # 更新部件位置
        self.move(new_pos)
        # 更新拖拽的起始位置
        #self.drag_position = event.pos()

    def mouseReleaseEvent(self, event):
        # 在鼠标释放时，不需要做任何特殊处理，因为移动已经在 mouseMoveEvent 中完成了
        pass