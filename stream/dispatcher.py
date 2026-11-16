import json
import random
import time
import uuid
from datetime import datetime, timezone

import pika

EXCHANGE = "rapido-dispatch"

ZONES = {
    "bangalore": ["koramangala", "indiranagar", "whitefield"],
    "chennai": ["tnagar", "adyar", "annanagar"],
}

TYPES = ["ride", "food"]


def connect():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="topic",
        durable=True,
    )

    return connection, channel


def publish_request(channel, count):
    city = random.choice(list(ZONES.keys()))
    zone = random.choice(ZONES[city])
    request_type = random.choice(TYPES)

    routing_key = f"{city}.{zone}.{request_type}"

    # Every 10th message is deliberately bad.
    if count % 10 == 0:
        message = {
            "id": str(uuid.uuid4())[:8],
            "city": city,
            # Deliberately missing "zone"
            "type": request_type,
            "ts": datetime.now(timezone.utc).isoformat(),
        }

        print(
            f"BAD MESSAGE #{count} | key={routing_key} | "
            f"missing zone | id={message['id']}",
            flush=True,
        )

    else:
        message = {
            "id": str(uuid.uuid4())[:8],
            "city": city,
            "zone": zone,
            "type": request_type,
            "ts": datetime.now(timezone.utc).isoformat(),
        }

        print(
            f"GOOD MESSAGE #{count} | key={routing_key} | "
            f"id={message['id']}",
            flush=True,
        )

    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=routing_key,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            content_type="application/json",
            delivery_mode=2,
        ),
    )


def main():
    connection, channel = connect()
    count = 0

    print("Dispatcher started...", flush=True)

    try:
        while True:
            count += 1
            publish_request(channel, count)
            time.sleep(2)

    except KeyboardInterrupt:
        print("Dispatcher stopped.", flush=True)

    finally:
        connection.close()


if __name__ == "__main__":
    main()
