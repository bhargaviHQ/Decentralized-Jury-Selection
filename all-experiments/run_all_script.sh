echo "starting"
cd  visualization/Fairness/

echo "########    equality_of_selection_visual   ############"
python equality_of_selection_visual.py > file_equality_of_selection_visual.txt

echo "########    frequency_of_selection_visual   ############"
python frequency_of_selection_visual.py > file_frequency_of_selection_visual.txt

cd ..
cd  Measure_of_Spread/Coverage
echo "########    fractional_coverage_visual   ############"
python fractional_coverage_visual.py > file_fractional_coverage_visual.txt

echo "########    maximum_coverage_visual   ############"
python maximum_coverage_visual.py > file_maximum_coverage_visual.txt

cd ..
cd  Diversity
echo "########    maximum_shortest_path_visual   ############"
python maximum_shortest_path_visual.py > file_maximum_shortest_path_visual.txt

echo "########    overlapping_coverage_visual   ############"
python overlapping_coverage_visual.py > file_overlapping_coverage_visual.txt