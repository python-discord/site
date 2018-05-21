def run(db, table, table_obj):
    """
    Ensure that there are no wiki articles that don't have titles
    """

    for document in db.pluck(table, table_obj.primary_key, "title"):
        if not document.get("title"):
            document["title"] = "No Title"

            db.insert(table, document, conflict="update", durability="soft")
    db.sync(table)
