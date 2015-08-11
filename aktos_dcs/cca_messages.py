try:
    import simplejson as json
except ImportError:
    print "WARNING: module simplejson not found, using json instead..."
    import json



import time
import uuid
import copy
import msgpack
# message functions
def unpack(message):
    return msgpack.unpackb(message)

def pack(msg):
    #assert(isinstance(msg, Message)) # this does not consume cpu
    return msgpack.packb(msg)


def envelp(message, msg_id):
    return {
        'sender': [],
        'timestamp': time.time(),
        'msg_id': msg_id, # {{.actor_id}}.{{serial}}
        'payload': message,
    }

def msg_body(msg):
    return msg['payload'].values()[0]

class Message(dict):

    sender = []
    debug = []

    def __init__(self, *args, **kwargs):
        for attr in dir(self):
            if not callable(getattr(self, attr)) and not attr.startswith("__"):
                #print attr
                default_val = getattr(self, attr)
                try:
                    assert kwargs[attr] != default_val
                except:
                    kwargs[attr] = copy.deepcopy(default_val)

        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

        self.timestamp = time.time()
        #self.msg_id = str(uuid.uuid4())
        self.cls = self.__class__.__name__

        # this should be the last one
        for k, v in kwargs.items():
            setattr(self, k, v)


class ProxyActorMessage(Message):
    contact_list = []
    new_contact_list = []
    reply_to = ""


class PingMessage(Message):
    text = ""


class PongMessage(PingMessage):
    pass


class FooMessage(PingMessage):
    pass

class BarMessage(FooMessage):
    pass


# --------------------------------
# this import should be after
# base message classes' definiton
#
from Messages import *
# --------------------------------


def test():
    try:
        a = Message(key="d", edge="rising_edge")
        a_sender = "foobar"
        a.sender.append(a_sender)

        b = ProxyActorMessage()
        b_sender = "baz"
        b.sender.append(b_sender)
        b.contact_list.append({"foo": "bar"})

        assert len(str(a)) == len(pack(a))
        assert a == unpack(pack(a))
        assert a.sender == [a_sender]

        assert len(str(b)) == len(pack(b))
        assert b == unpack(pack(b))
        assert b.sender == [b_sender]
        assert b.cls == 'ProxyActorMessage'
        assert b.contact_list == [{"foo": "bar"}]

        c = ProxyActorMessage()
        c.contact_list.append({'baz': 'foobar'})

        assert c.contact_list == [{'baz': 'foobar'}]

        x = TestMessage(foo="bar")
        assert x == unpack(pack(x))

        print "all tests went OK..."

    except AssertionError, e:
        print "ERROR: Something went WRONG!", e.message
        #raise
        import pdb
        pdb.set_trace()




if __name__ == "__main__":
    try:
        test()
    except:
        raise

        import pdb
        pdb.set_trace()



