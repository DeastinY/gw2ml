import sqlite3
from pathlib import Path
from gw2spidy import Gw2Spidy
from tqdm import tqdm

FILE_DB = Path("db.sqlite")


def save(data):
    conn = sqlite3.connect(str(FILE_DB))
    if not FILE_DB.exists():
        conn.execute('''CREATE TABLE data
                        (int id, string name, int sell_price, int buy_price, 
                        date last_update, int demand, int supply)''')
    c = conn.cursor()
    c.executemany('INSERT INTO data VALUES (?,?,?,?,?,?,?)', data)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    spidy = Gw2Spidy()
    data = []
    for item in tqdm(spidy.getAllItemsList()):
        if item["max_offer_unit_price"] != 0 and item["min_sale_unit_price"] != 0:
            data.append(
                (
                    item["data_id"],
                    item["name"],
                    item["min_sale_unit_price"],
                    item["min_sale_unit_price"],
                    item["price_last_changed"],
                    item["sale_availability"],
                    item["offer_availability"]
                )
            )
    save(data)



