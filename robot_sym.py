from udp_channels import UDPChannel
from sensor_message import RobotTargetMessage
from time import sleep

channel = UDPChannel(local_port=UDPChannel.default_remote_port, remote_port=UDPChannel.default_local_port)

msg = RobotTargetMessage()

while 1:
    msg.color = "red"
    channel.send_to(msg.encode_message())
    sleep(.5)

    msg.color = "blue"
    channel.send_to(msg.encode_message())
    sleep(.5)




  
