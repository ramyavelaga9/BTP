'''Change the dir_path and out_dir to directory containing images and output direcory respectively'''

import pytesseract
from pytesseract import Output
import cv2
import json
import os
from os import listdir
from os.path import isfile, join

app = Flask(__name__)

#Remove these two lines if working on ubuntu 
pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files\Tesseract-OCR\tesseract.exe"
tessdata_dir_config = r'--tessdata-dir "D:\Program Files\Tesseract-OCR\tessdata"'

dir_path=r"static\Images"
out_dir=r"static\Json"

def getAnnotations():
    images_list=[]
    print("in")
    for f in listdir(dir_path):
        if isfile(join(dir_path, f)):
            print(f)
            images_list.append(join(dir_path,f))
    
    for filename in images_list:
        l=[]
        s=(0,0,0,0,"")
        img = cv2.imread(filename)
        height = img.shape[0]
        width = img.shape[1]

        d = pytesseract.image_to_boxes(img, output_type=Output.DICT, config=tessdata_dir_config)

        n_boxes = len(d['char'])
        for i in range(n_boxes):
            (x1, h1, x2, h2, label) = (d['left'][i], d['top'][i], d['right'][i], d['bottom'][i], d['char'][i])
            s=(x1,height-h1,x2,height-h2,ord(label))
            l.append(s)
            cv2.rectangle(img, (s[0], s[1]), (s[2], s[3]), (0, 255, 0), 2)

        cv2.imshow('img', img)
        make_json(l,filename)

def make_json(l, file_path):
    dic={}
    for i in range(len(l)):
        dic[i]={}
        dic[i]["label"]=l[i][4]
        coord = []
        s=(l[i][0], l[i][1])
        coord.append(s)
        s=(l[i][2], l[i][3])
        coord.append(s)
        dic[i]["coordinates"]=coord
    head, filename = ntpath.split(file_path)
    pre,ext = os.path.splitext(filename)
    json_filename=pre+".json"
    json_filepath = join(out_dir, json_filename)
    print(json_filename)
    with open(json_filepath,"w") as f:
        json.dump(dic,f)

if __name__ == "__main__":
    getAnnotations()