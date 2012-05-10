from pygame.locals import *
import pygame, os
  
LEFT_ABILITY_EVENT = 25
is_debug = False
tick_rate = 30.0
step = 0
type_terrain = "grass"
magic_menu_button = "misc/button.png"
magic_menu_button_push = "misc/button_push"
forward = "misc/forward.png"

def reset_step():
  global step
  step = 0
  
def update_step():
  global step
  step = step + 1
  
def load_image(path):
  try:
    img = pygame.image.load(os.path.realpath("res/images/" + path))
  except pygame.error, message:
    print 'Cannot load image: ', path
    raise SystemExit, message

  img = img.convert()
  return img

def load_image_trans(path, pos_trans=(0,0)):
  img = load_image(path)
  img.set_colorkey(img.get_at(pos_trans), RLEACCEL)
  return img
  
  
