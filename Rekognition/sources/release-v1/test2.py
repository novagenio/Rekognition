from __future__ import print_function
import os, time, sys

import kivy
kivy.require('1.0.6') # replace with your current kivy version !

import boto3
import functions_rekognitionv2

from PIL import Image

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image as kivyImage
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

# Some variables
photoPath = "/home/pi/proyectos/Rekognition/sources/release-v1/"
photoName = time.strftime("%Y%m%d%H%M%S") + ".jpg"
photoResize = 512, 384
photoTitle = "Fred's Photo Booth!"
variable_photo="mano.jpg"


# Callback function for photo button
def photo_find(obj):
        # Define filename with timestamp
        photoName = "IMG" + time.strftime("%Y%m%d%H%M%S") +  ".jpg"
        # Take photo using "raspistill"
        os.system("raspistill -p '112, 40,575,400' -t 3000 --vflip -w 1920 -h 1440 -ae 32,0xff,0x808000 -a 'Hola, por favor mire la luz roja ... ' -o " + photoPath + photoName)
        ##
        nombre = "desconocido ..."
        functions_rekognitionv2.upload_file_s3(photoName,photoName)
        print("s3 ")
        face_id, porcentaje=functions_rekognitionv2.SearchFacesByImage(photoName)
        print("face ")
        nombre=functions_rekognitionv2.BuscaEnBd(face_id)
        print("El nombre encintrado es: " + nombre)
        ##
        # Resize the high res photo to create thumbnail
        saludo = "Hola, el sistema NovaGenio,  te ha identificado como: " + nombre + ", con una exactitud del: " + str(porcentaje) + "%, gracias."
        comando="raspistill -p '112, 40,575,400' --vflip -w 1920 -h 1440 -ae 32,0xff,0x808000 -a " + "'" + saludo + "'"        
        print(comando)
        functions_rekognitionv2.Play_Polly (saludo)
#        os.system("sudo rm " + photoName)
        os.system(comando)
#        Image.open(photoPath + photoName).resize(photoResize, Image.ANTIALIAS).save(photoPath + "loader2.gif")

def photo_add(obj):
        # Define filename with timestamp
        photoName = "add_" + time.strftime("%Y%m%d%H%M%S") +  ".jpg"
        # Take photo using "raspistill"
        os.system("raspistill -p '112, 40,575,400' --vflip -w 1920 -h 1440 -ae 32,0xff,0x808000 -a 'Hola, por favor mire la luz roja ... ' -o " + photoPath + photoName)   
        ##
        functions_rekognitionv2.upload_file_s3(photoName,photoName)
        print("grabando : " + photoName + "en s3 ")

class MyApp(App):
        # Display the latest thumbnail
#        photo = kivyImage(source="mano.jpg")
        photo = kivyImage(source=variable_photo)
        def build(self):
                # Set up the layout
                photobox = GridLayout(cols=3, spacing=0, padding=0)

                # Create the UI objects (and bind them to callbacks, if necessary)
                photoButton = Button(text="Rekognition", size_hint=(.20, 1)) # Button: 20% width, 100% height
                photoButton.bind(on_press=photo_find) # when pressed, trigger the photo_callback function
                printButton = Button(text="Capture", size_hint=(.20, 1)) # Button: 20% width, 100% height
                printButton.bind(on_press=photo_add) # when pressed, trigger the print_callback function

                # Periodically refresh the displayed photo using the callback function
                Clock.schedule_interval(self.callback, 1)

                # Add the UI elements to the layout
                photobox.add_widget(photoButton)
                photobox.add_widget(self.photo)
                photobox.add_widget(printButton)

                return photobox
                
                
        # Callback for thumbnail refresh
        def callback(self, instance):
                self.photo.reload()


if __name__ == '__main__':
        MyApp().run()


