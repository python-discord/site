def run(db, table, table_obj):
    """
    Remove stored email addresses from every user document - "apparently `update` doesn't update" update
    """

    for document in db.get_all(table):
        if "email" in document:
            del document["email"]

            db.insert(table, document, conflict="replace", durability="soft")
    db.sync(table)
