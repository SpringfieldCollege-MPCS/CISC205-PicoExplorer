import picographics
import jpegdec
import time
display = picographics.PicoGraphics(display=picographics.DISPLAY_PICO_EXPLORER)


fpath_img0 = "lofi.jpeg"
fpath_img1 = "home_alone.jpg"

for i in range(10):
    fpath_img = fpath_img0 if i % 2 == 0 else fpath_img1
  
    # Create a new JPEG decoder for our PicoGraphics
    j = jpegdec.JPEG(display)
    # Open the JPEG file
    j.open_file(fpath_img)

    # Decode the JPEG
    j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)

    # Display the result
    display.update()
    time.sleep(2)
