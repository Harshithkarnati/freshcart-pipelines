import json
import sys

import pika

EXCHANGE = "rapido-dispatch"


def main():
    if len(sys.argv) != 3:
        print("Usage: python driver.py NAME PATTERN")
        sys.exit(1)

    name = sys.argv[1]
    pattern = sys.argv[2]

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="topic",
        durable=True,
    )

    result = channel.queue_declare(
        queue="",
        exclusive=True,
        auto_delete=True,
    )

    queue_name = result.method.queue

    channel.queue_bind(
        exchange=EXCHANGE,
        queue=queue_name,
        routing_key=pattern,
    )

    channel.basic_qos(prefetch_count=1)

    print(
        f"Driver {name} listening | pattern={pattern}",
        flush=True,
    )

    def callback(ch, method, properties, body):
        try:
            message = json.loads(body.decode())

            # Reject messages that do not contain the zone field.
            if "zone" not in message:
                print(
                    f"REJECTED by {name} | key={method.routing_key} | "
                    f"reason=missing zone | id={message.get('id')}",
                    flush=True,
                )

                ch.basic_nack(
                    delivery_tag=method.delivery_tag,
                    requeue=False,
                )
                return

            # Process valid messages.
            print(
                f"PROCESSED by {name} | key={method.routing_key} | "
                f"message={message}",
                flush=True,
            )

            ch.basic_ack(
                delivery_tag=method.delivery_tag
            )

        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            print(
                f"REJECTED by {name} | invalid JSON | {error}",
                flush=True,
            )

            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=False,
            )

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=False,
    )

    try:
        channel.start_consuming()

    except KeyboardInterrupt:
        print(f"Driver {name} stopped.", flush=True)
        channel.stop_consuming()

    finally:
        connection.close()


if __name__ == "__main__":
    main()
