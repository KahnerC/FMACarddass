from PIL import Image, ImageDraw, ImageFont
import textwrap

input_text = "2,3,4"

img = Image.new("RGBA", (400, 48), color=(0,0,0,0))

tip = Image.open("components/ATK-Start tri.png")
tail = Image.open("components/ATK-End tri.png")
mid = Image.open("components/ATK-Mid.png")
font4 = ImageFont.load_default(size=25.0)

icon_A = Image.open("components/icon1 sml.png")
icon_F = Image.open("components/icon2 sml.png")
icon_G = Image.open("components/icon3 sml.png")

img.paste(tip, (0,0))
draw = ImageDraw.Draw(img)
if len(input_text.split(",")) > 1:
    line_len = 100
    if len(input_text.split(",")) > 2:
        img.paste(tip, (170,0),mask=tip)
        img.paste(tail, (170+48+40,0), mask=tail)
        for i in range(170+48, 170+48+40):
            img.paste(mid, (i,0))
        img.paste(icon_G, (170+48,4), mask=icon_G)
        draw.text((170+78,30), input_text.split(",")[2], fill=(255,255,255), font=font4, anchor="mm")
    for i in range(48, 52 + line_len):
        img.paste(mid, (i,0))
    img.paste(icon_A, (50,4), mask=icon_A)
    img.paste(icon_F, (100,4), mask=icon_F)
    draw.text((50+32,30), input_text.split(",")[0], fill=(255,255,255), font=font4, anchor="mm")
    draw.text((100+32,30), input_text.split(",")[1], fill=(255,255,255), font=font4, anchor="mm")
    input_text = ""
else:
    line_len = draw.textbbox((0,0), "this one", font=font4)[2]
    for i in range(48, 52 + line_len):
        img.paste(mid, (i,0))
draw.text((50,24), input_text, fill=(255,255,255), font=font4, anchor="lm")
img.paste(tail, (line_len+52,0), mask=tail)



img.show()
