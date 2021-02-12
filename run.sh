kill -9 $(ps aux | grep CarCompare.py | awk '{print $2}')
nohup python3 /root/car-compare/api/src/CarCompare.py &
