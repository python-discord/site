def run(db, table, table_obj):
    """
    Associate the ID of each team's code jam (team -> jam)
    """

    for document in db.get_all(table):
        if "jam" not in document:
            # find the code jam containing this team
            for jam in db.get_all("code_jams"):
                if document["id"] in jam["teams"]:
                    document["jam"] = jam["number"]
                    db.insert(table, document, conflict="update", durability="soft")
