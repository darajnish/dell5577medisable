# Disabling Intel ME on Dell Laptop

## Whats is intel ME ?

- [Intel Management Engine](https://en.wikipedia.org/wiki/Intel_Management_Engine) is an autonomous coprocessor which is integrated in all Intel CPUs created after 2006.
- It aims at accessing and controlling the PC over a network even when the main processor is switched off.
- It runs at ring -3 , completely out of the reach of the OS. It is completly independent of the controls of the main CPU.
- It has all memory and network access without the knowledge of the main processor.
- It's active even when the system is switched off or hibernating.
- It allows the sysadmins to take controls of the computer even when it's switched off, remotely over a network. It allows the company (Intel) and other authorized people to track and access your PC (probably when it's stolen or it's being misused). But, possible [vulnerablities](https://en.wikipedia.org/wiki/Intel_Management_Engine#Security_vulnerabilities) in it's system may allow unauthorised/attackers to [gain access](#) to it and grab a full control of the computer.
- It shares it's flash with the BIOS.
- The main Processor won't start if the ME is not working or broken, ME is required to start the system.

[More Info](https://github.com/corna/me_cleaner/wiki/How-does-it-work%3F)

## Can we disable it ?

Yes, it is now possible to disable intel ME, thanks to [NSA](#) and [Positive Technologies](http://blog.ptsecurity.com/2017/08/disabling-intel-me.html). On the request of NSA, Intel has provided a [kill switch](https://github.com/corna/me_cleaner/wiki/HAP-AltMeDisable-bit) to safely disable ME as it may cause various security issues, which was explored by security researchers at Positive Technologies and now even we can disable ME.
[Read more](http://blog.ptsecurity.com/2017/08/disabling-intel-me.html)

## How to disable it ?

Currently, There are three ways to disable it:

-  Some of the new Dell Laptops have an option to disable ME in in their UEFI settings.
- Enable the HAP (Intel ME >= 11) or the AltMeDisable (Intel ME < 11) bit in the flash descriptor of the BIOS firmware.
- Removing the non-fundamental partitions and modules of the ME firmware.
[know more](https://github.com/corna/me_cleaner/wiki/HAP-AltMeDisable-bit)

**This guide would tell you how I disabled ME through External Flashing with modified OEM firmware on my Dell Inspiron 15 5577 gaming laptop and other similar laptops. **

## Steps to Disable ME on Dell Inspiron 15 5577 Gaming

### Important!

The process involved will require re-flashing your system's BIOS-chip firmware image, and will almost certainly void your system warranty. It may result in your machine becoming 'bricked'. On some (though not many) PCs, the ME is used to initialize or manage certain system peripherals and/or provide silicon workarounds — if that is the case on your target machine, you may lose functionality by disabling it.

