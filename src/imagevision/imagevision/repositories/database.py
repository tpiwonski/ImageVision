from sqlalchemy import MetaData, Table, create_engine, Column, Integer, JSON, Unicode, select, insert, update, delete, \
    bindparam

metadata = MetaData()

image = Table('image', metadata,
              Column('image_id', Integer, primary_key=True, autoincrement=True),
              Column('image_file_name', Unicode(255), nullable=False),
              Column('image_mime_type', Unicode(255), nullable=False),
              Column('image_annotations', JSON, nullable=True))


def create_database(database_uri):
    engine = create_engine(database_uri)
    metadata.bind = engine
    metadata.create_all(checkfirst=True)


def drop_database(database_uri):
    engine = create_engine(database_uri)
    metadata.bind = engine
    metadata.drop_all()


def setup_database(app):

    def create_db():
        create_database(app.config['DATABASE_URI'])

    def drop_db():
        drop_database(app.config['DATABASE_URI'])

    app.cli.command()(create_db)
    app.cli.command()(drop_db)


class ImageRepository(object):

    all_columns = [image.c.image_id, image.c.image_file_name, image.c.image_mime_type, image.c.image_annotations]

    def __init__(self, database_uri):
        self.engine = create_engine(database_uri)
        self.connection = self.engine.connect()

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
        return dict(row)

    def get_images(self, offset, limit):
        stmt = select(self.all_columns).order_by(image.c.image_id).offset(offset).limit(limit)
        result = self.connection.execute(stmt)
        rows = result.fetchall()
        result.close()
        return [dict(row) for row in rows]

    def annotate_image(self, image_id, annotations):
        stmt = update(image).\
               where(image.c.image_id == bindparam('id')).\
               values(dict(image_annotations=annotations))
        self.connection.execute(stmt, id=image_id)

    def delete_image(self, image_id):
        stmt = delete(image).where(image.c.image_id == bindparam('id'))
        self.connection.execute(stmt, dict(id=image_id))
