import pandas as pd
from pandas.testing import assert_frame_equal

from tests.integration.fixtures import DaskTestCase


class GroupbyTestCase(DaskTestCase):
    def test_group_by(self):
        df = self.c.sql(
            """
        SELECT
            user_id, SUM(c) AS S
        FROM user_table_1
        GROUP BY user_id
        """
        )
        df = df.compute()

        expected_df = pd.DataFrame({"user_id": [2, 1], "S": [4, 3]})
        assert_frame_equal(df, expected_df)

    def test_group_by_all(self):
        df = self.c.sql(
            """
        SELECT
            SUM(c) AS S, SUM(2) AS X
        FROM user_table_1
        """
        )
        df = df.compute()

        expected_df = pd.DataFrame({"S": [7], "X": [6]})
        expected_df["S"] = expected_df["S"].astype("int64")
        expected_df["X"] = expected_df["X"].astype("int32")
        assert_frame_equal(df, expected_df)

    def test_group_by_case(self):
        df = self.c.sql(
            """
        SELECT
            user_id + 1, SUM(CASE WHEN c = 3 THEN 1 END) AS S
        FROM user_table_1
        GROUP BY user_id + 1
        """
        )
        df = df.compute()

        expected_df = pd.DataFrame({"EXPR$0": [3, 2], "S": [1, 1]})
        expected_df["EXPR$0"] = expected_df["EXPR$0"].astype("int64")
        expected_df["S"] = expected_df["S"].astype("float64")
        assert_frame_equal(df, expected_df)

    def test_group_by_nan(self):
        df = self.c.sql(
            """
        SELECT
            c
        FROM user_table_nan
        GROUP BY c
        """
        )
        df = df.compute()

        expected_df = pd.DataFrame({"c": [3, 1]})
        expected_df["c"] = expected_df["c"].astype("float64")
        assert_frame_equal(df, expected_df)

        df = self.c.sql(
            """
        SELECT
            c
        FROM user_table_inf
        GROUP BY c
        """
        )
        df = df.compute()

        expected_df = pd.DataFrame({"c": [3, 1, float("inf")]})
        expected_df["c"] = expected_df["c"].astype("float64")
        assert_frame_equal(df, expected_df)