import pygame
from pygame.sprite import Sprite, Group
from vec2d import vec2d
import json   #loading maps
import pickle #saving/loading games

from grafics import *

# Import the android module. If we can't import it, set it to None - this
# lets us test it, and check to see if we want android-specific behavior.
try:
    import android
    import pygame.mixer as mixer
except ImportError:
    android = None
    import android.mixer as mixer

# The FPS the game runs at.
FPS = 30

# Color constants.
class Colors:
    ROIG = (255, 0, 0, 255)
    VERD = (0, 255, 0, 255)

class Musica:
    FI_MUSICA = pygame.USEREVENT
    kairi = 'kairi.mp3'
    gummi_ship = 'gummi-ship.mp3'
    canco_actual = 'kairi.mp3'
    def play(self, ruta = ''):
        if ruta == '': ruta = self.canco_actual
        self.canco_actual = ruta
        mixer.init()
        mixer.music.load(ruta)
        mixer.music.play()
        
    def loop(self):
        if android:
           if mixer.music_channel.get_busy()==False:
              mixer.music.play()
        else:
           if mixer.music.get_busy()==False:
              mixer.music.play()
        
    
class Serp(Sprite):
    class Cap(Sprite):
        pos = (0,0)
        image = Imatges.cap
        rect = pygame.Rect(0,0,0,0)
        def __init__(self, centre):
            self.rect = self.image.get_rect()
            self.rect.center = centre
            
        def set_direccio(self, direccio):
            centre = self.rect.center
            angle = (self.rect.center - vec2d(direccio)).get_angle_between(vec2d(0,1))
            self.image = pygame.transform.rotate(Imatges.cap, angle)
            self.rect = self.image.get_rect()
            self.rect.center = centre
            
        def draw_onto(self, finestra):
            finestra.blit(self.image, self.rect)
            
            
    cap = None
    finestra = None
    posicio = vec2d(0,0)
    cua = pygame.sprite.OrderedUpdates()    #De moment
    direccio = vec2d(0,-1)  #cap amunt
    velocitat = .2
        
    def __init__(self, finestra, posicio = 'centre'):
        self.finestra = finestra
        if posicio == 'centre':
            self.posicio = vec2d(finestra.get_rect().center)
        self.direccio = vec2d(0,-1)
        self.cap = self.Cap(self.posicio)
        self.cap.set_direccio(self.direccio)
    
    def update(self, temps):
        self.posicio += self.velocitat * temps * self.direccio.normalized()
        self.cap.rect.center = self.posicio
        
    def orienta_cap_a(self, punt):
        self.direccio = punt - self.posicio
        self.cap.set_direccio(punt)
    
    def draw(self):
        #self.cua.draw()
        self.cap.draw_onto(self.finestra)

        
def main():
    def draw_all_things():
        def draw_background():
            pantalla.blit(Imatges.fons, (0,0))
        draw_background()
        serp.draw()
    
    def update_all_things(temps):
        serp.update(temps)
        
    def controls():
        if pygame.mouse.get_pressed()[0]:
            serp.orienta_cap_a(vec2d(pygame.mouse.get_pos()))
        
    pygame.init()
    # Set the screen size.
    pantalla = pygame.display.set_mode((800, 480))
    
    # Map the back button to the escape key.
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
    
    #rellotge
    rellotge = pygame.time.Clock()
    
    #musica
    Musica().play(Musica.gummi_ship)
    
    #serp
    serp = Serp(pantalla)
    
    en_marxa = True
    while en_marxa:
        # Android-specific:
        if android:
            if android.check_pause():
                android.wait_for_resume()
        
        for event in pygame.event.get():
            # When the user hits back, ESCAPE is sent. Handle it and end
            # the game.
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                en_marxa = False
        
        controls()
        Musica().loop()
        draw_all_things()
        pygame.display.flip()
            
        temps = rellotge.tick(FPS)
        update_all_things(temps)

# This isn't run on Android.
if __name__ == "__main__":
    main()
