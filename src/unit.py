import os
import random

from pygame.locals import *
import pygame

import utils

class Unit(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.pos = [0, 0]
    self.speed = 0
    self.game_speed = 0
    self.base_accuracy = 0
    self.attack_speed = 0
    self.game_attack_speed = 0
    self.next_attack = 0
    self.enemies = []
    self.friends = []
    self.side = 1
    self.health = 0
    self.damage = 0
    self.dodge = 0
    self.armor = {}
    self.armor["physical"] = 0
    self.armor["magical"] = 0
    self.status = []
    self.traits = {}

  def set_from_base(self):
    self.accuracy = self.base_accuracy
     
  def add_friends(self, list_units):
    for u in list_units:
      if u == self: continue
      if u.friends.count(self) == 0:
        u.friends.append(self)
      if self.friends.count(u) == 0:
        self.friends.append(u)
        
  def add_enemies(self, list_units):
    for u in list_units:
      if u == self: continue
      if u.friends.count(self) == 0:
        u.friends.append(self)
      if self.friends.count(u) == 0:
        self.friends.append(u)
        
  def remove_friends(self, list_units):
    for u in list_units:
      if not self.friends.count(u) == 0:
        self.friends.remove(u)
        
  def remove_enemies(self, list_units):
    for u in list_units:
      if not self.enemies.count(u) == 0:
        self.enemies.remove(u)
  
  def fight(self):
    # If the minion didn't attack anyone in the last 5 ticks, it must reload the attack
    if 'blind' in self.traits: return
    if (utils.step >= self.next_attack + 5):
      self.next_attack = utils.step + 5
      return
    if (utils.step >= self.next_attack):
      self.next_attack = utils.step + self.game_attack_speed
      enemy = self.enemies[0]
      hit = random.randint(0,self.accuracy)
      damage = random.randint(self.damage[0], self.damage[1])
      enemy.get_hit(self, hit, damage, "physical")
        
  def get_hit(self, enemy, hit, damage, dmg_type):
    # TODO: Hit and dodge shouldn't be used in all attacks
    if hit <= self.dodge: return
    self.health = self.health - self.apply_armor(damage, dmg_type)
    if self.health <= 0:
      self.die()

  def apply_armor(self, damage, dmg_type):
    reduction = damage * self.armor[dmg_type] / 100
    if reduction > damage: return 0
    if -reduction < -damage: return damage*2
    return damage - (damage * self.armor[dmg_type] / 100)

  def die(self):
    self.kill()
    for m in self.friends:
      m.remove_friends([self])
    for m in self.enemies:
      m.remove_enemies([self])

  def update(self):
    for s in self.status:
      s.update()
