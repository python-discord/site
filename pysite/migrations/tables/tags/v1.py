def run(db, table, table_obj):
    """
    Ensure that there are no tags that don't have image URLs
    """

    for tag in db.pluck(table, table_obj.primary_key, 'image_url'):
        if 'image_url' not in tag:
            tag['image_url'] = None

            db.insert(table, tag, conflict="update", durability="soft")
    db.sync(table)
