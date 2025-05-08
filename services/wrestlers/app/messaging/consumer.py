import json 
from pika import BlockingConnection, ConnectionParameters

TOKEN_CACHE = {}

def consume_messages():
    connection = BlockingConnection(ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    channel.queue_declare(queue='auth_events')

    def callback(ch, method, propierties, body):
        
        event = json.loads(body)
        if event['event_name'] == 'UserLoggedIn':
            
            # Actualizamos el caché local con el nuevo token
            TOKEN_CACHE[event['data']['token']] = event['data']['email']
    
    channel.basic_consume(queue='auth_events', on_message_callback=callback, auto_ack=True)
    print(" [*] Waiting for messages. To exit press CTRL+C ")
    channel.start_consuming()