stationID = 0 #0=repeater/pc station, 1-9 = transmitter/sensor with ID

StationIDs=range(10).fill(0) #we hold the stationIDs here
#StationIDs.fill(0)
StationSNs=range(10).fill(0)  #we hold the station S/N here
#StationSNs.fill(0)
StationData=range(10).fill(0)  #for each station we keep the last sent data
#StationData.fill(0)
RSSIv=bytearray(10) #statistics from the client stations (ID > 0) values -120 ~ -40
RSSIv.fill(0)
RSSIfromServer = -120 #the RSSI value from the last message from server
SensorData=bytearray(18)
SensorData.fill(0)

basic.show_number(stationID)
basic.clear_screen()
radio.set_group(77)
radio.set_transmit_power(7)


# send SYNC signals to stations
# so they can calculate succes/failure statistics
def on_button_pressed_ab():
    global stationID
    if stationID == 0:      #Can send calibration signals only if repeater or pc station
        # ---- START CALIBRATION ----
    # 90 calibration messages imply success rate 0.99, packet loss 0.95
    # RESET the station counters first
        for i in range(100):
            radio.send_value("RSTSYNC", i)
            basic.pause(50)

        for i in range(100):
            radio.send_value("SYNC100", i)
            basic.pause(50)

        for i in range(100):
            radio.send_value("ENDSYNC",0)
            basic.pause(50)
    # end if stationID
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_received_value(name, value):     #executed by clients stationID > 0
    global RSSIfromServer,stationID
    RSSIfromServer = radio.received_packet(RadioPacketProperty.SIGNAL_STRENGTH)
    if name=="RSTSYNC":
        pass
    elif name=="SYNC100":
        pass
    elif name=="ENDSYNC":
        pass
    elif name[0:6]=="DATARQ":
        statID = int(name[6:8])     # the last 2 digits are the station ID that must send data
        statID = Math.constrain(statID, 0, 9)
        if statID == stationID:
            sendData()
radio.on_received_value(on_received_value)

# the server receives client data
def on_received_buffer(receivedBuffer):
    pass
radio.on_received_buffer(on_received_buffer)

def sendData():

    global RSSIfromServer,SensorData
    SensorData[0] = stationID   # first byte is the current stationID
    SensorData[1] = input.compass_heading()
    SensorData[2] = input.temperature()
    SensorData[3] = Math.map(input.rotation(Rotation.PITCH),-180,180,0,255)
    SensorData[4] = Math.map(input.rotation(Rotation.ROLL),-180,180,0,255)
    SensorData[5] = input.light_level()
    SensorData[6] = Math.map(input.acceleration(Dimension.X),-1024,1024,0,255)
    SensorData[7] = Math.map(input.acceleration(Dimension.Y),-1024,1024,0,255)
    SensorData[8] = Math.map(input.acceleration(Dimension.Z),-1024,1024,0,255)

    #calculate how many tries based on current RSSI and 95% success
    tries = triesFromRSSI(RSSIfromServer, 0.95, 8)
    
    for i in range(tries+1):
        radio.send_buffer(SensorData)
        basic.pause(200)

#------------------- SETUP -----------------------
#change the transmitter ID. Up to 9 transmitters
def on_button_pressed_a():
    global stationID
    stationID = (stationID+1) % 10
    basic.show_number(stationID)
    basic.clear_screen()
input.on_button_pressed(Button.A, on_button_pressed_a)
#show the transmitter ID.
def on_button_pressed_b():
    global stationID
    basic.show_number(stationID)
    basic.clear_screen()
input.on_button_pressed(Button.B, on_button_pressed_b)
#--------------- END OF SETUP FUNCTIONS ----------

def triesN(y,p):
    return Math.ceil(Math.log(1-y)/Math.log(p))

def lossP(y,n):
    return Math.pow((1-y),1/n)

def triesFromRSSI(rssi: float, y:float, maxtries: int):
    rssi2 = rssi + 100
    p = Math.min(1,5936.2673*rssi2**(-3.7231)) # this function may return a p > 1
                                               # so we limit it to 1
    if p==1:
        t = maxtries
    else:
        t = Math.max(1,triesN(y,p))  #if tries fall below 1, at least 1 try
    return t


#print(triesFromRSSI(-85,0.9,20))
#print(triesFromRSSI(-85,0.95,20))
#print(triesFromRSSI(-95,0.95,20))
#print(str(control.device_serial_number() ^ 0xFFFFFFFF ))
#print(str(StationSNs.join()))
#k = "hello"
#print(k[0:3])

#pitchroll = bytearray(2)
#for i in range(100):
#    pit = input.rotation(Rotation.PITCH)
#    rol = input.rotation(Rotation.ROLL)
#    print(str(pit)+", "+str(rol))
#    pitchroll[0]=Math.map(pit,-180,180,0,255)
#    pitchroll[1]=Math.map(rol,-180,180,0,255)
#    print(">> "+str(pitchroll[0])+", "+str(pitchroll[1]))
#    basic.pause(2000)
