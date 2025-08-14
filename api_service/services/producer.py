"""
Module for Apache Kafka Producer Service
"""
import json
import logging
import asyncio
from aiokafka import AIOKafkaProducer

from api_service.core.config import settings

class ProducerService:
    def __init__(self):
        self.topic = settings.topic
        # Set the producer a async start and stop heres
        self._producer = self._create_producer()
        self.started = False

    def _create_producer(self):
        return AIOKafkaProducer(
            bootstrap_servers=settings.bootstrap_server
        )

    async def start(self):
        if self.started:
            await self._producer.start()
            self.started = True
            print('Starting Kafka Producer Service...')

    async def stop(self):
        if self.started:
            await self._producer.stop()
            self.started = False
            print('Shutting down Kafka connection...')

    # The commands below allow us to start and stop the service by creating our own context manager
    async def __aenter__(self):
        await self.start()
        return self
    
    async def __aexit__(self):
        await self.stop()

    # Helper method to make sure the key and value pairs are in bytes
    @staticmethod
    def _to_bytes(x:str):
        """
        Ensure string is bytes like
        """
        if not x: # If x is None return None
            return None
        
        return x if isinstance(x, bytes) else str(x).encode('utf-8')
    
    async def produce_message(self, key:str, value:dict):
        """
        Send messge to Kafka topic.
        """
        try:
            payload = await self._producer.send_and_wait(
                topic=self.topic,
                key=self._to_bytes(key),
                value=self._to_bytes(value)
            )

            print(f'Delivered message to topic {self.topic}. Payload: {key}:{value}')
            return payload
        except BufferError:
            print('Queue is full, flushing....')
            self.flush()
            # This will run once the messages have finished processing
            self.produce_message(self.topic, key, value)

    # May need a method for multiple documents being passed in

    async def flush(self):
        self._producer.flush()
    

# Define the producer here
producer: ProducerService | None
