import pika, faker, connect
from models import Contact

DELIVERY_METHODS = ['SMS', 'email']
faker = faker.Faker()

def generate_db_fakes(number):
    ids = []
    contacts = []
    for i in range(number):
        contact = Contact(fullname=faker.name(), email=faker.email(), phone_number=faker.phone_number(), delivery_method = faker.random.choice(DELIVERY_METHODS))
        contact.save()
        ids.append(contact.id)
        contacts.append(contact)

    return ids, contacts
    
def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='email')
    channel.queue_declare(queue='SMS')

    zipped = zip(*generate_db_fakes(5))

    for item, contact in zipped:
        string = str(item)
        contact = contact
        if contact.delivery_method == 'email':
            print(f'Sending with email {string}')
            channel.basic_publish(exchange='', routing_key='email', body=string)
        elif contact.delivery_method == 'SMS':
            print(f'Sending with SMS {string}')
            channel.basic_publish(exchange='', routing_key='SMS', body=string)
        else:
            print(f'Uknown delivery method {contact.delivery_method} for {string}! Message will not be sent.')

    print('[!!!] Fakes generated. Messages queued.')
    connection.close()
    
if __name__ == '__main__':
    main()