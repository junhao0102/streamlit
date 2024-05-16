from streamlit.testing.v1 import AppTest

def insert():
    # Create an instance of the app
    at = AppTest.from_file("app.py")
    # Test 
    at.run()
    
    at.input_text("insert_name", "lee")
    at.input_text("insert_phone", "0912345678")
    at.input_text("insert_email", "XXX@iii.org.tw")
    at.input_text("insert_address", "台北市")
    
    
def delete():
    # Create an instance of the app
    at = AppTest.from_file("app.py")
    # Test 
    at.run()
    
    at.input_text("delete_name", "lee")
    at.click("DELETE")
    at.assert_text("delete successfully")
    
    
def select():
    # Create an instance of the app
    at = AppTest.from_file("app.py")
    # Test 
    at.run()
    
    at.input_text("find_name", "lee")
    at.click("SELECT")
    at.assert_text("lee")
    
    