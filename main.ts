let stationID = 0
// 0=repeater/pc station, 1-9 = transmitter/sensor with ID
let RSSIv = control.createBuffer(10)
// statistics from the client stations (ID > 0) values -120 ~ -40
let RSSIfromServer = -120
// the RSSI value from the last message from server
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
    // executed by clients stationID > 0
    
    if (name == "RSTSYNC") {
        RSSIfromServer = radio.receivedPacket(RadioPacketProperty.SignalStrength)
    } else if (name == "SYNC100") {
        RSSIfromServer = radio.receivedPacket(RadioPacketProperty.SignalStrength)
    } else if (name == "ENDSYNC") {
        RSSIfromServer = radio.receivedPacket(RadioPacketProperty.SignalStrength)
    }
    
})
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
console.log("" + (control.deviceSerialNumber() ^ 0xFFFFFFFF))
