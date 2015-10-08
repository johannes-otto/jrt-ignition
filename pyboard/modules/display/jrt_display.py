from pyb import TFT, micros, elapsed_micros

class JrtDisplay(object):
	i=0
	last_rpm=0
	last_bmp_press=0
	last_bmp_tr=0
	last_max_tc=0
	last_max_tr=0
	last_velocity=0
	last_gear=0
	last_power=0
	last_torque=0
	def __init__(self):
		self.display=TFT('Y','X12','X11')
		self.display.initr()
		self.display.rotation(3)
		self.display.fill(0)

		self.init_display()


	def init_display(self):
		tft=self.display
		header_color=tft.WHITE
		header_position=0,5
		header_text='JRT-Control V0.3'
		tft.text(header_position,header_text,header_color)
		tft.line((0,header_position[1]+10),(160,header_position[1]+10),header_color)


		self.bmp_color=tft.RED
		bmp_position=0,header_position[1]+20
		bmp_text='BMP180'
		tft.text(bmp_position,bmp_text,self.bmp_color)
		tft.line((0,bmp_position[1]+10),(60,bmp_position[1]+10),self.bmp_color)

		bmp_temperature_string='Tr:    *C'
		bmp_temperature_position=0,bmp_position[1]+15
		self.display.text(bmp_temperature_position,bmp_temperature_string,self.bmp_color)

		bmp_pressure_position=0,bmp_temperature_position[1]+10
		bmp_pressure_string   ='p :    kPa'
		tft.text(bmp_pressure_position,bmp_pressure_string,self.bmp_color)

		x_unit=25
		self.bmp_update_pos=(x_unit,bmp_temperature_position[1]),(x_unit,bmp_pressure_position[1])

		max_string='MAX31885'
		self.max_color=tft.GREEN
		max_position=0,bmp_pressure_position[1]+15
		tft.text(max_position,max_string,self.max_color)
		tft.line((0,max_position[1]+10),(60,max_position[1]+10),self.max_color)

		max_temperature_r_string='Tr:    *C'
		max_temperature_r_string_position=0,max_position[1]+15
		tft.text(max_temperature_r_string_position,max_temperature_r_string,self.max_color)

		max_exhaust_string='Tc:    *C'
		max_exhaust_position=0,max_temperature_r_string_position[1]+10
		tft.text(max_exhaust_position,max_exhaust_string,self.max_color)

		self.max_update_pos=(x_unit,max_temperature_r_string_position[1]),(x_unit,max_exhaust_position[1])

		rpm_string='       Rpm'
		self.rpm_color=tft.YELLOW
		rpm_position=75,bmp_pressure_position[1]
		tft.text(rpm_position,rpm_string,self.rpm_color)


		gear_circ_pos=150,bmp_position[1]+10
		tft.fillcircle(gear_circ_pos,10,tft.YELLOW)

		self.gear_update_pos=gear_circ_pos[0]-7,gear_circ_pos[1]-7
		tft.text(self.gear_update_pos,'3',tft.BLACK,False,2)
		x_unit2=90
		self.rpm_update_pos=(x_unit2,rpm_position[1])

		self.velocity_update_pos=x_unit2,max_position[1]+10
		self.velocity_color=tft.YELLOW
		tft.text(self.velocity_update_pos,'100',self.velocity_color,False,2)

		velocity_unit_pos=x_unit2,max_exhaust_position[1]
		tft.text(velocity_unit_pos,'km/h',tft.YELLOW)

		self.torque_update_pos=0,110
		tft.text(self.torque_update_pos,'40 Nm',tft.PURPLE,False,2)

		self.kw_update_pos=x_unit2,self.torque_update_pos[1]
		tft.text(self.kw_update_pos,'8 kW',tft.PURPLE,False,2)

		tft.line((x_unit2-4,header_position[1]+10),
			(x_unit2-4,self.torque_update_pos[1]-4),
			header_color)
		tft.line((0,self.torque_update_pos[1]-4),(160,self.torque_update_pos[1]-4),header_color)

	def update(self,
		rpm=0,
		bmp_tr=0,
		bmp_press=0,
		max_tr=0,
		max_tc=0,
		time_frame=100,
		velocity=0,
		gear=1,
		power=0,
		torque=0):

		start=micros()
		tft=self.display

		if self.i==0:
			if elapsed_micros(start)>time_frame: return
			rpm=round(rpm)
			if not self.last_rpm == rpm:
				tft.fillrect(self.rpm_update_pos,(40,7),0)
				tft.text(self.rpm_update_pos,str(rpm),self.rpm_color)
				self.last_rpm=rpm
			self.i=1

		if self.i==1:
			if elapsed_micros(start)>time_frame: return
			bmp_press=round(bmp_press)
			if not self.last_bmp_press == bmp_press:
				tft.fillrect((self.bmp_update_pos[1]),(30,7),0)
				tft.text(self.bmp_update_pos[1],str(bmp_press),self.bmp_color)
				self.last_bmp_press=bmp_press
			self.i=2

		if self.i==2:
			if elapsed_micros(start)>time_frame: return
			max_tc=round(max_tc)
			if not self.last_max_tc == max_tc:
				if not 0<max_tc<1000:
					max_tc=0
				tft.fillrect((self.max_update_pos[1]),(30,7),0)
				tft.text(self.max_update_pos[1],str(max_tc),self.max_color)
				self.last_max_tc=max_tc
			self.i=3

		if self.i==3:
			if elapsed_micros(start)>time_frame: return
			max_tr=round(max_tr)
			if not self.last_max_tr == max_tr:
				tft.fillrect((self.max_update_pos[0]),(30,7),0)
				tft.text(self.max_update_pos[0],str(max_tr),self.max_color)
				self.last_max_tr=max_tr
			self.i=4

		if self.i==4:
			if elapsed_micros(start)>time_frame: return
			bmp_tr=round(bmp_tr)
			if not self.last_bmp_tr == bmp_tr:
				tft.fillrect((self.bmp_update_pos[0]),(30,7),0)
				tft.text(self.bmp_update_pos[0],str(bmp_tr),self.bmp_color)
				self.last_bmp_tr=bmp_tr
			self.i=5

		if self.i==5:
			if elapsed_micros(start)>time_frame: return
			velocity=round(velocity)
			if not self.last_velocity == velocity:
				tft.fillrect(self.velocity_update_pos,(49,14),0)
				tft.text(self.velocity_update_pos,str(velocity),self.velocity_color,False,2)
				self.last_velocity=velocity
			self.i=6

		if self.i==6:
			if elapsed_micros(start)>time_frame: return
			if not self.last_gear == gear:
				tft.fillrect(self.gear_update_pos,(16,14),tft.YELLOW)
				tft.text(self.gear_update_pos,str(gear),tft.BLACK,False,2)
				self.last_gear=gear
			self.i=7


		if self.i==7:
			if elapsed_micros(start)>time_frame: return
			power=round(power)
			if not self.last_power == power:
				tft.fillrect(self.kw_update_pos,(30,14),0)
				tft.text(self.kw_update_pos,str(power),tft.PURPLE,False,2)
				self.last_power=power
			self.i=8


		if self.i==8:
			if elapsed_micros(start)>time_frame: return
			torque=round(torque)
			if not self.last_torque == torque:
				tft.fillrect(self.torque_update_pos,(32,14),0)
				tft.text(self.torque_update_pos,str(torque),tft.PURPLE,False,2)
				self.last_torque=torque
			self.i=0
