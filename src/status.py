class Status:
  def __init__(self, unit, l):
    # l = [name, duration]
    # If there is a status with the same name
    for s in unit.status:
      if s.name == l[0]:
        # we reset the status duration
        s.duration = max(l[1], s.duration)
        return
    self.name = l[0]
    self.duration = l[1]
    self.unit = unit
    self.start()

  def start(self):
    self.unit.status.append(self)

  def update(self):
    self.duration -= 1
    self.update_effect()
    if self.duration == 0: self.end()

  def update_effect(self):
    pass

  def end(self):
    self.unit.status.remove(self)

  def copy(self, unit):
    return Status(self.name, unit, self.duration)
    
class BlindStatus(Status):
  def start(self):
    Status.start(self)
    # We need to be careful in the future with things like this
    # because there might be more effects affecting accuracies
    self.unit.accuracy = self.unit.accuracy - self.unit.base_accuracy
    self.unit.traits['blind'] = 1

  def end(self):
    self.unit.accuracy = self.unit.accuracy + self.unit.base_accuracy
    self.unit.traits.pop('blind')
    Status.end(self)
