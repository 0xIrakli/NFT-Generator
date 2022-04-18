from PIL import Image
import random as rand
import json
import math
import time
import sys
import os

ACCESSORIES = "accessories\\"
WHITE =      (255, 255, 255, 255)
BLACK =      (  0,   0,   0, 255)
GOLD =       (244, 224, 130, 255)
BACKGROUND = ( 35, 210, 120, 230)
amounts = {}
persons = []

lang = json.load(open('lang.json', 'r'))

def random():
    return rand.randint(0, 255), rand.randint(0, 255), rand.randint(0, 255)

def plus(p1, p2):
    return min(p1[0]+p2[0], 255), min(p1[1]+p2[1], 255), min(p1[2]+p2[2], 255)

def mult(p1, p2):
    return int(min(p1[0]*p2[0], 255)), int(min(p1[1]*p2[1], 255)), int(min(p1[2]*p2[2], 255))

def div(p1, p):
    return min(float(p1[0]/p), 255), min(float(p1[1]/p), 255), min(float(p1[2]/p), 255)

def chance(perc):
    return rand.randrange(0, 101) <= perc

def randrange(a, b):
    return rand.randrange(a, b)

def listfiles(dir):
    return os.listdir(dir)

def routine():
    for KEY in listfiles(ACCESSORIES):
        sum_ = sum(list(amounts[KEY].values()))
        for accessory in listfiles(f'{ACCESSORIES}{KEY}'):
            index = f'{ACCESSORIES}{KEY}\\{accessory}'
            val = amounts[KEY][index]
            amounts[KEY][index] = (float(val)/float(sum_))*float(100)
    with open('amounts.json', 'w') as f:
        txt = json.dumps(amounts, indent = 4)
        f.write(txt)

##colors = list(map(lambda X: base.getpixel((X/base.height, X/base.width)), list(range(base.width*base.height))))
probabilities = {}

def map_prob(file):
    data = json.load(file)
    for categorykey in data.keys():
        category = data[categorykey]
        n = 0
        if categorykey not in probabilities.keys():
            probabilities[categorykey] = {}
        for key in category.keys():
            prob = category[key]
            for i in range(n, n+prob):
                probabilities[categorykey][i] = key
            n += prob
    json.dump(probabilities, open('probabilty_map.json', 'w'), indent=4)

def setup():
    map_prob(file=open('chances.json', 'r'))
    for i in listfiles(ACCESSORIES):
        amounts[i] = {}
        for j in listfiles(ACCESSORIES+i):
            amounts[i][f'{ACCESSORIES}{i}\\{j}'] = 0

class Person:
    def __init__(self, base, eye_mask, golden=False):
        self.base = Image.open(base)
        self.eyemask = Image.open(eye_mask)
        
        self.golden = golden
        self.base_color = random()
        self.eye_color1 = random()
        self.eye_color2 = self.eye_color1
        
        self.accessories_ = []
        self.heterochromia = False
        
        self.img = Image.open(base)
        
    def color_skin(self):
        for y in range(self.img.height):
            for x in range(self.img.width):
                pix = self.img.getpixel((x, y))
                if pix == BLACK:
                    self.img.putpixel((x, y), self.base_color)
                elif pix == WHITE and self.golden:
                    self.img.putpixel((x, y), GOLD)
                elif pix == WHITE:
                    self.img.putpixel((x, y), WHITE)
                elif pix[3] == 255:
                    self.img.putpixel((x, y), plus(pix, self.base_color))
                elif pix[3] == 0:
                    self.img.putpixel((x, y), BACKGROUND)

    def color_eyes(self):
        for y in range(self.img.height):
            for x in range(self.img.width):
                if self.eyemask.getpixel((x, y)) == (0, 0, 0, 255):
                    self.img.putpixel((x, y), self.eye_color1)
                if self.eyemask.getpixel((x, y)) == (255, 255, 255, 255):
                    self.img.putpixel((x, y), self.eye_color2)
            
    def add_accessory(self, KEY, _chance, _accessory=None):
        indx = f'{ACCESSORIES}{KEY}\\'
        #when accessory not specified
        if not _accessory:
            accessory = probabilities[KEY][randrange(0, 100)]
        else:
            accessory = f'{indx}{_accessory}'
        if chance(_chance) or _accessory:
            if self.heterochromia:
                self.accessories_.append("Has Heterochromia")
            self.accessories_.append(lang[accessory])
            amounts[KEY][accessory]+=1
            
            acc = Image.open(accessory)
            for y in range(self.img.height):
                for x in range(self.img.width):
                    pix = acc.getpixel((x, y))
                    if pix[3] == 255:
                        self.img.putpixel((x, y), pix)
                    
    def save(self, n):
        self.img.save(f'outputs/raw/{n}.png')
        img = self.img.resize((540, 540), Image.NEAREST)
        img.save(f'outputs/{n}.png')

def main_notrandom():
    setup()
    num = len(listfiles('accessories\\eye'))*len(listfiles('accessories\\face'))*len(listfiles('accessories\\hat'))*len(listfiles('accessories\\neck'))-1#int(sys.argv[1])
    time1 = time.perf_counter()
    BACKGROUND = (100, 100, 100, 255)
    last = 0
    iteration = 0
    for EYE in listfiles('accessories\\eye'):
        for FACE in listfiles('accessories\\face'):
            for HAT in listfiles('accessories\\hat'):
                for NECK in listfiles('accessories\\neck'):
                    person = Person('base.png', 'eye_mask.png', False)
                    
                    person.color_skin()
                    if (chance(1)): #1% chance to have different colored eyes. (no eye accessory)
                        person.eye_color2 = random()
                    person.color_eyes()
                    person.add_accessory('eye', 30, EYE)#35
                    person.add_accessory('neck', 25, NECK)#25
                    person.add_accessory('face', 10, FACE)#10
                    person.add_accessory('hat', 60, HAT)#55

                    persons.append(person)
                    person.save(iteration)

                    now = time.perf_counter()
                    print(f'{iteration}/{num}  {round(now-last, 2)}s')
                    last = time.perf_counter()
                        
                    iteration+=1

metadata = {}
 
def main_random(num):
    setup()
    time1 = time.perf_counter()
    last = 0

    for iteration in range(num):
        person = Person('base.png', 'eye_mask.png')
        person.color_skin()
        if (chance(1)): #1% chance to have different colored eyes. (no eye accessory)
            person.eye_color2 = random()
            person.heterochromia = True
            
        person.color_eyes()
        person.add_accessory('eye', 20)#35
        person.add_accessory('neck', 20)#25
        person.add_accessory('face', 10)#10
        person.add_accessory('hat', 35)#55

        persons.append(person)
        person.save(iteration)
        metadata[iteration] = {}
        metadata[iteration]['accessories'] = person.accessories_
        metadata[iteration]['features'] = {}
        metadata[iteration]['features']['heterochromia'] = True
        metadata[iteration]['features']['base_color'] = person.base_color

        if iteration % 20 == 0:
            now = time.perf_counter()
            print(f'{iteration}/{num}  {round(now-last, 2)}s')
            last = time.perf_counter()
            
    with open('amounts.json', 'w') as f:
            txt = json.dumps(amounts, indent = 4)
            f.write(txt)
            
    with open('metadata.json', 'w') as f:
            txt = json.dumps(metadata, indent = 4)
            f.write(txt)

    time2 = time.perf_counter()
    print(f"I'm done! Elapsed: {round(time2-time1, 2)}s")

main_random(sys.argv[1])
routine()
input('Press Enter To Exit')