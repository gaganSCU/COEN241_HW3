Gagan Gupta
Professor Choi
COEN 241: Cloud Computing
Homework 3: Mininet

---Task 1---
1. What is the output of “nodes” and “net”
mininet> nodes
available nodes are:
h1 h2 h3 h4 h5 h6 h7 h8 s1 s2 s3 s4 s5 s6 s7
2. What is the output of “h7 ifconfig”
mininet> h7 ifconfig
h7-eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.0.0.7  netmask 255.0.0.0  broadcast 10.255.255.255
        inet6 fe80::5c06:13ff:fe07:801d  prefixlen 64  scopeid 0x20<link>
        ether 5e:06:13:07:80:1d  txqueuelen 1000  (Ethernet)
        RX packets 209  bytes 23784 (23.7 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 9  bytes 726 (726.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

---Task 2---
1. Draw the function call graph of this controller. For example, once a packet comes to the
controller, which function is the first to be called, which one is the second, and so forth?
_handle_PacketIn() > act_like_hub() > resend_packet() > connection.send()

2. Have h1 ping h2, and h1 ping h8 for 100 times (e.g., h1 ping -c100 p2).
mininet>h1 ping -c100 h2
--- 10.0.0.2 ping statistics ---
100 packets transmitted, 100 received, 0% packet loss, time 99266ms
rtt min/avg/max/mdev = 0.745/1.270/3.170/0.253 ms
mininet>h1 ping -c100 h8
--- 10.0.0.8 ping statistics ---
100 packets transmitted, 100 received, 0% packet loss, time 99265ms
rtt min/avg/max/mdev = 3.616/4.902/11.168/1.123 ms

	a. How long does it take (on average) to ping for each case?
	mininet>h1 ping -c100 h2
	Average: 1.270 ms
	mininet>h1 ping -c100 h2
	Average: 4.902 ms

	b. What is the minimum and maximum ping you have observed?
	mininet>h1 ping -c100 h2
	Minimum: 0.745 ms
	Maximum: 3.170 ms
	mininet>h1 ping -c100 h8
	Minimum: 3.616 ms
	Maximum: 11.168 ms

	c. What is the difference, and why?
	mininet>h1 ping -c100 h2
	Difference: 2.435 ms
	mininet>h1 ping -c100 h8
	Difference: 7.552 ms
	-This difference in max and min a.k.a. range is directly proportional to the number of hops in the shortest route from h1 to h2 (h1>s3>h2 --> 2 hops) and h1 to h8 (h1>s3>s2>s1>s5>s7>h8 --> 6 hops)(3x the hops and therefore about 3x the range).

3. Run “iperf h1 h2” and “iperf h1 h8”
-iperf h1 h2
*** Iperf: testing TCP bandwidth between h1 and h2 
*** Results: ['15.8 Mbits/sec', '19.7 Mbits/sec']
-iperf h1 h8
*** Iperf: testing TCP bandwidth between h1 and h8 
*** Results: ['5.34 Mbits/sec', '5.97 Mbits/sec']

	a. What is “iperf” used for?
	-iperf is used to test the TCP bandwidth two hosts/switches

	b. What is the throughput for each case?
	-iperf h1 h2
	Results: ['15.8 Mbits/sec', '19.7 Mbits/sec'] --> 17.75 Mbits/sec average
	-iperf h1 h8
	Results: ['5.34 Mbits/sec', '5.97 Mbits/sec'] --> 5.655 Mbits/sec average

	c. What is the difference, and explain the reasons for the difference.
	-The difference is about 12.095 Mbits/sec. The reason for this could be the binary tree topology of the system as the shortest route from h1 to h2 is h1>s3>h2 while from h1 to h8 it's h1>s3>s2>s1>s5>s7>h8. As the path between two hosts gets more complex, the more the bandwidth between those two hosts gets bottlenecked (going through 1 switch vs 5 switches).

4. Which of the switches observe traffic? Please describe your way for observing such
traffic on switches (e.g., adding some functions in the “of_tutorial” controller).
-I started to play around to see what information I could pull from the event argument in the _handle_PacketIn function. I came upon the event.dpid attribute as well as the dpid_to_str function from the pox.lib.util library. From this I was able to print dpid_to_str(event.dpid) which returns the 00-00-00-00-00-0X switch identifier. I define observing traffic as the _handle_PacketIn function in a switch being called. With dpid_to_str(event.dpid) printing in the _handle_PacketIn function, I called the h1 ping -c1 h2 mininet command and the POX server showed that all of the switches called the _handle_PacketIn as this controller does not have a map and instead floods packets to all switches. Since the printed information was not useful in a flooding controller, I commented out the print statement from the _handle_PacketIn function.

---Task 3---
1. Describe how the above code works, such as how the "MAC to Port" map is established.
You could use a ‘ping’ example to describe the establishment process (e.g., h1 ping h2).
-The MAC to Port map code above learns such that everytime the switch gets a new source that isn't in the map, the code inserts that into source a map where packet.src is the key and the packet_in in-port is the value. It then checks if the destination is in the map. If it is, then the resend_packet gets directly called with the corresponding destination port otherwise the resend_packet gets called with all ports except the input port. If we assume the map is initally empty then we call the h1 ping h2 command with the MAC to Port map code, then h1's port will be stored into the map and all ports will get flooded as h2's port isn't in the map. If we now call h2 ping h1, then h2's port will be added to the map but the resend_packet command will be directly called with h1's port as it is in the map. To setup the map completely in one go, one could ping from each host to populate the map (each host has to be the X in the X ping Y command at least once).

2. (Comment out all prints before doing this experiment) Have h1 ping h2, and h1 ping
h8 for 100 times (e.g., h1 ping -c100 p2).
mininet>h1 ping -c100 h2
--- 10.0.0.2 ping statistics ---
100 packets transmitted, 100 received, 0% packet loss, time 99241ms
rtt min/avg/max/mdev = 0.972/1.237/2.580/0.195 ms
mininet>h1 ping -c100 h8
--- 10.0.0.8 ping statistics ---
100 packets transmitted, 100 received, 0% packet loss, time 99276ms
rtt min/avg/max/mdev = 3.727/4.749/10.526/1.179 ms

	a. How long did it take (on average) to ping for each case?
	mininet>h1 ping -c100 h2
	Average: 1.237 ms
	mininet>h1 ping -c100 h2
	Average: 4.749 ms

	b. What is the minimum and maximum ping you have observed?
	mininet>h1 ping -c100 h2
	Minimum: 0.972 ms
	Maximum: 2.580 ms
	mininet>h1 ping -c100 h8
	Minimum: 3.727 ms
	Maximum: 10.526 ms

	c. Any difference from Task 2 and why do you think there is a change if there is?
	------Task 2------
	mininet>h1 ping -c100 h2
	Average: 1.270 ms
	Difference: 2.435 ms
	mininet>h1 ping -c100 h8
	Average: 4.902 ms
	Difference: 7.552 ms
	------Task 3------
	mininet>h1 ping -c100 h2
	Average: 1.237 ms
	Difference: 1.608 ms
	mininet>h1 ping -c100 h8
	Average: 4.749 ms
	Difference: 6.799 ms
	-There is no significant change from task 2 to task 3 and I believe this to be accurate with the given test. For example according to the map code we added, if we have an empty map and we do X ping Y then X is added to the map and we still flood all the ports, except the input port, because Y isn't in the map. If we then do X ping Z, X is already in the dictionary but we still flood all ports, except the input port, because Z isn't in the map. This test does the same where we do h1 ping -c100 h2 and then h1 ping -c100 h8 therefore flooding the ports in both cases. Another possible explanation could be that all we did was change the switch code but the links between any two hosts remained the same therefore the ping averages and ranges we very similar between tasks.

3. Run “iperf h1 h2” and “iperf h1 h8”.
mininet> iperf h1 h2
*** Iperf: testing TCP bandwidth between h1 and h2 
*** Results: ['58.6 Mbits/sec', '61.1 Mbits/sec']
mininet> iperf h1 h8
*** Iperf: testing TCP bandwidth between h1 and h8 
*** Results: ['5.68 Mbits/sec', '6.26 Mbits/sec']

	a. What is the throughput for each case?
	-iperf h1 h2
	Results: ['58.6 Mbits/sec', '61.1 Mbits/sec'] --> 59.85 Mbits/sec average
	-iperf h1 h8
	Results: ['5.68 Mbits/sec', '6.26 Mbits/sec'] --> 5.97 Mbits/sec average

	b. What is the difference from Task 2 and why do you think there is a change if
	there is?
	Task 2:
	-iperf h1 h2
	Results: ['15.8 Mbits/sec', '19.7 Mbits/sec'] --> 17.75 Mbits/sec average
	-iperf h1 h8
	Results: ['5.34 Mbits/sec', '5.97 Mbits/sec'] --> 5.655 Mbits/sec average
	Task 3:
	-iperf h1 h2
	Results: ['58.6 Mbits/sec', '61.1 Mbits/sec'] --> 59.85 Mbits/sec average
	-iperf h1 h8
	Results: ['5.68 Mbits/sec', '6.26 Mbits/sec'] --> 5.97 Mbits/sec average
	-The code that we added to the switch made each switch better but the bottleneck that was observed in task seems to still persist here as the shortest route from h1 to h2 is h1>s3>h2 while from h1 to h8 it's h1>s3>s2>s1>s5>s7>h8. As the path between two hosts gets more complex, the more the bandwidth between those two hosts gets bottlenecked (going through 1 switch vs 5 switches). Even though each switch is better, there is maybe some kind of bottleneck in switch-to-switch links that isn't in switch-to-host or host-to-switch links.
	
