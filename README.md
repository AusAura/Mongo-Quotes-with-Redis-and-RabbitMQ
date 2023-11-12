# Mongo-Quotes-with-Redis-and-RabbitMQ

App that seeds MongoDB with MongoEngine, allows searching through it by 'name', specific 'tag' or list of 'tags'. Uses Redis for LRU cache. Also, sends messages with RabbitMQ, depending on the delivery method.

1) Connects to MongoDB in the Cloud.
2) Using ODM MongoEngine to seed the database with data from 'quotes.json' file.
3) read.py allows searching the database by 'name', specific 'tag' or set of 'tags'. Searches by the part of the name or tag as well.
4) read.py uses Redis for LRU cache. Means that the same query will not be executed if the result of the operation is still in the Redis cache.
5) producer.py will generate fake data and seed the database with it. Also, every entry will have a 'devilery method' (email or SMS). Depending on which, script will queue a message to the user with RabbitMQ.
6) consumer_email.py and consumer_sms.py are dummies that handle sending the message.

## Commands with examples:

- name:Steve Martin
- tag:miracles
- tags:simile,miracles
