from PIL import Image, ImageDraw, ImageFont
from random import choice

templates = ["./references/templates/В1.jpg",
             "./references/templates/В2.jpg",
             "./references/templates/В3.jpg"]

ingredient_name_font = "./references/fonts/Montserrat-Medium.ttf"
ingredient_name_size = 70

image_size = (630, 635)

images_place = [(2688, 325),
                (2305, 1320),
                (3079, 1320),
                (2305, 2166),
                (3079, 2166),
                (2690, 3185)]

title_offset = 120


def get_image(answer):
    return "./references/notes/ваниль.jpg"


def paste_title(template, title: str, image_coord: tuple[int, int], middle=False):
    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype(ingredient_name_font,
                              ingredient_name_size, encoding='UTF-8')

    text_coord = (image_coord[0] + image_size[0]//2,
                  image_coord[1] + image_size[1] +
                  ((title_offset - 30) if middle and '\n' in title else title_offset))

    if not middle:
        title = title.replace('\n', ' ')

    draw.multiline_text(text_coord, title,
                        anchor="ms", align="center", fill="black", font=font)


def result_image(answers):
    with Image.open(choice(templates)) as working_template:
        working_template.load()

    for answer, place, i in zip(answers, images_place, range(6)):
        with Image.open(get_image(answer)) as note:
            note.load()
            working_template.paste(note.resize(image_size), place)
            paste_title(working_template, "лилия и\nиланг-иланг",
                        place, middle=not (i == 0 or i == 5))

    working_template.show()


print((result_image(["vanila", "coffe", "vanila",
      "coffe", "vanila", "coffe", "pivo"])))
