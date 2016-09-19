import math
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt

q = np.array([math.pi/4, math.pi/4, 0])
q0 = np.array([math.pi/4, math.pi/4, 0])
L = np.array([300,200,100])

def fwd_kin(x):
	ts_x=0
	ts_y=0
	for i in range(len(L)):
	    s=0
	    for j in range(i+1):
	        s+=(x[j])
	    ts_x+=(L[i]*np.cos(s));ts_y+=(L[i]*np.sin(s))
	return [ts_x,ts_y]

def fk_points(x):
	ts=[[0],[0]]
	ts_x=0
	ts_y=0
	for i in range(len(L)):
	    s=0
	    for j in range(i+1):
	        s+=(x[j])
	    ts_x+=(L[i]*np.cos(s))
	    ts_y+=(L[i]*np.sin(s))
	    ts[0].append(ts_x)
	    ts[1].append(ts_y)
	return ts

def invk(xy):
	def dist(x,*args):
		
		return np.sqrt(np.sum([(xi-yi)**2  for xi,yi in zip(x,q0)]))
	def x_c(x, xy):
		xc = fwd_kin(x)[0]-xy[0]
		return xc
	def y_c(x, xy):
		yc = fwd_kin(x)[1]-xy[1]
		return yc

	return scipy.optimize.fmin_slsqp( dist,q, eqcons=[x_c, y_c],args=(xy,), iprint=0)


fig, ax = plt.subplots()


def pllot(x,y):
	ax.clear()
	ax.axis([-500,500,-500,500])
	q = invk([x,y])
	xx = fk_points(q)[0]
	yy = fk_points(q)[1]
	ax.plot(xx,yy,'*-', lw=3)

	plt.draw()

# on_click and on_move - http://matplotlib.org/examples/pylab_examples/coords_demo.html

def on_click(event):
	# get the x and y coords, flip y from top to bottom
	x, y = event.x, event.y
	if event.button == 1:
		if event.inaxes is not None:
			print('data coords %f %f' % (event.xdata, event.ydata))
			pllot(event.xdata, event.ydata)

def on_move(event):
    # get the x and y pixel coords
    x, y = event.x, event.y

    if event.inaxes:
        ax = event.inaxes  # the axes instance
    	print('data coords %f %f' % (event.xdata, event.ydata));pllot(event.xdata, event.ydata)

a = input("Select\nTrack Mouse : 1 \t Reach goal point on click : 2\nEnter : ")
if(a==1):
	binding_id = plt.connect('motion_notify_event', on_move)
else:
	plt.connect('button_press_event', on_click)
plt.show()
