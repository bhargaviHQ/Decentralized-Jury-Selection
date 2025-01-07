cd ..
cd Measure_of_Spread/Coverage/
echo " **** "
nohup python3 -u BA_fractional_cov_pool.py 1> BA_fractional_cov_pool.py.out 2> BA_fractional_cov_pool.py.err &
wait
echo " **** "
nohup python3 -u BA_fractional_cov_prob.py 1> BA_fractional_cov_prob.py.out 2> BA_fractional_cov_prob.py.err &
wait
echo " **** "
nohup python3 -u BA_max_cov_pool.py 1> BA_max_cov_pool.py.out 2> BA_max_cov_pool.py.err &
wait
echo " **** "
nohup python3 -u BA_max_cov_prob.py 1> BA_max_cov_prob.py.out 2> BA_max_cov_prob.py.err &
wait

cd ..
cd Diversity/
echo " **** "
nohup python3 -u BA_max_shortpath_pool.py 1> BA_max_shortpath_pool.py.out 2> BA_max_shortpath_pool.py.err &
wait
echo " **** "
nohup python3 -u BA_max_shortpath_prob.py 1> BA_max_shortpath_prob.py.out 2> BA_max_shortpath_prob.py.err &
wait
echo " **** "
nohup python3 -u BA_overlap_cov_pool.py 1> BA_overlap_cov_pool.py.out 2> BA_overlap_cov_pool.py.err &
wait
echo " **** "
nohup python3 -u BA_overlap_cov_prob.py 1> BA_overlap_cov_prob.py.out 2> BA_overlap_cov_prob.py.err &
wait
echo " **** "

echo "Completed BA"

cd ..
cd ..
cd ..
cd ER/
cd Fairness/

echo "Starting ER"
echo " **** "
nohup python3 -u  ER_disparity_pool.py 1> ER_disparity_pool.py.out 2> ER_disparity_pool.py.err &
wait
echo " **** "
nohup python3 -u  ER_disparity_prob.py 1> ER_disparity_prob.py.out 2> ER_disparity_prob.py.err &
wait
echo " **** "
nohup python3 -u  ER_disparity_trend_pool.py 1> ER_disparity_trend_pool.py.out 2> ER_disparity_trend_pool.py.err &
wait
echo " **** "
nohup python3 -u  ER_disparity_trend_prob.py 1> ER_disparity_trend_prob.py.out 2> ER_disparity_trend_prob.py.err &
wait
echo " **** "
nohup python3 -u  ER_equality_pool.py 1> ER_equality_pool.py.out 2> ER_equality_pool.py.err &
wait
echo " **** "
nohup python3 -u  ER_equality_prob.py 1> ER_equality_prob.py.out 2> ER_equality_prob.py.err &
wait

cd ..
cd Measure_of_Spread/Coverage/
echo " **** "
nohup python3 -u ER_fractional_cov_pool.py 1> ER_fractional_cov_pool.py.out 2> ER_fractional_cov_pool.py.err &
wait
echo " **** "
nohup python3 -u ER_fractional_cov_prob.py 1> ER_fractional_cov_prob.py.out 2> ER_fractional_cov_prob.py.err &
wait
echo " **** "
nohup python3 -u ER_max_cov_pool.py 1> ER_max_cov_pool.py.out 2> ER_max_cov_pool.py.err &
wait
echo " **** "
nohup python3 -u ER_max_cov_prob.py 1> ER_max_cov_prob.py.out 2> ER_max_cov_prob.py.err &
wait

cd ..
cd Diversity/
echo " **** "
nohup python3 -u ER_max_shortpath_pool.py 1> ER_max_shortpath_pool.py.out 2> ER_max_shortpath_pool.py.err &
wait
echo " **** "
nohup python3 -u ER_max_shortpath_prob.py 1> ER_max_shortpath_prob.py.out 2> ER_max_shortpath_prob.py.err &
wait
echo " **** "
nohup python3 -u ER_overlap_cov_pool.py 1> ER_overlap_cov_pool.py.out 2> ER_overlap_cov_pool.py.err &
wait
echo " **** "
nohup python3 -u ER_overlap_cov_prob.py 1> ER_overlap_cov_prob.py.out 2> ER_overlap_cov_prob.py.err &
wait
echo " **** "

echo "Completed ER"

cd ..
cd ..
cd ..

cd LFR/
cd Fairness/

echo "Starting LFR"
echo " **** "
nohup python3 -u  LFR_disparity_pool.py 1> LFR_disparity_pool.py.out 2> LFR_disparity_pool.py.err &
wait
echo " **** "
nohup python3 -u  LFR_disparity_prob.py 1> LFR_disparity_prob.py.out 2> LFR_disparity_prob.py.err &
wait
echo " **** "
nohup python3 -u  LFR_disparity_trend_pool.py 1> LFR_disparity_trend_pool.py.out 2> LFR_disparity_trend_pool.py.err &
wait
echo " **** "
nohup python3 -u  LFR_disparity_trend_prob.py 1> LFR_disparity_trend_prob.py.out 2> LFR_disparity_trend_prob.py.err &
wait
echo " **** "
nohup python3 -u  LFR_equality_pool.py 1> LFR_equality_pool.py.out 2> LFR_equality_pool.py.err &
wait
echo " **** "
nohup python3 -u  LFR_equality_prob.py 1> LFR_equality_prob.py.out 2> LFR_equality_prob.py.err &
wait
echo " **** "

cd ..
cd Measure_of_Spread/Coverage/
echo " **** "
nohup python3 -u LFR_fractional_cov_pool.py 1> LFR_fractional_cov_pool.py.out 2> LFR_fractional_cov_pool.py.err &
wait
echo " **** "
nohup python3 -u LFR_fractional_cov_prob.py 1> LFR_fractional_cov_prob.py.out 2> LFR_fractional_cov_prob.py.err &
wait
echo " **** "
nohup python3 -u LFR_max_cov_pool.py 1> LFR_max_cov_pool.py.out 2> LFR_max_cov_pool.py.err &
wait
echo " **** "
nohup python3 -u LFR_max_cov_prob.py 1> LFR_max_cov_prob.py.out 2> LFR_max_cov_prob.py.err &
wait

cd ..
cd Diversity/
echo " **** "
nohup python3 -u LFR_max_shortpath_pool.py 1> LFR_max_shortpath_pool.py.out 2> LFR_max_shortpath_pool.py.err &
wait
echo " **** "
nohup python3 -u LFR_max_shortpath_prob.py 1> LFR_max_shortpath_prob.py.out 2> LFR_max_shortpath_prob.py.err &
wait
echo " **** "
nohup python3 -u LFR_overlap_cov_pool.py 1> LFR_overlap_cov_pool.py.out 2> LFR_overlap_cov_pool.py.err &
wait
echo " **** "
nohup python3 -u LFR_overlap_cov_prob.py 1> LFR_overlap_cov_prob.py.out 2> LFR_overlap_cov_prob.py.err &
wait
echo " **** "

echo "Completed LFR"