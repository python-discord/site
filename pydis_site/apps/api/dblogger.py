from logging import LogRecord, StreamHandler


class DatabaseLogHandler(StreamHandler):
    """Logs entries into the database."""

    def emit(self, record: LogRecord):
        """Write the given `record` into the database."""
        # This import needs to be deferred due to Django's application
        # registry instantiation logic loading this handler before the
        # application is ready.
        from pydis_site.apps.api.models.log_entry import LogEntry

        entry = LogEntry(
            application='site',
            logger_name=record.name,
            level=record.levelname.lower(),
            module=record.module,
            line=record.lineno,
            message=self.format(record)
        )
        entry.save()
