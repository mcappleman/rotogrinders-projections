
if [ ! -z $2 ]
then
    echo "ENDING!!!"
    echo "Getting DraftKings by Rotogrinders"
    python write_projections.py -s DraftKings -o PointsSortWeek$1_Games$2 -k points -e $2
    python write_projections.py -s DraftKings -o CeilingSortWeek$1_Games$2 -k ceiling -e $2
    python write_projections.py -s DraftKings -o FloorSortWeek$1_Games$2 -k floor -e $2

    echo "Getting DraftKings by FFA"
    python write_projections.py -s DraftKings -o FFA_PointsSortWeek$1_Games$2 -k ffa_points -e $2
    python write_projections.py -s DraftKings -o FFA_CeilingSortWeek$1_Games$2 -k ffa_ceiling -e $2
    python write_projections.py -s DraftKings -o FFA_FloorSortWeek$1_Games$2 -k ffa_floor -e $2

    echo "Getting FanDuel by Rotogrinders"
    python write_projections.py -s FanDuel -o PointsSortWeek$1_Games$2 -k points -e $2
    python write_projections.py -s FanDuel -o CeilingSortWeek$1_Games$2 -k ceiling -e $2
    python write_projections.py -s FanDuel -o FloorSortWeek$1_Games$2 -k floor -e $2

    echo "Getting FanDuel by FFA"
    python write_projections.py -s FanDuel -o FFA_PointsSortWeek$1_Games$2 -k ffa_points -e $2
    python write_projections.py -s FanDuel -o FFA_CeilingSortWeek$1_Games$2 -k ffa_ceiling -e $2
    python write_projections.py -s FanDuel -o FFA_FloorSortWeek$1_Games$2 -k ffa_floor -e $2

    echo "Writing the Lineup CSV Comparator"
    python write_lineup_csvs.py -w $1 -e $2

else
    echo "No ENDING!"
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

fi