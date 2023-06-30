
from itemadapter import ItemAdapter
import psycopg2
import os

class SrealityPipeline:

    def __init__(self):
        host = 'database'
        # host = '127.0.0.1'
        port = '5432'
        user = 'luxonis'
        password = 'luxonis1'
        dbname = 'sreality'

        self.connection = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname)
        self.cur = self.connection.cursor()
        self.cur.execute('''
                         CREATE TABLE IF NOT EXISTS flats(
                             id serial PRIMARY KEY,
                             title text,
                             image_url text)
                             ''')
        self.cur.execute(''' DELETE FROM flats * ''')

    def process_item(self, item, spider):
        self.cur.execute(''' insert into flats (title, image_url) values (%s,%s) ''', (
            item['title'],
            str(item['image_url'])))
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.cur.execute(''' SELECT * FROM flats ''')
        flats = self.cur.fetchall()


        html = "<html><meta charset='UTF-8'><style>th { text-align: center; }</style>"
        html += '<table>'
        html += "<tr><th colspan='2' style='font-size: 20px; padding-bottom: 30px;'>Newest flats for sale</th></tr>\n"
        html += '<tr><th>Title</th><th>Image URL</th></tr>\n'

        lines = []
        for flat in flats:
            line = f"<tr><td>{flat[1]}</td><td><img src='{flat[2]}'></td></tr>\n"
            lines.append(line)
        html = f"{html}{''.join(lines)}</table></html>"

        with open('./http_server/sreality.html', 'w+', encoding='utf-8') as f:
            f.write(html)

        self.cur.close()
        self.connection.close()
