import pygame

from target_function import TargetFunction
import unit

class Magic:
  def __init__(self):
    self.cooldown = 0
    self.refreshtime = 0
    self.general = None

  def update(self):
    if self.refreshtime > 0:
      self.refreshtime = self.refreshtime - 1

  def can_be_cast(self):
    return self.refreshtime <= 0

  def cast(self):
    if self.can_be_cast():
      self.refreshtime = self.cooldown

class ApplyStatus(Magic):
  def __init__(self, target_function, general, cooldown, status_class, status_params):
    self.cooldown = cooldown
    self.refreshtime = cooldown
    self.status_class = status_class
    self.status_params = status_params
    self.general = general
    self.tf = target_function

  def cast(self):
    if self.can_be_cast():
      for u in self.tf.select():
        self.status_class(u, self.status_params) 
      self.refreshtime = self.cooldown

class Nuke(Magic):
  def __init__(self, target_function, general, cooldown, damage, dmg_type):
    self.cooldown = cooldown
    self.refreshtime = cooldown
    self.damage = damage
    self.dmg_type = dmg_type
    self.general = general
    self.tf = target_function

  def cast(self, units):
    if self.can_be_cast():
      for u in self.tf.select():
        u.get_hit(self.general, 1000, self.damage, self.dmg_type)
      self.refreshtime = self.cooldown
