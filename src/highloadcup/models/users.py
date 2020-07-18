from . import db


# TODO: Explore bakery


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger(), primary_key=True)
    # TODO: Swap to hashing?
    email = db.Column(db.Unicode(100), unique=True)
    first_name = db.Column(db.Unicode(50))
    last_name = db.Column(db.Unicode(50))
    gender = db.Column(db.String(1))
    birth_date = db.Column(db.BigInteger())


class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.BigInteger(), primary_key=True)
    place = db.Column(db.UnicodeText())
    country = db.Column(db.Unicode(50))
    city = db.Column(db.Unicode(50))
    distance = db.Column(db.BigInteger())


class Visit(db.Model):
    __tablename__ = "visits"

    id = db.Column(db.BigInteger(), primary_key=True)
    location = db.Column(db.BigInteger(), db.ForeignKey("locations.id"))
    user = db.Column(db.BigInteger(), db.ForeignKey("users.id"))
    visited_at = db.Column(db.BigInteger())
    mark = db.Column(db.Integer())
