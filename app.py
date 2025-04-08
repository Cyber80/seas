import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import os

def connect_to_gsheet():
    try:
        # ตรวจสอบว่าอยู่ใน Streamlit Cloud หรือไม่
        if st.secrets.get("gcp_service_account"):
            # ใช้ Secrets ของ Streamlit
            creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        else:
            # ใช้ไฟล์ credentials.json ในเครื่อง
            creds = Credentials.from_service_account_file(".streamlit/credentials.json")
        
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")
        return None

def main():
    st.title("ระบบจัดการนักเรียน")
    
    client = connect_to_gsheet()
    if client:
        st.success("เชื่อมต่อกับ Google Sheets เรียบร้อยแล้ว!")
        # ดำเนินการต่อ...
    else:
        st.warning("โหมดทดสอบ: ใช้ข้อมูลตัวอย่าง")
        # แสดงข้อมูลตัวอย่าง...

if __name__ == "__main__":
    main()