from app.extensions import db
from sqlalchemy.orm import aliased


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
    name: str = db.Column(db.Text)

    @property
    def serialized(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    national_pokedex_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    form_name = db.Column(db.Text)
    pokedex_entries = db.relationship("Pokedex", backref="pokemon", lazy=True)


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)


class Ability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)


class StatSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hp = db.Column(db.Integer)
    atk = db.Column(db.Integer)
    # def = db.Column(db.Integer)
    spa = db.Column(db.Integer)
    spd = db.Column(db.Integer)
    spe = db.Column(db.Integer)


class Pokedex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, db.ForeignKey("pokemon.id"))
    type_set_id = db.Column(db.Integer, db.ForeignKey("type_set.id"))
    ability_set_id = db.Column(db.Integer, db.ForeignKey("ability_set.id"))
    stat_set_id = db.Column(db.Integer, db.ForeignKey("stat_set.id"))


class TypeSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primary_type_id = db.Column(db.Integer, db.ForeignKey("type.id"))
    secondary_type_id = db.Column(db.Integer, db.ForeignKey("type.id"))


class AbilitySet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primary_ability_id = db.Column(db.Integer, db.ForeignKey("ability.id"))
    secondary_ability_id = db.Column(db.Integer, db.ForeignKey("ability.id"))
    hidden_ability_id = db.Column(db.Integer, db.ForeignKey("ability.id"))


class PokemonView(db.Model):
    name = db.Column(db.Text)
    form_name = db.Column(db.Text)
    primary_type_name = db.Column(db.Text)
    secondary_type_name = db.Column(db.Text)
    primary_ability_name = db.Column(db.Text)
    secondary_ability_name = db.Column(db.Text)
    hidden_ability_name = db.Column(db.Text)
    hp = db.Column(db.Integer)
    atk = db.Column(db.Integer)
    def_ = db.Column(db.Integer)
    spa = db.Column(db.Integer)
    spd = db.Column(db.Integer)
    spe = db.Column(db.Integer)

    @property
    def serialized(self):
        return {
            "name": self.name,
            "form_name": self.form_name,
            "primary_type_name": self.primary_type_name,
            "secondary_type_name": self.secondary_type_name,
            "primary_ability_name": self.primary_ability_name,
            "secondary_ability_name": self.secondary_ability_name,
            "hidden_ability_name": self.hidden_ability_name,
            "hp": self.hp,
            "atk": self.atk,
            "def": self.def_,
            "spa": self.spa,
            "spd": self.spd,
            "spe": self.spe
        }

