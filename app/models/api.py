from app.extensions import db


class Pokedex(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(150))
    content: str = db.Column(db.Text)


class Pokemon(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(150))


class Game(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(150))

    @property
    def serialized(self):
        return {
            "id": self.id,
            "name": self.name
        }


class GamePokedex(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    game_id: int = db.Column(db.Integer)
    name: str = db.Column(db.String(150))

    @property
    def serialized(self):
        return {
            "id": self.id,
            "name": self.name
        }
