import sys
import cv2
import numpy as np
from statistics import mean
import webcolors

def open_im(img):
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def init_list_of_elt(img, l):
    dst = []
    for elt in l:
        dst.append(decoupe(img, elt))
    return dst

def in_form(elt, x_, y_):
    # return True si le point est dans la forme
    x, y, w, h = elt
    if x_ >= x and x_ <= x + w:
        if y_ >= y and y_ <= y + h:
            return True
    return False

def draw_contours_find(list_contour, img, color = (0,255,0)):
    for x, y, w, h in list_contour:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),color,2)

def decoupe(img, elt):
    x, y, w, h = elt
    crop_img = img[y:y+h, x:x+w]
    return crop_img

def complete_border(im):
    row, col= im.shape[:2]
    bottom= im[row-2:row, 0:col]
    if (row > col):
        bordersize= int((row - col)/ 2)
        border=cv2.copyMakeBorder(im, top=0, bottom=0, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=[255,255,255] )
    elif (row < col):
        bordersize= int((col - row)/ 2)
        border=cv2.copyMakeBorder(im, top=bordersize, bottom=bordersize, left=0, right=0, borderType= cv2.BORDER_CONSTANT, value=[255,255,255] )
    else:
        border = im

    return border

def add_border(im):
    row, col= im.shape[:2]
    bottom= im[row-2:row, 0:col]
    bordersize= int(max(row,col) * 0.025)
    border=cv2.copyMakeBorder(im, top=1, bottom=1, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=[255,255,255] )

    return border


def delete_bad_contour(l):
    dst = []
    for elt in l:
        x, y, w, h = elt
        dead = False
        for tmp in l:
            x_, y_, w_, h_ = tmp

            n1 = 0

            if (in_form(tmp, x , y) == True):
                n1 += 1
            if (in_form(tmp, x , y + h) == True):
                n1 += 1
            if (in_form(tmp, x + w , y + h) == True):
                n1 += 1
            if (in_form(tmp, x + w, y) == True):
                n1 += 1

            if (n1 == 4):
                if (w*h < w_*h_):
                    dead = True
                    break

        if (dead == False):
            dst.append(elt)

    return dst


def segmentation(img):
    # on trouve tout les contours

    hight, weidth = img.shape

    contours,hierarchy = cv2.findContours(img, 1, 2)
    result_list = []
    for i in contours:
        x,y,w,h = cv2.boundingRect(i)
        if x != 0 or y != 0 or hight != h or weidth != w:
            if  w  > 3 and h > 3 and w*h > 5:
                tmp = (x, y, w, h)
                result_list.append(tmp)
    return result_list

def pre_traitement(img):
    # on met l image en noir et blanc
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh3 = cv2.threshold(img_gray,200,255,cv2.THRESH_BINARY)
    #ret,thresh4 = cv2.threshold(thresh3,127,0,cv2.THRESH_TOZERO)
    return thresh3

def resize_elt(l):
    dst = []
    for elt in l:
        tmp = cv2.resize(elt,(28,28))
        gaus = cv2.adaptiveThreshold(tmp, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 12)
        dst.append(gaus)
    return dst


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name


def main_prepro(path):
    img = cv2.imread(path)
    #img = add_border(img)
    gaus = pre_traitement(img)
    l = segmentation(gaus)
    l = delete_bad_contour(l)
    squared = list(map(lambda x: x[2]*x[3], l))
    elt = squared.index(max(squared))
    l = [l[elt]]

    #draw_contours_find(l,img, (0,0,255))
    n = decoupe(gaus, l[0])
    color_img = decoupe(img, l[0])
    
    color = cv2.resize(color_img,(1,1))
    color_name = ""
    rgb = (color[0][0][2],color[0][0][1],color[0][0][0])
    actual_name, closest_name = get_colour_name(rgb)
    if actual_name == None:
        color_name = closest_name
    else:
        color_name = actual_name

    new2 = add_border(n)
    new2 = complete_border(new2)
    #open_im(new2)
    res = cv2.resize(new2,(28,28))

    imagem = cv2.bitwise_not(res)
    #open_im(imagem)
    return imagem, color_name, rgb

#main_prepro("test_set/shoes_01.jpg")

