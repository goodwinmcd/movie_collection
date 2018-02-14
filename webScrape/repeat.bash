#!/bin/bash
while true
do
  python getMovieInfo.py
  pkill -f firefox
done
