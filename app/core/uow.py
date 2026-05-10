class UnitOfWork:
    def __init__(self, db):
        self.db = db

    def __enter__(self):
        return self

    def __exit__(self, exc_type, *_):
        if exc_type:
            self.rollback()
        else:
            self.commit()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def flush(self):
        self.db.flush()