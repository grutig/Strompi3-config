# Strompi3-config
boot time configuration script for Joy-it strompi3

Strom-Pi3 is a Raspberry Pi UPS Hat that can be used to shutdown the RPi if the primary power fails.
The supplied software, however, lacks a module to automatically configure the hat at boot, and is also written (but this is a personal consideration) in a rather chaotic way.
So I wrote this script, which configures the functional parameters in an automatic and repetitive way.
The configuration parameters are those used to use the hat as an UPS that initiate a system shutdown after a predefines amount of time in the event of a power failure.
To keep in mind that the Stompi3 simply sends predefined strings over the serial channel when the power fails and comes back: the shutdown process must be triggered by a separate daemon script (shutd.py) that runs in background.
The configuration can be easily adapted to other uses just editing the 'setconfig' lines at the end of the script.
The settable values are identified by an index, the ones relative at firmware version 1.72c are listed in the index.txt file

A note about the serial channel.
The serial channel of Stromp PI3 is set to 38kBaud, which is a value too high to be managed by the miniUART of RPIs 3 and 4.
It would have been more logical, in my opinion, to use a lower and manageable speed by miniUART, given the modest data flow over that interface.
To work at 38kBaud it is necessary to switch the full UART (ttyAMA0) from the bluetooth module to the GPIO channel, as noted in script comments. 
