set format '$%g$'
set terminal epslatex standalone color dashed

set output "A_MODEL.tex"

set key spacing 1.5

set grid
set yrange[-1:1]
set xrange[0:20]

set ylabel "Position [m], Angle [rad]"
set xlabel "Time [s]"


plot "A_MODEL.txt" using 1:6 with line linecolor rgb "blue" linewidth 5 title "Input",\
     "A_MODEL.txt" using 1:2 with line linecolor rgb "red" linewidth 5 title "Ball position",\
