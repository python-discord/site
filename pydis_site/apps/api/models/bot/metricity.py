from django.db import connections


class NotFound(Exception):
    """Raised when an entity cannot be found."""

    pass


class Metricity:
    """Abstraction for a connection to the metricity database."""

    def __init__(self):
        self.cursor = connections['metricity'].cursor()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.cursor.close()

    def user(self, user_id: str) -> dict:
        """Query a user's data."""
        columns = ["verified_at"]
        query = f"SELECT {','.join(columns)} FROM users WHERE id = '%s'"
        self.cursor.execute(query, [user_id])
        values = self.cursor.fetchone()

        if not values:
            raise NotFound()

        return dict(zip(columns, values))

    def total_messages(self, user_id: str) -> int:
        """Query total number of messages for a user."""
        self.cursor.execute(
            "SELECT COUNT(*) FROM messages WHERE author_id = '%s' AND NOT is_deleted",
            [user_id]
        )
        values = self.cursor.fetchone()

        if not values:
            raise NotFound()

        return values[0]
