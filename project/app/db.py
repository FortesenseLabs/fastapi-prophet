import os

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine)
from sqlalchemy.sql import func

from databases import Database


DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()
predictions = Table(
        "predictions",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("ticker", String(6)),
        Column("prediction", String),
        Column("created_date", DateTime, default=func.now(), nullable=False),
        )

# databases query builder
database = Database(DATABASE_URL)