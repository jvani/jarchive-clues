# -*- coding: utf-8 -*-
import os
import parsel
from enum import Enum
from peewee import (
    SqliteDatabase, Model, CharField, DateTimeField, IntegerField, BooleanField
)


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), 'jarchive.db')
DATABASE = SqliteDatabase(DB_PATH)


class Round(Enum):
    jeopardy = 1
    double_jeopardy = 2
    final_jeopardy = 3


class BaseModel(Model):
    class Meta:
        database = DATABASE


class Game(BaseModel):
    season = CharField()
    url = CharField(unique=True, index=True)
    description = CharField()
    players = CharField()
    crawled = DateTimeField(null=True)

    @classmethod
    def parse_get_or_create(cls, tr, crawled=None):
        return cls.get_or_create(
            url=tr.xpath('.//a/@href').get("").replace("https://", "http://"),
            defaults={
                "season": tr.xpath('normalize-space(//h2[@class="season"])').get(),
                "description": tr.xpath('normalize-space(td[1])').get(),
                "players": tr.xpath('normalize-space(td[2])').get(),
                "crawled": crawled
            }
        )


class Question(BaseModel):
    identifier = CharField()
    url = CharField()
    order = IntegerField(null=True)
    value = IntegerField(null=True)
    round = IntegerField()
    daily_double = BooleanField(default=False)
    category = CharField()
    clue = CharField()
    answer = CharField()

    @staticmethod
    def parse_mouseover(td):
        mo = td.xpath('.//div/@onmouseover')
        html = mo.re_first(r"toggle\('\w+', '\w+', '(.+)'\)", '')
        return parsel.Selector(html)

    @classmethod
    def parse_create(cls, td, rnd, categories, url):
        clue = td.xpath('normalize-space(.//*[@class="clue_text"])').get()
        if clue:
            if rnd.name == "final_jeopardy":
                index = 0
            else:
                index = int(td.xpath('.//*[@class="clue_text"]/@id').re_first(r'(\d+)_\d+')) - 1
            mouseover = cls.parse_mouseover(td)
            return cls.create(
                url=url.replace("https://", "http://"),
                identifier=td.xpath('.//*[@class="clue_text"]/@id').get(),
                order=int(td.xpath('normalize-space(.//*[@class="clue_order_number"])').re_first(r'(\d+)', 0)) or None,
                value=int(td.xpath('.//*[@class="clue_value"]').re_first(r'(\d+)', 0)) or None,
                round=rnd.value,
                daily_double=bool(td.xpath('.//*[@class="clue_value_daily_double"]')),
                category=categories[index],
                clue=clue,
                answer=mouseover.xpath('normalize-space(//em)').get()
            )


if __name__ == "__main__":
    if os.path.isfile(DB_PATH):
        print(f"Database exists: {DB_PATH}")
    else:
        print(f"Creating database: {DB_PATH}")
        DATABASE.connect()
        DATABASE.create_tables([Game, Question])
        DATABASE.close()
