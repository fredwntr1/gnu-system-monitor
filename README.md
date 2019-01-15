GNU System Monitor


This is a qt app written in Python3 designed to be a more comprehensive system monitor than the one's offered by Gnome or KDE desktop. When the software is complete it will have all the functionality 
of a standard system monitor as well as the options to overclock your gpu and set fan curves for your gpu and cpu. The last feature added will be the network monitor as well as a builtin net limiter
as well as preventing apps from accessing the internet.

So far the dependencies are just PyQt4 because it can't be installed through pip. All other deps are part of the virtual enviroment.


![Image of Processes Page](https://github.com/fredwntr1/gnu-system-monitor/processes.png)

![Image of CPU Page](https://github.com/fredwntr1/gnu-system-monitor/gnucpu.png)



Currently only Nvidia with the binary driver is supported as Python modules already exist for displaying gpu stats as well as overclocking, AMD cards will have to be written entirely using subprocess 
which will take some time.

![Image of GPU Page](https://github.com/fredwntr1/gnu-system-monitor/gnugpu.png)


![Image of Net Page](https://github.com/fredwntr1/gnu-system-monitor/gnunet.png)


