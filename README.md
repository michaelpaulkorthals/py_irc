# py_irc
Python infrared remote control utilities for Raspberry Pi

In the home theater, the devices (e.g. Bluray player, projector, monitor, amplifier, lights, etc.) are usually controlled with infrared remote controls. The problem is that the operation of these devices is completely different and separated. Each device is controlled with its own remote control. This turns the home theater into an uncomfortable, complex technical workplace until the movie is shown.

In order to optimize this situation, it is desirable to combine the individual operating procedures at the push of a button, e.g.:
 * Play the movie with the projector on the screen in a quiet sound mix
   * Configure the 4x4 4K HDMI Matrix to connect the devices:
     * Input: 4K Bluray Player
     * Output: 4K HDMI to analog 7.1 extractor
     * Output: Projector
   * Turn on the 4K projector
   * Turn on the 4K Bluray Player
   * Enable 4K HDMI to analog 7.1 extractor
   * Switch on dynamic compressor for channels FL, FR, CENTER, SUBW
   * Switch on dynamic compressor for channels SL, SR, RL, RR
   * Switch 7 speakers and a subwoofer line-out to the analog amplifier
   * Switch on analog amplifier 7.1
   * Adjust the sound volume accordingly depending on the time of day
   * Switch the subwoofer off
   * Open the Bluray Player drive
   * Switch off the lights or roll down the blinds depending on the time of day

This requires to build up and LAMP Server on a headless Raspberry Pi Zero W. This webserver will provide the website with that and further macro buttons on your mobile phone or tablet. 
In addition the Raspberry Pi Zero W must be extended by IR Receiver and Transmitter circuits and a 5 V power supply. 

The complete device could look like this:

![Infrared Remote control outside](https://github.com/michaelpaulkorthals/py_irc/blob/main/images/rpi_irc_1.png)

![Infrared Remote control inside](https://github.com/michaelpaulkorthals/py_irc/blob/main/images/rpi_irc_2.png)

This prototype I have successfully in operation in my home theatre since November 2020.

As an expierienced DIY home automation expert, you are capable to build this device easily and to have fun on a rainy weekend.

Please note:
The photo above shows an in-build switching power supply, which converts the power from 230V AC to 5V DC. This needs the skills of a licenced Ham Radio operator, electrician, electrical or electronic engineer. If you don't have these competences, you must replace this by an commercially available plug-in power supply for Raspberry Pi with a low voltage power cord to the device. Keep every time in mind that open voltages over 40 V (e.g. 110 V AC or 230 V AC from the power grid) could cause deadly injuries.

Study the [schematic diagrams](https://github.com/michaelpaulkorthals/py_irc/blob/main/irc_circuit/irc_circuit.pdf) and data sheets of my infrared remote control in the [irc_circuit folder](https://github.com/michaelpaulkorthals/py_irc/tree/main/irc_circuit).
May this help your to find a way to design your own device. In the event that you want to adapt the circuit to your own needs or capabilities, I have also stored the files of my ["KiCad"](https://www.kicad.org/) project there.

Software


