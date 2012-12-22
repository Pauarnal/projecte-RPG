import pygame
from vec2d import vec2d
import json   #loading maps

class Tileset(object):
    """documentacio:
        Classe per a carregar i gastar Tilesets.
        
        Es pot gastar com una llista de nomes lectura de 
        Surfaces distintes que son childs de la imatge base
        del Tileset.
        
        Cadascuna d'aquestes Surfaces coincideix amb un Tile. Amb
        l'index 0 s'indica una Tile buida.
        
        exemple d'us:
            terrenys_nevats = Tileset('terrenys_nevats.png', 32, 32)
            blank_tile = terrenys_nevats[0]
            tile_1 = terrenys_nevats[1]
    """
    
    image =  None
    tiles = []
    def __init__(self, ruta, (width_tile, height_tile)):
        """documentacio:
            carrega un nou Tileset.
            
            Args:
                ruta: la ruta en la que es troba la imatge corresponent al tileset
                width_tile: l'amplaria de cada tile
                height_tile: l'altura de cada tile
        """
        self.image = pygame.image.load(ruta)
        rect_imatge = self.image.get_rect()
        
        n_columnes = rect_image.width / width_tile
        n_files = rect_image.height / height_tile
        self.tiles = [pygame.Surface((width_tile, height_tile))]
        for fila in range(n_files):
            for columna in range(n_columnes):
                topleft = vec2d(rect_imatge.topleft) + (width_tile*fila,
                                                        height_tile*columna) 
                size = (width_tile, height_tile)
                rect = pygame.Rect(topleft, size)
                tiles.append(self.image.subsurface(rect))
        
    def __getitem__(self, key):
        if type(key) != int: raise TypeError, "int type expected"
        if key > len(self): raise IndexError
        return tiles[key]
        
    def __len__(self):
        return len(self.tiles)-1

class Map:
    class Taula_dades:
    tilesets = {}
    
    def __init__(self, ruta):
        """documentacio:
            Carrega un nou Mapa a partir d'un arxiu json creat amb Tiled.
            
            Args:
                ruta: la ruta de l'arxiu json.
        """
        if type(ruta) != str: raise TypeError, "str type expected"
        data = json.load(ruta)
        for tileset in data['tilesets']:
            self.tilesets[tileset['name']] = Tileset(tileset['image'],
                                                        (tileset['tilewidth'],
                                                        tileset['tileheight']))
        
        
        
        
    def to_surface(self,(posx,posy),(width,height),coords_representen_centre = False):
        """documentacio:
            Crea una pygame.Surface d'una regio del mapa i la torna
            
            Args:
                posx, posy: les coordenades del punt top-left de la regio del mapa.
                width, height: el tamany de la regio del mapa que es desitja.
                coords_representen_centre: quan True, posx i posy fan referencia al centre del mapa.
        """

class Camera:
    


####---------TESTING---------####