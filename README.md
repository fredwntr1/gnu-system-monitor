#Complete System Monitor


This is a qt app written in Python3 designed to be a more comprehensive system monitor than the one's offered by Gnome or KDE desktop. When the software is complete it will have all the functionality 
of a standard system monitor as well as the options to overclock your gpu and set fan curves for your gpu. The last feature added will be the network monitor as well as a builtin net limiter
as well as preventing apps from accessing the internet.
Currently overclocking for Nvidia cards with the binary driver is supported but setting fan speeds 
and fan curve works for Nvidia and AMD with amdgpu-pro and open source kernel driver. <br/><br/> 
Dependencies:<br/>
    <ul><li>python3-pyqt4<br/>
	<li>mesa-utils <br/> 
	<li>lm-sensors - (make sure to run sensors-detect)  
</ul>

 <br/>

Then copy amdfc into your /bin folder, copy amdfc.service and amdst.service into /etc/systemd/system/ <br/>
Run "sudo systemctl enable amdfc.service" and "sudo systemctl enable amdst.service". Then start the serivces and that will be enough to run the fan control portion for AMD graphics cards.

<br/>
Then run "sudo -H python3 -m pip install -r requirements.txt"


![Image of Processes Page](https://github.com/fredwntr1/gnu-system-monitor/blob/master/processes.png)

![Image of CPU Page](https://github.com/fredwntr1/gnu-system-monitor/blob/master/gnucpu.png)




![Image of GPU Page](https://github.com/fredwntr1/gnu-system-monitor/blob/master/gnugpu.png)


![Image of Net Page](https://github.com/fredwntr1/gnu-system-monitor/blob/master/gnunet.png)




	

