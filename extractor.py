"""
## This file contains classes for extracting texts and image from a page belongs to a pdf file and drawing them in a new pdf file.
"""

import os
import pymupdf
import json

class Extractor:
    def __init__(self, path: str, page_number: int) -> None:
        self.path = path
        self.file = pymupdf.open(self.path)

        try:
            self.page = self.file[page_number]
        except IndexError:
            print(f"La page {page_number} ne se trouve pas dans le document") 
            exit(1)    


    def extract_page_size(self) -> tuple:
        size = self.page.bound()
        return size[2], size[3]

    def extract_image_rect(self) -> list:
        image_list = self.page.get_images()
        if image_list != []:
            rect_image_list = []
            for image in image_list:
                coords = self.page.get_image_rects(image)
                rect_image_list.append((image[0], coords[0], image[7]))

            return rect_image_list
        else:
            print("Aucune image trouvée !!")
            return
   
    def extract_image(self) -> int:
        image_list = self.page.get_images()
        if image_list != []:

            if not os.path.exists('Images'):
                os.mkdir('Images')

            for image in image_list:
                xref = image[0]
                pix = pymupdf.Pixmap(self.file, xref)

                if pix.n - pix.alpha > 3:
                    pix = pymupdf.Pixmap(pymupdf.csRGB, pix)

                pix.save(f"Images/{image[7]}.png")
                pix = None

            return 1
        else:
            return 0

    def extract_image_json(self):
        images_list = self.page.get_image_info(True, True)
        for img in images_list:
            temp = img['digest']
            img['digest'] = f"{temp}"
            temp = None
        json_object = json.dumps(images_list, indent=4)
        with open('JSON/images.json', 'w', encoding='utf-8') as output_file:
            output_file.write(json_object)

    

    def extract_text_json(self):
        content = self.page.get_text("json")
        with open('JSON/infos.json', 'w', encoding='utf-8') as output_file:
            output_file.write(content)


    def extract_graphics(self):
        return self.page.get_drawings()
    
    def extract_graphics_txt(self):
        with open('JSON/graphics.txt', 'w', encoding='utf-8') as output_file:
            graphic_list = self.page.get_drawings()
            for element in graphic_list:
                output_file.write("{\n")
                for key, value in element.items():
                    output_file.write(f'\t{key} : {value}\n')
                output_file.write('}\n')

    def extract_text_info(self):
        content = self.page.get_text("dict")
        blocks = content['blocks']

        for block in blocks:
            if block['type'] == 0:
                for line in block['lines']:
                    for s in line['spans']:

                        print("")
                        font_properties = "Font: '%s', size %g, color #%06x" % (
                            s["font"],  # font name
                            s["size"],  # font size
                            abs(s["color"]),  # font color
                        )
                        print("Text: '%s'" % s["text"])  # simple print of text
                        print(font_properties)

   
if __name__ == "__main__":
    e = Extractor('test/doc.pdf', 0)
    # print(e.extract_image_rect())
    # e.extract_image_json()
    e.extract_text_json()
    # print(e.extract_graphics())
    # e.extract_graphics_txt()
    # e.extract_image()
    # e.extract_text_info()
    e.file.close()






            

    