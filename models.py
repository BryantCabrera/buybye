import datetime #to make timestamps for our posts
from peewee import * #to talk to database

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('buybye.db')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=70)
    member_since = DateTimeField(default=datetime.datetime.now)
    id_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE 
        ##can give it value of DATABASE we want to use
        ##lets our model talk to whatever database we want to create

    ##lets user retrieve their post
    def get_posts(self):
        return Post.select().where(Post.user == self)

    # def get_stream(self):
    #     return Post.select().where(
    #         (Post.user == self)
    #     )

    @classmethod
    ##1st parameter = class itself
    def create_user(cls, username, email, password, admin=False):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password), 
                is_admin=admin
            )
        except IntegrityError:
            raise ValueError('User already Exists')

class Post(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        model=User,
        backref='posts'
    )
    content = TextField()
    img = TextField()

    class Meta:
        database = DATABASE
        ##takes in a tuple
        ##need a trailing comma or else it won't create the tuple
        ##shows most recent post first
        order_by = ('-timestamp',)


#connects to and creates our tables in Sqlite
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post], safe=True)
    DATABASE.close()