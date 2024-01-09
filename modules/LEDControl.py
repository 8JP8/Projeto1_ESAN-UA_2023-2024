import serial #pip install pyserial
import time

def control_led_strip(port, led1_pwm, led2_pwm, led3_pwm):
    # Serial port configuration
    baud_rate = 9600

    # Function to send PWM values to MSP430
    def set_pwm(led, pwm_value):
        command = f"{led},{pwm_value}\n"
        ser.write(command.encode())
        #time.sleep(0.01)  # Add a delay to allow the MSP430 to process the command

    # Connect to the specified serial port
    ser = serial.Serial(port, baud_rate, timeout=1)

    # Set PWM values for each LED
    set_pwm("LED1", led1_pwm)
    set_pwm("LED2", led2_pwm)
    set_pwm("LED3", led3_pwm)

    # Close the serial port
    ser.close()


if __name__ == '__main__':
    # Example usage:
    port_name = "COM10"  # Replace 'xx' with the correct COM port number
    led1_pwm_value = 255
    led2_pwm_value = 255
    led3_pwm_value = 255

    # Call the control_led_strip function
    control_led_strip(port_name, led1_pwm_value, led2_pwm_value, led3_pwm_value)