#!/bin/bash

python_programs=("BA_disparity_prob.py" "BA_disparity_trend_pool.py" "BA_disparity_trend_prob.py" "BA_disparity_trend.py" "BA_disparity.py" "BA_equality_pool.py" "BA_equality_prob.py" "BA_equality.py")

for program in "${python_programs[@]}"; do
    nohup python "$program" > "$program.log" 2>&1 &
    wait
done

# Run each Python program sequentially as nohup
for python_program in "${python_programs[@]}"; do
  nohup python3 "$python_program" &
  echo "Waiting for $python_program to finish..."
  wait
done

# All Python programs have finished running
echo "All Python programs have finished running."




