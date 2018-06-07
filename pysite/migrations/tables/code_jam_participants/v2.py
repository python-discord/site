def run(db, table, table_obj):
    """
    GitHub usernames -> Store as GitLab username, this will be correct for most jammers
    """

    for document in db.get_all(table):
        if "github_username" in document:
            document["gitlab_username"] = document["github_username"]
            del document["github_username"]

            db.insert(table, document, conflict="replace", durability="soft")
    db.sync(table)
