import json

from flask import g, Flask
from sqlalchemy import MetaData, Table, create_engine, Column, Integer, Unicode, select, insert, update, delete, \
    bindparam, TEXT

from imagevision.injector import inject

metadata = MetaData()

image = Table('image', metadata,
              Column('image_id', Integer, primary_key=True, autoincrement=True),
              Column('image_file_name', Unicode(255), nullable=False),
              Column('image_mime_type', Unicode(255), nullable=False),
              Column('image_annotations', TEXT, nullable=True))


def create_database(database_uri):
    engine = create_engine(database_uri)
    metadata.bind = engine
    metadata.create_all(checkfirst=True)


def drop_database(database_uri):
    engine = create_engine(database_uri)
    metadata.bind = engine
    metadata.drop_all()


def open_connection(database_uri):
    if not hasattr(g, 'database_connection'):
        engine = create_engine(database_uri)
        g.database_connection = engine.connect()

    return g.database_connection


def close_connection(error):
    if hasattr(g, 'database_connection'):
        g.database_connection.close()


def setup_database(app):

    def create_db():
        create_database(app.config['DATABASE_URI'])

    def drop_db():
        drop_database(app.config['DATABASE_URI'])

    app.cli.command()(create_db)
    app.cli.command()(drop_db)

    app.teardown_appcontext(close_connection)


class ImageRepository(object):
    """
    A class for storing and retrieving images data.
    """

    all_columns = [image.c.image_id, image.c.image_file_name, image.c.image_mime_type, image.c.image_annotations]

    @inject(app=Flask)
    def __init__(self, app):
        self.database_uri = app.config['DATABASE_URI']

    @property
    def connection(self):
        return open_connection(self.database_uri)

    def create_image(self, file_name, mime_type):
        stmt = insert(image).\
               values(dict(image_file_name=file_name,
                           image_mime_type=mime_type))
        result = self.connection.execute(stmt)
        return result.inserted_primary_key[0]

    def get_image(self, image_id):
        stmt = select(self.all_columns).\
               where(image.c.image_id == image_id)
        result = self.connection.execute(stmt)
        row = result.fetchone()
        result.close()
        if row is None:
            return None

        return self._format_row(row)

    def get_images(self, offset, limit):
        stmt = select(self.all_columns).order_by(image.c.image_id).offset(offset).limit(limit)
        result = self.connection.execute(stmt)
        rows = result.fetchall()
        result.close()
        return [self._format_row(row) for row in rows]

    def annotate_image(self, image_id, annotations):
        stmt = update(image).\
               where(image.c.image_id == bindparam('id')).\
               values(dict(image_annotations=self._serialize_annotations(annotations)))
        self.connection.execute(stmt, id=image_id)

    def delete_image(self, image_id):
        stmt = delete(image).where(image.c.image_id == bindparam('id'))
        self.connection.execute(stmt, dict(id=image_id))

    def _format_row(self, row):
        result = dict(row)
        if 'image_annotations' in result:
            result['image_annotations'] = self._deserialize_annotations(result['image_annotations'])

        return result

    def _serialize_annotations(self, annotations):
        return json.dumps(annotations)

    def _deserialize_annotations(self, annotations):
        return json.loads(annotations)
