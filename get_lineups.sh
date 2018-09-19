echo "Getting DraftKings by Rotogrinders"
python write_projections.py -s DraftKings -o PointsSortWeek$1 -k points
python write_projections.py -s DraftKings -o CeilingSortWeek$1 -k ceiling
python write_projections.py -s DraftKings -o FloorSortWeek$1 -k floor

echo "Getting DraftKings by FFA"
python write_projections.py -s DraftKings -o FFA_PointsSortWeek$1 -k ffa_points
python write_projections.py -s DraftKings -o FFA_CeilingSortWeek$1 -k ffa_ceiling
python write_projections.py -s DraftKings -o FFA_FloorSortWeek$1 -k ffa_floor

echo "Getting FanDuel by Rotogrinders"
python write_projections.py -s FanDuel -o PointsSortWeek$1 -k points
python write_projections.py -s FanDuel -o CeilingSortWeek$1 -k ceiling
python write_projections.py -s FanDuel -o FloorSortWeek$1 -k floor

echo "Getting FanDuel by FFA"
python write_projections.py -s FanDuel -o FFA_PointsSortWeek$1 -k ffa_points
python write_projections.py -s FanDuel -o FFA_CeilingSortWeek$1 -k ffa_ceiling
python write_projections.py -s FanDuel -o FFA_FloorSortWeek$1 -k ffa_floor