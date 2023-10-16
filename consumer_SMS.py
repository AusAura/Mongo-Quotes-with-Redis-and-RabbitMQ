import pika, connect
from models import Contact

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='SMS')

    def send_SMS(ch, method, properties, body):
        print('Recieving message?')
        string = body.decode('utf-8')
        contact = Contact.objects(id=string)[0]
        print(f" [!!!] Send SMS to: {contact.phone_number} ")
        contact.is_sent = True
        contact.save()

    channel.basic_consume(queue='SMS', on_message_callback=send_SMS, auto_ack=False)
    print('[!!!] Active for SMS, waiting for messages.')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()