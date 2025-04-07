from app.extensions import db


class Pokedex(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(150))
    content: str = db.Column(db.Text)

    def __repr__(self):
        return f'<Post "{self.title}">'


class Pokemon(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(150))


class Game(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(150))


class GamePokedex(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(150))
