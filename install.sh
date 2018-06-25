installpath=/home/pi/Musik
if [ -d "$installpath" ]; then
echo "the gmtmp3 skript will be available in $installpath"
cp gmtmp3.py $installpath/gmtmp3.py
cp lcd.py $installpath/lcd.py 
apt install python3&& apt install mpc && apt install mpd
pip3 install youtube_dl
mpc add http://addrad.io/4WRMN2
else
echo "$installpath doesn't exist"
fi


