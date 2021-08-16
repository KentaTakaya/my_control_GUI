from math import *
import numpy as np
import time

class ODE_for_system():
    """
    docstring for .
    """

    def __init__(self, **args):
        self.args = args

        self.system_name = "A_MODEL.txt"

        self.N = 4
        self.M = 1
        self.R_SIZE = self.N + 1

        self.rhv = [0.0]*self.R_SIZE
        self.lhv = [0.0]*self.R_SIZE

        self.input = 0.01
        self.output = 0.0

        self.F_TIME = 30.0
        self.DT = 0.01
        self.r_time = 0.0

        self.setpoint = 0.0

        self.U_MAX = 1.0

        self.output_file = open(self.system_name, "w")

        self.format = "GNUPLOT"

        self.initial_value = self.rhv[1:]

    def init_system(self, initial_value):
        for i in range(1, self.R_SIZE):
            self.rhv[i] = initial_value[i - 1]
            print(i, self.rhv[i])

        self.initial_value = initial_value

    def system(self):
        u = 1.0*self.input/3.1415*180.0

        ee = self.setpoint - self.rhv[1]
        dee = -1.0*self.rhv[2]
        iee = self.rhv[3]

        # PID
        u = 0.1*ee + 0.1*dee + 0.01*iee

        # Sliding Mode
        S = dee + ee
        fs = 1.0/5.0*self.sgn(S)
        fs = 1.0/5.0*np.tanh(S)
        fs = 1.0/5.0*S # this is PD controll
        fs = 50.0/1.0*S*S*S*S*S # this is PD controll

        u = fs

        # fuzzy pid
        start = time.time()
        u = -1.0*get_fuzzy_pid_cmd(ee, iee, dee)

        #print("time {}".format(time.time() - start))

        if abs(u) > self.U_MAX:
            print("u is bigger than U_max {} {}".format(u, self.U_MAX))
            if u < 0:
                u = -1.0*self.U_MAX
            else:
                u = self.U_MAX

        self.input = u
        u = u/np.pi*180.0 # deg to rad

        self.lhv[1] = self.rhv[2]
        self.lhv[2] = 0.53*u
        self.lhv[3] = ee # e dot
        self.lhv[4] = self.rhv[3] # integral of e
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

        #print(self.r_time, self.rhv[1], self.rhv[2])

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

    def sgn(self, value):
        if value >= 0.0:
            return 1.0
        else:
            return -1.0

C1 = 1.0 # Center of P
C2 = 0.5 # Center of D
C3 = 0.01 # Center of I
C4 = 1.0 # u Small
C5 = 2.0 # u Midium
C6 = 4.0 # u Large

def get_fuzzy_pid_cmd(e, ei, ed):
    f1 = sigmoid(C1,  e)*sigmoid(C3,  ei)*sigmoid(C2,  ed) # p p p
    f2 = sigmoid(C1,  e)*sigmoid(C3,  ei)*sigmoid(-C2, ed) # p p n
    f3 = sigmoid(C1,  e)*sigmoid(-C3, ei)*sigmoid(C2,  ed) # p n p
    f4 = sigmoid(C1,  e)*sigmoid(-C3, ei)*sigmoid(-C2, ed) # p n n
    f5 = sigmoid(-C1, e)*sigmoid(C3,  ei)*sigmoid(C2,  ed) # n p p
    f6 = sigmoid(-C1, e)*sigmoid(C3,  ei)*sigmoid(-C2, ed) # n p n
    f7 = sigmoid(-C1, e)*sigmoid(-C3, ei)*sigmoid(C2,  ed) # n n p
    f8 = sigmoid(-C1, e)*sigmoid(-C3, ei)*sigmoid(-C2, ed) # n n n

    # for calculation speed, 0*f4 + 0*f5 is neglected
    num = -C6*f1 + C4*f2 + -C5*f3 + C5*f6 + -C4*f5 + C6*f8
    den = f1 + f2 + f3 + f4 + f5 + f6 + f7 + f8

    # avoid zero divition error
    if den == 0.0:
        den = 0.001

    return num/den

def sigmoid(C, X):
    return 1.0/(1.0 + exp(-C*X))

if __name__ == '__main__':
    ode = ODE_for_system()
    value = [0.5, 0.0, 0.0, 0.0]
    ode.init_system(value)
    ode.calculation()
