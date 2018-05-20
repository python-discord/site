from tests import SiteTest

class DatabaseTests(SiteTest):
    """ Test cases for the database module """
    def test_table_actions(self):
        import string
        import secrets
        from pysite.database import RethinkDB

        alphabet = string.ascii_letters
        generated_table_name = ''.join(secrets.choice(alphabet) for i in range(8))

        rdb = RethinkDB()
        # Create table name and expect it to work
        result = rdb.create_table(generated_table_name)
        self.assertEqual(result, True)

        # Create the same table name and expect it to already exist
        result = rdb.create_table(generated_table_name)
        self.assertEqual(result, False)

        # Drop table and expect it to work
        result = rdb.drop_table(generated_table_name)
        self.assertEqual(result, True)

        # Drop the same table and expect it to already be gone
        result = rdb.drop_table(generated_table_name)
        self.assertEqual(result, False)

        # This is to get some more code coverage
        self.assertEqual(rdb.teardown_request('_'), None)
