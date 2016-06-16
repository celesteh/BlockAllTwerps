# BlockAllTwerps
A twitter bot to block people

Requires: tweepy, PIL


On a Raspberry pi:
==================
* `sudo apt-get install python-imaging-tk`
* `sudo pip install tweepy`
* `sudo pip install setproctitle`
* To make the mouse pointer vanish: `sudo apt-get install unclutter`
* In order to prevent the screen from dimming, you can install xscreensaver `sudo apt-get install xscreensaver` and use the GUI to disale dimming. Or else google for how to disable screen dimming

* Set the installation to start automatically on booting into the X server GUI:
  * Edit BlockAllTwerps.desktop so the path in it points to where you have put the files
  * Then move the file to ~/.config/autostart (you may need to make this directory)
  * [More information is here ] (https://www.raspberrypi.org/forums/viewtopic.php?f=26&t=18968)

* Set the installation to start automatically, headlessly:
  * Edit BlockAllTwerps.init.d so the path in it points to where you have put the files
  * `cp BlockAllTwerps.init.d /etc/init.d/BlockAllTwerps`

* If you install both of the above and boot into a GUI, it will run the installation
* If you want to change whether it runs headlessly or not `sudo raspi-config`

