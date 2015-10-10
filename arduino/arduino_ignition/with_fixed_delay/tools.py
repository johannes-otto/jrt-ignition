offset=45 #vor ot
def_ignition=26.292

rpm_points=1000,2000,3000,4000,5000,6000,7000

rpm2mic=lambda x: 60*1000*1000/x
dt=lambda x: rpm2mic(x)/360*(offset-def_ignition)

for rp in rpm_points:
	print(rp,':\t',round(rpm2mic(rp)),'\t',round(dt(rp)))
