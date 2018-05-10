# coding=utf-8


def run(db, table, primary_key):
    for document in db.pluck(table, primary_key, "title"):
        if not document.get("title"):
            document["title"] = "No Title"

            db.insert(table, document, conflict="update", durability="soft")
    db.sync(table)
