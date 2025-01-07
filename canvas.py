import sys
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsPathItem
from PySide6.QtCore import QSize, QRectF, QPoint, Qt
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QPainterPath

from extractor import Extractor

# Screen size recovery function
def getResolutions() -> QSize:
    app = QApplication.instance() 
    if app is None:
        app = QApplication(sys.argv)
    return app.primaryScreen().size()

# Display window in center of screen
def centerWindow(window: QWidget) -> None:
    x = (getResolutions().width() - window.width()) // 2
    y = (getResolutions().height() - window.height()) // 2

    window.move(x, y)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.r = Extractor('test/doc.pdf', 0)
        self.setWindowTitle('Canvas')
        self.setMinimumSize(900, 900)
        centerWindow(self)

        self.centralArea = QWidget()
        self.setCentralWidget(self.centralArea)
        self.centralArea.setStyleSheet("background-color: #f6f6f6")

        # Build scene
        self.scene = QGraphicsScene()
        w = 600
        h = 800
        rect_scene = QRectF(0, 0, w, h)
        self.scene.setSceneRect(rect_scene)
        self.scene.setBackgroundBrush(QColor(255, 255, 255))

        # Build view
        view = QGraphicsView(self.centralArea)
        view.move((self.width() - w) // 2, (self.height() - h) // 2)
        view.setScene(self.scene)
        view.setRenderHint(QPainter.Antialiasing)

        self.draw()

    # def draw(self):
    #     graphic_list = self.r.extract_graphics()

    #     for graphic in graphic_list:

    #         if graphic["type"] == "s":
    #             color = graphic["color"]
    #             stroke_opacity = graphic["stroke_opacity"]
    #             width = graphic["width"]
    #             pen = QPen(QColor(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))
    #             pen.setWidth(width)
    #         elif graphic["type"] == "f":
    #             fill = graphic["fill"]
    #             fill_opacity = graphic["fill_opacity"]
    #             brush = QBrush(QColor(int(fill[0] * 255), int(fill[1] * 255), int(fill[2] * 255)))
    #         elif graphic["type"] == "fs":
    #             color = graphic["color"]
    #             stroke_opacity = graphic["stroke_opacity"]
    #             width = graphic["width"]
    #             pen = QPen(QColor(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))
    #             pen.setWidth(width)
    #             fill = graphic["fill"]
    #             fill_opacity = graphic["fill_opacity"]
    #             brush = QBrush(QColor(int(fill[0] * 255), int(fill[1] * 255), int(fill[2] * 255)))

    #         for item in graphic["items"]:
    #             if item[0] == 're':
    #                 rect = QRectF(QPoint(item[1].x0, item[1].y0), QPoint(item[1].x1, item[1].y1))
    #                 drawing = QGraphicsRectItem(rect) 
    #                 drawing.setBrush(brush)
    #                 if fill_opacity is not None:
    #                     drawing.setOpacity(fill_opacity)
    #                 elif stroke_opacity is not None:
    #                     drawing.setOpacity(stroke_opacity)
    #                 self.scene.addItem(drawing)  
    #             else:
    #                 path = QPainterPath()
    #                 start_point = item[1]
    #                 path.moveTo(start_point.x, start_point.y)
    #                 if item[0] == 'l':
    #                     point = item[2]
    #                     path.lineTo(point.x, point.y)

    #                 elif item[0] == 'c':
    #                     p2 = item[2]
    #                     p3 = item[3]
    #                     p4 = item[4]
    #                     path.cubicTo(QPoint(p2.x, p2.y), QPoint(p3.x, p3.y), QPoint(p4.x, p4.y))

    #                 if graphic["even_odd"]: 
    #                     path.setFillRule(Qt.WindingFill) 
    #                 else: 
    #                     path.setFillRule(Qt.OddEvenFill) 
            
    #                 drawing = QGraphicsPathItem(path)
    #                 drawing.setPen(pen)
    #                 if fill_opacity is not None:
    #                     drawing.setOpacity(fill_opacity)
    #                 elif stroke_opacity is not None:
    #                     drawing.setOpacity(stroke_opacity)
    #                 self.scene.addItem(drawing)

    #                 rect = QRectF(QPoint(graphic['rect'].x0, graphic['rect'].y0), QPoint(graphic['rect'].x1, graphic['rect'].y1))
    #                 draw_rect = QGraphicsRectItem(rect)
    #                 draw_rect.setBrush(brush)
    #                 if fill_opacity is not None:
    #                     draw_rect.setOpacity(fill_opacity)
    #                 elif stroke_opacity is not None:
    #                     draw_rect.setOpacity(stroke_opacity)
    #                 self.scene.addItem(draw_rect)


    # def draw(self):
    #     graphic_list = self.r.extract_graphics()

    #     for graphic in graphic_list:
    #         fill = graphic['fill']
    #         color = graphic['color']
    #         fill_opacity = graphic['fill_opacity']
    #         stroke_opacity = graphic['stroke_opacity']

    #         for item in graphic['items']:
    #             if item[0] == 're':
    #                 rect = QRectF(QPoint(item[1].x0, item[1].y0), QPoint(item[1].x1, item[1].y1))
    #                 drawing = QGraphicsRectItem(rect)
    #                 if fill is None and color is not None:
    #                     pen = QPen(QColor(color[0] * 255, color[1] * 255, color[2] * 255))
    #                     pen.setWidth(graphic['width'])
    #                     drawing.setPen(pen)
    #                 elif fill is not None and color is None:
    #                     brush = QBrush(QColor(fill[0] * 255, fill[1] * 255, fill[2] * 255))
    #                     pen = QPen(QColor(fill[0] * 255, fill[1] * 255, fill[2] * 255))
    #                     pen.setWidth(1)
    #                     drawing.setBrush(brush)
    #                     drawing.setPen(pen)
    #                 elif fill is not None and color is not None:
    #                     pen = QPen(QColor(color[0] * 255, color[1] * 255, color[2] * 255))
    #                     pen.setWidth(graphic['width'])
    #                     brush = QBrush(QColor(fill[0] * 255, fill[1] * 255, fill[2] * 255))
    #                     drawing.setBrush(brush)
    #                 else:
    #                     print("impossible")

    #                 if fill_opacity is not None:
    #                     drawing.setOpacity(fill_opacity)
    #                 elif stroke_opacity is not None:
    #                     drawing.setOpacity(stroke_opacity)

    #                 self.scene.addItem(drawing)
    #             else:

    #                 rect = QRectF(QPoint(graphic['rect'].x0, graphic['rect'].y0), QPoint(graphic['rect'].x1, graphic['rect'].y1))
    #                 draw_rect = QGraphicsRectItem(rect)
    #                 self.scene.addItem(draw_rect)

    #                 path = QPainterPath()
    #                 start_point = item[1]
    #                 path.moveTo(start_point.x, start_point.y)
    #                 if item[0] == 'l':
    #                     point = item[2]
    #                     path.lineTo(point.x, point.y)
    #                 elif item[0] == 'c':
    #                     p2 = item[2]
    #                     p3 = item[3]
    #                     p4 = item[4]
    #                     path.cubicTo(QPoint(p2.x, p2.y), QPoint(p3.x, p3.y), QPoint(p4.x, p4.y))
    #                 drawing = QGraphicsPathItem(path)

                    

    #                 if fill is None and color is not None:
    #                     pen = QPen(QColor(color[0] * 255, color[1] * 255, color[2] * 255))
    #                     pen.setWidth(graphic['width'])
    #                     drawing.setPen(pen)
    #                 elif fill is not None and color is None:
    #                     brush = QBrush(QColor(fill[0] * 255, fill[1] * 255, fill[2] * 255))
    #                     pen = QPen(QColor(fill[0] * 255, fill[1] * 255, fill[2] * 255))
    #                     pen.setWidth(1)
    #                     drawing.setBrush(brush)
    #                     drawing.setPen(pen)
    #                 elif fill is not None and color is not None:
    #                     pen = QPen(QColor(color[0] * 255, color[1] * 255, color[2] * 255))
    #                     pen.setWidth(graphic['width'])
    #                     drawing.setPen(pen)
    #                     brush = QBrush(QColor(fill[0] * 255, fill[1] * 255, fill[2] * 255))
    #                     draw_rect.setBrush(brush)
    #                 else:
    #                     print("impossible")

    #                 if fill_opacity is not None:
    #                     drawing.setOpacity(fill_opacity)
    #                 elif stroke_opacity is not None:
    #                     drawing.setOpacity(stroke_opacity)

    #                 self.scene.addItem(drawing)


    def type_draw(self, type: str, fill: tuple | None, color: tuple | None, width: float | None) -> QBrush | QPen | tuple:
        if type == 'f':
            brush = QBrush(QColor(int(fill[0] * 255), int(fill[1] * 255), int(fill[2] * 255)))
            return brush
        elif type == 's':
            pen = QPen(QColor(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))               
            pen.setWidth(int(width))
            return pen
        elif type == 'fs':
            brush = QBrush(QColor(int(fill[0] * 255), int(fill[1] * 255), int(fill[2] * 255)))
            pen = QPen(QColor(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))
            pen.setWidth(int(width))
            return brush, pen


    def draw(self):
        graphic_list = self.r.extract_graphics()

        for graphic in graphic_list:
            fill = graphic['fill']
            color = graphic['color']
            width = graphic['width']
            fill_opacity = graphic['fill_opacity']
            stroke_opacity = graphic['stroke_opacity']
            even_odd = graphic["even_odd"]

            # if graphic['type'] == 'f':        
            #     brush = QBrush(QColor(int(fill[0] * 255), int(fill[1] * 255), int(fill[2] * 255)))
            # elif graphic['type'] == 's':
            #     pen = QPen(QColor(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))               
            #     pen.setWidth(int(width))
            # elif graphic['type'] == 'fs':
            #     brush = QBrush(QColor(int(fill[0] * 255), int(fill[1] * 255), int(fill[2] * 255)))
            #     pen = QPen(QColor(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))
            #     pen.setWidth(int(width))

            for item in graphic['items']:
                if item[0] == 're':
                    rect = QRectF(QPoint(item[1].x0, item[1].y0), QPoint(item[1].x1, item[1].y1))
                    drawing = QGraphicsRectItem(rect)
                    result = self.type_draw(graphic['type'], fill, color, width)
                    if isinstance(result, QBrush):
                        drawing.setBrush(result)
                        drawing.setPen(result.color())
                    elif isinstance(result, QPen):
                        drawing.setPen(result)
                    else:
                        drawing.setBrush(result[0])
                        drawing.setPen(result[1])
                        
                    if fill_opacity is not None:
                        drawing.setOpacity(fill_opacity)
                    elif stroke_opacity is not None:
                        drawing.setOpacity(stroke_opacity)

                    self.scene.addItem(drawing)

                else:
                    path = QPainterPath()
                    p1 = item[1]
                    path.moveTo(p1.x, p1.y)

                    if item[0] == 'l':
                        p2 = item[2]
                        path.lineTo(p2.x, p2.y)
                    elif item[0] == 'c':
                        p2 = item[2]
                        p3 = item[3]
                        p4 = item[4]
                        path.cubicTo(QPoint(p2.x, p2.y), QPoint(p3.x, p3.y), QPoint(p4.x, p4.y))

                    if even_odd is not None:
                        path.setFillRule(Qt.OddEvenFill) if even_odd else path.setFillRule(Qt.WindingFill)

                    drawing = QGraphicsPathItem(path)
                    
                    result = self.type_draw(graphic['type'], fill, color, width)

                    if isinstance(result, QBrush): 
                        drawing.setBrush(result)
                    elif isinstance(result, QPen):                    
                        if graphic['lineCap'] is not None:
                            line_cap = int(max(graphic['lineCap'])) if isinstance(graphic['lineCap'], tuple) else int(graphic['lineCap'])
                            if line_cap == 1:
                                result.setCapStyle(Qt.RoundCap)
                            elif line_cap == 2:
                                result.setCapStyle(Qt.SquareCap)
                            else:
                                result.setCapStyle(Qt.FlatCap)

                        if graphic['lineJoin'] is not None:
                            line_join = int(max(graphic['lineJoin'])) if isinstance(graphic['lineJoin'], tuple) else int(graphic['lineJoin'])
                            if line_join == 1:
                                result.setJoinStyle(Qt.RoundJoin)
                            elif line_join == 2:
                                result.setJoinStyle(Qt.MiterJoin)
                            else:
                                result.setJoinStyle(Qt.BevelJoin)

                        drawing.setPen(result)
                    else:
                        # rect = QRectF(QPoint(graphic['rect'].x0, graphic['rect'].y0), QPoint(graphic['rect'].x1, graphic['rect'].y1))
                        # draw_rect = QGraphicsRectItem(rect)
                        # draw_rect.setBrush(result[0])
    
                        # if fill_opacity is not None:
                        #     draw_rect.setOpacity(fill_opacity)

                        # self.scene.addItem(draw_rect)
                        if graphic['lineCap'] is not None:
                            line_cap = int(max(graphic['lineCap'])) if isinstance(graphic['lineCap'], tuple) else int(graphic['lineCap'])
                            if line_cap == 1:
                                result[1].setCapStyle(Qt.RoundCap)
                            elif line_cap == 2:
                                result[1].setCapStyle(Qt.SquareCap)
                            else:
                                result[1].setCapStyle(Qt.FlatCap)

                        if graphic['lineJoin'] is not None:
                            line_join = int(max(graphic['lineJoin'])) if isinstance(graphic['lineJoin'], tuple) else int(graphic['lineJoin'])
                            if line_join == 1:
                                result[1].setJoinStyle(Qt.RoundJoin)
                            elif line_join == 2:
                                result[1].setJoinStyle(Qt.MiterJoin)
                            else:
                                result[1].setJoinStyle(Qt.BevelJoin)
                        drawing.setPen(result[1])
                        drawing.setBrush(result[0])

                    if fill_opacity is not None:
                        drawing.setOpacity(fill_opacity)
                    elif stroke_opacity is not None:
                        drawing.setOpacity(stroke_opacity)

                    self.scene.addItem(drawing)
                    

            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())