# py_irc
Python infrared remote control utilities for Raspberry Pi

In the home theater, the devices (e.g. Bluray player, projector, monitor, amplifier, lighting, etc.) are usually controlled with infrared remote controls. The problem is that the operation of these devices is completely different. Each device is controlled with its own remote control. This turns the home theater into an uncomfortable, complex technical workplace until the movie is shown.

In order to optimize this situation, it is desirable to combine the individual operating procedures at the push of a button. e.g .:
 * Play the movie with the projector on the screen in a quiet sound mix
  * Configure the HDMI Matrix to connect the devices:
   * 4K Bluray Player
   * 4K HDMI to analog 7.1 extractor
   * Projector
  * Turn on the projector
  * Turn on the 4K Bluray Player
  * Enable 4K HDMI to analog 7.1 extractor
  * Switch on dynamic compressor for channels FL, FR, CENTER, SUBW
  * Switch on dynamic compressor for channels SL, SR, RL, RR
  * Switch 7 speakers and a subwoofer to the analog amplifier
  * Switch on analog amplifier 7.1
  * Adjust the volume accordingly depending on the time of day
  * Open the Bluray Player drive

![Infrared Remote control outside](https://github.com/michaelpaulkorthals/py_irc/blob/main/images/rpi_irc_1.png)

![Infrared Remote control inside](https://github.com/michaelpaulkorthals/py_irc/blob/main/images/rpi_irc_2.png)
