import time
# import accelerometer modules
from pimoroni_i2c import PimoroniI2C
from pimoroni import PICO_EXPLORER_I2C_PINS
from breakout_msa301 import BreakoutMSA301

# import graphics and jpeg decoder
import picographics
import jpegdec

# NOTE - YOU MUST CREATE THE DISPLAY FIRST, BEFORE CONNECTING TO ACCELEROMETER
# Configure display on Pico Explorer Board
display = picographics.PicoGraphics(display=picographics.DISPLAY_PICO_EXPLORER)
j = jpegdec.JPEG(display) # jpeg decoder
default_img = "lofi.jpeg" # default picture when no alarm is present
alarm_img = "home_alone.jpg" # alarm picture when movement is detected

# Create connection to accelerometer
i2c = PimoroniI2C(**PICO_EXPLORER_I2C_PINS)
msa = BreakoutMSA301(i2c)
# Configure accelerometer
part_id = msa.part_id()
print("Found MSA301 (accel). Part ID: 0x", '{:02x}'.format(part_id), sep="")
# msa.enable_interrupts(BreakoutMSA301.FREEFALL | BreakoutMSA301.ORIENTATION)
# print(dir(msa))

def update_image(alarm=False):
    fpath_img = alarm_img if alarm else default_img
    # Open the JPEG file
    j.open_file(fpath_img)
    # Decode the JPEG
    j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
    # Display the result
    display.update()

# gather data for calibration
time_to_gather_data = 5
start_time = time.time()

x_vals = []
y_vals = []
z_vals = []

print(f"Gathering data for {time_to_gather_data} seconds to perform calibration....")
while time.time() < (start_time + time_to_gather_data):
    x = msa.get_x_axis()
    y = msa.get_y_axis()
    z = msa.get_z_axis()
    
    x_vals.append(x)
    y_vals.append(y)
    z_vals.append(z)
    time.sleep(0.1)
    

def gather_stats(x_vals):
    "Return mean and std"
    x_mean = sum(x_vals) / len(x_vals)
    x_var = sum([((x - x_mean) ** 2) for x in x_vals]) / len(x_vals)
    return (x_mean, x_var ** 0.5)

def print_stats(stat, axis='X'):
    print(f"{axis}:\t{stat[0]:5.2f}\t{stat[1]:5.2f}")

c_stats = [gather_stats(num_list) for num_list in [x_vals, y_vals, z_vals]]

print("Finished calibration; means and standard deviation statistics")
print(f"  \t{'Mean':>5}\t{'Std':>5}")
print_stats(c_stats[0], 'X')
print_stats(c_stats[1], 'Y')
print_stats(c_stats[2], 'Z')
print("")


def out_of_range(val, mean, std, multiplier=3):
    return abs(val-mean) > (std * multiplier)

alarm = False
alarm_time = None
alarm_reset_time = 5 # seconds

update_image(alarm)
while True:
    # Alarm reset
    if alarm and time.time() > (alarm_time + alarm_reset_time):
        alarm = False
        update_image(alarm)
    
    # get data
    x = msa.get_x_axis()
    y = msa.get_y_axis()
    z = msa.get_z_axis()
    freefall = 1 # msa.read_interrupt(BreakoutMSA301.FREEFALL)
    orientation = 1 # msa.get_orientation()
    
    # check if there has been a bump and set alarm if not already set
    x_flag = out_of_range(x, *c_stats[0])
    y_flag = out_of_range(y, *c_stats[1])
    z_flag = out_of_range(z, *c_stats[2])
    
    current_alarm_flag = x_flag or y_flag or z_flag
    if not alarm and current_alarm_flag:
        alarm = True
        alarm_time = time.time()
        update_image(alarm)
    

    print("X:", x, end=",\t")
    print("Y:", y, end=",\t")
    print("Z:", z, end=",\t")
    print("Freefall?", freefall, end=",\t")
    print("Orientation:", orientation)
    
#     if alarm:
#         print("ALARM")
    
    time.sleep(0.1)
    
    
# Orientation
# 1 - Face Up
# 0 - Upside Down
# 2 - Standing up On Left Edge
# 3 - Standing up On Right Edge
