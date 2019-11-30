from mininet.net import Mininet
from mininet.node import Controller, RemoteController, CPULimitedHost
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.util import pmonitor
from signal import SIGINT
from time import time
import os 

 # controller=RemoteController, 
  #Waktu Running iperf
#Ex_seconds = 25
#Mo_seconds = Ex_seconds + 20

def topology():

	os.system('mn -c')
	#os.system('sysctl -w net.ipv4.tcp_congestion_control=cubic')
	os.system('sysctl -w net.ipv4.tcp_congestion_control=reno')

	net = Mininet(controller=RemoteController, link=TCLink, host=CPULimitedHost)
	
	# Add hosts and router
	r1 = net.addHost( 'r1', ip="200.122.2.1/29" )
	server = net.addHost( 'server', ip="200.122.2.2/29", mac="00:00:00:00:00:01" )
	pc = net.addHost( 'pc', ip="200.122.3.2/29", mac="00:00:00:00:00:02" )
	

	#create link between host
	net.addLink( r1, server, cls=TCLink, bw=2, max_queue_size=60 )
	net.addLink( r1, pc, cls=TCLink, bw=1000, max_queue_size=60 )

	net.build()
	
	# config interface of R1
	r1.cmd("ifconfig r1-eth0 0")
	r1.cmd("ifconfig r1-eth1 0")

	# set value of each mac addr
	r1.cmd('ifconfig r1-eth0 hw ether 00:00:00:00:00:01 ')
	r1.cmd('ifconfig r1-eth1 hw ether 00:00:00:00:00:02 ')

	# set default gateway for each host
	r1.cmd("ip addr add 200.122.2.1/29 brd + dev r1-eth0")
	r1.cmd("ip addr add 200.122.3.1/29 brd + dev r1-eth1")
	r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

	#set default route for each host
	server.cmd("ip route add default via 200.122.2.1")
	pc.cmd("ip route add default via 200.122.3.1")


	net.start()
	# popens = {}
	# hosts=net.hosts
	# popens[(hosts[1], 'server')] = hosts[1].popen('iperf -s')
	# popens[(hosts[2], 'pc')] = hosts[2].popen('iperf -c {} -t {}'
	#                             .format(hosts[1].IP(), str(Ex_seconds)))
	# print 'Monitoring output untuk', Mo_seconds, 'seconds'
	# endTime = time() + Mo_seconds
	# for h, line in pmonitor(popens, timeoutms=500):
	#     if h:
	#         print '%s %s: %s' % (h[0].name, h[1], line)
	#     if time() >= endTime:
	#         for p in popens.values():
	#                 p.send_signal(SIGINT)


	#congestion control configuration
	# print pc.cmd('sysctl -w net.ipv4.tcp_congestion_control=cubic')
	# print server.cmd('sysctl -w net.ipv4.tcp_congestion_control=cubic')

	print "*** Running MININET"

	CLI( net )

	print "*** Stopping MININET"

	net.stop()

      

if __name__ == '__main__':

    setLogLevel( 'info' )
    topology() 
