from MySQLdb.cursors import DictCursor
from django.core.management import BaseCommand
import MySQLdb as mdb
import datetime

from community.models import Member
from forum.models import Category, Topic, Board, Post


class Importer(object):
    SOURCE_DB = "tlforum"
    SOURCE_HOST = 'localhost'
    SOURCE_USER = 'root'
    SOURCE_PASSWORD = ''

    def _query(self, query):
        connection = mdb.connect(self.SOURCE_HOST, self.SOURCE_USER, self.SOURCE_PASSWORD, self.SOURCE_DB)
        cur = connection.cursor(DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
        return rows

    def import_members(self):
        rows = self._query("select * from smf_members")

        for row in rows:
            if row['gender'] == 0:
                gender = 't'
            elif row['gender'] == 2:
                gender = 'f'
            else:
                gender = 'm'

            Member.objects.create(
                id=row['ID_MEMBER'],
                username=row["memberName"],
                date_joined=datetime.datetime.fromtimestamp(row['dateRegistered']),
                last_activity=datetime.datetime.fromtimestamp(row['lastLogin']),
                first_name=row['realName'],
                password=row['passwd'],
                email=row['emailAddress'],
                gender=gender,
                birth_date=row['birthdate'],
                website=row['websiteUrl'],
                location=row['location'],
                icq=row['ICQ'])

    def import_categories(self):
        rows = self._query("select * from smf_categories")
        for row in rows:
            Category.objects.create(
                id=row['ID_CAT'],
                name=row['name'],
                order=row['catOrder'])

    def import_boards(self):
        rows = self._query("select * from smf_boards order by ID_PARENT")
        for row in rows:
            category = Category.objects.get(id=row['ID_CAT'])
            if row['ID_PARENT'] == 0:
                parent = None
            else:
                parent = Board.objects.get(id=row['ID_PARENT'])
            Board.objects.create(
                id=row['ID_BOARD'],
                category=category,
                parent=parent,
                order=row['boardOrder'],
                name=row['name'],
                description=row['description'])

    def import_topics(self):
        rows = self._query("select * from smf_topics")

        for row in rows:
            Topic.objects.create(
                id=row['ID_TOPIC'],
                is_sticky=row['isSticky'],
                board=Board.objects.get(id=row['ID_BOARD']))

    def import_posts(self):
        rows = self._query("select * from smf_messages")

        for row in rows:
            if row['ID_MEMBER'] != 0:
                member = Member.objects.get(id=row['ID_MEMBER'])
            else:
                member=None

            Post.objects.create(
                id=row['ID_MSG'],
                topic=Topic.objects.get(id=row['ID_TOPIC']),
                created_at=datetime.datetime.fromtimestamp(row['posterTime']),
                created_by=member,
                subject=row['subject'],
                body=row['body'],
                icon=row['icon'])

class Command(BaseCommand):
    help = "Import legacy smf forum"
    def handle(self, *args, **kwargs):
        importer = Importer()
        importer.import_members()
        importer.import_categories()
        importer.import_boards()
        importer.import_topics()
        importer.import_posts()