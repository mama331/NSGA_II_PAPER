#for i in {1..10}
for i in $(seq 1 20)
do
  python3 NSGA_II_1.py
  echo $i
done
