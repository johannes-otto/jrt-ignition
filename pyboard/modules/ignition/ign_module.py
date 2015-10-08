from pyb import Pin, elapsed_micros,micros,udelay

class IgnitionModule(object):
	ignited=False
	ign_point=0

	def __init__(self,pin='X5',ignition_length=500):
		self.pin=Pin(pin,Pin.OUT_PP)
		self.ignition_length=ignition_length
		self.pin.low()

	def ignite(self,ign_point=0):
		self.ignited=False
		self.ign_point=ign_point

	def update(self,round_start):
		if not self.ignited:
			while elapsed_micros(round_start)<self.ign_point:
				self.pin.low()
			self.pin.high()
			udelay(self.ignition_length)
			self.pin.low()
			self.ignited=True
		else:
			self.pin.low()
