def run(db, table, table_obj):
    for document in db.get_all(table):
        if "email" in document:
            del document["email"]

            db.insert(table, document, conflict="update", durability="soft")
    db.sync(table)
