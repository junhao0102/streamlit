import unittest
from unittest.mock import patch, MagicMock
from app import select, insert, delete


class TestDatabaseOperations(unittest.TestCase):

    @patch("app.get_db_connection")
    def setUp(self, mock_get_db_connection):
        # 創建模擬的數據庫連接和游標
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        mock_get_db_connection.return_value = self.mock_conn
        self.mock_conn.cursor.return_value.__enter__.return_value = self.mock_cursor

        # 清理數據庫，確保測試數據不重複
        self.mock_cursor.execute("TRUNCATE TABLE data;")
        self.mock_conn.commit()

        # 添加調試信息
        print("Setup complete: Database cleared")

    @patch("app.get_db_connection")
    def test_insert(self, mock_get_db_connection):
        # 設置模擬對象
        mock_get_db_connection.return_value = self.mock_conn

        # 模擬 select 查詢的返回值
        self.mock_cursor.fetchall.return_value = []

        # 添加調試信息
        print(
            "Mocked fetchall return value for insert test:",
            self.mock_cursor.fetchall.return_value,
        )

        # 測試插入數據
        result = insert("Test Name", "1234567890", "test@example.com", "123 Test St")

        # 添加調試信息
        print("Insert result:", result)

        # 檢查結果
        self.assertEqual(result, "Insert successfully")

        # 檢查 SQL 執行是否正確
        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO data VALUES (%s, %s, %s, %s);",
            ("Test Name", "1234567890", "test@example.com", "123 Test St"),
        )

        # 檢查事務提交
        self.mock_conn.commit.assert_called()

    @patch("app.get_db_connection")
    def test_delete(self, mock_get_db_connection):
        # 設置模擬對象
        mock_get_db_connection.return_value = self.mock_conn

        # 模擬 select 查詢的返回值，表示名稱存在
        self.mock_cursor.fetchall.return_value = [
            ("Test Name", "1234567890", "test@example.com", "123 Test St")
        ]

        # 添加調試信息
        print(
            "Mocked fetchall return value for delete test:",
            self.mock_cursor.fetchall.return_value,
        )

        # 測試刪除數據
        result = delete("Test Name")

        # 添加調試信息
        print("Delete result:", result)

        # 檢查結果
        self.assertEqual(result, "Delete successfully")

        # 檢查 SQL 執行是否正確
        self.mock_cursor.execute.assert_any_call(
            "DELETE FROM data WHERE name = %s;", ("Test Name",)
        )

        # 檢查事務提交
        self.mock_conn.commit.assert_called()


if __name__ == "__main__":
    unittest.main()
