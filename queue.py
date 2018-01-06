
from google.cloud import pubsub
from google.api_core.exceptions import AlreadyExists
from google.cloud.pubsub_v1.types import PushConfig
from functools import partial

publisher_client = pubsub.PublisherClient()
subscriber_client = pubsub.SubscriberClient()

def get_publisher(name):
  topic_name = publisher_client.topic_path('cloudcomputingcompiler', name + '_jobs')
  
  publisher_client.get_topic(topic_name)

  sub_name = subscriber_client.subscription_path('cloudcomputingcompiler', name + '_jobs')
  push_config = PushConfig()
  push_config.push_endpoint = 'https://worker-dot-cloudcomputingcompiler.appspot.com/_ah/' + name + '/'

  try:
    subscription = subscriber_client.create_subscription(sub_name, topic_name, push_config, ack_deadline_seconds=30)
  except AlreadyExists:
    pass
  
  return partial(publisher_client.publish, topic=topic_name)
  

