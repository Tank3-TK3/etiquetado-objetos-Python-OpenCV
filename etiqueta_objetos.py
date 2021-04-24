import cv2
from matplotlib import pyplot as plt
import numpy as np
import os

def umbra( img1 ):
    img = img1.copy()
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if img[i][j] >= 128:
                img[i][j] = 255
            else:
                img[i][j] = 0
    return img

def contVec( img , i , j ):
    cont = 0
    try:
        if img[i][j] == img[i-1][j-1]:
            cont+=1
    except:
        pass
    try:
        if img[i][j] == img[i][j-1]:
            cont+=1
    except:
        pass
    try:
        if img[i][j] == imimg[i+1][j-1]:
            cont+=1
    except:
        pass
    try:
        if img[i][j] == img[i-1][j]:
            cont+=1
    except:
        pass
    try:
        if img[i][j] == img[i+1][j]:
            cont+=1
    except:
        pass
    try:
        if img[i][j] == img[i-1][j+1]:
            cont+=1
    except:
        pass
    try:
        if img[i][j] == img[i][j+1]:
            cont+=1
    except:
        pass
    try:
        if img[i][j] == img[i+1][j+1]:
            cont+=1
    except:
        pass
    return cont

def limpiar( img1 ):
    img = img1.copy()
    cont = 0
    for i in range( 0 , img.shape[0] ):
        for j in range( 0 , img.shape[1] ):
            cont = contVec(img, i, j)
            if cont < 3:
                if img[i][j] == 255:
                    img[i][j] = 0
                else:
                    img[i][j] = 255
            cont = 0
    return img

def findPixel( img1 ):
    img = img1.copy()
    bandera = True
    for i in range( 0 , img.shape[0] ):
        for j in range( 0 , img.shape[1] ):
            if img[i][j] >= 100 and img[i][j] <= border:
                bandera = False
            if img[i][j] == 0:
                bandera = True
            if ( img[i][j] == 255 ) and bandera == True:
                return [ i , j ]
    return None

def vecinos( img , indexsA ):
    colonia = [ None , None , None , None , None , None , None , None ]
    try:
        colonia[0] = img[indexsA[0]][indexsA[1]-1]
    except:
        pass
    try:
        colonia[1] = img[indexsA[0]+1][indexsA[1]-1]
    except:
        pass
    try:
        colonia[2] = img[indexsA[0]+1][indexsA[1]]
    except:
        pass
    try:
        colonia[3] = img[indexsA[0]+1][indexsA[1]+1]
    except:
        pass
    try:
        colonia[4] = img[indexsA[0]][indexsA[1]+1]
    except:
        pass
    try:
        colonia[5] = img[indexsA[0]-1][indexsA[1]+1]
    except:
        pass
    try:
        colonia[6] = img[indexsA[0]-1][indexsA[1]]
    except:
        pass
    try:
        colonia[7] = img[indexsA[0]-1][indexsA[1]-1]
    except:
        pass
    return colonia

def nextPixel( colonia , indexsA ):
    if colonia[0] == 0 and (colonia[1] == 255 or colonia[1] == border):
        return [indexsA[0]+1,indexsA[1]-1]
    if colonia[1] == 0 and (colonia[2] == 255 or colonia[2] == border):
        return [indexsA[0]+1,indexsA[1]]
    if colonia[2] == 0 and (colonia[3] == 255 or colonia[3] == border):
        return [indexsA[0]+1,indexsA[1]+1]
    if colonia[3] == 0 and (colonia[4] == 255 or colonia[4] == border):
        return [indexsA[0],indexsA[1]+1]
    if colonia[4] == 0 and (colonia[5] == 255 or colonia[5] == border):
        return [indexsA[0]-1,indexsA[1]+1]
    if colonia[5] == 0 and (colonia[6] == 255 or colonia[6] == border):
        return [indexsA[0]-1,indexsA[1]]
    if colonia[6] == 0 and (colonia[7] == 255 or colonia[7] == border):
        return [indexsA[0]-1,indexsA[1]-1]
    if colonia[7] == 0 and (colonia[0] == 255 or colonia[0] == border):
        return [indexsA[0],indexsA[1]-1]

def borde( img1 ):
    img = img1.copy()
    indexsA = findPixel( img )
    indexsS = []
    indexsS.append(indexsA[0])
    indexsS.append(indexsA[1])
    try:
        while img[indexsS[0]][indexsS[1]] != border:
            if img[indexsA[0]][indexsA[1]] != 0:
                img[indexsA[0]][indexsA[1]] = border
            colonia = vecinos( img , indexsA )
            indexsS = nextPixel( colonia , indexsA )
            indexsA[0] = indexsS[0]
            indexsA[1] = indexsS[1]
    except:
        pass
    return img

def etiqueta( img1 ):
    img = img1.copy()
    for i in range( 0 , img.shape[0] ):
        for j in range( 0 , img.shape[1] ):
            if img[i-1][j] >= 100 and img[i-1][j] <= border and img[i][j] == 255:
                img[i][j] = img[i-1][j]
    return img

border = 100
img1 = cv2.imread( './img/objetos.jpg', 0 )
img2 = np.zeros( img1.shape , dtype=np.uint8 )

img2 = umbra( img1 )

for i in range(0,10):
    img2 = limpiar( img2 )
    print("Limpieza:",i+1)

while findPixel(img2) != None:
    img2 = borde( img2 )
    border+=1
    print("Bordes:",border-100)

img2 = etiqueta( img2 )

plt.subplot( 1 , 2 , 1 )
plt.imshow( img1 , 'gray' )
plt.title( 'Objetos' )
plt.axis( 'off' )

plt.subplot( 1 , 2 , 2 )
plt.imshow( img2 , 'gray' )
plt.title( 'Objetos Umbralizado' )
plt.axis( 'off' )

plt.show()


file = open("./img.csv", "w")
for i in range(0,img2.shape[0]):
    string = ""
    for j in range(0,img2.shape[1]):
        string += str(img2[i][j])+","
    string+="\n"
    file.write(string)
file.close()
print("<<<Archivo CSV generado correctamente>>>")
