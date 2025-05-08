import json 
from pika import BlockingConnection, ConnectionParameters

def publish_event(event_name, data):

    connection = BlockingConnection(ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    # Declaramos la cola
    channel.queue_declare(queue='auth_events')

    event = {
        "event_name" : event_name,
        "data": data
    }

    channel.basic_publish(exchange='', routing_key='auth_events', body=json.dumps(event))

    connection.close()

