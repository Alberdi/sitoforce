import os
import random
import sys

from pygame.locals import *
import pygame
import pygame.key

from tactic import *
from minion import Minion
from general import General
from status import *
import utils

class Battle_Menu(pygame.surface.Surface):
  def __init__(self, surface, cursor, left_general):
    self.surface = surface
    self.unit = None
    self.left_general = left_general
    self.font = pygame.font.get_default_font()
    self.font_text = pygame.font.SysFont(self.font, 20)
    self.color_text = (0, 0, 0)
    self.draw_generals()
    self.background = surface.copy()
    self.cursor = cursor
    self.left_rect_abilities()
    self.left_rect_strategies()

  def update(self):
    self.check_buttons()
    self.write_minion_stat()
      
  def check_buttons(self):
    collides_a = pygame.sprite.spritecollide(self.cursor, self.left_abilities, False, pygame.sprite.collide_circle)
    collides_b = pygame.sprite.spritecollide(self.cursor, self.left_strategies, False, pygame.sprite.collide_circle)
    for b in self.left_abilities:
      b.set_idle_button()
      if len(collides_a) > 0 and b == collides_a[0]:
	if (1, 0, 0) == pygame.mouse.get_pressed():
	  b.set_pressed_button()
	for e in pygame.event.get(MOUSEBUTTONUP):
	  if e.button == 1:
	    pygame.event.post(pygame.event.Event(utils.LEFT_ABILITY_EVENT, name=collides_a[0].option))
      b.draw_botton(self.surface)
    for s in self.left_strategies:
      s.set_idle_button()
      s.draw_botton(self.surface)
      
  def draw_generals(self):
    left_position = (10, 10)
    rect_left = self.left_general.portrait.get_rect()
    rect_left.topleft = left_position
    self.surface.set_clip(rect_left)
    self.surface.blit(self.left_general.portrait, left_position)
    self.surface.set_clip(None)
    self.left_rect_abilities()
    self.left_rect_strategies()
    self.draw_abilities()
    
  def left_rect_abilities(self):
    self.left_abilities = pygame.sprite.RenderUpdates([])
    self.left_abilities.add(Icon_Abilities((self.left_general.magic_1), (228, 608), "magic_l1"))
    self.left_abilities.add(Icon_Abilities((self.left_general.magic_2), (270, 608), "magic_l2"))
    self.left_abilities.add(Icon_Abilities((self.left_general.magic_3), (228, 650), "magic_l3"))
    self.left_abilities.add(Icon_Abilities((self.left_general.magic_4), (270, 650), "magic_l4"))
    
  def left_rect_strategies(self):
    self.left_strategies = pygame.sprite.RenderUpdates([])
    #self.left_strategies.add(Icon_Strategies(utils.load_image_trans(utils.forward), (321, 608), "forward"))
    
  def draw_abilities(self):
    self.surface.set_clip(226, 7, 300, 85)
    for m in self.left_abilities:
      self.surface.blit(m.icon, (m.pos[0]+2, m.pos[1] - 598))
    for s in self.left_strategies:
      self.surface.blit(s.icon, (s.pos[0]+2, s.pos[1] - 598))
    self.surface.set_clip(None)
      
  def write_minion_stat(self):
    self.surface.set_clip(100, 5, 120, 90)
    self.surface.blit(self.background, (0, 0))
    if self.unit is not None and not self.unit.alive():
      self.unit = None
    if self.unit is not None:
      self.write(self.unit.name, self.color_text, (100, 5))
      self.write("Health: " + str(self.unit.health), self.color_text, (100, 20))
      self.write("Enemies: " + str(len(self.unit.enemies)), self.color_text, (100, 35))
      self.write("Accuracy: " + str(self.unit.accuracy), self.color_text, (100, 50))
      self.write("Status: " + str(self.unit.status), self.color_text, (100, 65))
      self.write("NextAttack: " + str(self.unit.next_attack), self.color_text,(100,80))
      
  def update_menu(self, unit):
    self.unit = unit
    
  def write(self, text, color, pos):
    surface_text = self.font_text.render(text, True, color)
    self.surface.blit(surface_text, pos)
    
    
class Icon_Abilities(pygame.sprite.Sprite):
  def __init__(self, icon, pos, option):
    pygame.sprite.Sprite.__init__(self)
    self.icon = icon
    self.idle = utils.load_image_trans("misc/button.png", (10,10))
    self.pressed = utils.load_image_trans("misc/button_push.png", (10,10))
    self.image = self.idle
    self.rect = icon.get_rect()
    self.pos = pos
    self.rect.topleft = pos
    self.option = option
    self.status = 0
    
  def set_idle_button(self):
    if self.status != 0:
      self.image = self.idle
      self.status = 0
    
  def set_pressed_button(self):
    if self.status != 1:
      self.image = self.pressed
      self.status = 1
    
  def draw_botton(self, surface):
    surface.set_clip(self.pos[0], self.pos[1]-600, 40, 40)
    surface.blit(self.image, (self.pos[0], self.pos[1]-600))
    surface.set_clip(None)
    
    
class Icon_Strategies(pygame.sprite.Sprite):
  def __init__(self, icon, pos, option):
    pygame.sprite.Sprite.__init__(self)
    self.icon = icon
    self.idle = utils.load_image_trans("misc/s_button.png", (10,10))
    self.pressed = utils.load_image_trans("misc/s_button_push.png", (10, 10))
    self.image = self.idle
    self.rect = icon.get_rect()
    self.pos = pos
    self.rect.topleft = pos
    self.option = option
    self.status = 0
    
  def set_idle_button(self):
    if self.status != 0:
      self.image = self.idle
      self.status = 0
    
  def set_pressed_button(self):
    if self.status != 1:
      self.image = self.pressed
      self.status = 1
    
  def draw_botton(self, surface):
    surface.set_clip(self.pos[0], self.pos[1]-600, 44, 24)
    surface.blit(self.image, (self.pos[0], self.pos[1]-600))
    surface.set_clip(None)  
  
