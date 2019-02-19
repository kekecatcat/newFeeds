from cloudAMQP_client import CloudAMQPClient

# use your own queue url
CLOUDAMQP_URL = "amqp://efsjggzv:MdR4Q2p5a8JNkTniqgWKJ28qw39xn90b@caterpillar.rmq.cloudamqp.com/efsjggzv"
NEWS_FETCH_TASK_QUEUE_NAME = "test"

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, NEWS_FETCH_TASK_QUEUE_NAME)

    sentMsg = {"test": "test"}
    client.sendMessage(sentMsg)
    receivedMsg = client.getMessage()
    assert sentMsg == receivedMsg
    print("test_basic passed")

if __name__ == "__main__":
    test_basic()