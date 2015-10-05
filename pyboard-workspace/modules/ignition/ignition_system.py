from pyb import ExtInt,Pin,micros,elapsed_micros
from modules.ignition.ign_module import IgnitionModule
from modules.ignition.jrt_control import JrtControl

interruptor_opened=False
def interruptor_callback(line):
  global interruptor_opened
  interruptor_opened=True

interruptor_interrupt=ExtInt('X1', ExtInt.IRQ_FALLING, Pin.PULL_DOWN, interruptor_callback)




class IgnitionSystem(object):
  ignition_module=IgnitionModule()
  jrt_control=JrtControl()

  round_start=micros()


  def __init__(self):
    with open('data/ignition_table.txt','r') as data_file:
      data=data_file.read().split('\n')

    self.ignition_table=list(map(lambda x: int(x),data))

    current_rpm_index= lambda x: int(750000/x)
    self.ign_delay=lambda t_round: self.ignition_table[current_rpm_index(t_round)]
    self.emergency_ignition_delay=sum(self.ignition_table)/len(self.ignition_table)


  def update(self):
    global interruptor_opened
    if interruptor_opened:
      interruptor_opened=False
      round_time=elapsed_micros(self.round_start)
      self.round_start=micros()
      try:
        self.ignition_module.ignite(self.ign_delay(round_time))
      except IndexError:
        self.ignition_module.ignite(self.emergency_ignition_delay)
      self.jrt_control.update(round_time)
    self.ignition_module.update(self.round_start)
