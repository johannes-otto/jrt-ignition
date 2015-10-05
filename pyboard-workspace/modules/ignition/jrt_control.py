from pyb import micros,ExtInt,Pin,elapsed_micros,millis,elapsed_millis,UART
from modules.sensors.bmp180 import BMP180
from modules.sensors.max31885 import MAX31885
from modules.display.jrt_display import JrtDisplay
from math import sin,cos,pi
from modules.sensors.fusion import Fusion
from modules.sensors.mpu9150 import MPU9150


wheel_scope=1.97 # *m
wheel_start=micros()
wheel_time=0
l_wheel_time=0

def wheel_callback(line):
	global wheel_start,wheel_time,l_wheel_time
	l_wheel_time,wheel_time=wheel_time,elapsed_micros(wheel_start)
	wheel_start=micros()

wheel_interrupt=ExtInt('X2', ExtInt.IRQ_FALLING, Pin.PULL_DOWN, wheel_callback)


class JrtControl(object):
	tft=JrtDisplay()

	gears = [21, 13, 9, 7]
	rpm_times=0
	rpm_count=0

	update_interval=100
	last_update=millis()

	bmp180=BMP180('Y')
	max31885=MAX31885(CS_pin='X7',SO_pin='X8',SCK_pin='X6')
	uart=UART(1)
	uart.init(115200)
	v=0
	P_a=0
	P_h=0

	def __init__(self):
		pass
	def read_arduino(self):
		self.uart.write('a\n')
		if self.uart.any():
			try:
				data=self.uart.readline().decode().replace('\r\n','').split('\t')
				data=tuple(map(float,data))
				if len(data)==3:
					return data
			except ValueError:
				pass
		return 0,0,0
	def get_gear(self):
		if wheel_time==0:
			return 0
		d_wheel_time=elapsed_micros(wheel_start)*(wheel_time-l_wheel_time)/wheel_time
		rpm_ratio_diff=lambda ratio: abs(self.rpm_times/self.rpm_count*ratio-wheel_time-d_wheel_time)
		diffs=tuple(map(rpm_ratio_diff,self.gears))
		d=min(diffs)
		if d>(wheel_time+d_wheel_time)/5:
			return 0
		return diffs.index(d)+1

	def get_speed(self,last_velocity):
		if wheel_time==0:
			self.P_a=0
			return 0
		d_wheel_time=elapsed_micros(wheel_start)*(wheel_time-l_wheel_time)/wheel_time
		velocity= wheel_scope/1000/((wheel_time+d_wheel_time)/1000000)*3600
		dv=(velocity-last_velocity)/3.6

		m=195
		self.P_a=m*dv**2/(wheel_time/1000000)


		if dv<0:
			self.P_a*=-1

		yaw,pitch,roll=self.read_arduino()
		m=105+90
		g=9.81
		#print(yaw,pitch,roll)
		#print(sin(roll*pi/180),roll)
		self.P_h=m*g*sin(roll*pi/180)*velocity/3.6*(wheel_time+d_wheel_time)/1000000
		#print(P_h)
		if 0<velocity<150:
			return velocity
		return -1

	def get_torque(self,P,rpm):
		M=P/rpm*(30000/pi)
		if M<99:
			return M
		else:
			return 99

	def get_power(self,v=0):
		v/=3.6
		m_mz=105
		m_drv=90
		cw=0.7
		A=1.0
		rho=1.189
		P_cw=v*(cw*A*rho/2*v**2)

		t=elapsed_micros(wheel_start)/1000000

		P=P_cw+self.P_a+self.P_h
		P_kW=P/1000
		if P_kW<0:
			return 0
		elif P_kW>20:
			return 20
		else:
			return P_kW

	def update(self,round_time):
		self.rpm_count+=1
		self.rpm_times+=round_time
		if elapsed_millis(self.last_update)>self.update_interval:
			rpm=self.rpm_count/self.rpm_times*60000000
			self.v=self.get_speed(self.v)
			P=self.get_power(self.v)
			max_tc,max_tr=self.max31885.read()
			self.tft.update(rpm=rpm,
				bmp_tr=self.bmp180.temperature,
				bmp_press=self.bmp180.pressure/1000,
				max_tr=max_tr,
				max_tc=max_tc,
				time_frame=round_time/4,
				velocity=self.v,
				gear=self.get_gear(),
				torque=self.get_torque(P,rpm),
				power=P)
			self.rpm_count=0
			self.rpm_times=0
			self.last_update=millis()
