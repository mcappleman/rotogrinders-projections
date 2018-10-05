echo "Generating the input CSVs"
python generate_input_csvs.py

echo ""
echo "All Players"
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

echo "Writing the Lineup CSV Comparator"
python write_lineup_csvs.py -w $1

echo ""
echo "Players for 1 o'clock games"
echo "Getting DraftKings by Rotogrinders"
python write_projections.py -s DraftKings -o PointsSortWeek$1_Games_1 -k points -e "_1"
python write_projections.py -s DraftKings -o CeilingSortWeek$1_Games_1 -k ceiling -e "_1"
python write_projections.py -s DraftKings -o FloorSortWeek$1_Games_1 -k floor -e "_1"

echo "Getting DraftKings by FFA"
python write_projections.py -s DraftKings -o FFA_PointsSortWeek$1_Games_1 -k ffa_points -e "_1"
python write_projections.py -s DraftKings -o FFA_CeilingSortWeek$1_Games_1 -k ffa_ceiling -e "_1"
python write_projections.py -s DraftKings -o FFA_FloorSortWeek$1_Games_1 -k ffa_floor -e "_1"

echo "Getting FanDuel by Rotogrinders"
python write_projections.py -s FanDuel -o PointsSortWeek$1_Games_1 -k points -e "_1"
python write_projections.py -s FanDuel -o CeilingSortWeek$1_Games_1 -k ceiling -e "_1"
python write_projections.py -s FanDuel -o FloorSortWeek$1_Games_1 -k floor -e "_1"

echo "Getting FanDuel by FFA"
python write_projections.py -s FanDuel -o FFA_PointsSortWeek$1_Games_1 -k ffa_points -e "_1"
python write_projections.py -s FanDuel -o FFA_CeilingSortWeek$1_Games_1 -k ffa_ceiling -e "_1"
python write_projections.py -s FanDuel -o FFA_FloorSortWeek$1_Games_1 -k ffa_floor -e "_1"

echo "Writing the Lineup CSV Comparator"
python write_lineup_csvs.py -w $1 -e "_1"

echo ""
echo "Players for 1 & 4 o'clock games"
echo "Getting DraftKings by Rotogrinders"
python write_projections.py -s DraftKings -o "PointsSortWeek$1_Games_1&4" -k points -e "_1&4"
python write_projections.py -s DraftKings -o "CeilingSortWeek$1_Games_1&4" -k ceiling -e "_1&4"
python write_projections.py -s DraftKings -o "FloorSortWeek$1_Games_1&4" -k floor -e "_1&4"

echo "Getting DraftKings by FFA"
python write_projections.py -s DraftKings -o "FFA_PointsSortWeek$1_Games_1&4" -k ffa_points -e "_1&4"
python write_projections.py -s DraftKings -o "FFA_CeilingSortWeek$1_Games_1&4" -k ffa_ceiling -e "_1&4"
python write_projections.py -s DraftKings -o "FFA_FloorSortWeek$1_Games_1&4" -k ffa_floor -e "_1&4"

echo "Getting FanDuel by Rotogrinders"
python write_projections.py -s FanDuel -o "PointsSortWeek$1_Games_1&4" -k points -e "_1&4"
python write_projections.py -s FanDuel -o "CeilingSortWeek$1_Games_1&4" -k ceiling -e "_1&4"
python write_projections.py -s FanDuel -o "FloorSortWeek$1_Games_1&4" -k floor -e "_1&4"

echo "Getting FanDuel by FFA"
python write_projections.py -s FanDuel -o "FFA_PointsSortWeek$1_Games_1&4" -k ffa_points -e "_1&4"
python write_projections.py -s FanDuel -o "FFA_CeilingSortWeek$1_Games_1&4" -k ffa_ceiling -e "_1&4"
python write_projections.py -s FanDuel -o "FFA_FloorSortWeek$1_Games_1&4" -k ffa_floor -e "_1&4"

echo "Writing the Lineup CSV Comparator"
python write_lineup_csvs.py -w $1 -e "_1&4"