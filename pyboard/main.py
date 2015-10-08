# main.py -- put your code here!
from modules.other.blinker import Blinker
from modules.ignition.ignition_system import IgnitionSystem


blinker=Blinker()
ignition_system=IgnitionSystem()


while True:
	ignition_system.update()
	blinker.update()
