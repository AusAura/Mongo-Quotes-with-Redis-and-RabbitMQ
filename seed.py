from models import Tag, Author, Quote
import json, connect

FILE_NAME_1 = 'authors.json'
FILE_NAME_2 = 'quotes.json'

def read_json(file_name):
    with open(file_name, 'r') as fh:
        result = json.load(fh)   
    return result

def seed_author(data):
    for item in data:
        author = Author(fullname=item['fullname'], born_date=item['born_date'], born_location=item['born_location'], description=item['description'])
        author.save()

def seed_quote(data):
    
    def create_tags(list):
        for item in list:
            tag_list = []
            tag = Tag(name=item)
            tag_list.append(tag)
        return tag_list
    
    for item in data:
        result = Author.objects(fullname=item['author'])

        author = [row for row in result]

        quote = Quote(tags=create_tags(item['tags']), author=author[0].id, quote=item['quote'])
        quote.save() 


if __name__ == '__main__':
    seed_author(read_json(FILE_NAME_1))
    seed_quote(read_json(FILE_NAME_2))
    print('DONE')