let stationID = 0
// 0=repeater/pc station, 1-9 = transmitter/sensor with ID
let StationIDs = _py.range(10).fill(0)
// we hold the stationIDs here
// StationIDs.fill(0)
let StationSNs = _py.range(10).fill(0)
// we hold the station S/N here
// StationSNs.fill(0)
let StationData = _py.range(10).fill(0)
// for each station we keep the last sent data
// StationData.fill(0)
let RSSIv = control.createBuffer(10)
// statistics from the client stations (ID > 0) values -120 ~ -40
RSSIv.fill(0)
let RSSIfromServer = -120
// the RSSI value from the last message from server
let SensorData = control.createBuffer(18)
SensorData.fill(0)
basic.showNumber(stationID)
basic.clearScreen()
radio.setGroup(77)
radio.setTransmitPower(7)
//  send SYNC signals to stations
//  so they can calculate succes/failure statistics
//  end if stationID
input.onButtonPressed(Button.AB, function on_button_pressed_ab() {
    let i: number;
    
    if (stationID == 0) {
        // Can send calibration signals only if repeater or pc station
        //  ---- START CALIBRATION ----
        //  90 calibration messages imply success rate 0.99, packet loss 0.95
        //  RESET the station counters first
        for (i = 0; i < 100; i++) {
            radio.sendValue("RSTSYNC", i)
            basic.pause(50)
        }
        for (i = 0; i < 100; i++) {
            radio.sendValue("SYNC100", i)
            basic.pause(50)
        }
        for (i = 0; i < 100; i++) {
            radio.sendValue("ENDSYNC", 0)
            basic.pause(50)
        }
    }
    
})
radio.onReceivedValue(function on_received_value(name: string, value: number) {
    let statID: number;
    // executed by clients stationID > 0
    
    RSSIfromServer = radio.receivedPacket(RadioPacketProperty.SignalStrength)
    if (name == "RSTSYNC") {
        
    } else if (name == "SYNC100") {
        
    } else if (name == "ENDSYNC") {
        
    } else if (name.slice(0, 6) == "DATARQ") {
        statID = parseInt(name.slice(6, 8))
        //  the last 2 digits are the station ID that must send data
        statID = Math.constrain(statID, 0, 9)
        if (statID == stationID) {
            sendData()
        }
        
    }
    
})
function sendData() {
    
    SensorData[0] = stationID
    //  first byte is the current stationID
    SensorData[1] = input.compassHeading()
    SensorData[2] = input.temperature()
    SensorData[3] = input.rotation(Rotation.Pitch)
    SensorData[4] = input.rotation(Rotation.Roll)
    SensorData[5] = input.lightLevel()
    
}

// ------------------- SETUP -----------------------
// change the transmitter ID. Up to 9 transmitters
input.onButtonPressed(Button.A, function on_button_pressed_a() {
    
    stationID = (stationID + 1) % 10
    basic.showNumber(stationID)
    basic.clearScreen()
})
// show the transmitter ID.
input.onButtonPressed(Button.B, function on_button_pressed_b() {
    
    basic.showNumber(stationID)
    basic.clearScreen()
})
// --------------- END OF SETUP FUNCTIONS ----------
function triesN(y: number, p: number): number {
    return Math.ceil(Math.log(1 - y) / Math.log(p))
}

function lossP(y: number, n: number): number {
    return Math.pow(1 - y, 1 / n)
}

function triesFromRSSI(rssi: any, y: number, maxtries: number): number {
    let t: number;
    let rssi2 = rssi + 100
    let p = Math.min(1, 5936.2673 * rssi2 ** -3.7231)
    //  this function may return a p > 1
    //  so we limit it to 1
    if (p == 1) {
        t = maxtries
    } else {
        t = Math.max(1, triesN(y, p))
    }
    
    // if tries fall below 1, at least 1 try
    return t
}

// print(triesFromRSSI(-85,0.9,20))
// print(triesFromRSSI(-85,0.95,20))
// print(triesFromRSSI(-95,0.95,20))
// print(str(control.device_serial_number() ^ 0xFFFFFFFF ))
// print(str(StationSNs.join()))
// k = "hello"
// print(k[0:3])
for (let i = 0; i < 100; i++) {
    console.log(input.rotation(Rotation.Pitch))
    console.log(input.rotation(Rotation.Roll))
    basic.pause(1000)
}
