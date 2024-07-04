class TestAppRouter:
    def db_for_read(self, model, **hints):
        return "other"

    def db_for_write(self, model, **hints):
        return "other"

    def allow_relation(self, *args, **kwargs):
        return True

    def allow_syncdb(self, *args, **kwargs):
        return True

    def allow_migrate(self, *args, **kwargs):
        return True
