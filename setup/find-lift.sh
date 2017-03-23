cd /home/pi/dev/cv/Vision-2016
killall python
python find_lift.py 10.10.76.2 noninteractive log-images &
sleep 10
./set_camera_params.sh
