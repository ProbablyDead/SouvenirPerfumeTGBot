from PIL import Image, ImageDraw, ImageFont
from random import choice

templates = ["./references/templates/В1.jpg",
             "./references/templates/В2.jpg",
             "./references/templates/В3.jpg"]

ingredient_name_font = "./references/fonts/Montserrat-Medium.ttf"
# perfume_title_font = "./references/fonts/gogol_regular.otf"
perfume_title_font = "./references/fonts/Montserrat-Medium.ttf"
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


def get_image(answer):
    return "./references/notes/ваниль.jpg"


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


def paste_perfume_title(template, title):
    font = ImageFont.truetype(perfume_title_font,
                              perfume_title_size, encoding='UTF-8')
    line_height = sum(font.getmetrics())

    fontimage = Image.new('L', (font.getbbox(title)[2], line_height))

    ImageDraw.Draw(fontimage).text((0, 0), title, fill=255, font=font)

    fontimage = fontimage.rotate(270, resample=Image.BICUBIC, expand=True)

    new_height = int(perfume_title_place_size[0]/fontimage.height)
    new_width = int(perfume_title_place_size[0]/fontimage.height)

    fontimage = fontimage.resize((int(perfume_title_place_size[1]/fontimage.height*fontimage.width),
                                  perfume_title_place_size[1]))

    template.paste((0, 0, 0), box=(perfume_title_place[0] - fontimage.width//2, perfume_title_place[1] - fontimage.height//2),
                   mask=fontimage)


def result_image(answers):
    with Image.open(choice(templates)) as working_template:
        working_template.load()

    for answer, place, i in zip(answers, images_place, range(6)):
        with Image.open(get_image(answer)) as note:
            note.load()
            working_template.paste(note.resize(image_size), place)
            paste_ingredient_title(working_template, "ваниль",
                                   place, middle=not (i == 0 or i == 5))

    paste_perfume_title(working_template, answers[-1])

    working_template.show()


print((result_image(["vanila", "coffe", "vanila",
      "coffe", "vanila", "coffe", "ол"])))
