from FlaskApp.models import *
from FlaskApp import app
import sys

def create_db():

    with app.app_context():
        db.create_all()


def drop_db():
    with app.app_context():
        db.drop_all()
        db.session.commit()



def create_users():
    with app.app_context():
        user = User(username='kite', email='kite@gmail.con', password='1234')
        db.session.add(user)
        db.session.commit()




def create_post():
    with app.app_context():
        user = User.query.filter_by(id=4).first()
        post1 = Post(title='Post number 1', content='one one one', user_id=user.id)
        post2 = Post(title='Post number 1', content='one one one', user_id=user.id)
        post3 = Post(title='Post number 1', content='one one one', user_id=user.id)
        db.session.add(post1)
        db.session.add(post2)
        db.session.add(post3)
        db.session.commit()

def read_users():
    with app.app_context():
        user = User.query.all()
        for ele in user:
            print(ele)
        # for post in user.posts:
        #     print(post.title)

def read_posts():
    with app.app_context():
        user = User.query.filter_by(id=1).first()
        for ele in user.posts:
            print(ele)
        # for post in user.posts:
        #     print(post.title)


def friends():
    with app.app_context():
        user = Friendship.query.all()
        for ele in user:
            print(ele.user_id, ele.friend_id)
        # for post in user.posts:
        #     print(post.title)

def delete_users():
    with app.app_context():
        user = User.query.filter_by(id=1).first()
        print(user)
        db.session.delete(user)
        db.session.commit()
        # for post in user.posts:
        #     print(post.title)


if __name__ == '__main__':
    globals()[sys.argv[1]]()