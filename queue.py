
from google.cloud import pubsub
from google.api_core.exceptions import AlreadyExists
from google.cloud.pubsub_v1.types import PushConfig
from functools import partial

publisher_client = pubsub.PublisherClient()
subscriber_client = pubsub.SubscriberClient()

def get_publisher(name):
  topic_name = publisher_client.topic_path('cloudcomputingcompliler', name + '_jobs')
  try:
    publisher_client.create_topic(topic_name)
  except AlreadyExists:
    pass

  sub_name = subscriber_client.subscription_path('cloudcomputingcompliler', name + '_jobs')
  push_config = PushConfig()
  push_config.push_endpoint = 'https://cloudcomputingcompliler.appspot.com/_ah/' + name + '/'
  try:
    subscription = subscriber_client.create_subscription(sub_name, topic_name, push_config)
  except AlreadyExists:
    pass
  
  return partial(publisher_client.publish, topic=topic_name)
  

