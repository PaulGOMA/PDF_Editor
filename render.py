"""
## This file contains classes for extracting graphics from a page belongs to a pdf file and drawing them in a new pdf file.
"""

import os
import pymupdf
from extractor import Extractor

class Render:
    def __init__(self) -> None:
        self.page = Extractor('test/fiche2.pdf', 0)
        self.doc = pymupdf.open()
        page_width = self.page.page.rect.width
        page_height = self.page.page.rect.height
        self.output_page = self.doc.new_page(width=page_width, height=page_height)
        
        if os.path.exists('JSON/infos.json'):
            os.remove('JSON/infos.json')
        
        # self.page.extract_text_json()
        
        # with open('JSON/infos.json', 'r') as file:
        #     self.texts_dict = json.load(file)

        self.texts_dict = self.page.page.get_text("dict")

    def render_graphics(self) -> None:
        paths = self.page.extract_graphics()
        shape = self.output_page.new_shape()

        # loop through the paths and draw them
        for path in paths:
            # draw each entry of the 'items' list
            for item in path["items"]:  # these are the draw commands
                if item[0] == "l":  # line
                    shape.draw_line(item[1], item[2])
                elif item[0] == "re":  # rectangle
                    shape.draw_rect(item[1])
                elif item[0] == "qu":  # quad
                    shape.draw_quad(item[1])
                elif item[0] == "c":  # curve
                    shape.draw_bezier(item[1], item[2], item[3], item[4])
                else:
                    raise ValueError("unhandled drawing", item)
            
            # Set default values if not provided
            stroke_opacity = path.get("stroke_opacity", 1)
            fill_opacity = path.get("fill_opacity", 1)
            lineCap = path.get("lineCap", 0)  # Default to 0 (Butt cap)
            lineJoin = path.get("lineJoin", 0)  # Default to 0 (Miter join)
            closePath = path.get("closePath", False)

            # Ensure values are not None and are integers
            stroke_opacity = 1 if stroke_opacity is None else stroke_opacity
            fill_opacity = 1 if fill_opacity is None else fill_opacity
            lineCap = 0 if lineCap is None else (lineCap[0] if isinstance(lineCap, tuple) else int(lineCap))
            lineJoin = 0 if lineJoin is None else (lineJoin[0] if isinstance(lineJoin, tuple) else int(lineJoin))
            closePath = False if closePath is None else closePath

            # all items are drawn, now apply the common properties to finish the path
            shape.finish(
                fill=path["fill"],  # fill color
                color=path["color"],  # line color
                dashes=path["dashes"],  # line dashing
                even_odd=path.get("even_odd", True),  # control color of overlaps
                closePath=closePath,  # whether to connect last and first point
                lineJoin=lineJoin,  # how line joins should look like
                lineCap=lineCap,  # how line ends should look like
                width=path["width"],  # line width
                stroke_opacity=stroke_opacity,  # same value for both
                fill_opacity=fill_opacity,  # opacity parameters
            )
        
        # all paths processed - commit the shape to its page
        shape.commit()

    def render_images(self) -> None:
        image_list = self.page.extract_image_rect()
        for image in image_list:
            self.output_page.insert_image(image[1], pixmap=pymupdf.Pixmap(self.page.file, image[0]))

    def render_texts(self) -> None:       
        if self.texts_dict['blocks'] != []:
            for block in self.texts_dict['blocks'] :
                if block['type'] == 0:
                    for line in block['lines']:
                        for span in line['spans']:
                            
                            font_file = None
                            if 'times'.lower() in span['font'].lower():
                                if 'bold'.lower() in span['font'].lower():
                                    # font_file = "font/TimesNewRoman-Bold.ttf"
                                    # font_name = "times-new-roman-bold"
                                    font_name = "tibo"
                                else:
                                    # font_name = "font/TimesNewRoman.ttf"
                                    # font_name = "times-new-roman"
                                    font_name = "tiro"
                            elif 'cambria'.lower() in span['font'].lower():
                                if 'bold'.lower() in span['font'].lower():
                                    font_file = "font/Cambria-Bold.ttf"
                                    font_name = "cambria-bold"
                                else:
                                    font_file = "font/Cambria.ttf"
                                    font_name = "cambria"
                            else:
                                font_name = "tiro"

                            self.output_page.insert_text(
                                point=pymupdf.Point(
                                    span['origin'][0], 
                                    span['origin'][1]
                                ),
                                text= span['text'] if "\u2019" not in span['text'] else span['text'].replace("\u2019", "'"),
                                fontsize=span['size'],
                                fontname=font_name,
                                fontfile=font_file if font_file is not None else None,
                                color=pymupdf.sRGB_to_pdf(span['color'])
                            )


if __name__ == "__main__":
    r = Render()
    r.render_graphics()
    # r.render_images()
    r.render_texts()  # Appeler la nouvelle fonction pour ajouter les textes
    r.doc.save('test/output.pdf')
    r.doc.close()


           


    


