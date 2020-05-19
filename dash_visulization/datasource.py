import MySQLdb
import pandas as pd

from scrapy_APP.settings import MYSQL_HOST, MYSQL_CHARSET, MYSQL_DB, MYSQL_PASSWORD, MYSQL_USER


class DataLoader:

    batch_size = 100
    offset = 0
    col_names = ['id', 'tag', 'title', 'content', 'time', 'comments', 'url',
                 'education', 'IT', 'animals', 'medicine','famus', 'poetry', 'sensitives',
                 'car_brand_part', 'law', 'financial', 'food', 'positives', 'negatives']
    df = None

    def __init__(self):
        self.conn = MySQLdb.connect(
            MYSQL_HOST,
            MYSQL_USER,
            MYSQL_PASSWORD,
            MYSQL_DB,
            charset=MYSQL_CHARSET,
            use_unicode=True
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute("select count(*) from wangyiitem")
        self.news_num = self.cursor.fetchone()[0]

    def fetch_batch(self, idx: int) -> pd.DataFrame:
        print("fetching")
        sql = "select * from wangyiitem limit {},{}"
        start = max(0, idx-self.batch_size//2)
        self.cursor.execute(sql.format(start, self.batch_size))
        self.offset = start+1
        data = self.cursor.fetchall()
        self.df = pd.DataFrame(data, columns=self.col_names)
        return self.df

    def fetch_by_id(self, news_id: int) -> pd.DataFrame:
        if self.df is None or news_id < self.offset or news_id >= self.offset + self.batch_size:
            # 缓存未命中
            self.fetch_batch(news_id)
        row_no = news_id - self.offset
        return self.df.iloc[row_no]

    def get(self, news_id) -> tuple:
        data = self.fetch_by_id(news_id)
        content_percentage = data.iloc[7:-2]
        emotion = data.iloc[-2:]
        return list(content_percentage), list(emotion), data.tag, data.title, data.content, data.url


if __name__ == '__main__':
    dl = DataLoader()
    print(dl.news_num)
