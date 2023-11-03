import random
from datetime import datetime
from app.utils.audio_feature_utils import audio_feature_extractor

from app import db, create_app


class Song(db.Model):
    songId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    upload_date = db.Column(db.DateTime)
    duration_ms = db.Column(db.Integer)
    explicit = db.Column(db.Integer)
    mode = db.Column(db.Integer)
    key = db.Column(db.Integer)
    tempo = db.Column(db.Float)
    energy = db.Column(db.Float)
    danceability = db.Column(db.Float)
    loudness = db.Column(db.Float)
    acousticness = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    liveness = db.Column(db.Float)
    speechiness = db.Column(db.Float)
    valence = db.Column(db.Float)
    popularity = db.Column(db.Integer)
    filepath = db.Column(db.Text)

    def __repr__(self):
        return f"<Song {self.songId}>"

    @classmethod
    def create(cls, **kwargs):
        song = cls(upload_date=datetime.now(), popularity=0, **kwargs)
        db.session.add(song)
        db.session.commit()
        return song

    @classmethod
    def search_by_id(cls, song_id):
        song = db.session.get(cls, song_id)
        if song:
            song.popularity += 1
            db.session.commit()
        return song

    @classmethod
    def search_by_name(cls, name, increment_popularity=False, limit=100):
        query = cls.query.filter(cls.name.ilike(f"%{name}%"))

        if increment_popularity:
            for song in query.all():
                song.popularity += 1
            db.session.commit()

        query = query.order_by(cls.popularity.desc())
        if limit:
            query = query.limit(limit)

        return query.all()


if __name__ == "__main__":
    audio_path = "app/static/uploads/sample-12s.mp3"
    features = audio_feature_extractor(audio_path)
    song_details = {
        "name": "Song Name Here",
        "duration_ms": 200000,  # Example duration in ms
        "filepath": audio_path
    }
    song_data = {**song_details, **features}
    app = create_app('DevelopmentConfig')
    with app.app_context():
        # add song example
        S = Song()
        print(S.create(**song_data))
        # search song by name example
        matching_songs = Song.search_by_name("Song Name Here", limit=10)
        for song in matching_songs:
            print(song.name)
        # query song by id example
        print(song.search_by_id(1).name)