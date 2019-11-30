#!/bin/bash

gnuplot -persist <<"EOF"
set style data linespoints
show timestamp
set xlabel "time (seconds)"
set ylabel "segments (cwnd, ssthresh)"
plot "renoSetQueue40.txt" using 1:7 title "snd_cwnd", \
      "renoSetQueue40.txt" using 1:($8>=2147483647 ? 0 : $8) title "snd_ssthresh"
EOF
