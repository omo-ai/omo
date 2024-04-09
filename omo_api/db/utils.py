import logging
from omo_api.db.connection import SessionLocal

logger = logging.getLogger(__name__)

def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance, False
    else:
        kwargs |= defaults or {}
        instance = model(**kwargs)
        try:
            session.add(instance) # try creating the instance
            session.commit()
        except Exception as e:
            logger.debug(f"Exception in get_or_create: {e}")
            session.rollback()
            instance = session.query(model).filter_by(**kwargs).one() # TODO revisit this section
            return instance, False
        else:
            return instance, True



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()