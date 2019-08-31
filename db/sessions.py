from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import config


def get():
    Session = sessionmaker(autocommit=False,
                           autoflush=False,
                           bind=create_engine(config.DB_URI))
    session = scoped_session(Session)

    return session
