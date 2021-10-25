class CalcIp(object):

	def __init__(self, ipaddr):
		self.divide = ipaddr.split('/')
		self.ipaddr = self.divide[0]
		self.subnet = self.divide[1]

	def dec_to_binery(self, decimal):
		biner = list(map(lambda x: bin(int(x))[2:].zfill(8), decimal))
		return biner

	def calc_netmaskz(self):
		maskz = ''
		count = 0
		subnt = []

		for i in range(32):
			count = count + 1 if count < 8 else 1
			maskz = maskz+'1' if i+1 <= int(self.subnet) else maskz+'0'
			if count == 8:
				subnt.append(maskz)
				maskz = ''
		return subnt

	def reverse_maskz(self):
		wildsub = []
		submask = list(map(lambda x: int(x,2), self.calc_netmaskz()))
		for i in submask:
			wildsub.append(255 - int(i))
		return wildsub

	def calc_networkz(self):
		network = []
		ipbiner = self.dec_to_binery(self.ipaddr.split('.'))
		submask = self.calc_netmaskz()
		for a, b in zip(ipbiner, submask):
			network.append(str(int(a, 2) & int(b, 2)))
		return network

	def calc_broacast(self):
		broadst = []
		ipbiner = self.dec_to_binery(self.ipaddr.split('.'))
		submask = self.dec_to_binery(self.reverse_maskz())
		for a, b in zip(ipbiner, submask):
			broadst.append(str(int(a, 2) | int(b, 2)))
		return broadst

	def calc_ipaddres(self):
		submask = list(map(lambda x: str(int(x,2)), self.calc_netmaskz()))
		data = {
			'submask': '.'.join(submask),
			'network': '.'.join(self.calc_networkz()),
			'broadst': '.'.join(self.calc_broacast())
		}
		return data