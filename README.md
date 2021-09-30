# Disabling Intel ME on Dell Laptop

## Whats is intel ME ?

- [Intel Management Engine](https://en.wikipedia.org/wiki/Intel_Management_Engine) is an autonomous coprocessor which is integrated in all Intel CPUs created after 2006.
- It aims at accessing and controlling the PC over a network even when the main processor is switched off.
- It runs at ring -3, completely out of the reach of the OS or other low level processes. It is completely independent of the controls of the main CPU.
- It has all memory and network access without the knowledge of the main processor.
- It's active even when the system is switched off or hibernating.
- It allows the sysadmins to take controls of the computer even when it's switched off, remotely over a network. It allows the company (Intel) and other authorized people to track and access your PC (probably when it's stolen or it's being misused). But, possible [vulnerabilities](https://en.wikipedia.org/wiki/Intel_Management_Engine#Security_vulnerabilities) in it's system may allow unauthorized/attackers to [gain access](docs/How-To-Hack-A-Turned-Off-Computer-Or-Running-Unsigned-Code-In-Intel-Management-Engine.pdf) to it and grab a full control of your computer.
- It shares it's flash with the BIOS.
- The main Processor won't start if the ME is not working or broken, ME is required to start the system.

[More Info](docs/Rootkit_in_your_laptop.pdf)

## Can we disable it ?

Yes, it is now possible to disable intel ME, thanks to [NSA](docs/HAP-Challenges.pdf) and [Positive Technologies](https://www.ptsecurity.com/). On request of NSA, Intel has provided a [kill switch](https://github.com/corna/me_cleaner/wiki/HAP-AltMeDisable-bit) to safely disable ME, as it may cause various security issues, which was explored by security researchers at Positive Technologies and now even we can disable ME.
Thankfully, Nicola Corna has developed a script [me_cleaner](https://github.com/corna/me_cleaner) to ease our work of modifying and making the changes in the BIOS firmware.

[Read more](http://blog.ptsecurity.com/2017/08/disabling-intel-me.html)

## How to disable it ?

Currently, There are three ways to disable it:

- Some new Dell Laptops have an option to disable ME in in their UEFI settings.
- Enable the **HAP** (Intel ME >= 11) or the **AltMeDisable** (Intel ME <= 11) bit in the flash descriptor of the BIOS firmware.
- Removing the non-fundamental partitions and modules of the ME firmware.

[Read more](https://github.com/corna/me_cleaner/wiki/HAP-AltMeDisable-bit)

**This guide would tell you how I disabled ME through External Flashing with modified OEM firmware on my Dell Inspiron 15 5577 gaming laptop and other similar laptops.**

## Steps to Disable ME on Dell Inspiron 15 5577 Gaming

### Important!

**WARNING**
> **The process involved will require re-flashing your system's BIOS-chip firmware image, and will almost certainly void your system warranty. It may result in your machine becoming 'bricked'. On some (though not many) PCs, the ME is used to initialize or manage certain system peripherals and/or provide silicon workarounds — if that is the case on your target machine, you may lose functionality by disabling it. Although the most reliable method, external flashing does require you to open the case of your PC, an action that by itself is likely to void the warranty on non-desktop systems. Always observe proper [ESD protective measures](https://www.computerhope.com/esd.htm) when working with exposed system boards, and ensure that you have all external power sources and batteries removed. Backup any important files before proceeding. Read all instructions carefully and proceed only if you are comfortable, and at your own risk. Do it completely at your own risk, I don't provide warranty of any kind and neither I'm responsible for any damage or losses.**

Before proceeding further, I'd recommend to read these pages which I followed to understand the process,

- [Get the status of Intel ME](https://github.com/corna/me_cleaner/wiki/Get-the-status-of-Intel-ME) (To check the current status of ME before changing anything)
- [How does it work ?](https://github.com/corna/me_cleaner/wiki/How-does-it-work%3F) (Basic knowledge of what's being done)
- [Nicola Corna's Guide to external flashing](https://github.com/corna/me_cleaner/wiki/External-flashing) (Generic steps through external flashing)
- [Gentoo Wiki's great detailed guide for external flashing](https://wiki.gentoo.org/wiki/Sakaki%27s_EFI_Install_Guide/Disabling_the_Intel_Management_Engine)* (The best step by step guide for this process which I followed)

### Short Description

So, What actually we are going to do? What are the steps?
In short, we're going to read the BIOS firmware from the BIOS Flash IC on the motherboard into a file, we'll then verify the firmware read into the file. Then, we'll use [me_cleaner](https://github.com/corna/me_cleaner) to check the status of Intel ME in the firmware and disable it using either of the two last methods (See [How to disable it ?](#how-to-disable-it-)) and write the modified firmware into a file. And, then we'll flash (write) the modified firmware with disabled ME back into the BIOS IC.

So, The entire process can be divided into the following steps:

 - Check the current status of Intel ME along with the information on presence of [Intel Boot Guard](https://en.wikipedia.org/wiki/Intel_vPro#Intel_Boot_Guard)
 - Set up a Raspberry Pi 2/3/4 to be used as a SPI flash programmer
 - Disassemble the laptop and find the BIOS flash IC
 - Setup the connections between BIOS flash IC and Raspberry Pi
 - Read and verify the firmware from the BIOS flash chip
 - Disable the Intel ME into the firmware image file and produce a modified image file
 - Flash the modified firmware image back into the flash chip
 - Reassemble the laptop
 - Recheck the status of Intel ME
 
**It is recommended to go through the [Gentoo wiki](https://wiki.gentoo.org/wiki/Sakaki%27s_EFI_Install_Guide/Disabling_the_Intel_Management_Engine)* as it is the more detailed procedure, which guided me along with every precautions and safety to successfully perform this process.**

### Things Required

- SOIC-8 SOP-8 flash clip, to attach it to the 8 pins of the BIOS flash chip to access its contents
![SOIC8 clip](imgs/clip.jpg)
- Raspberry PI 2/3/4 (with it's official power adapter), to use it as a SPI flash programmer
![Raspberry Pi 4B](imgs/rpi.jpg)
- WiFi router or WiFi hotspot, to connect Raspberry PI when it boots (Optional, if running Raspberry PI headless i.e without a display)
- 8GB microSD card to boot Arch Linux ARM on Raspberry PI
- An empty 8GB(or more) USB flash drive, the pen drive needs to empty as all the data will be lost during the process (Optional, for windows users only to boot a live kali linux image)
- 8 female to female jumper wires
- Tools to help in disassembly/assembly of the laptop
- A working internet connection
- Another device(laptop/desktop/tablet/smartphone) which can aid you reading the guides, pdfs, text files and lets you run a ssh client if you're going to run the Raspberry Pi headless.

### Step 1: Check Intel ME status

####  For Windows Users

- Download a latest version of [Kali linux](https://www.kali.org/downloads/) because it has all essential tools like git, gcc, make, etc pre-installed in the live image, which are required to proceed further.
- Use [Rufus](https://rufus.ie/) or [Yumi](https://www.pendrivelinux.com/yumi-multiboot-usb-creator/)  or [Eatcher](https://www.balena.io/etcher/) to install kali iso on a 8GB pen drive.
- After Kali is installed on the pen drive, reboot and boot Kali from the pen drive, add the kernel parameter `iomem=relaxed` into grub entry 'Live' before booting Kali. (To add the kernel parameter: When the screen shows the list of booting options, highlight 'Live' option and press 'e' then add the parameter `iomem=relaxed` at the end of line starting with 'linux' and press F10 to boot )
- Connect Kali to your wifi router / hotspot to get access to the internet.
- Right click on Kali desktop and click on 'open terminal' to open a terminal.
- Run `apt update && apt-get install libpci-dev zlib1g-dev` to install the remaining required packages on Kali.
- Now, follow the steps of **Linux** section.

####  For Linux Users

- Reboot adding `iomem=relaxed` in the kernel parameters (Not for those who did already using Kali above)
- Install `git`,`gcc`,`make` and development files (header files) for **pciutils** and **zlib**, if not already installed according to your distribution (Kali users skip this)
- Now open the terminal, and execute these to clone the **coreboot** git repository, compile **intelmetool** to check for Intel ME status:
```bash
git clone --depth=1 https://review.coreboot.org/coreboot
cd coreboot/util/intelmetool
make
sudo modprobe msr
sudo ./intelmetool -mb
```
The last command shows the status of Intel ME along with Intel Boot Guard.
If the line `Current Working State: Normal` shows 'Normal' then Intel ME is present and active.
To save the status execute :
```bash
sudo ./intelmetool -mb > mestatus-1.log
```
(_See [output](/logs/mestatus-before.log)_) 

If the line `ME Capability: BootGuard: ON` shows **ON** then Intel Boot Guard is on and we can't remove and destroy ME modules but we can disable ME by just setting HAP-bit. 
**Remember, If Intel Boot Guard is ON, changing anything else in the firmware may lead to system being unbootable which can not be reversed.**

- Save the `mestatus-1.log` file safely to the device other than this PC
- Don't close the terminals, and proceed to the next step for setting up Raspberry Pi as a SPI programmer
[More Info](https://github.com/corna/me_cleaner/wiki/Get-the-status-of-Intel-ME)

### Step 2: Setup the Raspberry Pi as a SPI programmer

I've used Raspberry PI 4B for my setup but you may use any Raspberry PI (2|3|4), you just need to install a linux operating system with SPI devices enabled. 
Here, we're installing [Arch Linux ARM](https://archlinuxarm.org/) for our purpose.

- Get a root shell and execute the other steps as a root user, you may use the following command to get a root shell.
```bash
sudo bash
```
And, follow the steps to install Arch Linux ARM for your Raspberry Pi board till step 6 (i.e stop just before unmounting the boot and root partitions) : [Raspberry Pi 2](https://archlinuxarm.org/platforms/armv7/broadcom/raspberry-pi-2) [Raspberry Pi 3](https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-3) [Raspberry Pi 4](https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-4) 

- Just after 6th step (i.e before unmounting the boot and root partitions) while installing Arch Linux ARM, append the line `device_tree_param=spi=on` into the file `boot/config.txt`, this would enable the SPI interface for devices on the Raspberry PI,
```bash
echo 'device_tree_param=spi=on' >> boot/config.txt
```

- After the above step, if you want to run the Raspberry Pi headless (i.e without a display), you'd need to make the Raspberry Pi automatically connect to your wifi hotspot on every boot. If not running headless, you may skip this step.

Create a file `root/etc/wpa_supplicant/wpa_supplicant-wlan0.conf` by the following, replace _SSID_ with your Hotspot's SSID and _PASSWORD_ with your wifi password:
```bash
wpa_passphrase "SSID" "PASSWORD" > root/etc/wpa_supplicant/wpa_supplicant-wlan0.conf
```
Then, enable the systemd services for auto connecting your Raspberry Pi to the wifi hotspot when it boots,
```bash
ln -svf /usr/lib/systemd/system/wpa_supplicant@.service root/etc/systemd/system/multi-user.target.wants/wpa_supplicant@wlan0.service
ln -svf /usr/lib/systemd/system/dhcpcd@.service root/etc/systemd/system/multi-user.target.wants/dhcpcd@wlan0.service
```

- The Raspberry lacks an inbuilt RTC module to keep track of the current time when it's powered off. So, we'd need to update it's system time to the current date and time in order to make it able to access the internet without issues.

To solve the issue, we'll add a few static ip addresses of NTP servers. Adding hostnames of the NTP servers instead of their static ip addresses would cause an issue in the DNS resolution of the given hostnames of the NTP servers, as the system time is already misconfigured to make requests to the DNS servers. That's why, it's important to add static ip addresses only. Here, these are the google's ntp servers, you may use any other server(s).
```bash
echo "FallbackNTP=216.239.35.0 216.239.35.4 216.239.35.8 216.239.35.12" >> root/etc/systemd/timesyncd.conf
```

- Now, you can return back to the respective Arch Linux ARM wiki page to continue with the 7th step and skip the part about connecting with ethernet. Instead, Turn ON your wifi hotspot before booting Raspberry Pi, and make sure to give internet access through the hotspot (if running headless). 

**Note: Use the official Raspberry Pi adapter to power the pi. Using an insufficient power supply will result in random, inexplicable errors and filesystem corruption.**

- Boot your Raspberry Pi using a sufficient power supply and login to it's root shell. If running it headless, you'll need to find the ip address of the Raspberry Pi over the hotspot  network and login to it's ssh shell and get a root shell access instead.
**If you've got a monitor connected to the Raspberry PI, you're easy to go and you must skip the stuffs about ssh and move to the next step.**

Looking for the ip address of the Raspberry Pi over your wifi network can be a tedious job. If you use a wifi router then you can easily go to the router settings page through your browser and login to see the connected clients and find out the ip address of the hostname _alarmpi_.

However, if you have used other methods (like a smartphone's wifi hotspot) then you can install **nmap** on your linux distro to find out the ip addresses of clients connected to the wifi hotspot (Kali users already have nmap installed).
First know your own ip address on the wifi by executing,
```bash
ip addr
```
This will list all the network interfaces, the interface name starting with _wlan_ or _wlp_ name is wifi interface and the ip address after the word _inet_ is what we're looking for (ex: 192.168.0.142/24).
Now we'll use this ip address to probe other devices connected to the network. Just by replacing the last byte of the address with 0 (ex: 192.168.0.142/24 to 192.168.0.0/24) and probing using nmap will fetch the list of connected devices. 
```bash
nmap -sn 192.168.0.0/24
```
Now, if you've connected just your laptop and Raspberry Pi to the wifi network, then the ip address other than your laptop's ip address in the output of nmap is the ip address of the Raspberry Pi.
If there are many devices connected on the network, then you can power off the Pi and probe using `nmap` and then power on and again probe using nmap, then simply compare the changes in the output of nmap to find out the ip address of the Pi.

Now, you can login to the Raspberry Pi through ssh. (install **openssh** if you don't have ssh client installed) 
For example, if you've got the Raspberry Pi's ip address as `192.168.0.184`, then you may login to it's ssh by executing,
```bash
ssh alarm@192.168.0.184
```

- Use the password **alarm** when prompted for password while logging into the Raspberry Pi over ssh or into the user _alarm_. Then, login to the _root_ shell and use the password **root** when prompted for root user's password while logging into the Raspberry Pi.
```bash
su --login root
```

- After logging in as root user, initialize the pacman keyring, populate the Arch Linux ARM package signing keys and update the arch linux & install the required packages, 
```bash
pacman-key --init
pacman-key --populate archlinuxarm
pacman -Syu
pacman -S python python-setuptools python-pip flashrom wget git base-devel
pip install RPi.GPIO
exit
```
To check if raspberry shows SPI devices execute `ls /dev/spidev*`, if the out says **No such file or directory**, then SPI devices is not yet enabled, check if `/boot/config.txt` contains the line `device_tree_param=spi=on`. Or else, everything is setup and ready, and you're good to go.

- Now, you can execute `exit` and get exit from the ssh shell.

### Step 3: Disassemble the Laptop

Make proper backup of all your important files before opening your laptop. Disconnect and remove the external power cables (and we've even got to remove the batteries after opening the laptop case as per in the service manual) and all other devices connected to the laptop.

Look for Dell's official service manual guide for your dell laptop and follow the steps carefully till "Remove the System Board", following all the prerequisites with proper care. You may also download the service manual for Inspiron 15 5577 [here](docs/inspiron-15-5577-gaming-laptop_service-manual_en-us.pdf) .
If you aren't able to find the service manual, you can watch disassembly videos for your model on youtube and may take a risk to follow their instructions.
Make sure to disconnect the batteries and CMOS cell from the motherboard while performing the disassembly.

**Important Tips**

1. Handle the screws with care while unscrewing or screwing them and after they're removed. You may land into a trouble if they get stripped while screwing or unscrewing or if they get lost or mixed with other screws of different type. (If any screw gets stripped or worn while trying to unscrew, you may use a proper T4 to T10 type screwdriver to get a grip into the worn pit of the screw to force rotate and unscrew)
1. Take proper care to prevent [ESD](https://www.computerhope.com/esd.htm) while disassembling the inner parts of the laptop, as electrostatic discharges may damage the inner components.
1. Make sure to place the removed components and the motherboard on a clean and safe place.
1. Handle the boards and components by their edges, avoid touching the components by hands.
 
### Step 4: Setup the Connections

- Now, you've got the motherboard. We'll have to locate the BIOS flash IC. One of the ways to find this chip is to look at how it looks like on the board and then use a magnifying glass or a magnifier app on the smartphone to find all such ICs on the board, taking down the model numbers and other texts on them. Then, you can just google the texts for each IC to know if they're a flash chip and if they're used as a BIOS flash chip. For Dell Inspiron 15 5577 the BIOS chip was a SOIC-8 chip 'Winbond 25Q32JVSIQ' as shown in the figure.

![bioschip](imgs/bioschip.jpg)

- Now, when you've got the exact BIOS flash chip manufacturer's name and the model. We must find out the datasheet to get the complete details about the chip. Google IC's manufacturer's name and themodel number to get the datasheet for the IC. For 'Winbond 25Q32JVSIQ' the datasheet can be downloaded from [here](docs/w25q32jv-spi-revc-08302016.pdf).
- Look carefully in the datasheet, for pin configurations of SOIC type and input voltages. You may take time to read which pin does what if you want to make everything sure for your understanding. The circular dot or semi-circular cut on the ICs are used to mark which side is up. The numerical counting of the pins start from the top most left pin and ends at the bottom most right pin. The diagram shown below shows the 'Winbond 25Q32JVSIQ' IC pins and their numbers.

![IC diagram](imgs/ic.png)


| PIN | Pin Name | Description                                                                 |
|:---:|:--------:|-----------------------------------------------------------------------------|
| 1   | /CS      | Chip Select; Drive low to enable the device operations                      |
| 2   | DO(IO1)  | Data Output (Data Input Output 1); Data output from device for Standard SPI |
| 3   | IO2      | Data Input Output 2                                                         |
| 4   | GND      | Ground                                                                      |
| 5   | DI(IO0)  | Data Input (Data Input Output 0); Data input into device for Standard SPI   |
| 6   | CLK      | Serial Clock Input                                                          |
| 7   | IO3      | Data Input Output3                                                          |
| 8   | Vcc      | Power Supply                                                                |

**Mark the SOIC-8 flash chip test clip for the respective pin numbers of the IC to attach to, so that you don't get confused after wiring the clip with Raspberry Pi for which way to attach the clip and which side connects the top of IC.**

- The connections for SPI communication between the BIOS flash IC and the Raspberry Pi is as shown in the diagram. We'll have to use the SOIC-8 SOP-8 flash clip to connect the BIOS flash IC to the required Raspberry Pi SPI pins respectively. Connect the pins of the clip to the Raspberry Pi pins using female to female jumper wires accordingly. Identify all the pins on the IC through its datasheet and observe at the GPIO pin diagram for Raspberry Pi to locate the required pins for SPI communication, and connect the SOIC-8 clip pins with the Raspberry Pi GPIO pins as follows, so that it attaches to the correct pins on the IC after the clip is attached to the IC. The pin connection diagram between the BIOS flash IC and Raspberry Pi GPIO pins is shown here :

![Pin Diagram](imgs/pindiagram.png)

**WARNING :  Be very careful not to connect pins 2 or 4 on the RPi4's GPIO header to any pin of the IC clip - these are 5v (rather then 3.3v) and are likely to destroy your flash chip should you accidentally use them (See the datasheet to know about the appropriate input voltage).**


| SOIC-8 Flash IC Pin | PIN | Raspberry Pi GPIO Pin | PIN |
|:-------------------:|:---:|:---------------------:|:---:|
| Vcc                 | 8   | 3.3v                  | 17  |
| GND                 | 4   | Ground                | 25  |
| /CS                 | 1   | SPI0_CE0_N            | 24  |
| CLK                 | 6   | SPI_CLK               | 23  |
| DO                  | 2   | SPI_MISO              | 21  |
| DI                  | 5   | SPI_MOSI              | 19  |
| /WP (IO2)           | 3   | GPIO_GEN4             | 16  |
| /HOLD (IO3)         | 7   | GPIO_GEN5             | 18  |

**Note**: Don't attach the clip to the IC right now because it won't work as the Raspberry Pi is not ON and the pin modes are not yet set.

- If running headless, making sure your wifi router/hotspot is turned on, turn on the Raspberry P. It should automatically connect to the wifi while booting. If you've got a monitor attached to the raspberry pi, you're easy to go, you can just login. 

However, if you don't have a monitor and you're running the Raspberry PI headless, then we can access the Raspberry Pi's shell through ssh. If you've another PC or MAC, you can connect it to the same wifi and use an appropriate ssh client for the operating system to connect to the Raspberry Pi.

If you don't have another PC but you've an android smartphone or tablet, you can still access the Raspberry Pi through ssh. Connect the phone/tablet to the same wifi network (if your wifi hotspot is from the same phone/tablet, you're already on the same network) just install the [Termux](https://github.com/termux/termux-app) app from the the [F-Droid](https://f-droid.org/repository/browse/?fdid=com.termux) and install **openssh** and **nmap** packages on termux and connect to the Raspberry Pi using ssh. To install the packages **openssh** and **nmap** on termux,
```bash
pkg install openssh nmap
```
_Refer the 2nd step to probe Raspberry Pi's ip address and connect using ssh_

- Once you've got access to the Raspberry Pi's shell, get root login and make sure the internet works.
```bash
su --login root
ping -c 1 archlinux.org
```
- Now, We need to pull-up the GPIO pins 16 and 18 on the Raspberry Pi. I've created the following script for this purpose. However, you can do this using **wiringpi** package's **gpio** tool for Raspberry Pi Pi 2 or 3. But, **wiringpi**  fails for Pi 4 and its development seems to have stopped. Fortunately, the python library **RPi.GPIO**  works on all the three versions of Raspberry Pi. This is why, we've already installed **RPi.GPIO** in our arch linux installation in step 2 itself. I've made a short script to pull-up the GPIO pins 16 and 18 (GPIO 23 and 24) using **RPi.GPIO**, we just need to download an execute it,
```bash
wget https://raw.githubusercontent.com/darajnish/dell5577medisable/master/scripts/setup_gpio.py
python setup_gpio.py
```
It should output the current value read from the pins 23 and 24 be set to **1**, else something is wrong and you need to pull-up the pins by some other method and verify they're pulled up and then continue.

![Chip connected to Pi](imgs/chiptopi.jpg)

- Now, taking precautions to prevent [ESD](https://www.computerhope.com/esd.htm) and ensuring proper alignment of the clip with respect to the IC pins, carefully attach the IC clip to the IC.

![Clip seated on the IC](imgs/flashchipwithclip.jpg)

- Now, check if the BIOS chip is detected by **flashrom**. You may wish to change the value **spispeed** in the command below, according to the model of your BIOS chip and as per it's datasheet.
```bash
flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=8000
```
The output should be something like,
```
flashrom v1.1 on Linux 4.19.67-1-ARCH (armv7l)
flashrom is free software, get the source code at https://flashrom.org

Using clock_gettime for delay loops (clk_id: 1, resolution: 1ns).
Found Winbond flash chip "W25Q32.V" (4096 kB, SPI) on linux_spi.
No operations were specified.
```
( _See [output](/logs/identification.log)_ )

But, if you get `No EEPROM/flash device found` then recheck the connections and alignment of the clip with the IC; remove and reattach the IC clip over the IC and repeat the above command until it gets detected.

**WARNING: If flashrom reports that it has found a brand or make of chip that doesn't match what you expected, stop. Search online and only proceed if you are confident there is no ambiguity.**

### Step 5: Read and Verify Firmware

- Once the chip gets detected by **flashrom**, we can proceed further to read the firmware. Read the firmware image with **flashrom** using the following command (we'll read at least 3 copies),
```bash
flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=8000 -r original.rom
flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=8000 -r original2.rom
flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=8000 -r original3.rom
```
Output should be something like,
```
flashrom v1.1 on Linux 4.19.67-1-ARCH (armv7l)
flashrom is free software, get the source code at https://flashrom.org

Using clock_gettime for delay loops (clk_id: 1, resolution: 1ns).
Found Winbond flash chip "W25Q32.V" (4096 kB, SPI) on linux_spi.
Reading flash... done.
```
( _See [output](/logs/reading.log)_ )

- Now, we must verify if the read data is identical for all the three files. We can do so by checking the integrity of the read files using `md5sum`.
```bash
md5sum original*
```
> **WARNING: The hashes of the checksum of all the three should be identical. If any one of them is different then read the firmware again and again until the image files are identical. Make sure the IC clip is attached properly. You can reduce (adjust) the 'spispeed=' parameter value to what is given in the datasheet for your BIOS IC respectively. However, if you're still not able to read identical firmware data, PLEASE DO NOT PROCEED FURTHER UNTIL YOU'RE ABLE TO DO SO! Performing the 6th and 7th steps with such a dirty firmware image may result in a bricked system with your laptop unbootable, and there's no cure until you find a firmware image for your laptop's BIOS and correctly flash it again**

- Verify the structure of the firmware image using **ifdtool** from **coreboot**,
```bash
git clone --depth=1 https://review.coreboot.org/coreboot
cd coreboot/util/ifdtool
make
cd ../../..
./coreboot/util/ifdtool/ifdtool -d original.rom
```
You should get the output something like [this](/logs/ifdtoollog-original-rom.log) .

**WARNING: If ifdtool -d reports an error, or states that No Flash Descriptor found in this image, stop. Repeat the read process until you have the identical copies and this ifdtool -d check. PLEASE DO NOT PROCEED FURTHER UNTIL YOU'RE ABLE TO READ THE FIRMWARE CORRECTLY!**

Check if **me_cleaner**  tool understands this image,
```bash
git clone https://github.com/corna/me_cleaner
python me_cleaner/me_cleaner.py --check original.rom
```
See [output](/logs/me_cleaner-check.log).


- When the images read are identical, we can proceed to modify and disable Intel ME in the firmware file.

### Step 6: Modify the Firmware image

- You can disable Intel ME in two ways, you can choose either of these :
1. **soft-disable**:  It both removes the unneeded ME firmware and sets the **AltMeDisable/HAP** bit. **You can do this one only if you don't have Intel Boot Guard enabled.**
```bash
python me_cleaner/me_cleaner.py --soft-disable original.rom --output modified.rom
```
2. **soft-disable-only** (recommended): It sets the **AltMeDisable/HAP** bit only. **You must go for this if you've Intel Boot Guard enabled.**
```bash
python me_cleaner/me_cleaner.py --soft-disable-only original.rom --output modified.rom
```
See [output](/logs/me_cleaner-soft-disable-only.log) (for soft-disable-only)

- Now, check the modified image file using **me_cleaner**,
```bash
python me_cleaner/me_cleaner.py --check modified.rom
```
It shows `The HAP bit is SET` in the [output](/logs/me_cleaner-after-check.log).

- Make sure to keep a backup of `original.rom` file as it's the original firmware image of your BIOS, and it may be required later if the modified firmware causes some issue.

### Step 7: Write the modified Firmware

- Write the modified firmware into the BIOS flash IC using **flashrom**,
```bash
flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=8000 -w modified.rom
```
**flashrom** should show output something like,
```
flashrom v1.1 on Linux 4.19.67-1-ARCH (armv7l)
flashrom is free software, get the source code at https://flashrom.org

Using clock_gettime for delay loops (clk_id: 1, resolution: 1ns).
Found Winbond flash chip "W25Q32.V" (4096 kB, SPI) on linux_spi.
Reading old flash chip contents... done.
Erasing and writing flash chip... Erase/write done.
Verifying flash... VERIFIED.
```
( _See [output](/logs/writing.log)_ )

**WARNING: If flashrom reports an error here, or does not finish with the output `Verifying flash... VERIFIED`, stop. You almost surely have a corrupted flash. Try the write again, using a slower 'spispeed=' parameter, and if that also fails, try re-seating the IC clip on the IC.**

### Step 8: Reassemble the Laptop

If everything works without any error, then reassemble your laptop. Follow the procedure for "Replacing System Board" in the Dell Service manual. Power on the laptop. If it boots successfully, wait for 30 minutes to check if it auto shutdowns. 
If it doesn't auto shutdown and everything works fine then congratulations you've disabled Intel ME.
[Report](https://github.com/corna/me_cleaner/issues/3) your logs, system info and tell about problems you faced so that someone else may find it useful.

### Step 9: Recheck status of Intel ME

Follow Step 1 and check the status of ME again.
It should be disabled.

###  If Boot fails or the PC shuts down unexpectedly

**WARNING: If it fails to boot or shutdowns unexpectedly then we must revert the original firmware back into the BIOS flash chip. Disassemble the laptop again taking all safety precautions and write the file `original.rom` back into the BIOS flash chip**

- Disassemble the laptop again
- Setup the connections for IC clip and Raspberry Pi
- Attach the IC clip on the flash IC properly and write the original firmware image back into the IC
```bash
python setup_gpio.py
flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=8000 -w original.rom
```
- Now, reassemble the laptop and you'll get it back in the previous state, but with Intel ME enabled
- You can report about the problem [here](https://github.com/corna/me_cleaner/issues/new)

## Concluding

I hope this article helps anybody who is seeking information about Intel ME and the steps to disabling it. Feel Free to create an issue regarding any queries or doubt about any of the steps, and suggestions towards the improvement of this article are appreciated. I'm thankful to the Nicola Corna for me_cleaner and the basic wiki, and to Sakaki for Gentoo wiki* which guided me through the entire process.


* **Unfortunately the Gentoo Wiki by Sakaki is no more available :( so the links to the wiki in this guide doesn't work anymore**