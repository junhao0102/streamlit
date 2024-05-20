import unittest
import time
import pytest
from unittest.mock import patch
from app import select, insert, delete, run_app
from streamlit.testing.v1 import AppTest


class TestSQL(unittest.TestCase):
    # ----------------測試select函數--------------------
    @patch("app.get_db_connection")
    def test_select_empty(self, mock_get_db_connection):
        # 測試 select 函數當 name 為空時
        result = select("")
        expect = "Can not be empty"
        self.assertEqual(result, expect)

    @patch("app.get_db_connection")
    def test_select_exist(self, mock_get_db_connection):
        # 測試 select 函數當數據存在時
        mock_cursor = (
            mock_get_db_connection.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value
        )
        mock_cursor.fetchall.return_value = [
            ("John Doe", "0900000000", "XXX@gamil.com", "Taipei City")
        ]
        result = select("John Doe")
        expect = {
            "name": "John Doe",
            "phone": "0900000000",
            "email": "XXX@gamil.com",
            "address": "Taipei City",
        }
        self.assertEqual(result, expect)

    @patch("app.get_db_connection")
    def test_select_non_exist(self, mock_get_db_connection):
        # 測試 select 函數當數據不存在時
        mock_cursor = (
            mock_get_db_connection.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value
        )
        mock_cursor.fetchall.return_value = []
        result = select("name")
        expect = "Name does not exist"
        self.assertEqual(result, expect)

    # ----------------測試insert函數--------------------
    @patch("app.get_db_connection")
    @patch("app.select")
    def test_insert_success(self, mock_select, mock_get_db_connection):
        # 測試 insert 函數當數據不存在時
        mock_select.return_value = "Name does not exist"
        result = insert("John Doe", "1234567890", "john@example.com", "1234 Main St")
        expect = "Insert successfully"
        self.assertEqual(result, expect)

    @patch("app.select")
    def test_insert_fail(self, mock_select):
        # 測試 insert 函數當數據已存在時
        mock_select.return_value = {
            "name": "alice",
            "phone": "0911111111",
            "email": "alice@example.com",
            "address": "Taichung",
        }
        result = insert("alice", "0911111111", "alice@example.com", "Taichung")
        expect = "Name already exists"
        self.assertEqual(result, expect)

    # ----------------測試delete函數--------------------
    def test_delete_empty(self):
        # 測試 delete 函數當 name 為空時
        result = delete("")
        expect = "Name cannot be empty"
        self.assertEqual(result, expect)

    @patch("app.get_db_connection")
    @patch("app.select")
    def test_delete_success(self, mock_select, mock_get_db_connection):
        # 測試 delete 函數當數據存在時
        mock_select.return_value = {
            "name": "Tom",
            "phone": "0922222222",
            "email": "Tom@example.com",
            "address": "Xinyi",
        }
        mock_cursor = (
            mock_get_db_connection.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value
        )
        result = delete("Tom")
        expect = "Delete successfully"
        self.assertEqual(result, expect)
        # 測試是否有呼叫 cursor.execute 和 commit
        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM data WHERE name = %s;", ("Tom",)
        )
        mock_get_db_connection.return_value.__enter__.return_value.commit.assert_called_once()

    @patch("app.get_db_connection")
    def test_delete_fail(self, mock_get_db_connection):
        # 測試 delete 函數當數據不存在時
        mock_cursor = (
            mock_get_db_connection.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value
        )
        mock_cursor.fetchall.return_value = []
        result = delete("name")
        expect = "Name does not exist"
        self.assertEqual(result, expect)

if __name__ == "__main__":
    unittest.main()
