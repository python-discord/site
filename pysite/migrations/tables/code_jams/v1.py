def run(db, table, table_obj):
    """
    Add "teams" list to jams without it
    """

    for document in db.get_all(table):
        if "teams" not in document:
            document["teams"] = []

            db.insert(table, document, conflict="replace", durability="soft")
    db.sync(table)
