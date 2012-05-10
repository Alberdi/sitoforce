import os
import random
from xml.dom.minidom import parse

from pygame.locals import *
import pygame

import utils
import unit

def xml_general(general, name):
  try:
    xmlsource = open(os.path.realpath("data/generals/" + name + ".xml"))
    xml = parse(xmlsource).getElementsByTagName("general")[0]
    xml.attributes = xml.getElementsByTagName("attributes")[0]
  except pygame.error, message:
    print 'Cannot load xml_general: '
    raise SystemExit, message

  #Global
  path = xml.getAttribute("path")
  general.name = xml.getAttribute("name")
  general.image = utils.load_image_trans(path + xml.getAttribute("imagesrc"))
  general.portrait = utils.load_image_trans(path + xml.getAttribute("image_portrait"))
  general.rect = general.image.get_rect()
  
  #Atributes
  general.health = int(xml.attributes.getAttribute("health"))
  general.damage = tuple(int(x) for x in xml.attributes.getAttribute("damage").split(","))
  general.speed = int(xml.attributes.getAttribute("speed"))
  general.base_accuracy = int(xml.attributes.getAttribute("accuracy"))
  general.attack_speed = int(xml.attributes.getAttribute("attack_speed"))
  general.dodge = int(xml.attributes.getAttribute("dodge"))
  
  #Traits
  general.traits = {}
  traits = xml.getElementsByTagName("traits")[0].getElementsByTagName("trait")
  for t in traits:
    general.traits[t.getAttribute("type")] = 1
  
  #Spells
  spells = xml.getElementsByTagName("spells")[0].getElementsByTagName("spell")
  general.magic_1 = utils.load_image_trans(path + spells[0].getAttribute("icon"))
  general.magic_2 = utils.load_image_trans(path + spells[1].getAttribute("icon"))
  general.magic_3 = utils.load_image_trans(path + spells[2].getAttribute("icon"))
  general.magic_4 = utils.load_image_trans(path + spells[3].getAttribute("icon"))
      
class General(unit.Unit):
  def __init__(self, name, pos, side):
    unit.Unit.__init__(self)
    xml_general(self, name)
    self.rect.topleft = pos
    
    # Which side is the general "facing"
    # 1 for the ones attacking the right, -1 for the others
    self.side = side
    if self.side == 1:
      self.image = pygame.transform.flip(self.image, True, False)
      self.portrait = pygame.transform.flip(self.portrait, True, False)
    
    self.set_from_base()
    # We can only update once as the image is not going to change
    unit.Unit.update(self)
      
  def update(self):
    pass
        
