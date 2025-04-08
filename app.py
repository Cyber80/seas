import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="ระบบคัดเลือกนักเรียนเพื่อสอบเข้า ม.1 และ ม.4 โรงเรียนสระแก้ว",
    page_icon="🏫",
    layout="wide"
)

# ส่วนหัวของแอปพลิเคชัน
st.title("🏫 ระบบคัดเลือกนักเรียนเพื่อสอบเข้า ม.1 และ ม.4 sk")
st.markdown("---")

# ข้อมูลตัวอย่าง (ในระบบจริงควรเชื่อมต่อฐานข้อมูล)
@st.cache_data
def load_sample_data():
    data = {
        'รหัสนักเรียน': ['S001', 'S002', 'S003', 'S004', 'S005'],
        'ชื่อ-สกุล': ['สมชาย ใจดี', 'สมหญิง สวยงาม', 'สมคิด ฉลาด', 'สมศรี เก่งมาก', 'สมาน มานะ'],
        'ระดับชั้นที่สมัคร': ['ม.1', 'ม.4', 'ม.1', 'ม.4', 'ม.1'],
        'คะแนนคณิตศาสตร์': [85, 72, 90, 68, 78],
        'คะแนนวิทยาศาสตร์': [80, 75, 88, 70, 82],
        'คะแนนภาษาไทย': [75, 80, 72, 85, 78],
        'คะแนนภาษาอังกฤษ': [70, 68, 75, 72, 80],
        'คะแนนสัมภาษณ์': [20, 18, 19, 17, 20],
        'สถานะ': ['ผ่าน', 'รอตรวจสอบ', 'ผ่าน', 'ไม่ผ่าน', 'ผ่าน']
    }
    return pd.DataFrame(data)
global df
df = load_sample_data()

# เมนูด้านข้าง
menu = st.sidebar.selectbox("เมนูหลัก", ["หน้าหลัก", "ลงทะเบียนนักเรียน", "ตรวจสอบผลคัดเลือก", "ตั้งเกณฑ์คัดเลือก", "รายงานผล"])

if menu == "หน้าหลัก":
    st.subheader("ยินดีต้อนรับสู่ระบบคัดเลือกนักเรียน sk")
    st.image("https://img.freepik.com/free-vector/school-building-educational-institution-college_107791-1051.jpg", width=600)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### สถิติการสมัคร")
        st.metric("จำนวนผู้สมัครทั้งหมด", len(df))
        st.metric("สมัครเข้า ม.1", len(df[df['ระดับชั้นที่สมัคร'] == 'ม.1']))
        st.metric("สมัครเข้า ม.4", len(df[df['ระดับชั้นที่สมัคร'] == 'ม.4']))
    
    with col2:
        st.markdown("### สถิติผลคัดเลือก")
        st.metric("ผ่านการคัดเลือก", len(df[df['สถานะ'] == 'ผ่าน']))
        st.metric("ไม่ผ่านการคัดเลือก", len(df[df['สถานะ'] == 'ไม่ผ่าน']))
        st.metric("รอตรวจสอบ", len(df[df['สถานะ'] == 'รอตรวจสอบ']))
    
    st.markdown("### ข้อมูลนักเรียนทั้งหมด")
    st.dataframe(df)

elif menu == "ลงทะเบียนนักเรียน":
    st.subheader("แบบฟอร์มลงทะเบียนนักเรียน")
    
    with st.form("student_form"):
        col1, col2 = st.columns(2)
        with col1:
            student_id = st.text_input("รหัสนักเรียน*")
            full_name = st.text_input("ชื่อ-สกุล*")
            birth_date = st.date_input("วันเกิด*", datetime(2010, 1, 1))
            level = st.selectbox("ระดับชั้นที่สมัคร*", ["ม.1", "ม.4"])
        
        with col2:
            math_score = st.number_input("คะแนนคณิตศาสตร์ (0-100)*", 0, 100)
            science_score = st.number_input("คะแนนวิทยาศาสตร์ (0-100)*", 0, 100)
            thai_score = st.number_input("คะแนนภาษาไทย (0-100)*", 0, 100)
            english_score = st.number_input("คะแนนภาษาอังกฤษ (0-100)*", 0, 100)
        
        interview_score = st.number_input("คะแนนสัมภาษณ์ (0-20)*", 0, 20)
        notes = st.text_area("หมายเหตุ")
        
        submitted = st.form_submit_button("บันทึกข้อมูล")
        
        if submitted:
            if not student_id or not full_name:
                st.error("กรุณากรอกข้อมูลที่จำเป็นให้ครบถ้วน")
            else:
                # ในระบบจริงควรบันทึกลงฐานข้อมูล
                new_data = {
                    'รหัสนักเรียน': student_id,
                    'ชื่อ-สกุล': full_name,
                    'ระดับชั้นที่สมัคร': level,
                    'คะแนนคณิตศาสตร์': math_score,
                    'คะแนนวิทยาศาสตร์': science_score,
                    'คะแนนภาษาไทย': thai_score,
                    'คะแนนภาษาอังกฤษ': english_score,
                    'คะแนนสัมภาษณ์': interview_score,
                    'สถานะ': 'รอตรวจสอบ'
                }
                # เพิ่มข้อมูลใหม่ลง DataFrame (ในระบบจริงควรบันทึกลงฐานข้อมูล)
                
                df = df.append(new_data, ignore_index=True)
                st.success("บันทึกข้อมูลนักเรียนเรียบร้อยแล้ว!")

elif menu == "ตรวจสอบผลคัดเลือก":
    st.subheader("ตรวจสอบผลคัดเลือก")
    
    search_option = st.radio("วิธีการค้นหา", ["รหัสนักเรียน", "ชื่อ-สกุล"])
    
    if search_option == "รหัสนักเรียน":
        student_id = st.text_input("กรอกรหัสนักเรียน")
        if student_id:
            result = df[df['รหัสนักเรียน'] == student_id]
    else:
        full_name = st.text_input("กรอกชื่อ-สกุล")
        if full_name:
            result = df[df['ชื่อ-สกุล'].str.contains(full_name)]
    
    if 'result' in locals() and not result.empty:
        st.success("พบข้อมูลนักเรียน")
        st.dataframe(result)
        
        # คำนวณคะแนนรวม
        total_score = (
            result['คะแนนคณิตศาสตร์'].values[0] +
            result['คะแนนวิทยาศาสตร์'].values[0] +
            result['คะแนนภาษาไทย'].values[0] +
            result['คะแนนภาษาอังกฤษ'].values[0] +
            result['คะแนนสัมภาษณ์'].values[0]
        )
        
        st.metric("คะแนนรวม", total_score)
        st.metric("สถานะการคัดเลือก", result['สถานะ'].values[0])
    elif 'result' in locals() and result.empty:
        st.warning("ไม่พบข้อมูลนักเรียน")

elif menu == "ตั้งเกณฑ์คัดเลือก":
    st.subheader("ตั้งเกณฑ์การคัดเลือก")
    
    with st.form("criteria_form"):
        st.markdown("### เกณฑ์คะแนนขั้นต่ำ")
        math_min = st.number_input("คณิตศาสตร์", 0, 100, 50)
        science_min = st.number_input("วิทยาศาสตร์", 0, 100, 50)
        thai_min = st.number_input("ภาษาไทย", 0, 100, 50)
        english_min = st.number_input("ภาษาอังกฤษ", 0, 100, 50)
        interview_min = st.number_input("สัมภาษณ์", 0, 20, 10)
        
        st.markdown("### เกณฑ์คะแนนรวมขั้นต่ำ")
        total_min = st.number_input("คะแนนรวมขั้นต่ำ", 0, 420, 250)
        
        submitted = st.form_submit_button("บันทึกเกณฑ์")
        if submitted:
            st.success("บันทึกเกณฑ์การคัดเลือกเรียบร้อยแล้ว")

elif menu == "รายงานผล":
    st.subheader("รายงานผลการคัดเลือก")
    
    report_type = st.selectbox("เลือกประเภทรายงาน", [
        "สรุปผลการคัดเลือกทั้งหมด",
        "รายชื่อนักเรียนที่ผ่านการคัดเลือก",
        "รายชื่อนักเรียนที่ไม่ผ่านการคัดเลือก",
        "สถิติคะแนนสอบ"
    ])
    
    if report_type == "สรุปผลการคัดเลือกทั้งหมด":
        st.dataframe(df)
        
        # สรุปจำนวนนักเรียนที่ผ่าน/ไม่ผ่าน
        status_counts = df['สถานะ'].value_counts()
        st.bar_chart(status_counts)
        
    elif report_type == "รายชื่อนักเรียนที่ผ่านการคัดเลือก":
        passed = df[df['สถานะ'] == 'ผ่าน']
        st.dataframe(passed)
        st.metric("จำนวนนักเรียนที่ผ่าน", len(passed))
        
    elif report_type == "รายชื่อนักเรียนที่ไม่ผ่านการคัดเลือก":
        failed = df[df['สถานะ'] == 'ไม่ผ่าน']
        st.dataframe(failed)
        st.metric("จำนวนนักเรียนที่ไม่ผ่าน", len(failed))
        
    elif report_type == "สถิติคะแนนสอบ":
        st.markdown("### ค่าเฉลี่ยคะแนนสอบ")
        avg_scores = df[['คะแนนคณิตศาสตร์', 'คะแนนวิทยาศาสตร์', 'คะแนนภาษาไทย', 'คะแนนภาษาอังกฤษ']].mean()
        st.bar_chart(avg_scores)
        
        st.markdown("### การกระจายของคะแนนรวม")
        df['คะแนนรวม'] = df['คะแนนคณิตศาสตร์'] + df['คะแนนวิทยาศาสตร์'] + df['คะแนนภาษาไทย'] + df['คะแนนภาษาอังกฤษ'] + df['คะแนนสัมภาษณ์']
        st.line_chart(df['คะแนนรวม'])

# ส่วนท้าย
st.markdown("---")
st.markdown("พัฒนาโดยใช้ Python Streamlit | โรงเรียนตัวอย่าง | ปีการศึกษา 2566")
