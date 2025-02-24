import json
import time
from confluent_kafka import Consumer, KafkaError, KafkaException
from telegram import Bot
from settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Kafka consumer setup
conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest',
    'socket.timeout.ms': 10000,  # Increase timeout
    'session.timeout.ms': 10000,
}

def create_kafka_consumer():
    retries = 5
    while retries > 0:
        try:
            consumer = Consumer(conf)
            consumer.subscribe(['user-registered'])
            return consumer
        except KafkaException as e:
            print(f"Failed to connect to Kafka: {e}. Retrying in 5 seconds...")
            time.sleep(5)
            retries -= 1
    raise Exception("Failed to connect to Kafka after multiple retries")

def send_telegram_message(message):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def process_message(msg):
    user_data = json.loads(msg.value())
    message = f"New user registered: {user_data['username']} (ID: {user_data['id']})"
    send_telegram_message(message)

def main():
    consumer = create_kafka_consumer()
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Kafka error: {msg.error()}")
                    break
            process_message(msg)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == '__main__':
    main()