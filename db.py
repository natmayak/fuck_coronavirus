from pymongo import MongoClient
import settings

db = MongoClient(settings.MONGO_LINK)[settings.MONGO_DB]


def get_or_create_user(db, effective_user):
    user_in_db = db.users.find_one({'user_id': effective_user.id})
    if not user_in_db:
        user_in_db = {'user_id': effective_user.id, 'subscribed': False}
        db.users.insert_one(user_in_db)


# def toogle_subscription(coll, update):
#
