import socket
import time
import re


HOST = '218.199.110.35'
PORT = 12602
LOGIN_INFO = "type@=loginreq/username@=qq_aPSMdfM5"+"/password@=1234567890123456/roomid@=138286" + "/"
JION_GROUP = "type@=joingroup/rid@=138286" + "/gid@=1"+"/"
ROOM_ID = "type@=qrl/rid@=138286"+ "/"
KEEP_ALIVE = "type@=keeplive/tick@=" + str(int(time.time())) + "/vbw@=0/k@=19beba41da8ac2b4c7895a66cab81e23/"



def tranMsg(content):
	length = bytearray([len(content) + 9, 0x00, 0x00, 0x00])
	code = length
	magic = bytearray([0xb1, 0x02, 0x00, 0x00])
	end = bytearray([0x00])
	trscont = bytes(content.encode('utf-8'))
	return bytes(length + code + magic + trscont + end)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
s.sendall(tranMsg(LOGIN_INFO))
data = s.recv(1024)
print repr(data)
s.sendall(tranMsg(JION_GROUP))


sendlive = 0
while True:
	if sendlive%40==0:
		print "----------------------------------Keep Alive----------------------------------"
		s.sendall(tranMsg(KEEP_ALIVE))
	sendlive+=1
	time.sleep(1)
	data = s.recv(4000)
	strdata = repr(data)
	if "type@=chatmsg" in strdata:
		try:
			sender_id = re.search('\/nn@=(.+?)\/', data).group(1)
			chatmsg = sender_id
			sender_content = re.search('\/txt@=(.+?)\/', data).group(1)
			print chatmsg,"said:",sender_content,"at:",time.strftime('%H-%I-%M',time.localtime(time.time()))

		except Exception, e:
			print "error occur:",repr(data)
		finally:
			pass
s.close()