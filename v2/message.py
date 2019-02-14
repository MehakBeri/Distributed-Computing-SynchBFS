class Message():
    def __init__(self, sender_id, receiver_id, is_ack):
        self.senderID = sender_id
        self.receiverID = receiver_id
        self.is_ack = is_ack

    def __repr__(self):
        return "<Message sender: %s receiver: %s is_ack: %s>" % (self.senderID, self.receiverID, self.is_ack)




