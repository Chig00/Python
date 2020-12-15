"""Script for calculating projectile motion and trajectory."""

import math

global grav_acc

grav_acc = 9.80665 #acceleration due to gravity

class Projectile:
    """Base class for projectile creation.

    A projectile object will have an initial velocity and angle as
    arguments for the __init__() method.

    Using the arguments, the perpendicular components are calculated,
    which in turn are used for the creation of the time of flight,
    the horizontal displacement, and the maximum height.
    
    """

    def __init__(self, init_vel, init_angle):
        """Create a projectile.

        The projectile is created with an initial velocity and angle.

        The rest of the projectile's attributes (time of flight,
        the horizontal displacement, and the maximum height) are
        calculated as well.

        """

        self.init_vel = init_vel
        self.init_angle = init_angle

        #calculates the perpendicular components for the calculations
        self.component_calc()

        #calculates and stores the projectile's attributes
        self.flight_time_calc()
        self.disp_calc()
        self.max_height_calc()

    def component_calc(self):
        """Calculate the perpendicular components.

        The vertical and horizontal velocities of the projectile are
        calculated and stored.

        """

        self.vert_vel = self.init_vel * sin(self.init_angle)
        self.hori_vel = self.init_vel * cos(self.init_angle)

    def flight_time_calc(self):
        """Calcuate the projectile's time of flight.

        The time of flight is derived from the SUVAT equation
        s = ut + 1/2at^2.

        As s = 0, the formula can be rearranged to give t = 2u/g.

        """

        self.flight_time = 2 * self.vert_vel / grav_acc

    def disp_calc(self):
        """Calculate the horizontal displacement.

        Uses the formula s = 1/2(u + v)/t with u = v to give s = vt.

        """

        self.disp = self.hori_vel * self.flight_time

    def max_height_calc(self):
        """Calculate the projectile's maximum height.

        Uses the formula s = ut + 1/2at^2 with t = 1/2time of flight
        u = vertical velocity and a = -acceleration due to gravity.

        """

        self.max_height = (self.vert_vel * self.flight_time/2
                           + (1/2) * (-grav_acc) * (self.flight_time/2) ** 2)

    def attribute_display(self):
        """Display the projectile's attributes."""

        print("Projectile's horizontal displacement:", round(self.disp, 5),
              "\nProjectile's maximum height:", round(self.max_height, 5),
              "\nProjectile's time of flight:", round(self.flight_time, 5))

class Trajectory:
    """Base class for trajectory creation.

    Uses a projectile object as the only argument for the __init__()
    method (excluding self), where the trajectory is calculated as a
    graphical function of form y = -ax(x - b), where b is the
    projectile's horizontal displacement and a is a is a value to be
    calculated for the trajectory to match the real trajectory.

    """

    def __init__(self, projectile):
        """Create the projectile's trajectory.

        The trajectory will be a graphical function in the form
        y = -ax(x - b), where b is the projectile's horizontal
        displacement and a is the value where the projectile's
        maximum height = -ax(x - b), where x = b/2, which simplifies
        to a = 4y/b^2

        If the angle is zero, then a trajectory of formula
        y = -ax^2 is used instead.

        """

        self.b = projectile.disp
        if self.b == 0:
            time = 1 / projectile.hori_vel #time to go 1 unit of displacment
            self.a = (1/2) * grav_acc * time ** 2 #y = -a (s = ut + 1/2at^2)
            
        else:
            self.a = 4 * projectile.max_height / self.b ** 2 #a = 4y/b^2

    def point_find(self, projectile):
        """Find a point on the trajectory (via its graph function).

        y values are found with the formula y = -ax(x-b)
        x values are found with the formula x = sqrt(b^2/4 - y/a) + b/2

        The velocity and angle of the projectile at the point(s) are
        also displayed by using differentiation and trigonometry.
        dy/dx = d(-ax^2 + abx)/dx = -2ax + ab

        """

        while True:
            value_type = input("Find horizontal displacement (x), height (y),"
                               " or quit (q)? ")
            if value_type == "q":
                return
            
            elif value_type == "y":
                #loop for correct input
                while True:
                    try:
                        x = float(input("x: "))

                        break

                    except ValueError: print("Please use a number.")

                print("y =", round(-self.a * x * (x - self.b), 5))
                dy_dx = -2 * self.a * x + self.a * self.b #differentiate
                angle = atan(dy_dx) #arctangent for the angle
                velocity = projectile.hori_vel / cos(angle) #h = a/cos(x)
                print("Velocity:", round(velocity, 5),
                      "\nAngle:", round(angle, 5))

            elif value_type == "x":
                #loop for correct input
                while True:
                    try:
                        y = float(input("y: "))

                        if y > projectile.max_height: raise ValueError

                        break

                    except ValueError: print("Please use a number"
                                             " < maximum height.")

                #x can take two different values (parabolic function)
                x_one = (self.b ** 2 / 4 - y/self.a) ** 0.5 + self.b/2
                x_two = -(self.b ** 2 / 4 - y/self.a) ** 0.5 + self.b/2
                
                print("x =", round(x_one, 5))
                dy_dx = -2 * self.a * x_one + self.a * self.b
                angle = atan(dy_dx)
                velocity = projectile.hori_vel / cos(angle)
                print("Velocity:", round(velocity, 5),
                      "\nAngle:", round(angle, 5))

                print("OR x =", round(x_two, 5))
                dy_dx = -2 * self.a * x_two + self.a * self.b
                angle = atan(dy_dx)
                velocity = projectile.hori_vel / cos(angle)
                print("Velocity:", round(velocity, 5),
                      "\nAngle:", round(angle, 5))

            else: print("Please use x, y, or q.")

def sin(x):
    """Perform the sin function on x.

    Takes the value of x in degrees rather than radians.

    """

    return math.sin(math.radians(x))

def cos(x):
    """Perform the cosine function on x.

    Takes the value of x in degrees rather than radians.

    """

    return math.cos(math.radians(x))

def atan(x):
    """Perform the arctangent function on x.

    Returns the value of x in degrees rather than radians.

    """

    return math.degrees(math.atan(x))

def main():
    """Create projectile and trajectory objects from input() input.

    The projectile is created by getting an input for the initial
    velocity and the projectile's angle.

    The projectile's attributes (maximum height, horizontal
    displacement, time of flight, etc.) are created automatically
    with some degree of inaccuracy (due to float rounding errors).

    Using the projectile's attributes, a trajectory can also be created
    that will be in graphical form y = -ax(x - b), where b is the
    horizontal displacement, and a will be calculated to fit the
    projectile's actual flight path.

    """

    #main loop
    while True:
        #loop for useable input
        while True:
            try:
                init_vel = float(input("Projectile's initial velocity: "))                
                init_angle = float(input("Projectile's initial angle: "))
                break

            except ValueError: print("Please use numeric values.")

        projectile = Projectile(init_vel, init_angle)

        projectile.attribute_display()

        trajectory = Trajectory(projectile)

        trajectory.point_find(projectile)

        while True:
            check = input("Make another projectile? (y/n) ")
            if check == "y" or check == "n": break
            else: print("Sorry, I didn't get that.")

        if check == "n": break

if __name__ == "__main__":
    main()
