"""
## This file contains classes for extracting graphics from a page belongs to a pdf file and drawing them in a new pdf file.
"""

import pymupdf
from extractor import Extractor

class Render:
    def __init__(self, resource: Extractor) -> None:
        self.resource = resource
        self.page = self.resource.page

    def render_graphics(self, output_page: pymupdf.Page) -> None:
        paths = self.page.get_drawings()
        shape = output_page.new_shape()

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

    def render_images(self, output_page: pymupdf.Page) -> None:
        image_list = self.resource.extract_image_rect()
        for image in image_list:
            output_page.insert_image(image[1], pixmap=pymupdf.Pixmap(self.resource.file, image[0]))

    

if __name__ == "__main__":
    e = Extractor('test/doc.pdf', 0)
    doc = pymupdf.open()
    page = doc.new_page(width=e.page.rect.width, height=e.page.rect.height)
    r = Render(e)
    r.render_graphics(page)
    r.render_images(page)
    doc.save('test/output.pdf')
    doc.close()
    e.file.close()

    




           


    


