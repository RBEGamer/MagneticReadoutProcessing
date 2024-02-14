mkdir /tmp/temp
mkdir /tmp/temp_results
MRPCli --basepath /tmp/temp config setup temp
MRPCli --basepath /tmp/temp config setupsensor temp
MRPCli --basepath /tmp/temp sensor info temp
MRPCli --basepath /tmp/temp sensor query temp

wget --quiet http://192.168.178.88/printer/gcode/script?script=SET_HEATER_TEMPERATURE%20HEATER=heater_bed%20TARGET=0



for i in {20..50}
do
  echo i: $i


    rm /tmp/temp/*.mag.json

    wget --quiet http://192.168.178.88/printer/gcode/script?script=SET_HEATER_TEMPERATURE%20HEATER=heater_bed%20TARGET=$i
    sleep 60
    wget --quiet http://192.168.178.88/printer/gcode/script?script=SET_HEATER_TEMPERATURE%20HEATER=heater_bed%20TARGET=0
    sleep 10
    MRPCli --basepath /tmp/temp measure run temp

    #cp /tmp/linear/*SID0*.mag.json /home/pi/linear_results/DISTANCE=$i.mag.json
    cp /tmp/temp/*.mag.json /tmp/temp_results/TEMPERATURE=$i.mag.json
done

wget --quiet http://192.168.178.88/printer/gcode/script?script=SET_HEATER_TEMPERATURE%20HEATER=heater_bed%20TARGET=0