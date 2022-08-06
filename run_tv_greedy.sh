#for i in {1..10}
for i in $(seq 1 180)
do
  python3 MWSNs2/pylot.py
  echo $i
done
