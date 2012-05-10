class Tactic:
  def __init__(self):
    pass

  def apply(self, minions, queue=False):
    for m in minions:
      if not queue: m.target = []
      self.set_target(m)

  def set_target(self, minion):
    pass

class StopTactic(Tactic):
  def set_target(self, minion):
    minion.target.append(minion.pos)

class AdvanceTactic(Tactic):
  def set_target(self, minion):
    if minion.side == 1:
      # We need variables for field dimensions
      minion.target.append([992, minion.pos[1]])
    else:
      minion.target.append([0, minion.pos[1]])

class RetreatTactic(Tactic):
  def set_target(self, minion):
    if minion.side == 1:
      minion.target.append([0, minion.pos[1]])
    else:
      minion.target.append([992, minion.pos[1]])
