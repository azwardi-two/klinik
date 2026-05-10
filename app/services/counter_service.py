from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app.models.counter import Counter


class CounterService:
    def __init__(self, db):
        self.db = db

    def _get_or_create_counter(self, key, period):
        counter = (
            self.db.query(Counter)
            .filter_by(key=key, period=period)
            .with_for_update()
            .first()
        )

        if not counter:
            try:
                counter = Counter(
                    key=key,
                    period=period,
                    last_value=0
                )
                self.db.add(counter)
                self.db.flush()
            except IntegrityError:
                self.db.rollback()
                counter = (
                    self.db.query(Counter)
                    .filter_by(key=key, period=period)
                    .with_for_update()
                    .first()
                )

        return counter

    def generate_no_rm(self):
        today = datetime.now().strftime("%Y%m%d")
        counter = self._get_or_create_counter("no_rm", today)
        counter.last_value += 1
        return f"{today}-{counter.last_value:03d}"

    def generate_no_reg(self):
        month = datetime.now().strftime("%Y%m")
        counter = self._get_or_create_counter("no_reg", month)
        counter.last_value += 1
        return f"{month}-{counter.last_value:03d}"

    def generate_no_tahunan(self):
        year = datetime.now().strftime("%Y")
        counter = self._get_or_create_counter("no_tahunan", year)
        counter.last_value += 1
        return f"{year}-{counter.last_value:03d}"