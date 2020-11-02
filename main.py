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
    if name=="RSTSYNC":
        RSSIfromServer = radio.received_packet(RadioPacketProperty.SIGNAL_STRENGTH)
    elif name=="SYNC100":
        RSSIfromServer = radio.received_packet(RadioPacketProperty.SIGNAL_STRENGTH)
    elif name=="ENDSYNC":
        RSSIfromServer = radio.received_packet(RadioPacketProperty.SIGNAL_STRENGTH)
    elif name[0:6]=="DATARQ":
        statID = int(name[6:8])     # the last 2 digits are the station ID that must send data
        statID = Math.constrain(statID, 0, 9)
        if statID == stationID:
            sendData()
radio.on_received_value(on_received_value)

def sendData():
    pass

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
print(str(StationSNs.join()))
k = "hello"
print(k[0:3])