def run(db, table, table_obj):
    """
    Remove stored dates of birth from code jam participants
    """

    for document in db.get_all(table):
        if "dob" in document:
            del document["dob"]

            db.insert(table, document, conflict="replace", durability="soft")
    db.sync(table)
