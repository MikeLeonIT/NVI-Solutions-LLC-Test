import encodings
import os
import shutil
import sys

import pdf_reader
from design import *


class Leonscene(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None):
        super(Leonscene, self).__init__(parent)

    def mousePressEvent(self, event):
        super(Leonscene, self).mousePressEvent(event)
        self.xRect = event.scenePos().x()
        self.yRect = event.scenePos().y()

    def mouseReleaseEvent(self, event):
        super(Leonscene, self).mouseReleaseEvent(event)
        add_rect = QtWidgets.QGraphicsScene.addRect(self, self.xRect, self.yRect, self.endX -
                                                    self.xRect, self.endY - self.yRect)
        add_rect.setBrush(QtGui.QColor(0, 0, 255, 0))  # Заливка
        add_rect.setPen(QtCore.Qt.GlobalColor.red)  # Контур

    def mouseMoveEvent(self, event):
        super(Leonscene, self).mouseMoveEvent(event)
        self.endX = event.scenePos().x()
        self.endY = event.scenePos().y()


class MyApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.btnBrowse.clicked.connect(self.open_file)
        self.ui.nextButton.clicked.connect(self.next)
        self.ui.previousButton.clicked.connect(self.previous)
        self.result = []
        self.count = 0

    def closeEvent(self, event):
        path_name = "tmp"
        if os.path.exists(path_name):
            for filename in os.listdir(path_name):
                file_path = os.path.join(path_name, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
            os.rmdir(path_name)
        event.accept()

    def show_page(self, count):
        scene = Leonscene(self)
        pixmap = QtGui.QPixmap(self.result[count])
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        scene.addItem(item)

        self.ui.graphicsView.setScene(scene)

    def open_file(self):
        if self.result == [] and self.count == 0:
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                "Open File", ".",
                                                                "PDF Files (*.pdf);;All Files (*)",
                                                                encodings.normalize_encoding('utf-8'))
            self.result = pdf_reader.convert_pdf(filename)
            self.show_page(self.count)
        else:
            self.result = []
            self.count = 0
            self.open_file()

    def next(self):
        if self.count + 1 <= len(self.result) - 1:
            self.count += 1
            self.show_page(self.count)
        else:
            self.count = 0
            self.show_page(self.count)

    def previous(self):
        if self.count - 1 >= 0:
            self.count -= 1
            self.show_page(self.count)
        else:
            self.count = len(self.result) - 1
            self.show_page(self.count)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    class_instance = MyApp()
    class_instance.show()
    sys.exit(app.exec())
