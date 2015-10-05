import pyb

class Blinker(object):
	relais_left=pyb.Pin('X3',pyb.Pin.OUT_PP)
	relais_right=pyb.Pin('X4',pyb.Pin.OUT_PP)

	left_blink_sw=pyb.Pin('X11',pyb.Pin.IN,pyb.Pin.PULL_UP)
	right_blink_sw=pyb.Pin('X12',pyb.Pin.IN,pyb.Pin.PULL_UP)	

	def __init__(self, blink_time=500):
		self.relais_left.high()
		self.relais_right.high()		
		self.blink_start=pyb.millis()
		self.blink_time=blink_time


	def update(self):
		if not self.left_blink_sw.value():
			self.relais_right.high()
			relais=self.relais_left
		elif not self.right_blink_sw.value():
			self.relais_left.high()
			relais=self.relais_right
		else:
			self.relais_right.high()
			self.relais_left.high()
			self.blink_start=pyb.millis()
			return
		self.blink(relais)
			
	def blink(self,relais):
		if pyb.elapsed_millis(self.blink_start)<self.blink_time:
			relais.low()
		else:
			relais.high()
			if pyb.elapsed_millis(self.blink_start)>2*self.blink_time:
				self.blink_start=pyb.millis()