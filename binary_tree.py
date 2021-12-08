from mininet.topo import Topo

class BinaryTreeTopo( Topo ):
    #"Binary Tree Topology Class."

    def __init__( self ):
        #"Create the binary tree topology."

        # Initialize topology
        Topo.__init__( self )
	
	hosts=[]
	switches=[]
	
	# Add hosts
	for host in range(8):
		hosts.append(self.addHost('h'+str(host+1)))
	
	# Add switches
	for switch in range(7):
		switches.append(self.addSwitch('s'+str(switch+1)))
	
	# Add links
	#switch-to-switch links
	self.addLink(switches[0], switches[1])
	self.addLink(switches[0], switches[4])
	self.addLink(switches[1], switches[2])
	self.addLink(switches[1], switches[3])
	self.addLink(switches[4], switches[5])
	self.addLink(switches[4], switches[6])
	
	#switch-to-host links
	self.addLink(switches[2], hosts[0])
	self.addLink(switches[2], hosts[1])
	self.addLink(switches[3], hosts[2])
	self.addLink(switches[3], hosts[3])
	self.addLink(switches[5], hosts[4])
	self.addLink(switches[5], hosts[5])
	self.addLink(switches[6], hosts[6])
	self.addLink(switches[6], hosts[7])

topos = { 'binary_tree': ( lambda: BinaryTreeTopo() ) }
