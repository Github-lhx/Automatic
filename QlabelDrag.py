from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QDialog
from PyQt5.QtGui import QPixmap, QImage,QMouseEvent,QPainter,QPen
from PyQt5.QtCore import Qt, QPoint, QEventLoop, QMimeData, QBuffer,QEvent

class DraggableLabel_1(QLabel):
    def __init__(self,parent=None):
        super(DraggableLabel_1, self).__init__(parent)
        self.dragging = False
        self.drag_start_position = QPoint()
        self.setMouseTracking(True)  # 允许在鼠标未按下时跟踪鼠标移动
        self.is_selected = False

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            print("单击")
            self.dragging = True
            self.drag_start_position = event.pos() - self.pos()
        elif event.button() == Qt.RightButton and not self.dragging:
            if event.type() == QEvent.MouseButtonDblClick:
                print("双击")
                self.is_selected = not self.is_selected
                self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging and event.buttons() & Qt.LeftButton:
            new_pos = event.pos() - self.drag_start_position
            self.move(new_pos)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.is_selected:
            # 绘制虚线框
            painter = QPainter(self)
            pen = QPen(Qt.DashLine)
            pen.setWidth(2)
            painter.setPen(pen)
            rect = self.rect().adjusted(0, 0, -1, -1)  # 稍微缩小一点以避免线条重叠在边缘上
            painter.drawRect(rect)
            painter.end()
