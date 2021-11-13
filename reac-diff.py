#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from matplotlib.animation import FuncAnimation

# Laplacian matrix
Del2 = np.array([[0.05, 0.2, 0.05], [0.2, -1, 0.2], [0.05, 0.2, 0.05]])

# Parameters

# Diffusion rates
Da = 1.0
Db = 0.5

f = 0.055		# feed rate
k = 0.062		# kill rate

# Coral growth
# f = 0.0545      
# k = 0.0620      

# Mitosis
# f = 0.0367
# k = 0.0649

dt = 1.0       # Delta t between iterations
n = 2000       # Total number of iterations

# Initializing grid with concentrations A and B
x = 100
y = 100
A = np.ones((x, y))
B_no_seed = np.zeros((x, y))

def convolve(X, Y, Del2):
	"""
	Performs 2D convolution, or calculates the Laplacian to give the difference between the average values of the neighbouring cells and the current cell, to calculate diffusion

	Parameters:
	X 		:   Initial A grid (2x2)
	Y 		:   Initial B grid (2x2)
	Del2	:	Laplacian matrix (3x3)

	Returns convolved A and B matrices
	"""

	X_conv = signal.convolve2d(X, Del2, mode='same')
	Y_conv = signal.convolve2d(Y, Del2, mode='same')

	return X_conv, Y_conv

def seeding(X, x_start, y_start, width, depth):
	"""
	Seeds the specified area of a matrix X with a value (currently 1)

	Parameters:
	X 		:	2x2 matrix to be seeded
	x_start	:	Starting x value in the matrix to be seeded
	y_start :	Starting y value in the matrix to be seeded
	width	:	Width of the seeded area
	depth 	:	Depth of the seeded area

	Returns the seeded matrix
	"""

	x_end = x_start + width
	y_end = y_start + depth
	X[x_start:x_end, y_start:y_end] = 1

	return X

# Seeding coordinates
startx = 40
starty = 40
w = 20
d = 20
B = seeding(B_no_seed, startx, starty, w, d)

# Initializing plot
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_title("Reaction-Diffusion Simulation")
pos = ax.imshow(B, cmap='viridis')
bar = plt.colorbar(pos)

def reaction_diffusion(i, dtime, kill, feed, Dx, Dy):
	"""
	Implements the reaction-diffusion equation according to the tutorial here: https://www.karlsims.com/rd.html. This is also the function used for the animation

	Parameters:
	i 		:	frame number for the animation
	dtime	:	time increments 
	kill	: 	kill rate in the simulation
	feed	:	feed rate in the simulation
	Dx 		: 	diffusion rate of A
	Dy		:	diffusion rate of B

	Returns the updated array at every iteration of the animation
	"""

	global A 
	global B 

	A_conv, B_conv = convolve(A, B, Del2)
	A_new = A + (Dx*A_conv - A*B**2 + feed*(1-A))*dtime
	B_new = B + (Dy*B_conv + A*B**2 - (kill+feed)*B)*dtime
	A = A_new
	B = B_new

	pos.set_array(B_new)

	return pos,

# Initializing animation
params = (dt, k, f, Da, Db)
anim = FuncAnimation(fig, reaction_diffusion, frames=range(n), fargs=params, interval=1000, blit=True)
anim.save('reac-diff.gif')