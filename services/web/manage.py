from flask.cli import FlaskGroup

from project import app, db, GroundStation, Measure


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    station = GroundStation(type="fake", active=False, lat=-30.0, lon=30.0)
    db.session.add(station)
    db.session.commit()
    measure = Measure(type="pm25", value=12.5, time="right now",
                      station_id=station.id)
    db.session.add(measure)
    db.session.commit()


if __name__ == "__main__":
    cli()
