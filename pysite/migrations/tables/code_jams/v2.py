def run(db, table, table_obj):
    """
    Clean list of teams from teams that do not exist anymore.
    """
    for document in db.get_all(table):
        for team_id in document["teams"]:
            if db.get("code_jam_teams", team_id) is None:
                document["teams"].remove(team_id)
            db.insert(table, document, conflict="update", durability="soft")
    db.sync(table)
