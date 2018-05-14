def run(db, table, table_obj):
    for document in db.pluck(table, table_obj.primary_key, "title"):
        if not document.get("title"):
            document["title"] = "No Title"

            db.insert(table, document, conflict="update", durability="soft")
    db.sync(table)
