import serial
import threading
import time

PhotoElectricState = True
SlotCounter = 0
apple_list = []
last_apple = (0, "", 0)
sensor_bool = False
lock = threading.Lock()  # To synchronize access to shared variables

def continuous_sensor_update(serial_port):
    global PhotoElectricState, SlotCounter, sensor_bool
    with serial.Serial(serial_port, 9600) as ser:
        try:
            while True:
                ser.write(b'REQUEST_SENSOR\n')  # Send a command to request the sensor value
                data = ser.readline().decode('utf-8').strip()

                component, value = data.split(',')

                if component == "SENSOR":
                    with lock:
                        sensor_bool = bool(value)
                        if sensor_bool:
                            if PhotoElectricState:
                                PhotoElectricState = False
                            else:
                                PhotoElectricState = True
                                SlotCounter += 1

                time.sleep(1)  # Adjust sleep duration as needed

        except Exception as e:
            print(f"Error in continuous sensor update thread: {e}")

def get_sensor_value(apple_type, diameter):
    global PhotoElectricState, SlotCounter, last_apple, apple_list, sensor_bool
    with lock:
        SlotCounter, PhotoElectricState, sensor_bool = SlotCounter, PhotoElectricState, sensor_bool

    if last_apple[0] == SlotCounter:  # if the apple is in the same slot
        if last_apple[1] == apple_type:
            diameter = (diameter + last_apple[3]) / 2  # perform the average of the diameters (probably it is the same apple)
        else:
            apple_list.append(last_apple)  # append if the type is different in the same slot (to deal later)
    else:
        apple_list.append(last_apple)  # always append the previous apple when it changes slot

    last_apple = (SlotCounter, apple_type, diameter)
    return SlotCounter, PhotoElectricState, sensor_bool

def print_sensor_value():
    global sensor_bool
    while True:
        with lock:
            print(f"Sensor Value: {sensor_bool}")
        time.sleep(1)

def get_apple_data():
    global SlotCounter, apple_list
    with lock:
        return SlotCounter, list(apple_list)
    
def reset_apple_list():
    global apple_list
    apple_list = []

def reset_slot_count():
    global apple_list
    SlotCounter = 0

def sendlist_to_next_machine():
    pass
    # Code to send the list

if __name__ == '__main__':
    microcontroller_port = 'COM10'  # Replace 'COMX' with the appropriate serial port
    sensor_thread = threading.Thread(target=continuous_sensor_update, args=(microcontroller_port,))
    sensor_thread.daemon = True
    sensor_thread.start()

    print_thread = threading.Thread(target=print_sensor_value)
    print_thread.daemon = True
    print_thread.start()

    while True:
        pass
