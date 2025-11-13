from PIL import Image, ImageDraw, ImageFont
import textwrap
import pandas

att_dict = {"B21":"Earth Type", "B22":"Fire Type", "B23":"Water Type", "B24":"Wind Type", "B25":"Thunder Type", "B31":"Metallurgy", "B32":"Melee Type", "B33":"Indirect Type", "B34":"Weapon Type", "B35":"Defense Type", "B40":"Chimera Type", "B70":"Homunculus Type", "C11":"Male","C12":"Female","C13":"Dog","C21":"Soldier","C22":"Master","C23":"Male (Animal)","C24":"Librarian","C25":"Policeman","C26":"Saint","C27":"Doctor","C28":"Lord of numbers","C29":"Phantom thief","C20":"Butcher","C31":"Chimera","C32":"Scientist","C33":"The Führer","C34":"Death row prisoner","C35":"Young lady","C41":"Alchemist","C42":"Foundation leader","C43":"Film director","C51":"Mechanical armourer","C61":"Homunculus","C62":"State alchemist","C81":"Ishvalan","E50":"Alchemy","E51":"Chimera"}

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
            sample_line = "<stub1> " + bullet_line#And yet here was Matthew Cuthbert, at half-past [stub1] three on the afternoon of a busy day, placidly driving over the hollow and up the hill; moreover, he wore a white collar and his best suit of clothes, which was plain proof that he was going out of Avonlea; and he had the buggy and the sorrel mare, which betokened that he was going a considerable distance. Now, where was Matthew Cuthbert going and why was he going there?"
            line_blank = ""
            line_len_max = 580
            lineheight = 29#very subject to change

            for word in sample_line.split(" "):
                oldlen = len(line_blank)
                if word[0] == "<" and word[-1] == ">":
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
        generate_card(serial=ssheet.iat[row_index, 0], name=ssheet.iat[row_index, 2], AFicon=ssheet.iat[row_index, 5], underline_types=ssheet.iat[row_index, 7], bullet1=ssheet.iat[row_index, 10], bullet2=ssheet.iat[row_index, 13], numbersTR=ssheet.iat[row_index, 3], APDP=ssheet.iat[row_index, 4], BP=ssheet.iat[row_index, 6])
    row_index += 1
