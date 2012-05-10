import os
import random
from xml.dom.minidom import parse

from pygame.locals import *
import pygame

import utils
import unit

def xml_minion(minion, name):
  try:
     xmlsource = open("data/minions/" + name + ".xml")
     xml = parse(xmlsource).getElementsByTagName("minion")[0]
     xml.attributes = xml.getElementsByTagName("attributes")[0]
  except pygame.error, message:
    print 'Cannot load xml_minion: '
    raise SystemExit, message
  
  minion.name = xml.getAttribute("name")
  minion.imagesrc = xml.getAttribute("imagesrc")
  minion.image = utils.load_image_trans(minion.imagesrc)
  minion.rect = minion.image.get_rect()
  minion.health = int(xml.attributes.getAttribute("health"))
  minion.damage = tuple(int(x) for x in xml.attributes.getAttribute("damage").split(","))
  minion.speed = int(xml.attributes.getAttribute("speed"))
  minion.base_accuracy = int(xml.attributes.getAttribute("accuracy"))
  minion.attack_speed = int(xml.attributes.getAttribute("attack_speed"))
  minion.dodge = int(xml.attributes.getAttribute("dodge"))
      
class Minion(unit.Unit):
  def __init__(self, name, pos, side):
    unit.Unit.__init__(self)
    xml_minion(self, name)
    
    # We should order those initializations (alphabetically, for example)
    self.pos = pos
    self.rect.topleft = (pos[0], pos[1])
    self.target = [pos]
    self.direction = [0,0]
    self.game_speed = (self.speed * 2)/utils.tick_rate
    self.game_attack_speed =  (5 * utils.tick_rate)/ self.attack_speed
    self.next_attack = self.game_attack_speed
    self.enemies = []
    self.friends = []
    # Which side is the minion "facing"
    # 1 for the ones attacking the right, -1 for the others
    self.side = side
    if self.side == 1:
      self.image = pygame.transform.flip(self.image, True, False)
    self.set_from_base()
    
  def update(self):
      unit.Unit.update(self)
      self.prepare_move()
      if self.direction != [0,0]:
        self.pos[0] = self.pos[0] + self.game_speed * self.direction[0]
        self.pos[1] = self.pos[1] + self.game_speed * self.direction[1]
        self.rect.topleft = (self.pos[0], self.pos[1])
        
  def prepare_directions(self):
    for z in [0,1]:
      if self.target[0][z] > self.pos[z]:
        self.direction[z] = 1
      elif self.target[0][z] == self.pos[z]:
        self.direction[z] = 0
      else:
        self.direction[z] = -1
        
  def prepare_target(self):
    if not len(self.target) <= 1:
      for z in [0, 1]:
	threshold = 10 * self.direction[z]
	if self.target[0][z] * self.direction[z] > self.pos[z] * self.direction[z] and \
	(self.pos[z] + threshold) * self.direction[z] > self.target[0][z] * self.direction[z]:
	  self.delete_target()
  
  def delete_target(self):
    self.target = self.target[1:]
        
  def prepare_move(self):
    self.prepare_directions()
    self.prepare_target()
    for l in [self. friends, self.enemies]:
      for f in l:
        if not f.alive(): continue
        if self.pos[0] < f.pos[0] and self.pos[0] + 30 > f.pos[0] and self.direction[0] == 1:
          self.direction[0] = 0
        if self.pos[0] > f.pos[0] and self.pos[0] - 30 < f.pos[0] and self.direction[0] == -1:
          self.direction[0] = 0
        if self.pos[1] < f.pos[1] and self.pos[1] + 30 > f.pos[1] and self.direction[1] == 1:
          self.direction[1] = 0
        if self.pos[1] > f.pos[1] and self.pos[1] - 30 < f.pos[1] and self.direction[1] == -1:
          self.direction[1] = 0
