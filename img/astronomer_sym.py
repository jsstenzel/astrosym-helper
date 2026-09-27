

#arguments
#asteroid number
#string of 1-3 letters for top part
#'base', or 'star', or string of 1-3 letters for bottom part

from PIL import Image
import argparse

def open_transparently(img_string):
    img = Image.open(img_string)
    #img = img.convert("RBGA")
    datas = img.getdata()
    
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0)) #turning white into transparent
        else:
            newData.append(item)
        
    img.putdata(newData)
    return img
    
    
def save_flat(img, filename):
    datas = img.getdata()
    
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 255)) #turning transparent into white
        else:
            newData.append(item)
        
    img.putdata(newData)
    img.save(filename)
    
def needs_flip(letter):
    if letter == 'A' or letter == 'V' or letter == 'Y':
        return True
        
def needs_top(letter):
    if letter in ['B','C','D','E','G','J','L','O','Q','S','U','V','Z','@']:
        return True
        
def needs_high(letter):
    if letter in ['A','F','H','K','M','N','P','R','W','X']:
        return True

  
def main(num, top, bottom):
    basepic = 'symbemes/' + bottom + '.png'
    blanktop = 'symbemes/blanktop.png'
    blankhigh = 'symbemes/blankhigh.png'
        
    base_img = open_transparently(basepic)
    blanktop_img = open_transparently(blanktop)
    blankhigh_img = open_transparently(blankhigh)
          
    if len(top) == 1:
        letter = top[0]
        pic = 'symbemes/' + ('_' if letter.islower() else ('mid' if letter in ['A','V'] else '' )) + letter + '.png'
        img = open_transparently(pic)
        if needs_top(letter):
            base_img.paste(blanktop_img, (0,0), blanktop_img)
        elif needs_high(letter):
            base_img.paste(blankhigh_img, (0,0), blankhigh_img)
        base_img.paste(img, (75 - (int(img.width / 2.0)), 9), img)

    elif len(top) == 2:
        left_letter = top[0]
        leftpic = 'symbemes/' + ('_' if left_letter.islower() else '') + left_letter + '.png'
        left_img = open_transparently(leftpic)
        if needs_flip(left_letter):
            left_img = left_img.transpose(Image.FLIP_LEFT_RIGHT)
        if left_letter == 'v':
            base_img.paste(blankhigh_img, (0,0), blankhigh_img)
        if left_letter.islower():
            base_img.paste(left_img, (32+13,9), left_img)
        else:
            base_img.paste(left_img, (32,9), left_img)
                        
        right_letter = top[1]
        rightpic = 'symbemes/' + ('_' if right_letter.islower() else '') + right_letter + '.png'
        right_img = open_transparently(rightpic)
        base_img.paste(right_img, (73,9), right_img)
    elif len(top) == 3:
        left_letter = top[0]
        mid_letter = top[1]
        right_letter = top[2]
            
        midpic = 'symbemes/' + \
            ('_' if mid_letter.islower() else ('mid' if mid_letter in ['A','V'] else '' )) + mid_letter + '.png'
        mid_img = open_transparently(midpic)
        if needs_top(mid_letter):
            base_img.paste(blanktop_img, (0,0), blanktop_img)
        elif needs_high(mid_letter):
            base_img.paste(blankhigh_img, (0,0), blankhigh_img)
        base_img.paste(mid_img, (53,9), mid_img)
            
        leftpic = 'symbemes/' + ('_' if left_letter.islower() else '') + left_letter + '.png'
        left_img = open_transparently(leftpic)
        if needs_flip(left_letter):
            left_img = left_img.transpose(Image.FLIP_LEFT_RIGHT)
        if left_letter.islower():
            base_img.paste(left_img, (21,9), left_img)
        else:
            base_img.paste(left_img, (8,9), left_img)
            
        rightpic = 'symbemes/' + ('_' if right_letter.islower() else '') + right_letter + '.png'
        right_img = open_transparently(rightpic)
        base_img.paste(right_img, (93,9), right_img)
            
    else:
        print("wrong top")
        exit()
          
    #Saved in the same relative location
    save_flat(base_img, (str(num) + ".png"))
          
  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate asteroid symbols ')
    parser.add_argument('-l', action="store_true", help='Set this flag to iterate through auto_sym_list.txt instead')
    parser.add_argument('asteroid_num', metavar='asteroid_num', type=str, nargs='?', default="0", help='The number of the asteroid.')
    parser.add_argument('top', metavar='top', type=str,  nargs='?', default="@", help='The 1-3 letters on top of the symbol.')
    parser.add_argument('bottom', metavar='bottom', type=str,  nargs='?', default="empty", help="The bottom of the symbol, either 'base' or 'star' or 'mw'.")
    args = parser.parse_args()
    
    if args.l:
        with open("auto_sym_list.txt", 'r') as file:
            for line in file:
                line = line.strip('\n')
                row = line.split(" ")
                try:
					if row[0][0] != '#':
                        main(row[0], row[1], row[2])
                except:
                    print("Skipping "+row[0]+" "+row[1]+" "+row[2])
    else:
        try:
            main(args.asteroid_num, args.top, args.bottom)
        except:
            print("cringe ass")










