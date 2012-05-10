import os
import random
import sys

#import psyco
#psyco.full()

from pygame.locals import *
import pygame
import pygame.key

from battle_menu import Battle_Menu
from general import General
from magic import *
from minion import Minion
from status import *
from tactic import *
from target_function import TargetFunction
import utils

class Game:
  def __init__(self):
    pygame.init()
    utils.reset_step()

    self.paused = False
    self.clock = pygame.time.Clock()
    
    pygame.display.set_caption('Sito Force')
    self.screen = pygame.display.set_mode((1024, 700), HWSURFACE)

    #Background size 1024x600
    self.background = utils.load_image("misc/" + utils.type_terrain + "_background.png")
    self.cp_background = self.background.copy()
    self.screen.blit(self.background, (0, 0))
    
    self.menu = utils.load_image("misc/battle_menu.png")
    self.cp_menu = self.menu.copy()
    self.screen.blit(self.menu, (0, 600))

    pygame.display.flip()
    
  def print_deb(self):
    font_text = pygame.font.SysFont(pygame.font.get_default_font(), 20)
    surface_text = font_text.render("FPS: " + str(self.clock.get_fps()), True, (0, 0, 0))
    self.screen.blit(surface_text, (0,0))
    
    font_text = pygame.font.SysFont(pygame.font.get_default_font(), 20)
    surface_text = font_text.render("Step: " + str(utils.step), True, (0, 0, 0))
    self.screen.blit(surface_text, (0, 15))

  def pause(self):
    self.paused = not self.paused
    
  def capture_events(self):
    for event in pygame.event.get():
      if event.type == QUIT:
        exit()
      elif event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          exit()
        elif event.key == K_F1:
          pygame.display.toggle_fullscreen()
        elif event.key == K_F9:
          utils.is_debug = (utils.is_debug == False)
        elif event.key == K_F10:
          self.pause()
      elif event.type == MOUSEBUTTONDOWN:
        if event.button == 1:
          self.cursor.check_click(self.allunits, self.battle_menu)
      elif event.type == utils.LEFT_ABILITY_EVENT:
      	if event.name == "magic_l1":
          # We need to move the magics to be attributtes of the general
          m = ApplyStatus(TargetFunction(1, self, "enemies", "everyone"), self.left_general, 0, BlindStatus, ["Lightness", 50])
          m.cast()
        elif event.name == "magic_l2":
          m = Nuke(TargetFunction(1, self, "all", "random_bomb", radius=50, outer_radius = 400), self.left_general, 0, 100, "magical")
          m.cast(self.allunits)
	  
  def left_minions(self):
    l = []
    for i in range(1,10):
      for j in range(1, 11):
        pos = [40+i*40, 80+j*40]
        m = Minion("soldiermonkey", pos, 1)
        l.append(m)
    self.units_l.add(l)
    self.allunits.add(l)
        
  def rigth_minions(self):
    l = []
    for i in range(1,10):
      for j in range(1,11):
        pos = [940-i*40, 80+j*40]
        m = Minion("flyingninja", pos, -1)
        l.append(m)
    self.units_r.add(l)
    self.allunits.add(l)
     
  def other_sprites(self):
    self.left_general = General("gamekaa", (6, 256), 1)
    self.allunits.add(self.left_general)
    self.cursor = Cursor()
    self.gcursor = pygame.sprite.GroupSingle(self.cursor)

  def start(self):
    utils.update_step()
    
    self.units_l = pygame.sprite.Group([])
    self.units_r = pygame.sprite.Group([])
    self.allunits = pygame.sprite.LayeredUpdates([])
    
    self.left_minions()
    self.rigth_minions()
    self.other_sprites()

    self.allunits.update()
    
    t1 = AdvanceTactic()
    t2 = StopTactic()
    t3 = RetreatTactic()

    t1.apply(self.units_l)
    t1.apply(self.units_r)

    #t1.apply(self.units_l, queue=False)
    #t3.apply(self.units_r, queue=True)
    
    self.battle_menu = Battle_Menu(self.menu, self.cursor, self.left_general)
    
    while 1:
      self.capture_events()
      if self.paused: continue

      utils.step = utils.step + 1
      self.clock.tick(utils.tick_rate)

      for m in self.allunits:
        #if m != self.cursor:
          m.friends = []
          m.enemies = []
      
      collides_l = pygame.sprite.groupcollide(self.units_l, self.units_r, False, False)
      collides_r = pygame.sprite.groupcollide(self.units_r, self.units_l, False, False)
      for m in collides_l:
        m.enemies = collides_l[m]
        m.fight()     
      for m in collides_r:
        m.enemies = collides_r[m]
        m.fight()

      for m in self.units_l:
        collides_l = pygame.sprite.spritecollide(m, self.units_l, False, pygame.sprite.collide_rect)
        m.add_friends(collides_l)        

      for m in self.units_r:
        collides_r = pygame.sprite.spritecollide(m, self.units_r, False, pygame.sprite.collide_rect)
        m.add_friends(collides_r)

      self.allunits.update()
      self.cursor.update()
      self.battle_menu.update()
      self.screen.blit(self.background, (0, 0))
      if utils.is_debug:
        self.print_deb()
      self.screen.blit(self.menu, (0, 600))
      self.allunits.draw(self.screen)
      self.gcursor.draw(self.screen)
      pygame.display.flip()


class Cursor(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    pygame.mouse.set_visible(0)
    self.name = "cursor"
    self.image = utils.load_image_trans("misc/cursor.png")
    self.rect = Rect(self.image.get_rect().left, self.image.get_rect().top, 1, 1)
    self.radius = 1
    
  def check_click(self, units, battle_menu):
    collides = pygame.sprite.spritecollide(self, units, False, pygame.sprite.collide_rect)
    if not collides == []:
      unit = collides[0]
      battle_menu.update_menu(unit)
    
  def update(self):
    self.pos = pygame.mouse.get_pos()
    self.rect.topleft = self.pos

if __name__ == "__main__":
  g = Game()
  g.start()
