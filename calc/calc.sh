#!/bin/sh
python3 sliding_mode.py
gnuplot plot.plt
pdflatex A_MODEL.tex

pdftoppm -png A_MODEL.pdf > A_MODEL.png
