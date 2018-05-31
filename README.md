# BlockAllTwerps
A twitter bot to block people

Requires: tweepy, PIL, setproctitle



## @BlockAllTwerps Installation Programme Notes

Twitter is awash with rubbish. Aside from annoying or uninteresting content, there is the intentionally bad: tweets that are deliberately abusive to other users. Such attacks are often coordinated, while the victims – who include a disproportionate number of women – are left to fend for themselves within Twitter's largely unmoderated platform.

Block All Twerps is a twitter bot that blocks everyone associated with tweets intended to incite harassment. The bot blocks a selected abusive tweet's original writer, any retweeter(s), and all followers of the writer/retweeters' accounts at the maximum speed allowed by the Twitter API.

Given that many abusive tweets are deliberately picked up and shared by hub accounts which effectively coordinate attacks and may have thousands of followers, it can take weeks to respond to an incident that might have unfolded in a single afternoon. One recent abusive tweet resulted in more than 50,000 accounts being blocked over a period of around two weeks.

The block bot is intended to highlight to the impossibility for normal users to effectively respond to coordinated harassment attacks online. It is also intentionally wholly symbolic – it blocks user from seeing the bot's feed itself instead of acting as a shield to a real person.


## @BlockAllTwerps physical presence:

A Raspberry Pi computer, optionally attached to a monitor or projector.

- With a monitor, it would show the tweet it was blocking and the user ID and icon image of accounts as it blocked them. Due to Twitter API rate limiting, it would show a count down when it was waiting to start blocking again.

- Without a monitor, this is an example of 'programme note art' where viewers depend on posted programme notes.



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

