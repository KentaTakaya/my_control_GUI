#define RSIZE 3 // システムの次元+1
#define D_TIME 0.01  //sim perametr
#define F_TIME 10.0

#define NN 2 // システムの次元

#define U_NUM 2 // データの列番号
#define Y_NUM 1 // データの列番号
#define FILE_DEL " " // ファイルのデリミタ


#include <stdio.h>
#include <math.h>
#include <signal.h>

#include <iostream>
#include <Eigen/Dense>

#include <string>
#include <vector>

#include <fstream>

FILE *fp; // file pointer
FILE *fp2; // observation data file

double r_time;
double output;
double input;
double lhv[RSIZE], rhv[RSIZE] = {0.0, 0.01, 0.01};

double J = 1.0;
double C = 1.0;
double Kt = 1.0;
double Ra = 1.0;

std::vector<double> y_array;
std::vector<double> u_array;

int main(int argc, char *argv[])
{
    extern void runge_kutta(double, double);
    extern std::vector<std::string> split(std::string str, char del);
    extern void read_data(const char* file_name);

    fp = fopen("sim2.dat", "w");

    read_data(argv[1]);

    fprintf(fp, "#t in out x1 x2\n");
    do
    {
        input = 10.0;
        runge_kutta(D_TIME, r_time);
        fprintf(fp, "%f %f %f %f %f\n",r_time, input, output, rhv[1], rhv[2]);

        r_time += D_TIME;
    }
    while(r_time < F_TIME);
    fclose(fp);
    return 0;
}

//runge_kutta-gill method

void runge_kutta(double h, double tm)
{
  extern void filt(void);
  int i;
  double a, b;
  double fn, r;
  double work[RSIZE];
  a = 1.0 - sqrt((double)0.5);
  b = 2.0 -a;

  for(i = 0; i < RSIZE; i++)
  {
    work[i] = 0.0;
  }
  rhv[0] = tm;
  lhv[0] = 1.0;
  filt();

  for(i = 0; i < RSIZE; i++)
  {
    fn = h*lhv[i];
    r = 0.5*fn - work[i];
    work[i] = work[i] + 3.0*r - 0.5*fn;
    rhv[i] += r;
  }
  filt();

  for(i = 0; i < RSIZE; i++)
  {
    fn = h*lhv[i];
    r = a*(fn - work[i]);
    work[i] = work[i] + 3.0*r - a*fn;
    rhv[i] += r;
  }
  filt();

  for(i = 0; i < RSIZE; i++)
  {
    fn = h*lhv[i];
    r = b*(fn - work[i]);
    work[i] = work[i] + 3.0*r - b*fn;
    rhv[i] += r;
  }
  filt();

  for(i = 0; i < RSIZE; i++)
  {
    fn = h*lhv[i];
    r = (fn - 2.0*work[i])/6.0;
    rhv[i] += r;
  }
}

// state equation

void filt(void)
{
  lhv[1] = rhv[2];
  lhv[2] = -Kt*Kt/Ra/J*rhv[2] + Kt/J*input;
  output = rhv[1];
}
