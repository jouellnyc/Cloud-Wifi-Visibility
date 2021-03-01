#### Cloud Wifi Visibility 

Recently I was looking to upgrade my security posture on my home Wi-Fi network. Historically it has been very difficult for me to gain full visibility on all of the devices traffic on my network. Using a Linux ethernet bridge in front of the Wifi router  I was able to see all the outgoing packets, but I wasn't able to identify precisely from which device it had come from easily - mainly because of the fact the wireless router device was doing NAT and the IDS/Linux Bridgle only saw the external IP of the Router. This can get really complicated/maybe impossible based on what the manufacturer allows customer to do in terms of configuration -- and there could be many waysto achieve it. This is a medium tolow cost solution that worked to hit my requirements of full device visibilty.

In this case I am using Tp-Link AX50. With a couple of tweaks --  I was able to see all of the traffic, send it to the cloud, and setup an IDSon all the traffic. In addition some other service were setup but for now the main piece is focusing on the overall visibility.


First here’s a picture of my final config:
![Final Config](final_config.png)

Let's see how it looks in Loggly:
![Loggly](loggly.png)


What's important to keep in mind here is that you can see that there are various internal Source IP addresses -- they are all different --  those represent different devices on my local lan.  Without this setup they would all be the external IP of the Wifi/Router as assigned by the ISP -- because that's what Surciata 'sees'.  Now -- on rasberry pi A -- Suricata sees the traffic before it is NAT'ed -- so the internal IPs are preserved/sent to loggly, and then NAT'edL

![NAT'ed Client](loggly2.png)

## What is the main key configuration that allows the visiblity to happen?
If you refer to the diagram you can see that the wan port of the Tp-Link AX50 is not used. We are completely bypassing the device's ability touse NAT (and all its fancy QoS and magic anti-virus features) and simply using it's Wi-Fi capabilities and its ethernet switch capabilities. Considering that CPU of the device is significantly upgraded (dual core), it was worth it for me to do this. Also it is WiFi 6 capable so, has the future in mind. More Details here: https://dongknows.com/tp-link-archer-ax50-review/


## Requirements
Cloud Logger and Rasberry Pi
