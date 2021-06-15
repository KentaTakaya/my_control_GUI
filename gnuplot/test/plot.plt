set format '$%g$'
set terminal epslatex standalone color dashed

set key spacing 1.5

set grid
set output "sin.tex"
set yrange[-1.5:1.5]
set xrange[0:10]
set xlabel "$x$"
set ylabel "$y$"
plot sin(x) title "$y = \\sin(x)$",\
     cos(x) title "$y = \\cos(x)$"
