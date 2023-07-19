import pygame
import time
from pylsl import StreamInfo, StreamOutlet
from datetime import datetime
import os
import pandas as pd
import numpy as np


C = 1 
N1 = 0 
N2 = 7 
R = 1
F= 8 
freq_list= []
T = 1/F-0.02

class Stimulus(object):

    def __init__(self, id_Subject, cc_Subject, loc):

        pygame.init()
        
        pygame.display.set_caption('Agudeza de Vernier')
        
        self.__width = 600 
        
        self.__height = 600
        
        self.__size = 600,600 
        
        self.__screen = pygame.display.set_mode(self.__size)
        
        pygame.display.flip()
        
        self.id = id_Subject
        
        self.cc = cc_Subject
        
        self.loc = loc
        
        self.carpetas = "logmar"
        
        self.nombre = ["1366x768","1680x1050"]
        
        self.vector = []
        
        self.rest_image = pygame.image.load(r"C:\Users\valer\OneDrive\Documentos\Estimulacion_checkboard\fondo_negro.png")
        
        for nombre in range(0,len(self.nombre)):
            for folder in range(1,8):
                for img in range(0,2):
                    self.images = pygame.image.load(r'C:\Users\valer\OneDrive\Documentos\Estimulacion_checkboard'+'\\'+self.carpetas+str(folder)+'\\'+self.nombre[nombre]+'\\'+str(img) + '.png')
                    print(r'C:\Users\valer\OneDrive\Documentos\Estimulacion_checkboard'+'\\'+self.carpetas+str(folder)+'\\'+self.nombre[nombre]+'\\'+str(img) + '.png')
                    
                    self.vector.append(self.images)
                    #se crea un vector con las imagenes en orden por nombre, logmar y numero
                    
        # black = (0, 0, 0)
        # white = (250, 250, 250)

        # self.__screen.fill(black)
        # pygame.draw.rect(self.__screen, white, [0, 0, 10, 10])
        # wait = False
        # while wait == False:
        #     for event in pygame.event.get():
        #         if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #             wait = True



    def display(self, img):

        try:
            
            img_width = int(img.get_width())
            
            img_height = int(img.get_height())
            
            img = pygame.transform.scale(img, (img_width, img_height))
            
            position_x = self.__width / 2 - img.get_width() // 2
            
            position_y = self.__height / 2 - img.get_height() // 2
            
            self.__screen.blit(img, (int(position_x), int(position_y)))
            
            pygame.display.flip()
            
            
        except:
            
            pygame.quit()

    def save(self, Mark):

        now = datetime.now()
        
        d = (now.strftime("%m-%d-%Y"), now.strftime("%H-%M-%S"))
        
        date = {'H': [str(d[1])]}
        
        loc = self.loc + '/'+d[0]
        
        file = loc + '/' + 'Mark_'+str(self.id)+'_'+str(self.cc)+'.csv'
        
        if not os.path.isfile(file):
            
            header = True
        else:
            
            header = False
            
        M = pd.DataFrame(date, columns=['H'])
        
        M['M'] = Mark
        
        M.to_csv(file, mode='a', header=header, index=True, sep=';')

    def start_stimulus(self):
        
        try:

            RUNNING, PAUSE = 0, 1
            
            state = RUNNING
            #pause_text = pygame.font.SysFont('Consolas', 32).render('Pausa', True, pygame.color.Color('White'))  
            for num in range(0,28,2):#pedir explicacion
                
                ini = datetime.now()
                cont = 0
                while cont <= 5:
                    for e in pygame.event.get():
                       if e.type == pygame.QUIT:
                           break
                       if e.type == pygame.KEYDOWN:
                           # if e.key == pygame.K_p:  # key p: pause
                           #     state = PAUSE
                           # if e.key == pygame.K_s:  # key s: start
                           #     state = RUNNING
                           if e.key == pygame.K_ESCAPE:  # key escape: exit
                               pygame.quit()
                    print(num)
                    time1 = datetime.now()
                    self.display(self.vector[num])
                    pygame.time.delay(int(280*T))
                    self.display(self.vector[num+1])
                    pygame.time.delay(int(280*T))
                    time2 = datetime.now()
                    tiempo=time2-time1
                    sec = tiempo.seconds
                    micro = tiempo.microseconds
                    su= sec + micro
                    freq=int(1/su * 1000000)
                    print(str(freq),"Hz")
                            
                    freq_list.append(freq)                               
                    cont = time2 - ini
                    cont = int(cont.seconds)
#                    print (cont,"seg",type(cont))
                    self.display(self.rest_image)
                    
            pygame.time.delay(int(2000))

            pygame.quit()
          
            freq_data=pd.DataFrame(freq_list)
            freq_data.to_csv('freq_est.csv', header=False, index=False, decimal=".")
            
        except:
            
            pygame.quit() 

if __name__ == '__main__':

     estimulo = Stimulus('H1', '1152207135', r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Proyecto Banco de la republica\Trabajo de grado\Herramienta\HVA\GITLAB\interface\ViAT\Records\H1_1152207135')
     estimulo.start_stimulus()
