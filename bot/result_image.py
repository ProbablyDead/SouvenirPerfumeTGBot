from PIL import Image, ImageDraw, ImageFont
from random import choice

path_to_refs = "./references"

templates = [path_to_refs + "/templates/В1.jpg",
             path_to_refs + "/templates/В2.jpg",
             path_to_refs + "/templates/В3.jpg"]
images_path = path_to_refs + "/notes/"

ingredient_name_font = path_to_refs + "/fonts/Montserrat-Medium.ttf"
perfume_title_font = path_to_refs + "/fonts/Montserrat-Medium.ttf"
ingredient_name_size = 70
perfume_title_size = 100

image_size = (630, 635)

images_place = [(2688, 325),
                (2305, 1320),
                (3079, 1320),
                (2305, 2166),
                (3079, 2166),
                (2690, 3185)]
ingredient_name_offset = 120

perfume_title_place = (933, 2730)

perfume_title_place_size = (660, 1400)


class ResultImage:
    @staticmethod
    def get_name(ingredient) -> str:
        match ingredient:
            case "bedsheets":
                return "свежее\nпостельное белье"
            case "berry":
                return "вишня"
            case "breeze":
                return "морской бриз"
            case "caramel":
                return "соленая карамель"
            case "chocolate":
                return "шоколад"
            case "cigarette":
                return "табак и кофе"
            case "cinnamon":
                return "корица"
            case "citrus":
                return "цитрус"
            case "cognac":
                return "коньячность,\nшоколад"
            case "jasmine":
                return "жасмин, мята"
            case "lemon":
                return "лимон и мята"
            case "lily":
                return "лилии, иланг-иланг"
            case "mango":
                return "манго"
            case "meadow":
                return "луг"
            case "pepper":
                return "розовый перец"
            case "pistachios":
                return "фисташка"
            case "powder":
                return "пудра"
            case "rose":
                return "розы, пионы"
            case "sault":
                return "морская соль"
            case "spices":
                return "специи"
            case "sugar":
                return "ваниль и сахар"
            case "tree":
                return "тиковое дерево"
            case "vanilla":
                return "ваниль"
            case "wind":
                return "свежий ветер"
            case _:
                return ""

    @staticmethod
    def get_image(answer):
        return images_path + answer + ".jpg"

    @staticmethod
    def paste_ingredient_title(template, ing_name: str, image_coord: tuple[int, int], middle=False):
        draw = ImageDraw.Draw(template)
        font = ImageFont.truetype(ingredient_name_font,
                                  ingredient_name_size, encoding='UTF-8')

        text_coord = (image_coord[0] + image_size[0]//2,
                      image_coord[1] + image_size[1] +
                      ((ingredient_name_offset - 30) if middle and '\n' in ing_name else ingredient_name_offset))

        if not middle:
            ing_name = ing_name.replace('\n', ' ')

        draw.multiline_text(text_coord, ing_name,
                            anchor="ms", align="center", fill="black", font=font)

    @staticmethod
    def paste_perfume_title(template, title):
        font = ImageFont.truetype(perfume_title_font,
                                  perfume_title_size, encoding='UTF-8')
        line_height = sum(font.getmetrics())

        fontimage = Image.new('L', (font.getbbox(title)[2], line_height))

        ImageDraw.Draw(fontimage).text((0, 0), title, fill=255, font=font)

        fontimage = fontimage.rotate(270, resample=Image.BICUBIC, expand=True)

        new_width = int(perfume_title_place_size[1]
                        / fontimage.height*fontimage.width)
        new_height = perfume_title_place_size[1]

        if len(title) < 10:
            new_width = fontimage.width * 2
            new_height = fontimage.height * 2

        fontimage = fontimage.resize((new_width, new_height))

        template.paste((0, 0, 0),
                       box=(perfume_title_place[0] - fontimage.width//2,
                            perfume_title_place[1] - fontimage.height//2),
                       mask=fontimage)

    @staticmethod
    def result_image(answers):
        with Image.open(choice(templates)) as working_template:
            working_template.load()

        for answer, place, i in zip(answers[:6], images_place, range(6)):
            with Image.open(ResultImage.get_image(answer)) as note:
                note.load()
                working_template.paste(note.resize(image_size), place)
                ResultImage.paste_ingredient_title(working_template, ResultImage.get_name(answer),
                                                   place, middle=not (i == 0 or i == 5))

        ResultImage.paste_perfume_title(working_template, answers[-1])

        return working_template
