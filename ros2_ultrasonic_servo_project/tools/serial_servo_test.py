import time
import serial

PORT = "/dev/ttyUSB0"
BAUD = 115200

with serial.Serial(PORT, BAUD, timeout=0.2) as ser:
    print(f"Opened {PORT} at {BAUD} baud. Waiting for Arduino reset...")
    time.sleep(3)

    ser.write(b"S:90\n")
    ser.flush()
    print("Sent S:90")
    time.sleep(3)

    ser.write(b"S:0\n")
    ser.flush()
    print("Sent S:0")
    time.sleep(1)

    print("Reading distance samples for 3 seconds...")
    end = time.time() + 3
    while time.time() < end:
        line = ser.readline().decode(errors="ignore").strip()
        if line:
            print(line)
