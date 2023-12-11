import nidaqmx

# Create a dictionary to map LED strip numbers to R, G, B pins
led_strip_pins = {
    0: ("Dev4/port1/line0", "Dev4/port1/line1", "Dev4/port1/line2"),  # LED strip 0
}

def control_led_strip(strip_number, r, g, b):
    if strip_number not in led_strip_pins:
        print("Invalid strip number.")
        return

    r_pin, g_pin, b_pin = led_strip_pins[strip_number]

    digital_output_channels = [r_pin, g_pin, b_pin]

    # Create a boolean pattern to control the transistors for the selected LED strip
    pattern = [int(r == 1), int(g == 1), int(b == 1)]

    # Create a digital output task and use a 'with' statement to automatically release resources
    with nidaqmx.Task() as task:
        for i, channel in enumerate(digital_output_channels):
            bit = pattern[i]
            task.do_channels.add_do_chan(channel)
        task.write([bool(bit) for bit in pattern])

    print(f"LED strip {strip_number}: R={r}, G={g}, B={b} controlled successfully.")

if __name__ == "__main__":
    # Example usage:
    strip_number = 0
    red_value = 0  # Set to 1 for on, 0 for off
    green_value = 0  # Set to 1 for on, 0 for off
    blue_value = 0   # Set to 1 for on, 0 for off
    control_led_strip(strip_number, red_value, green_value, blue_value)
