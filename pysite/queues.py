from kombu import Queue

QUEUES = {  # RabbitMQ Queue definitions, they'll be declared at gunicorn start time
    "bot_events": Queue("bot_events", durable=True)
}
