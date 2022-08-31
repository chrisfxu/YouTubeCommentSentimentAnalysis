import csv 
from datetime import datetime as dt

comments = []
today = dt.today().strftime('%d-%m-%Y')

def process_comments(response_items):
    for res in response_items:
        #handle replies

        if 'replies' in res.keys():
            for reply in res['replies']['comments']:
                comment = reply['snippet']
                comment['commentId'] = reply['id']
                comments.append(comment)
        else:
            comment = {}
            comment['snippet'] = res['snippet']['topLevelComment']['snippet']
            comment['snippet']['parentId'] = None
            comment['snippet']['commentId'] = res['snippet']['topLevelComment']['id']
            comments.append(comment['snippet'])

    return comments

def make_csv(comments, title = None):
    header = comments[0].keys()

    if title:
        filename = f'data_{title}_{today}.csv'

    else:
        filename = f'comments_{today}.csv'

    with open(filename, 'w', encoding = 'utf8', newline = '') as f:
        writer = csv.DictWriter(f, fieldnames = header)
        writer.writeheader()
        writer.writerows(comments)
     