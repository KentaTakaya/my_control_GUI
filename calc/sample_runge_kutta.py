from math import *

class ODE_for_system():
    """
    docstring for .
    """

    def __init__(self, **args):
        self.args = args

        self.system_name = "A_MODEL.txt"

        self.N = 2
        self.M = 1
        self.R_SIZE = self.N + 1

        self.rhv = [0.0]*self.R_SIZE
        self.lhv = [0.0]*self.R_SIZE

        self.input = 1.0
        self.output = 1.0

        self.F_TIME = 10.0
        self.DT = 0.01
        self.r_time = 0.0

        self.output_file = open(self.system_name, "w")

        self.format = "GNUPLOT"

        self.initial_value = self.rhv[1:]

    def init_system(self, initial_value):
        for i in range(1, self.R_SIZE):
            self.rhv[i] = initial_value[i - 1]
            print(i, self.rhv[i])

        self.initial_value = initial_value

    def system(self):

        self.lhv[1] = self.rhv[2]
        self.lhv[2] = self.input
        self.output = self.rhv[1]

    def runge_kutta(self, h, tm):
        fn = 0.0
        r = 0.0
        work = [0.0]*self.R_SIZE

        a = 1.0 - sqrt(0.5)
        b = 2.0 - a

        self.rhv[0] = tm
        self.lhv[0] = 1.0
        self.system()

        for i in range(0, self.R_SIZE):
            fn = h*self.lhv[i]
            r = 0.5*fn - work[i]
            work[i] = work[i] + 3.0*r - 0.5*fn
            self.rhv[i] += r
        self.system()

        for i in range(0, self.R_SIZE):
            fn = h*self.lhv[i]
            r = a*(fn - work[i])
            work[i] = work[i] + 3.0*r - a*fn
            self.rhv[i] += r
        self.system()

        for i in range(0, self.R_SIZE):
            fn = h*self.lhv[i]
            r = b*(fn - work[i])
            work[i] = work[i] + 3.0*r - b*fn
            self.rhv[i] += r
        self.system()

        for i in range(0, self.R_SIZE):
            fn = h*self.lhv[i]
            r = (fn - 2.0*work[i])/6.0
            self.rhv[i] += r

        print(self.r_time, self.rhv[1], self.rhv[2])

    def write_data(self):
        if self.format == "CSV":
            pass
        else:
            ss = "{} ".format(self.r_time)
            for i in range(1, self.R_SIZE):
                ss = ss + "{} ".format(self.rhv[i])

            ss = ss + "{} ".format(self.input)
            ss = ss + "\n"
            self.output_file.write(ss)

    def calculation(self):
        while self.r_time < self.F_TIME:
            self.runge_kutta(self.DT, self.r_time)
            self.write_data()
            self.r_time = self.r_time + self.DT


if __name__ == '__main__':
    ode = ODE_for_system()
    value = [1.0, 0.0]
    ode.init_system(value)
    ode.calculation()
