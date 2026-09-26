import sqlite3


class PricingStore:
    def __init__(self,path="pricing.db"):
        self.path=path
        with sqlite3.connect(path) as db: db.execute("CREATE TABLE IF NOT EXISTS pricing (provider TEXT, model TEXT, input_per_1k REAL NOT NULL, output_per_1k REAL NOT NULL, PRIMARY KEY(provider,model))")
    def put(self,provider,model,input_per_1k,output_per_1k):
        if input_per_1k<0 or output_per_1k<0: raise ValueError("pricing must be non-negative")
        with sqlite3.connect(self.path) as db: db.execute("INSERT OR REPLACE INTO pricing VALUES(?,?,?,?)",(provider,model,input_per_1k,output_per_1k))
    def get(self,provider,model):
        with sqlite3.connect(self.path) as db: return db.execute("SELECT provider,model,input_per_1k,output_per_1k FROM pricing WHERE provider=? AND model=?",(provider,model)).fetchone()
