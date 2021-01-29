"""
Produces an ASCII-based animation of the atomic orbital in the command line.

Each frame is a cross-section of the orbital. As the animation progresses, the user is taken from one end of the atom to the other.

The values displayed correspond to probability. The wavefunction is calculated by multiplying the value of the spherical harmonic at each point in 3D Cartesian space by an exponential radial decay factor; the wavefunction is then squared to yield probability.

Visualizations for a given pair of l and m should resemble the images shown here, when viewplane "xz" is used: https://en.wikipedia.org/wiki/Atomic_orbital#Orbitals_table

Inputs:

	l: angular momentum

	m: spin angular momentum

	x_min, x_max: The bounding interval of the visualization in the X axis. No units are specified.

	y_min, y_max: The bounding interval of the visualization in the Y axis. No units are specified.

	z_min, z_max: The bounding interval of the visualization in the Z axis. No units are specified.

	radial_decay_factor: The factor by which the spherical harmonic exponentially decays.

	viewplane: May be "xy", "xz", or "yz". Corresponds to the two perpendicular axes defining the viewing plane.

There is no support for quantum number n.

For aesthetically pleasing visualizations, a bounding interval of [-10,10] on each axis is recommended, along with a radial decay factor of 0.08.
"""

import math,time

"""Calculates the real value of a spherical harmonic at a point (x,y,z) in 3D Cartesian space given principle quantum numbers l (angular momentum) and m (spin angular momentum). Returns a tuple containing the textual symbol of the atomic orbital as well as the calculated value."""
def real_spherical_harmonic_lookup(l,m,x,y,z):
	#Calculates distance of point (x,y,z) from the origin.
	r=math.sqrt(float(x**2)+float(y**2)+float(z**2))
	#Looks up appropriate formula to use given l and m, and then calculates the value.
	if ((l==0) and (m==0)):
		atomic_orbital_symbol="s"
		spherical_harmonic=0.5*math.sqrt(1.0/math.pi)
	elif ((l==1) and (m==-1)):
		atomic_orbital_symbol="p_y"
		spherical_harmonic=math.sqrt(3.0/(4.0*math.pi))*(y/r)
	elif ((l==1) and (m==0)):
		atomic_orbital_symbol="p_z"
		spherical_harmonic=math.sqrt(3.0/(4.0*math.pi))*(z/r)
	elif ((l==1) and (m==1)):
		atomic_orbital_symbol="p_x"
		spherical_harmonic=math.sqrt(3.0/(4.0*math.pi))*(x/r)
	elif ((l==2) and (m==-2)):
		atomic_orbital_symbol="d_xy"
		spherical_harmonic=0.5*math.sqrt(15.0/math.pi)*((x*y)/(r**2))
	elif ((l==2) and (m==-1)):
		atomic_orbital_symbol="d_yz"
		spherical_harmonic=0.5*math.sqrt(15.0/math.pi)*((y*z)/(r**2))
	elif ((l==2) and (m==0)):
		atomic_orbital_symbol="d_z^2"
		spherical_harmonic=0.25*math.sqrt(5.0/math.pi)*(((-(x**2))-(y**2)+(2*(z**2)))/(r**2))
	elif ((l==2) and (m==1)):
		atomic_orbital_symbol="d_xz"
		spherical_harmonic=0.5*math.sqrt(15.0/math.pi)*((x*z)/(r**2))
	elif ((l==2) and (m==2)):
		atomic_orbital_symbol="d_x^2-y^2"
		spherical_harmonic=0.25*math.sqrt(15.0/math.pi)*(((x**2)-(y**2))/(r**2))
	elif ((l==3) and (m==-3)):
		atomic_orbital_symbol="f_y(3x^2-y^2)"
		spherical_harmonic=0.25*math.sqrt(35.0/(2*math.pi))*((((3*(x**2))-(y**2))*y)/(r**3))
	elif ((l==3) and (m==-2)):
		atomic_orbital_symbol="f_xyz"
		spherical_harmonic=0.5*math.sqrt(105.0/math.pi)*((x*y*z)/(r**3))
	elif ((l==3) and (m==-1)):
		atomic_orbital_symbol="f_yz^2"
		spherical_harmonic=0.25*math.sqrt(21.0/(2*math.pi))*((((4*(z**2))-(x**2)-(y**2))*y)/(r**3))
	elif ((l==3) and (m==0)):
		atomic_orbital_symbol="f_z^3"
		spherical_harmonic=0.25*math.sqrt(7.0/math.pi)*((((2*(z**2))-(3*(x**2))-(3*(y**2)))*z)/(r**3))
	elif ((l==3) and (m==1)):
		atomic_orbital_symbol="f_xz^2"
		spherical_harmonic=0.25*math.sqrt(21.0/(2*math.pi))*((((4*(z**2))-(x**2)-(y**2))*x)/(r**3))
	elif ((l==3) and (m==2)):
		atomic_orbital_symbol="f_z(x^2-y^2)"
		spherical_harmonic=0.25*math.sqrt(105.0/math.pi)*((((x**2)-(y**2))*z)/(r**3))
	elif ((l==3) and (m==3)):
		atomic_orbital_symbol="f_x(x^2-3y^2)"
		spherical_harmonic=0.25*math.sqrt(35.0/(2*math.pi))*((((x**2)-(3*(y**2)))*x)/(r**3))
	elif ((l==4) and (m==-4)):
		atomic_orbital_symbol="g_xy(x^2-y^2)"
		spherical_harmonic=0.75*math.sqrt(35.0/math.pi)*(((x*y)*((x**2)-(y**2)))/(r**4))
	elif ((l==4) and (m==-3)):
		atomic_orbital_symbol="g_zy^3"
		spherical_harmonic=0.75*math.sqrt(35.0/(2*math.pi))*(((y*z)*((3*(x**2))-(y**2)))/(r**4))
	elif ((l==4) and (m==-2)):
		atomic_orbital_symbol="g_z^2xy"
		spherical_harmonic=0.75*math.sqrt(5.0/math.pi)*(((x*y)*((7*(z**2))-(r**2)))/(r**4))
	elif ((l==4) and (m==-1)):
		atomic_orbital_symbol="g_z^3y"
		spherical_harmonic=0.75*math.sqrt(5.0/(2*math.pi))*(((y*z)*((7*(z**2))-(3*(r**2))))/(r**4))
	elif ((l==4) and (m==0)):
		atomic_orbital_symbol="g_z^4"
		spherical_harmonic=0.1875*math.sqrt(1.0/math.pi)*(((35*(z**4))-(30*(z**2)*(r**2))+(3*(r**4)))/(r**4))
	elif ((l==4) and (m==1)):
		atomic_orbital_symbol="g_z^3x"
		spherical_harmonic=0.75*math.sqrt(5.0/(2*math.pi))*(((x*z)*((7*(z**2))-(3*(r**2))))/(r**4))
	elif ((l==4) and (m==2)):
		atomic_orbital_symbol="g_z^2(x^2-y^2)"
		spherical_harmonic=0.375*math.sqrt(5.0/math.pi)*((((x**2)-(y**2))*((7*(z**2))-(r**2)))/(r**4))
	elif ((l==4) and (m==3)):
		atomic_orbital_symbol="g_zx^3"
		spherical_harmonic=0.75*math.sqrt(35.0/(2*math.pi))*((((x**2)-(3*(y**2)))*(x*z))/(r**4))
	elif ((l==4) and (m==4)):
		atomic_orbital_symbol="g_x^4+y^4"
		spherical_harmonic=0.1875*math.sqrt(35.0/math.pi)*((((x**2)*((x**2)-(3*(y**2))))-((y**2)*((3*(x**2))-(y**2))))/(r**4))
	#Returns atomic orbital symbol and calculated spherical harmonic value.
	return atomic_orbital_symbol,spherical_harmonic

""""Generates the animation of the atomic orbital."""
def visualize_atomic_orbital(l,m,x_min,x_max,y_min,y_max,z_min,z_max,radial_decay_factor,viewplane):
	#Defines the delay between each frame. 0.25 is recommended.
	frame_delay=0.25
	#Defines the ASCII characters which encode different probability levels.
	probability_coding={
	0.2:"$",
	0.15:"O",
	0.1:"o",
	0.05:".",
	0.0:" "
	}
	#Carries out the animation according to the user-specified viewing plane.
	if viewplane=="xy":
		for z in range(z_min,z_max):
			#Populates a new frame with probability visualization data.
			frame=""
			for y in range(y_max,y_min,-1):
				for x in range(x_min,x_max):
					#If nucleus is encountered, identifies it with an "N".
					if ((x==0) and (y==0) and (z==0)):
						frame+="N"
						continue
					#Looks up the value of the spherical harmonic at the current point.
					spherical_harmonic_value=real_spherical_harmonic_lookup(l,m,x,y,z)[1]
					#Calculates distance of the point from the origin.
					r=math.sqrt(float(x**2)+float(y**2)+float(z**2))
					#Calculates the probability at this particular point.
					probability=(spherical_harmonic_value*math.exp(-radial_decay_factor*r))**2
					#Looks up the ASCII character appropriate for the current probability and writes it to the frame.
					for magnitude in probability_coding:
						if probability>=magnitude:
							frame+=probability_coding[magnitude]
							break
				frame+="\n"
			#Displays the frame for a short period.
			print(frame)
			time.sleep(frame_delay)
	#Functionality is as described above.
	elif viewplane=="xz":
		for y in range(y_min,y_max):
			frame=""
			for z in range(z_max,z_min,-1):
				for x in range(x_min,x_max):
					if ((x==0) and (y==0) and (z==0)):
						frame+="N"
						continue
					r=math.sqrt(float(x**2)+float(y**2)+float(z**2))
					spherical_harmonic_value=real_spherical_harmonic_lookup(l,m,x,y,z)[1]
					probability=(spherical_harmonic_value*math.exp(-radial_decay_factor*r))**2
					for magnitude in probability_coding:
						if probability>=magnitude:
							frame+=probability_coding[magnitude]
							break
				frame+="\n"
			print(frame)
			time.sleep(frame_delay)
	elif viewplane=="yz":
		for x in range(x_min,x_max):
			frame=""
			for y in range(y_max,y_min,-1):
				for z in range(z_min,z_max):
					if ((x==0) and (y==0) and (z==0)):
						frame+="N"
						continue
					r=math.sqrt(float(x**2)+float(y**2)+float(z**2))
					spherical_harmonic_value=real_spherical_harmonic_lookup(l,m,x,y,z)[1]
					probability=(spherical_harmonic_value*math.exp(-radial_decay_factor*r))**2
					for magnitude in probability_coding:
						if probability>=magnitude:
							frame+=probability_coding[magnitude]
							break
				frame+="\n"
			print(frame)
			time.sleep(frame_delay)

"""Validates all input. Returns False if an error is encountered, otherwise returns True."""
def validate_input(l,m,x_min,x_max,y_min,y_max,z_min,z_max,radial_decay_factor,viewplane):
	#Ensures inputs l through z_max are integers.
	for argument in [l,m,x_min,x_max,y_min,y_max,z_min,z_max]:
		if type(argument)!=int:
			print("Error. Inputs l through z_max must be integers.")
			return False
	#Ensures l and m are of valid magnitude relative to each other.
	if abs(m)>l:
		print("Error. m must be of magnitude smaller than or equal to l.")
		return False
	#Ensures bounding intervals for visualization are valid.
	if x_min>=x_max:
		print("Error. x_min must be smaller than x_max.")
		return False
	elif y_min>=y_max:
		print("Error. y_min must be smaller than y_max.")
		return False
	elif z_min>=z_max:
		print("Error. z_min must be smaller than z_max.")
		return False
	#Ensures radial_decay_factor is a floating point.
	if type(radial_decay_factor)!=float:
		print("Error. radial_decay_factor must be a floating point.")
		return False
	#Ensures viewplane is one of either "xy", "xz", or "yz".
	if type(viewplane)!=str:
		print("Error. viewplane must be a string.")
		return False
	elif viewplane not in ["xy","xz","yz"]:
		print("Error. viewplane must be one of either \"xy\", \"xz\", or \"yz\".")
		return False
	#Returns True if all input is valid.
	return True

"""Main. Define arguments here, then run in the command line: python ./atomic_orbital_visualizer.py"""
def main():
	l=2
	m=1
	#The following are good defaults.
	x_min=-10
	x_max=10
	y_min=-10
	y_max=10
	z_min=-10
	z_max=10
	radial_decay_factor=0.08
	viewplane="xz"
	#Validates input.
	if not validate_input(l,m,x_min,x_max,y_min,y_max,z_min,z_max,radial_decay_factor,viewplane):
		return -1
	#Creates animation.
	visualize_atomic_orbital(l,m,x_min,x_max,y_min,y_max,z_min,z_max,radial_decay_factor,viewplane)
	return 0

if __name__=="__main__":
	main()
