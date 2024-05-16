import psycopg2
import streamlit as st

# 连接到 PostgreSQL 数据库
conn = psycopg2.connect(
        dbname="mydb",
        user="postgres",
        password="mysecretpassword",
        host="db",
        port="5432"
    )

# 创建游标对象
cursor = conn.cursor()
    
#init
def create_table():
    # 创建表
    create_sql = """
        CREATE TABLE IF NOT EXISTS data(
            name VARCHAR(20),
            phone VARCHAR(50),
            email VARCHAR(50),
            address VARCHAR(50)
        )
    """
    cursor.execute(create_sql)
    # 提交事务
    conn.commit()
    # 关闭游标和连接
    cursor.close()
    conn.close()
    print("initial successfully")
    
# 查询数据 (name為parameter)
def select(name):
    cursor.execute(f"SELECT * FROM data WHERE name = '{name}';")
    data = cursor.fetchall()
    if name == '':
        return 'Can not be empty'
    elif data == []:
        return 'Name is not exist'
    else:
        print(data)
        return {'name': data[0][0], 'phone': data[0][1], 'email': data[0][2], 'address': data[0][3]}   
# 插入数据
def insert (name, phone, email, address):
   _name = select(name)
   if name == '' or phone == '' or email == '' or address == '':
         return 'Any block cannot be empty'
   elif _name == 'Name is not exist':
         cursor.execute(f"INSERT INTO data VALUES ('{name}', '{phone}', '{email}', '{address}');")
         return 'insert successfully'
   else:
        return 'Name is exist'
   
    
# 刪除数据(name為parameter)
def delete(name):
    _name = select(name)
    if name == '':
        return 'Can not be empty'
    elif _name == 'Name is not exist':
        return 'Name is not exist'
    else:
        cursor.execute(f"DELETE FROM data WHERE name = '{name}';")
        return 'delete successfully'
  
                
#streamlit

 
#插入資料
st.title("Inter your information!")
name = st.text_input("Name",key="insert_name")
phone = st.text_input("Phone",key="insert_phone")
email = st.text_input("Email",key="insert_email")
address = st.text_input("Address",key="insert_address")
button_insert = st.button("INSERT")
if button_insert:
    st.write(insert(name, phone, email, address))
   
#刪除資料  
st.title("Delete your information!")
delete_name = st.text_input("Name",key="delete_name")
button_delete = st.button("DELETE")
if button_delete:
    st.write(delete(delete_name))
    
#查詢資料  
st.title("Find your information!")
find_name = st.text_input("Name",key="find_name")
button_SELECT = st.button("SELECT") 
if button_SELECT:
    st.write(select(find_name))
    
if __name__ == "__main__":
    create_table()