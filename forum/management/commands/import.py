import datetime
import HTMLParser

from MySQLdb.cursors import DictCursor
from django.core.files import File
from django.core.management import BaseCommand
import MySQLdb as mdb
from django.db.models import DateTimeField
import os
import subprocess
import glob
import pytz

from community.models import Member
from forum.models import Category, Topic, Board, Post, Attachment
from shoutbox.models import ShoutBox, Shout


def disable_auto_now(model):
    for field in model._meta.local_fields:
        if isinstance(field, DateTimeField):
            field.auto_now_add = False
            field.auto_now = False

class Importer(object):
    SOURCE_DB = "tlforum"
    SOURCE_HOST = 'localhost'
    SOURCE_USER = 'root'
    SOURCE_PASSWORD = ''
    ATTACHMENT_TEMP = os.path.join(os.path.dirname(__file__), "attachment_temp")
    TZ = pytz.timezone("Europe/Berlin")

    def _query(self, query):
        connection = mdb.connect(self.SOURCE_HOST, self.SOURCE_USER, self.SOURCE_PASSWORD, self.SOURCE_DB, charset="utf8")
        cur = connection.cursor(DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
        return rows

    def import_members(self):
        print "* Importing members"
        rows = self._query("select * from smf_members")

        for row in rows:
            if row['gender'] == 0:
                gender = 't'
            elif row['gender'] == 2:
                gender = 'f'
            else:
                gender = 'm'

            member = Member(
                id=row['ID_MEMBER'],
                username=row["memberName"],
                date_joined=self.TZ.localize(datetime.datetime.fromtimestamp(row['dateRegistered'])),
                last_activity=self.TZ.localize(datetime.datetime.fromtimestamp(row['lastLogin'])),
                first_name=row['realName'],
                password=row['passwd'],
                email=row['emailAddress'],
                gender=gender,
                birth_date=row['birthdate'],
                website=row['websiteUrl'],
                location=row['location'],
                icq=row['ICQ'])
            disable_auto_now(member)
            member.save()

    def import_shoutboxes(self):
        print "* Importing shoutboxes"
        rows = self._query("select * from smf_sp_shoutboxes")

        for row in rows:
            shoutbox = ShoutBox(
                id=row['ID_SHOUTBOX'],
                name=row['name'])
            shoutbox.save()

    def import_shouts(self):
        print "* Importing shouts"
        html_parser = HTMLParser.HTMLParser()
        rows = self._query("select * from smf_sp_shouts")

        for row in rows:
            try:
                member = Member.objects.get(id=row['ID_MEMBER'])
                shout = Shout(
                    id=row['ID_SHOUT'],
                    shoutbox=ShoutBox.objects.get(id=row['ID_SHOUTBOX']),
                    created_by=member,
                    created_at=self.TZ.localize(datetime.datetime.fromtimestamp(row['log_time'])),
                    body=html_parser.unescape(row['body']).replace("<br />", "\n"))

                disable_auto_now(shout)
                shout.save()
            except Member.DoesNotExist:
                pass

    def import_categories(self):
        print "* Importing categories"
        rows = self._query("select * from smf_categories")
        for row in rows:
            category = Category(
                id=row['ID_CAT'],
                name=row['name'],
                order=row['catOrder'])
            disable_auto_now(category)
            category.save()

    def import_boards(self):
        print "* Importing boards"
        rows = self._query("select * from smf_boards order by ID_PARENT")
        for row in rows:
            category = Category.objects.get(id=row['ID_CAT'])
            if row['ID_PARENT'] == 0:
                parent = None
            else:
                parent = Board.objects.get(id=row['ID_PARENT'])
            board = Board(
                id=row['ID_BOARD'],
                category=category,
                parent=parent,
                order=row['boardOrder'],
                name=row['name'],
                description=row['description'])
            disable_auto_now(board)
            board.save()

    def import_topics(self):
        print "* Importing topics"
        rows = self._query("select * from smf_topics")

        for row in rows:
            topic = Topic(
                id=row['ID_TOPIC'],
                is_sticky=row['isSticky'],
                board=Board.objects.get(id=row['ID_BOARD']))
            disable_auto_now(topic)
            topic.save()

    def import_posts(self):
        print "* Importing posts"
        rows = self._query("select * from smf_messages")
        html_parser = HTMLParser.HTMLParser()

        for row in rows:
            if row['ID_MEMBER'] != 0:
                member = Member.objects.get(id=row['ID_MEMBER'])
            else:
                member = None

            post = Post(
                id=row['ID_MSG'],
                topic=Topic.objects.get(id=row['ID_TOPIC']),
                created_at=self.TZ.localize(datetime.datetime.fromtimestamp(row['posterTime'])),
                created_by=member,
                subject=html_parser.unescape(row['subject'].replace("Re:", "")),
                body=html_parser.unescape(row['body']).replace("<br />", "\n"),
                icon=row['icon'])
            disable_auto_now(post)
            post.save()

    def fetch_attachments(self):
        if not os.access(self.ATTACHMENT_TEMP, os.R_OK):
            os.makedirs(self.ATTACHMENT_TEMP)
            subprocess.check_call([
                "scp",
                "-r",
                "thejester@timelord.de:/home/www/www.timelord.de/forum/attachments/*",
                self.ATTACHMENT_TEMP
            ])

    def import_attachments(self):
        print "* Importing attachments"
        rows = self._query("select * from smf_attachments")
        for row in rows:
            try:
                fname = glob.glob(os.path.join(self.ATTACHMENT_TEMP, "%s_*" % row['ID_ATTACH']))[0]
                if row['ID_MSG'] != 0:
                    if row["ID_THUMB"] != 0:
                        post = Post.objects.get(id=row['ID_MSG'])
                        attachment = Attachment(
                            post=post
                        )
                        with open(fname) as thefile:
                            attachment.image.save(row['filename'], File(thefile))
                        attachment.save()
                elif row['ID_MEMBER'] != 0:
                    member = Member.objects.get(id=row['ID_MEMBER'])
                    with open(fname) as thefile:
                        member.avatar.save(row['filename'], File(thefile))
            except IndexError:
                print "skipped", row


class Command(BaseCommand):
    help = "Import legacy smf forum"

    def handle(self, *args, **kwargs):
        importer = Importer()
        importer.import_members()
        importer.import_shoutboxes()
        importer.import_shouts()
        importer.import_categories()
        importer.import_boards()
        importer.import_topics()
        importer.import_posts()
        importer.fetch_attachments()
        importer.import_attachments()
