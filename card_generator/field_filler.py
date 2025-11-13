from PIL import Image, ImageDraw, ImageFont
import textwrap
import pandas
import os

att_dict = {"B21":"Earth Type", "B22":"Fire Type", "B23":"Water Type", "B24":"Wind Type", "B25":"Thunder Type", "B31":"Metallurgy", "B32":"Melee Type", "B33":"Indirect Type", "B34":"Weapon Type", "B35":"Defense Type", "B40":"Chimera Type", "B70":"Homunculus Type", "C11":"Male","C12":"Female","C13":"Dog","C21":"Soldier","C22":"Master","C23":"Male (Animal)","C24":"Librarian","C25":"Policeman","C26":"Saint","C27":"Doctor","C28":"Lord of numbers","C29":"Phantom thief","C20":"Butcher","C31":"Chimera","C32":"Scientist","C33":"The Führer","C34":"Death row prisoner","C35":"Young lady","C41":"Alchemist","C42":"Foundation leader","C43":"Film director","C51":"Mechanical armourer","C61":"Homunculus","C62":"State alchemist","C81":"Ishvalan","E50":"Alchemy","E51":"Chimera"}

def generate_badge(input_text=""):
    #input_text = "2,3,4"
    AFG = False
    if str(input_text) != "nan" and not os.path.isfile("components/badges/"+"AFG-" + input_text+".png") and not os.path.isfile("components/badges/"+input_text.replace(",","-")+".png"):
        img = Image.new("RGBA", (800, 48), color=(0,0,0,0))

        tip = Image.open("components/ATK-Start tri.png")
        tail = Image.open("components/ATK-End tri.png")
        mid = Image.open("components/ATK-Mid.png")
        font4 = ImageFont.load_default(size=25.0)

        icon_A = Image.open("components/icon1 sml.png")
        icon_F = Image.open("components/icon2 sml.png")
        icon_G = Image.open("components/icon3 sml.png")

        img.paste(tip, (0,0))
        draw = ImageDraw.Draw(img)
        if len(input_text.split(",")) > 1 and len(input_text.split(" ")) == 1:
            AFG = True
            line_len = 100
            if len(input_text.split(",")) > 2:
                line_len = 206
                img.paste(tip, (170,0),mask=tip)
                img.paste(tail, (152,0), mask=tail)
                for i in range(170+48, 170+48+40):
                    img.paste(mid, (i,0))
                img.paste(icon_G, (170+48,4), mask=icon_G)
                draw.text((170+78,30), input_text.split(",")[2], fill=(255,255,255), font=font4, anchor="mm")
            for i in range(48, 52 + 100):
                img.paste(mid, (i,0))
            img.paste(icon_A, (50,4), mask=icon_A)
            img.paste(icon_F, (100,4), mask=icon_F)
            draw.text((50+32,30), input_text.split(",")[0], fill=(255,255,255), font=font4, anchor="mm")
            draw.text((100+32,30), input_text.split(",")[1], fill=(255,255,255), font=font4, anchor="mm")
            #input_text = ""
        else:
            line_len = draw.textbbox((0,0), input_text, font=font4)[2]
            for i in range(48, 52 + line_len):
                img.paste(mid, (i,0))
            draw.text((50,24), input_text, fill=(255,255,255), font=font4, anchor="lm")
        #print(line_len)
        img.paste(tail, (line_len+52,0), mask=tail)
        crop_img = img.crop((0,0,line_len+100,48))
        if AFG:
            crop_img.save("components/badges/"+"AFG-" + input_text+".png")
        elif input_text != "EFF" and input_text != "EXC":
            crop_img.save("components/badges/"+input_text.replace(" ","_")+".png")

def generate_card(serial="X-000", name="", AFicon="A", underline_types="", flavour="", bandaitag="", bullet1="", bullet2="", numbersTR="", APDP="", BP=""):

    #determine card type:
    cardtype = serial.split("-")[0][-1]
    if cardtype == "P":
        cardtype = "C"
    if cardtype == "C":
        if str(APDP) != "nan":
            cardtype += "M"
        else:
            cardtype += "S"
    
    #canvas
    img = Image.new("RGB", (700, 1000), color=(128,128,128))

    #card art and template
    cardart = Image.open("components/art.png")
    if cardtype == "B":
        cardbase = Image.open("components/bbase.png")
    if cardtype == "CM":
        cardbase = Image.open("components/cmbase.png")
    if cardtype == "CS":
        cardbase = Image.open("components/csbase.png")
    if cardtype == "E":
        cardbase = Image.open("components/ebase.png")
    img.paste(cardart, (0,50))
    img.paste(cardbase, (0,0), mask=cardbase)

    #text setup
    font1 = ImageFont.load_default(size=45.0)
    font2 = ImageFont.load_default(size=65.0)
    font3 = ImageFont.load_default(size=15.0)
    font4 = ImageFont.load_default(size=25.0)

    #icon
    if AFicon == "A":
        cardicon = Image.open("components/icon1.png")
    else:
        cardicon = Image.open("components/icon2.png")
    img.paste(cardicon, (30,650), mask=cardicon)

    #topright values
    draw = ImageDraw.Draw(img)
    if str(numbersTR) != "nan":
        draw.text((500, 70), numbersTR.split(",")[0], fill=(255,255,255), font=font1, anchor="mm")
        draw.text((575, 70), numbersTR.split(",")[1], fill=(255,255,255), font=font1, anchor="mm")
        draw.text((650, 70), numbersTR.split(",")[2], fill=(255,255,255), font=font1, anchor="mm")
    #BP
    if str(BP) != "nan":
        draw.text((640, 690), str(int(BP)), fill=(255,255,255), font=font1, anchor="mm")
    #AP/DP
    if str(APDP) != "nan":
        AP = APDP.split("-")[0]
        DP = APDP.split("-")[1]
        draw.text((80, 950), "+"+AP, fill=(255,128,128), font=font2, anchor="mm")
        draw.text((620, 950), "+"+DP, fill=(128,128,255), font=font2, anchor="mm")
    #Card name
    draw.text((350, 690), name, fill=(0,0,0), font=font1, anchor="mm")
    #ID number
    draw.text((225, 980), serial, fill=(0,0,0), font=font3, anchor="mm")
    #Copyright text
    draw.text((510, 980), bandaitag, fill=(0,0,0), font=font3, anchor="rm")
    #Flavour text
    draw.text((350, 915), flavour, fill=(0,0,0), font=font3, anchor="mm")
    #Black bar attributes
    attributes = str(underline_types).split("-")#["MALE", "ISHVALAN", "HOMUNCULUS"]
    attribute_string = ""
    if attributes[0] != "Blank":
        for att in attributes:
            attribute_string += (att_dict[cardtype[0]+att] + "  ")
    if cardtype == "B" or cardtype == "CM":
        draw.text((190, 945), attribute_string, fill=(255,255,255), font=font3, anchor="lm")
    else:
        draw.text((50, 945), attribute_string, fill=(255,255,255), font=font3, anchor="lm")

    #Word wrap only relevant for effects
    #d = ImageDraw.Draw(img)
    current_line = 0
    line_total = ""
    bullet_lines = []
    if str(bullet1) != "" and str(bullet1) != "nan":
        bullet_lines.append(str(bullet1))
        if str(bullet2) != "" and str(bullet2) != "nan":
            bullet_lines.append(str(bullet2))
    if len(bullet_lines) > 0:
        for bullet_line in bullet_lines:
            #print(bullet_line)
            sample_line = bullet_line#And yet here was Matthew Cuthbert, at half-past [stub1] three on the afternoon of a busy day, placidly driving over the hollow and up the hill; moreover, he wore a white collar and his best suit of clothes, which was plain proof that he was going out of Avonlea; and he had the buggy and the sorrel mare, which betokened that he was going a considerable distance. Now, where was Matthew Cuthbert going and why was he going there?"
            line_blank = ""
            line_len_max = 580
            lineheight = 29#very subject to change

            for word in sample_line.split(" "):
                oldlen = len(line_blank)
                if word[0] == "<" and word[-1] == ">":
                    #print(word)
                    stub = Image.open("components/badges/" + word[1:-1] + ".png")
                    if word[1:-1] == "EFF" or word[1:-1] == "EXC":
                        line_len = draw.textbbox((0,0), line_blank, font=font4)[2]
                        img.paste(stub, (60 + line_len,745 + current_line*lineheight), mask=stub)
                        final_line_len = line_len + stub.size[0]
                    else:
                        line_len = draw.textbbox((0,0), line_blank, font=font4)[2]
                        if word[1:5] == "AFG-":
                            img.paste(stub, (25 + line_len,740 + current_line*lineheight), mask=stub)
                            final_line_len = -60+15 + line_len + stub.size[0]
                        else:
                            img.paste(stub, (30 + line_len,740 + current_line*lineheight), mask=stub)
                            final_line_len = -60+20 + line_len + stub.size[0]
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
            line_total += (line_blank + "\n")
            current_line += 1
            line_blank = ""
            draw.text((60, 745), line_total, fill=(0,0,0), font=font4, anchor="la")

    #d.text((50,50), line_total, font=font1)
    #print(newbox)
    img.save("outputs/"+serial+".jpg")
#img.show()


ssheet = pandas.read_excel("../numbers - data entry.ods", engine="odf")
row_index = 0
#dotheseones = ["B-001", "B-002", "B-003", "B-004", "B-005", "B-006", "B-007", "B-008", "B-009", "B-010", "B-011", "B-012", "B-013", "B-014", "B-015", "B-016", "B-017", "B-018", "B-019", "B-020", "B-021", "E-005", "C-010"]
dotheseones = []
for i in range(1,22):
    dotheseones.append("B-"+("000"+str(i))[-3:])
    dotheseones.append("C-"+("000"+str(i))[-3:])
for i in range(1,16):
    dotheseones.append("E-"+("000"+str(i))[-3:])
for index, row in ssheet.iterrows():
    if ssheet.iat[row_index, 0] in dotheseones:
        card_bullet1 = ""
        card_bullet2 = ""
        if str(ssheet.iat[row_index, 10]) != "nan":
            if str(ssheet.iat[row_index, 8]) != "nan":
                generate_badge(ssheet.iat[row_index, 8])
                card_bullet1 += "<" + ssheet.iat[row_index, 8].replace(" ","_") + "> "
                if str(ssheet.iat[row_index, 9]) != "nan":
                    generate_badge(ssheet.iat[row_index, 9])
                    card_bullet1 += "<" + "AFG-" + ssheet.iat[row_index, 9] + "> "
            card_bullet1 += ssheet.iat[row_index, 10]
        if str(ssheet.iat[row_index, 13]) != "nan":
            if str(ssheet.iat[row_index, 11]) != "nan":
                generate_badge(ssheet.iat[row_index, 11])
                card_bullet2 += "<" + ssheet.iat[row_index, 11].replace(" ","_") + "> "
                if str(ssheet.iat[row_index, 12]) != "nan":
                    generate_badge(ssheet.iat[row_index, 12])
                    card_bullet2 += "<" + "AFG-" + ssheet.iat[row_index, 12] + "> "
            card_bullet2 += ssheet.iat[row_index, 13]
        #bullet1=ssheet.iat[row_index, 10], bullet2=ssheet.iat[row_index, 13]
        generate_card(serial=ssheet.iat[row_index, 0], name=ssheet.iat[row_index, 2], AFicon=ssheet.iat[row_index, 5], underline_types=ssheet.iat[row_index, 7], bullet1=card_bullet1, bullet2=card_bullet2, numbersTR=ssheet.iat[row_index, 3], APDP=ssheet.iat[row_index, 4], BP=ssheet.iat[row_index, 6])
    row_index += 1
