#for i in {1..10}
for i in $(seq 1 200)
do
  python3.8 3.py
  echo $i
done
