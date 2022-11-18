import time
import serial
import math

# Set up Constands
BAUD_RATE = 9600
filterPercentage = 0.5
millisecDelay = 50

arduino = serial.Serial(port="COM6", baudrate=BAUD_RATE, timeout=.6)

rollValueFiltered = 90
pitchValueFiltered = 90

# Write Data to Serial
def writeServoPositionsToSerial(servoPosArr):
    global rollValueFiltered
    global pitchValueFiltered
    
    firstConvert = math.floor(servoPosArr[0])
    secondConvert = math.floor(servoPosArr[1])
    
    #Filter Values
    rollValueFiltered = math.floor((firstConvert * filterPercentage) + (rollValueFiltered * (1-filterPercentage)))
    pitchValueFiltered = math.floor((secondConvert * filterPercentage) + (pitchValueFiltered * (1-filterPercentage)))

    s = ":"
    strToSend = s.join((str(rollValueFiltered), str(pitchValueFiltered)))

    arduino.write(bytes(strToSend, 'utf-8'))

    print(strToSend)

counter = 0;

while True:
    time.sleep(millisecDelay/1000)

    counter += 5

    if counter == 180:
        counter = 0
        time.sleep(0.2)

    writeServoPositionsToSerial([counter, counter])
