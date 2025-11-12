from PIL import Image, ImageDraw, ImageFont
import textwrap

#canvas
img = Image.new("RGB", (700, 1000), color=(128,128,128))

#card art and template
cardart = Image.open("components/art.png")
cardbase = Image.open("components/bbase.png")
img.paste(cardart, (0,50))
img.paste(cardbase, (0,0), mask=cardbase)

#text setup
font1 = ImageFont.load_default(size=45.0)
font2 = ImageFont.load_default(size=65.0)
font3 = ImageFont.load_default(size=15.0)
font4 = ImageFont.load_default(size=25.0)

#icon
cardicon = Image.open("components/icon2.png")
img.paste(cardicon, (30,650), mask=cardicon)

#topright values
draw = ImageDraw.Draw(img)
draw.text((500, 70), "3", fill=(255,255,255), font=font1, anchor="mm")
draw.text((575, 70), "3", fill=(255,255,255), font=font1, anchor="mm")
draw.text((650, 70), "3", fill=(255,255,255), font=font1, anchor="mm")
#BP
draw.text((640, 690), "3", fill=(255,255,255), font=font1, anchor="mm")
#AP/DP
draw.text((80, 950), "+300", fill=(255,128,128), font=font2, anchor="mm")
draw.text((620, 950), "+300", fill=(128,128,255), font=font2, anchor="mm")
#Card name
draw.text((350, 690), "Eddy the Alchemist", fill=(0,0,0), font=font1, anchor="mm")
#ID number
draw.text((225, 980), "X-205", fill=(0,0,0), font=font3, anchor="mm")
#Copyright text
draw.text((510, 980), "BANDAI OWNS THIS THING", fill=(0,0,0), font=font3, anchor="rm")
#Flavour text
draw.text((350, 915), "Howdy dowdy. It's morbin' time.", fill=(0,0,0), font=font3, anchor="mm")
#Black bar attributes
attributes = ["MALE", "ISHVALAN", "HOMUNCULUS"]
attribute_string = ""
for att in attributes:
    attribute_string += (att + "  ")
draw.text((190, 945), attribute_string, fill=(255,255,255), font=font3, anchor="lm")

#Word wrap only relevant for effects
#d = ImageDraw.Draw(img)
sample_line = "[stub1] And yet here was Matthew Cuthbert, at half-past [stub1] three on the afternoon of a busy day, placidly driving over the hollow and up the hill; moreover, he wore a white collar and his best suit of clothes, which was plain proof that he was going out of Avonlea; and he had the buggy and the sorrel mare, which betokened that he was going a considerable distance. Now, where was Matthew Cuthbert going and why was he going there?"
line_blank = ""
line_total = ""
line_len_max = 580
lineheight = 29#very subject to change
current_line = 0

for word in sample_line.split(" "):
    oldlen = len(line_blank)
    if word[0] == "[" and word[-1] == "]":
        stub = Image.open("components/" + word[1:-1] + ".png")
        line_len = draw.textbbox((0,0), line_blank, font=font4)[2]
        img.paste(stub, (60 + line_len,745 + current_line*lineheight))
        final_line_len = line_len + stub.size[0]
        while final_line_len > line_len:
            line_blank += " "
            line_len = draw.textbbox((0,0), line_blank, font=font4)[2]
        #print(stub.size)
    else:
        line_blank += word
    #print(line_blank)
    line_len = draw.textbbox((0,0), line_blank, font=font4)[2]
    #print(line_len)
    if line_len > line_len_max:
        line_total += (line_blank[:oldlen] + "\n")
        current_line += 1
        line_len = 0
        line_blank = word + " "
    else:
        line_blank += " "
line_total += line_blank
draw.text((60, 745), line_total, fill=(0,0,0), font=font4, anchor="la")

#d.text((50,50), line_total, font=font1)
#print(newbox)
img.save("artsample.jpg")
img.show()
