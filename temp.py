import redis
import redis.client

def message_handler(message):
    print(message['data'])

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
pubsub = r.pubsub()
pubsub.subscribe(**{'my-channel': message_handler})
pubsub.run_in_thread(sleep_time=2)

r.publish('my-channel', 'Hello Boom')
