from typing import List, NamedTuple


class Table(NamedTuple):
    primary_key: str
    keys: List[str]
    locked: bool = True


TABLES = {
    "hiphopify": Table("user_id", sorted(["user_id", "end_timestamp", "forced_nick"])),
    "hiphopify_namelist": Table("name", sorted(["name", "image_url"]), locked=False),
    "oauth_data": Table("id", sorted(["id", "access_token", "expires_at", "refresh_token", "snowflake"])),
    "tags": Table("tag_name", sorted(["tag_name", "tag_content"]), locked=False),
    "users": Table("user_id", sorted(["user_id", "roles", "username", "discriminator", "email"])),
    "wiki": Table("slug", sorted(["slug", "headers", "html", "rst", "text", "title"])),
    "wiki_revisions": Table("id", sorted(["id", "date", "post", "slug", "user"])),
    "_versions": Table("table", sorted(["table", "version"]))
}
