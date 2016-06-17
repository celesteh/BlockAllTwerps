# BlockAllTwerps
A twitter bot to block people

Requires: tweepy, PIL, setproctitle


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
  * Make script executable `sudo chmod 755 /etc/init.d/BlockAllTwerps`
  * Test starting the program `sudo /etc/init.d/BlockAllTwerps start`
  * Test stopping the program `sudo /etc/init.d/BlockAllTwerps stop`
  * To register your script to be run at start-up and shutdown, `sudo update-rc.d BlockAllTwerps defaults`
  * If you ever want to remove the script from start-up, `sudo update-rc.d -f BlockAllTwerps remove`

* If you install both of the above and boot into a GUI, it will run the installation
* If you want to change whether it runs headlessly or not `sudo raspi-config`
* If the network requires alogin via a web page, you will need to install lynx

