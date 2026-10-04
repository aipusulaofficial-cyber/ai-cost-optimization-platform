import math
import sqlite3


class PricingStore:
    def __init__(self, path="pricing.db"):
        self.path = path
        with sqlite3.connect(path) as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS pricing (provider TEXT NOT NULL, model TEXT NOT NULL, "
                "input_per_1k REAL NOT NULL, output_per_1k REAL NOT NULL, "
                "PRIMARY KEY(provider,model))"
            )

    def put(self, provider, model, input_per_1k, output_per_1k):
        if not isinstance(provider, str) or not provider.strip():
            raise ValueError("provider must be non-empty")
        if not isinstance(model, str) or not model.strip():
            raise ValueError("model must be non-empty")
        rates = (input_per_1k, output_per_1k)
        if any(
            isinstance(rate, bool)
            or not isinstance(rate, (int, float))
            or not math.isfinite(rate)
            or rate < 0
            for rate in rates
        ):
            raise ValueError("pricing must be finite and non-negative")
        with sqlite3.connect(self.path) as db:
            db.execute(
                "INSERT OR REPLACE INTO pricing VALUES(?,?,?,?)",
                (provider, model, input_per_1k, output_per_1k),
            )

    def get(self, provider, model):
        with sqlite3.connect(self.path) as db:
            return db.execute(
                "SELECT provider,model,input_per_1k,output_per_1k FROM pricing "
                "WHERE provider=? AND model=?",
                (provider, model),
            ).fetchone()
