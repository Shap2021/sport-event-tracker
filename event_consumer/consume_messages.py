"""
Module for consume message functions
"""
import asyncio
import contextlib

from core.config import settings
from services.mongodb import MongoDataManager
from services.consumer import ConsumerService

class ConsumeMessage:
    def __init__(self):
        self.consumer = None
        self.mongodb = None
        self.consumer_task = None
        self.shutdown_event = asyncio.Event()

    async def start_service(self):
        """
        Start MongoDB and Kafka Connections
        """
        print(f'Connecting to MongoDB....Subscribing to Kafka topic {settings.topic}....')
        self.mongodb = MongoDataManager()
        self.consumer = ConsumerService(
            bootstrap_server=settings.boostrap_server,
            group_id=settings.group_id,
            auto_offset=settings.offset,
            topics=[settings.topic]
        )

        self.consumer_task = asyncio.create_task(
            await self.consumer.consume_message(handler=self.mongodb.add_one_doc)
        )

    async def stop_service(self):
        """
        Stop MongoDB and Kafka Connections
        """
        print('Shutting down Kafka and MongoDB connections...')
        self.shutdown_event.set()

        if hasattr(self.consumer, "stop"):
            with contextlib.suppress(Exception):
                await self.consumer.shutdown()

        if self.consumer_task:
            self.consumer_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.consumer_task

        if hasattr(self.mongodb, "shutdown"):
            with contextlib.suppress(Exception):
                await self.mongodb.shutdown()

        print('Shutting down service completed....')
        
