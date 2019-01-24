GNU System Monitor


This is a qt app written in Python3 designed to be a more comprehensive system monitor than the one's offered by Gnome or KDE desktop. When the software is complete it will have all the functionality 
of a standard system monitor as well as the options to overclock your gpu and set fan curves for your gpu. The last feature added will be the network monitor as well as a builtin net limiter
as well as preventing apps from accessing the internet.



![Image of Processes Page](https://github.com/fredwntr1/gnu-system-monitor/blob/master/processes.png)

![Image of CPU Page](https://github.com/fredwntr1/gnu-system-monitor/blob/master/gnucpu.png)



Currently only Nvidia with the binary driver is supported.

![Image of GPU Page](https://github.com/fredwntr1/gnu-system-monitor/blob/master/gnugpu.png)


![Image of Net Page](https://github.com/fredwntr1/gnu-system-monitor/blob/master/gnunet.png)

Dependencies:
	python3-pyqt4
	python3-pip
	mesa-utils
	lm-sensors - (make sure to run sensors-detect)

Then cd into the folder and run 'pip3 install requirements.txt'


	

