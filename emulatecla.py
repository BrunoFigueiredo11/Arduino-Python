#!/usr/bin/python
# -*- coding: utf-8 -*-

# Programa simples com camera webcam e opencv que emula precionamento de teclas

import cv2
import os,sys, os.path
import numpy as np
import math

#importes para emular precionamento de teclas
from pynput.keyboard import Key, Controller
import pynput
import time
import random

import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)
global response
response = 0

def EnviaValor(valorArduino):
     global response
     #Se o led estiver desligado e houver uma cor compativel o led liga
     if(valorArduino > 0 and int(response) == 0):
            msg = '1'        
            ser.write(msg.encode()) # Envia a mensagem para o Arduino
            time.sleep(1)
            while ser.inWaiting() > 0:
                response = ser.readline().decode().strip()
    #Se o led estiver ligado e não houver uma cor compativel o led desliga
     elif(valorArduino < 0 and int(response) == 1):
            msg = '0'     
            ser.write(msg.encode())
            time.sleep(1)
            while ser.inWaiting() > 0:
                response = ser.readline().decode().strip()

def filtro_de_cor(img_bgr, low_hsv, high_hsv):
    """ retorna a imagem filtrada"""
    img = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, low_hsv, high_hsv)
    return mask 

def image_da_webcam(img):
 
    mask_hsv = filtro_de_cor(img, np.array([50, 150, 125])  , np.array([200, 255, 255])) #filtro rosa

    contornos, _ = cv2.findContours(mask_hsv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    
    mask_rgb = cv2.cvtColor(mask_hsv, cv2.COLOR_GRAY2RGB) 
    contornos_img = mask_rgb.copy()
    
    maior = None
    listArea = []
    for i in range (len(contornos)):
     listArea.append(contornos[i])
    for c in range (2):                
       listArea.sort(key=lambda listArea: cv2.contourArea(listArea),reverse=True)
       if(len(listArea) > 0):
         maior= listArea[0]
         M = cv2.moments(maior)
         #Se houver alguma imagem, ela é contornada
         if M["m00"] != 0:
                cv2.drawContours(contornos_img, [maior], -1, [255, 0, 0], 5)
                EnviaValor(1)
       else:
          EnviaValor(-1)

       
            
    

    return contornos_img

cv2.namedWindow("preview")
# define a entrada de video para webcam
vc = cv2.VideoCapture(0)

#configura o tamanho da janela 
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 540)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 380)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    
    img = image_da_webcam(frame) # passa o frame para a função imagem_da_webcam e recebe em img imagem tratada

    cv2.imshow("Original", frame)
    cv2.imshow("preview", img)
   
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()