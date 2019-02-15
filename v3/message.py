from enum import Enum

class Message():
    def __init__(self, sender_id, receiver_id, msg_type):
        self.senderID = sender_id
        self.receiverID = receiver_id
        self.msg_type = msg_type

    def __repr__(self):
        return "<Message sender: %s receiver: %s msg_type: %s>" % (self.senderID, self.receiverID, self.msg_type)

class MsgType(Enum):
    INTER_PROCESS = 0
    ACK = 1
    BROADCAST = 2



