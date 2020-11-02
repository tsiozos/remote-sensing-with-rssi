stationID = 0 #0=repeater/pc station, 1-9 = transmitter/sensor with ID
syncedTimes = 0 # how many SYNC signals have been received from this station
syncingNOW = False #syncing state: is this station syncing?

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
            radio.send_value("RSTSYNC", 0)
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
    global syncedTimes,syncingNOW
    if name=="RSTSYNC":
        syncedTimes = 0
        syncingNOW = True
    elif name=="SYNC100" and syncingNOW:
            syncedTimes = syncedTimes + 1
    elif name=="ENDSYNC":
            syncingNOW = False

radio.on_received_value(on_received_value)

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
    p = Math.min(1,5936.2673*rssi2**(-3.7231))
    if p==1:
        t = maxtries
    else:
        t = Math.max(1,triesN(y,p))  #if tries fall below 1, at least 1 try
    return t


#print(triesFromRSSI(-85,0.9,20))
#print(triesFromRSSI(-85,0.95,20))
#print(triesFromRSSI(-95,0.95,20))
print(str(control.device_serial_number()))