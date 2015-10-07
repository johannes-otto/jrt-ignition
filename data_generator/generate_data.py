__author__ = 'johannes'
import matplotlib.pyplot as pylab

ign_degree = ((0, -26.292),
              (500, -26.292),
              (1000, -26.292),
              (2000, -26.292),
              (3000, -26.292),
              (4000, -26.292),
              (5000, -26.292),
              (6000, -26.292),
              (7000, -26.292),
              (8000, -26.292),
              (9000, -26.292),
              (10000, -26.292))
offset = -35.19

x = list(map(lambda x: x[0], ign_degree))
y = list(map(lambda x: x[1], ign_degree))
f, ax = pylab.subplots(2, sharex=True)
ax[0].plot(x, y)
ax[0].set_title('Zuendung in Grad, bezogen auf OT')


def degree_to_ms(rpm, degree):
    if rpm == 0:
        rpm = 0.01
    deg_p_us = 1000000 *60 / rpm /360

    return (degree - offset) * deg_p_us


y_us = list(map(lambda x: degree_to_ms(x[0], x[1]), ign_degree))
print(y_us)
ax[1].set_title('Verzoegerung in us bezogen of ein Offset von {} Grad'.format(str(offset)))

from scipy import interpolate

x_interp = list(range(0, 9000, 80))
fx_fun = interpolate.interp1d(x, y_us,kind='slinear')
fx = lambda x: int(fx_fun(x))
y_us_interp = list(map(fx, x_interp))
ax[1].plot(x_interp[10:], y_us_interp[10:])

with open('./../pyboard-workspace/data/ignition_table.txt', 'w') as file:
    for y in y_us_interp:
        file.write(str(y) + '\n')

pylab.show()
