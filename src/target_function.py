import math
import random

import pygame

class TargetFunction():
  def __init__(self, side, board, selection, function, radius = 0, outer_radius = 0):
    self.side = side
    self.board = board
    self.selection = selection
    self.radius = radius
    self.outer_radius = outer_radius
    self.select = self.select_function(function)

  def select_function(self, function):
    if function == "none": return self.none
    elif function == "everyone": return self.everyone
    elif function == "circled_area": return self.circled_area
    elif function == "random_bomb": return self.random_bomb

  def select_units(self):
    if self.selection == "enemies":
      return self.board.units_r
    elif self.selection == "all":
      return self.board.allunits

  def none(self):
    return []

  def everyone(self):
    return self.select_units()

  def circled_area(self):
    prev_radius = self.board.cursor.radius
    self.board.cursor.radius = self.radius
    g = pygame.sprite.spritecollide(self.board.cursor, self.select_units(), False, pygame.sprite.collide_circle)
    self.board.cursor.radius = prev_radius
    return g

  def random_bomb(self):
    prev_radius = self.board.cursor.radius
    prev_rect = self.board.cursor.rect
    self.board.cursor.radius = self.radius

    # Mathemagic
    angle = random.uniform(0, 2*math.pi)
    r = random.uniform(0, self.outer_radius)
    self.board.cursor.rect.topleft = \
      (self.board.cursor.pos[0] + math.cos(angle) * r, self.board.cursor.pos[1] + math.sin(angle) * r)

    g = pygame.sprite.spritecollide(self.board.cursor, self.select_units(), False, pygame.sprite.collide_circle)

    self.board.cursor.radius = prev_radius
    self.board.cursor.rect = prev_rect
    return g
