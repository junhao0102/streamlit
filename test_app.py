import unittest
from unittest.mock import patch
from app import select, insert, delete


class TestSelectFunction(unittest.TestCase):
    @patch("app.get_db_connection")
    def test_select_empty(self, mock_get_db_connection):
        # 模擬資料庫連接以防止任何實際的資料庫操作
        mock_connection = mock_get_db_connection.return_value.__enter__.return_value
        mock_cursor = mock_connection.cursor.return_value.__enter__.return_value

        # 測試 select 函數
        result = select("")
        expect = "Can not be empty"
        assert result == expect

    @patch("app.get_db_connection")
    def test_select_exist(self, mock_get_db_connection):
        # 模擬資料庫連接以防止任何實際的資料庫操作
        mock_connection = mock_get_db_connection.return_value.__enter__.return_value
        mock_cursor = mock_connection.cursor.return_value.__enter__.return_value
        mock_cursor.fetchall.return_value = [
            ("John Doe", "0900000000", "XXX@gamil.com", "Taipei City")
        ]
        # 測試 select 函數
        result = select("John Doe")
        expect = {
            "name": "John Doe",
            "phone": "0900000000",
            "email": "XXX@gamil.com",
            "address": "Taipei City",
        }
        assert result == expect

    @patch("app.get_db_connection")
    def test_select_non_exist(self, mock_get_db_connection):
        # 模擬資料庫連接以防止任何實際的資料庫操作
        mock_connection = mock_get_db_connection.return_value.__enter__.return_value
        mock_cursor = mock_connection.cursor.return_value.__enter__.return_value

        # 模擬沒有找到數據
        mock_cursor.fetchall.return_value = []

        # 測試 select 函數
        result = select("name")
        expect = "Name does not exist"
        assert result == expect

    # @patch('app.get_db_connection')
    # @patch('app.select')
    # def test_insert_success(self, mock_select, mock_get_db_connection):
    #     # 設置模擬的返回值
    #     mock_select.return_value = "Name does not exist"
    #     # 設置模擬資料庫連接
    #     mock_connection = mock_get_db_connection.return_value.__enter__.return_value
    #     # 設置模擬資料庫游標
    #     mock_cursor = mock_connection.cursor.return_var.__enter__.return_value
    #     # 設置模擬游標執行的返回值
    #     mock_cursor.execute.return_value = None

    #     # 測試 insert 函數
    #     result = insert("John Doe", "1234567890", "john@example.com", "1234 Main St")
    #     self.assertEqual(result, "Insert successfully")


if __name__ == "__main__":
    unittest.main()
