from models import Author, Quote
import connect

import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host='localhost', port=6379, password=None)
cache = RedisLRU(client)

## name:Steve Martin
## tag:miracles
## tags:simile,miracles

@cache
def get_all_quotes(name: str) -> list:
    print(f'Getting quotes by name from DB: {name}')
    author = Author.objects(fullname__startswith=name)
    if not author:
        return 'FOUND NOTHING!'

    for item in author:
        author_id = item.id

    quotes = Quote.objects(author=author_id)
    quotes_list = []
    for item in quotes:
        quotes_list.append(item.quote)

    return quotes_list

@cache
def get_quotes_by_tag(tag):
    print(f'Getting quotes by tag from DB: {tag}')
    quotes = Quote.objects(tags__name__startswith=tag)

    quotes_list = []
    for item in quotes:
        quotes_list.append(item.quote)

    return quotes_list

@cache
def get_quotes_by_all_tags(tag_list):
    print(f'Getting quotes by tag combination from DB: {tag_list}')
    quotes = Quote.objects(tags__name__in=tag_list)

    quotes_list = []
    for item in quotes:
        quotes_list.append(item.quote)

    return quotes_list


function_dict = {
    'name': get_all_quotes,
    'tag': get_quotes_by_tag,
    'tags': get_quotes_by_all_tags
}


def parse_command(command: str) -> tuple:
    parsed = command.split(':')
    if parsed[0] == 'tags':
        parsed[1] = parsed[1].split(',')

    return parsed[0], parsed[1]


while True:
    command = input('Put some request("name:Steve Martin", "tags:life,live") -->>  ')
    if command == 'exit':
        exit()

    print('Working on the command.')
    command_name, command_args = parse_command(command)
    print(function_dict[command_name](command_args))
