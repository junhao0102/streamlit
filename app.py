import psycopg2
import streamlit as st
from logger import logger


def get_db_connection():
    """建立並返回一個新的數據庫連接。"""
    return psycopg2.connect(
        dbname="mydb",
        user="postgres",
        password="mysecretpassword",
        host="db",
        port="5432",
    )


def create_table():
    """創建數據表，如果表不存在"""
    create_sql = """
        CREATE TABLE IF NOT EXISTS data(
            name VARCHAR(20),
            phone VARCHAR(50),
            email VARCHAR(50),
            address VARCHAR(50)
        )
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(create_sql)
            conn.commit()
    logger.info("create table successful!")


def select(name):
    """根據名稱查詢數據。"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM data WHERE name = %s;", (name,))
            data = cursor.fetchall()
            if not name:
                logger.error("Name cannot be empty")
                return "Can not be empty"
            elif not data:
                logger.error("Name does not exist")
                return "Name does not exist"
            else:
                logger.info("select successful!")
                return {
                    "name": data[0][0],
                    "phone": data[0][1],
                    "email": data[0][2],
                    "address": data[0][3],
                }


def insert(name, phone, email, address):
    """插入數據"""
    if not name or not phone or not email or not address:
        logger.error("Any field cannot be empty")
        return "Any field cannot be empty"

    if select(name) == "Name does not exist":
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO data VALUES (%s, %s, %s, %s);",
                    (name, phone, email, address),
                )
                conn.commit()
        logger.info("insert successful!")
        return "Insert successfully"
    else:
        logger.error("Name already exists")
        return "Name already exists"


def delete(name):
    """刪除數據"""
    if not name:
        logger.error("Name cannot be empty")
        return "Name cannot be empty"

    if select(name) == "Name does not exist":
        logger.error("Name does not exist")
        return "Name does not exist"
    else:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM data WHERE name = %s;", (name,))
                conn.commit()
        logger.info("delete successful!")
        return "Delete successfully"


# Streamlit App
def run_app():
    st.title("Enter your information!")
    name = st.text_input("Name", key="insert_name")
    phone = st.text_input("Phone", key="insert_phone")
    email = st.text_input("Email", key="insert_email")
    address = st.text_input("Address", key="insert_address")
    button_insert = st.button("INSERT")
    if button_insert:
        st.info(insert(name, phone, email, address))

    st.title("Delete your information!")
    delete_name = st.text_input("Name", key="delete_name")
    button_delete = st.button("DELETE")
    if button_delete:
        st.info(delete(delete_name))

    st.title("Find your information!")
    find_name = st.text_input("Name", key="find_name")
    button_select = st.button("SELECT")
    if button_select:
        st.info(select(find_name))


# 初始化數據表
if __name__ == "__main__":
    create_table()
    run_app()
