"""
Module for Kafa Consumer Service
"""
from confluent_kafka import Consumer

# Don't forget to type each parameter for documentation
class ConsumerService:
    def __init__(self, bootstrap_server, group_id, auto_offset, topics):
        self.bootstrap_server = bootstrap_server
        self.group_id = group_id
        self.auto_offset = auto_offset
        self.topics = topics

        # Create consumer method would be here
        self.consumer = self._create_consumer()

    # internal method to create consumer - subscribe to topic
    def _create_consumer(self):
        config = {
            'bootstrap.servers': self.bootstrap_server,
            'group.id': self.group_id,
            'auto.offset.reset': self.auto_offset
        }

        return Consumer(config)

    # method to actually consume messages from the topic
    def consume_message(self, handler, timeout=1.0):
        # First you neeed to subscribe to a topic
        try:
            self.consumer.subscribe(self.topics)
            print(f'Subscribed to {self.topics}')

            while True:
                message = self.consumer.poll(timeout)
                if message is None:
                    continue

                if message.error():
                    print(f'Issue with consumer service: {message.error()}')

                print(f'Recieved message: {message.key()}:{message.value()}')
                handler(message)

        except KeyboardInterrupt:
            print('Consumer service interuppted....')
        finally:
            self.consumer.close()
            print('Consumer service is closed...')

    def shutdown(self):
        """
        shutdown Kafka connection
        """
        self.consumer.close()

# def handle_message(msg):
#     print(f"Processing message: {msg.value().decode('utf-8')}")
#     # This will be the mongodb insert here

# consumer = ConsumerService(
#     bootstrap_server='localhost:9092',
#     group_id='my-event-group',
#     auto_offset='earliest', # change to latest to only get the most recent message. Earliest will look for everything
#     topics=['game-event']
# )

# consumer.consume_message(handler=handle_message)
