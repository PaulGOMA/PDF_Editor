import sys
import os
import shutil
import json
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsPixmapItem, QGraphicsTextItem
from PySide6.QtCore import QSize, QRectF, QPoint, Qt
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QPainterPath, QPixmap, QFont
from pymupdf import Rect
from pymupdf import sRGB_to_rgb

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


class CustomGraphicsItem(QGraphicsItem):
    def __init__(self, bounding_rect: Rect, type_shape: QPen | tuple, path: QPainterPath | QRectF):
        super().__init__()
        self.bounding_rect = bounding_rect
        self.path = path
        self.type_shape = type_shape

        self.boundingRect()

    def boundingRect(self) -> QRectF:
        bounding = QRectF(QPoint(self.bounding_rect.x0, self.bounding_rect.y0), QPoint(self.bounding_rect.x1, self.bounding_rect.y1))
        return bounding
    
    def paint(self, painter: QPainter, option, widget):        
        if isinstance(self.type_shape, QPen):
            painter.setPen(self.type_shape)
            painter.drawRect(self.path) if isinstance(self.path, QRectF) else painter.drawPath(self.path)

        elif isinstance(self.type_shape, tuple):
            painter.setBrush(self.type_shape[0])
            painter.setPen(self.type_shape[1])
            painter.drawRect(self.path) if isinstance(self.path, QRectF) else painter.drawPath(self.path)


class CustomGraphicsPixmapItem(QGraphicsPixmapItem):
    def __init__(self, bounding_rect: Rect, filename: str):
        super().__init__()
        self.bounding_rect = bounding_rect
        self.filename = filename

        self.setPixmap(QPixmap(self.filename).scaled(int(abs(self.bounding_rect.x1 - self.bounding_rect.x0)), int(abs(self.bounding_rect.y1 - self.bounding_rect.y0))))
        self.setOffset(QPoint(QPoint(self.bounding_rect.x0, self.bounding_rect.y0)))




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.page = Extractor('test/document.pdf', 0)
        self.graphics_list = self.page.extract_graphics()

        if os.path.exists('JSON/infos.json'):
            os.remove('JSON/infos.json')
        
        self.page.extract_text_json()
        
        with open('JSON/infos.json', 'r') as file:
            self.texts_dict = json.load(file)
        
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
     
        if self.close():
            if os.path.exists('Images'):
                shutil.rmtree('Images')



    def type_draw(self, graphic: dict) -> tuple | QPen:
        
        if graphic['type'] == 'f':
            brush = QBrush(QColor(int(graphic['fill'][0] * 255), int(graphic['fill'][1] * 255), int(graphic['fill'][2] * 255)))
            pen = QPen(brush.color())
            return brush, pen
        
        elif graphic['type'] == 's':
            pen = QPen(QColor(int(graphic['color'][0] * 255), int(graphic['color'][1] * 255), int(graphic['color'][2] * 255)))               
            pen.setWidth(int(graphic['width']))

            if graphic['lineCap'] is not None:
                line_cap = int(max(graphic['lineCap'])) if isinstance(graphic['lineCap'], tuple) else int(graphic['lineCap'])
                if line_cap == 1:
                    pen.setCapStyle(Qt.RoundCap)
                elif line_cap == 2:
                    pen.setCapStyle(Qt.SquareCap)
                else:
                    pen.setCapStyle(Qt.FlatCap)

            if graphic['lineJoin'] is not None:
                line_join = int(max(graphic['lineJoin'])) if isinstance(graphic['lineJoin'], tuple) else int(graphic['lineJoin'])
                if line_join == 1:
                    pen.setJoinStyle(Qt.RoundJoin)
                elif line_join == 2:
                    pen.setJoinStyle(Qt.MiterJoin)
                else:
                    pen.setJoinStyle(Qt.BevelJoin)

            return pen
        
        elif graphic['type'] == 'fs':
            brush = QBrush(QColor(int(graphic['fill'][0] * 255), int(graphic['fill'][1] * 255), int(graphic['fill'][2] * 255)))
            pen = QPen(QColor(int(graphic['color'][0] * 255), int(graphic['color'][1] * 255), int(graphic['color'][2] * 255)))               
            pen.setWidth(int(graphic['width']))

            if graphic['lineCap'] is not None:
                line_cap = int(max(graphic['lineCap'])) if isinstance(graphic['lineCap'], tuple) else int(graphic['lineCap'])
                if line_cap == 1:
                    pen.setCapStyle(Qt.RoundCap)
                elif line_cap == 2:
                    pen.setCapStyle(Qt.SquareCap)
                else:
                    pen.setCapStyle(Qt.FlatCap)

            if graphic['lineJoin'] is not None:
                line_join = int(max(graphic['lineJoin'])) if isinstance(graphic['lineJoin'], tuple) else int(graphic['lineJoin'])
                if line_join == 1:
                    pen.setJoinStyle(Qt.RoundJoin)
                elif line_join == 2:
                    pen.setJoinStyle(Qt.MiterJoin)
                else:
                    pen.setJoinStyle(Qt.BevelJoin)

            return brush, pen

        
    def get_paths(self, graphic: dict) -> QRectF | QPainterPath:

        paths_list = graphic['items']

        if paths_list[0][0] == "re":
            item = paths_list[0][1]
            rect = QRectF(QPoint(item.x0, item.y0), QPoint(item.x1, item.y1))
            return rect
        
        else:
            path = QPainterPath()

            start_point = paths_list[0]
            path.moveTo(start_point[1].x, start_point[1].y)

            for item in paths_list:
                if item[0] == 'l':
                    p2 = item[2]
                    path.lineTo(p2.x, p2.y)
                    
                elif item[0] == 'c':
                    p2 = item[2]
                    p3 = item[3]
                    p4 = item[4]
                    path.cubicTo(QPoint(p2.x, p2.y), QPoint(p3.x, p3.y), QPoint(p4.x, p4.y))


            if graphic['even_odd'] is not None:
                path.setFillRule(Qt.OddEvenFill) if graphic['even_odd'] else path.setFillRule(Qt.WindingFill)

        return path


    def draw(self):

        for graphic in self.graphics_list:

            path = self.get_paths(graphic)
            result = self.type_draw(graphic)
            drawing = CustomGraphicsItem(bounding_rect=graphic['rect'], type_shape=result, path=path)

            if graphic['fill_opacity'] is not None:
                drawing.setOpacity(graphic['fill_opacity'])
            elif graphic['stroke_opacity'] is not None:
                drawing.setOpacity(graphic['stroke_opacity'])   
            
            self.scene.addItem(drawing)

        
        if self.page.extract_image():
            images_list = self.page.extract_image_rect()

            for content in images_list:
                image = CustomGraphicsPixmapItem(content[1], f"Images/{content[2]}.png")
                self.scene.addItem(image)

        if self.texts_dict['blocks'] != []:
            for block in self.texts_dict['blocks']:
                if block['type'] == 0:
                    for line in block['lines']:
                        for span in line['spans']:
                            self.span = span
                            if 'timesnewroman'.lower() in self.span['font'].lower():
                                font_family = "times New Roman"
                            elif 'cambria'.lower() in self.span['font'].lower():
                                font_family = "Cambria"
                            else:
                                font_family = "times New Roman"

                            text_font = QFont(font_family, (int(self.span['size']) - 3))

                            if 'bold'.lower() in self.span['font'].lower():
                                text_font.setBold(True)

                            font_color = sRGB_to_rgb(self.span['color'])
                            
                            text = QGraphicsTextItem()
                            text.setFont(text_font)
                            text.setDefaultTextColor(QColor(font_color[0], font_color[1], font_color[2]))
                            text.setTextInteractionFlags(Qt.TextEditorInteraction)
                            text.setPlainText(self.span['text'])
                            text.update(QRectF(QPoint(self.span['bbox'][0], self.span['bbox'][1]), QPoint(self.span['bbox'][2], self.span['bbox'][3])))
                            text.setPos(QPoint((self.span['origin'][0] - 4), (self.span['origin'][1]) - 15))
            
                            self.scene.addItem(text)


    


        
        


    
                    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())