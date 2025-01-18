import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsPathItem
from PySide6.QtGui import QPainterPath, QPen, QColor
from PySide6.QtCore import QPoint, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tracer un QPainterPath")
        self.setGeometry(100, 100, 800, 600)

        # Créer la scène graphique
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        # Ajouter le chemin à la scène
        self.add_paths([
            QPoint(71.1500015258789, 80.04998779296875), 
            QPoint(71.1500015258789, 77.70001220703125), 
            QPoint(73.0530014038086, 75.79998779296875), 
            QPoint(75.4000015258789, 75.79998779296875),
            QPoint(534.5999755859375, 75.79998779296875),
            QPoint(536.9500122070312, 75.79998779296875), 
            QPoint(538.8499755859375, 77.70001220703125), 
            QPoint(538.8499755859375, 80.04998779296875),
            QPoint(538.8499755859375, 97.04998779296875),
            QPoint(538.8499755859375, 99.39996337890625), 
            QPoint(536.9500122070312, 101.29998779296875), 
            QPoint(534.5999755859375, 101.29998779296875),
            QPoint(75.4000015258789, 101.29998779296875),
            QPoint(73.0530014038086, 101.29998779296875), 
            QPoint(71.1500015258789, 99.39996337890625), 
            QPoint(71.1500015258789, 97.04998779296875),
            QPoint(71.1500015258789, 80.04998779296875)
        ])

    def add_paths(self, points_list):
        path = QPainterPath()
        path.moveTo(points_list[0])
        path.cubicTo(points_list[1], points_list[2], points_list[3])
        path.lineTo(points_list[4])
        path.cubicTo(points_list[5], points_list[6], points_list[7])
        path.lineTo(points_list[8])
        path.cubicTo(points_list[9], points_list[10], points_list[11])
        path.lineTo(points_list[12])
        path.cubicTo(points_list[13], points_list[14], points_list[15])
        path.lineTo(points_list[16])

        drawing = QGraphicsPathItem(path)
        pen = QPen(QColor(Qt.red))
        pen.setWidth(3)
        drawing.setPen(pen)
        drawing.setBrush(QColor(Qt.yellow))
        self.scene.addItem(drawing)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
