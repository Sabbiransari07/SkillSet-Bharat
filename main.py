import streamlit as st
import pandas as pd
import random
import time

# ==========================================
# 1. CONFIG & DATA (The "Backend" Database)
# ==========================================
st.set_page_config(page_title="JobMate AI Prototype", page_icon="🤖", layout="wide")

# --- Mock Database: Jobs & Schemes ---
JOBS_DB = [
    {"id": 1, "title": "Junior Python Developer", "skills": ["Python", "SQL", "Flask"], "loc": "Remote", "salary": "₹4-6 LPA"},
    {"id": 2, "title": "Data Analyst", "skills": ["Excel", "Python", "Tableau"], "loc": "Delhi", "salary": "₹5-7 LPA"},
    {"id": 3, "title": "Web Developer", "skills": ["HTML", "CSS", "JavaScript"], "loc": "Mumbai", "salary": "₹3-5 LPA"},
    {"id": 4, "title": "AI Engineer", "skills": ["Python", "Machine Learning", "TensorFlow"], "loc": "Bangalore", "salary": "₹8-12 LPA"},
    {"id": 5, "title": "Digital Marketer", "skills": ["SEO", "Content Writing", "Facebook Ads"], "loc": "Remote", "salary": "₹3-5 LPA"},
]

SCHEMES_DB = {
    "Python": "Apply for 'PM-YUVA' Digital Literacy Scheme",
    "Machine Learning": "Get Govt Grant for AI Startups via NASSCOM",
    "Excel": "Free Government Skill India Course",
    "SEO": "Digital India Marketing Grant"
}

# --- Language Logic (Bonus: Hindi Support) ---
def get_text(key):
    if st.session_state.get('lang') == 'Hindi':
        texts = {
            "title": "आज का काम ढूंढें (Find Job)",
            "skills": "आपके कौशल (Select Skills)",
            "loc": "स्थान (Location)",
            "btn": "खोजें (Search)",
            "match": "मैच स्कोर",
            "quiz": "कौशल परीक्षण",
            "resume": "रिज़्यूme बनाएं"
        }
        return texts.get(key, key)
    return key

# Initialize Session State
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'English'

if 'user_skills' not in st.session_state:
    st.session_state['user_skills'] = []

# ==========================================
# 2. FRONTEND LAYOUT
# ==========================================

# --- Sidebar: Navigation & Settings ---
with st.sidebar:
    st.title("⚙️ Settings")
    lang_select = st.radio("Language / भाषा", ["English", "Hindi"])
    st.session_state['lang'] = lang_select
    
    st.markdown("---")
    st.info("💡 **Tip:** Use the Dashboard to find jobs, take a quiz to test skills, or generate a resume.")

    menu = st.radio("Go to", ["Job Finder Dashboard", "Skill Quiz", "Resume Generator"])

# ==========================================
# 3. MAIN LOGIC
# ==========================================

# --- PAGE 1: JOB FINDER DASHBOARD ---
if menu == "Job Finder Dashboard":
    st.title(f"🔍 {get_text('title')}")
    
    col1, col2 = st.columns(2)
    with col1:
        user_skills = st.multiselect(
            get_text('skills'), 
            options=["Python", "SQL", "Excel", "HTML", "CSS", "JavaScript", "Machine Learning", "SEO", "Content Writing", "Flask"]
        )
        # ✅ FIX: Store skills in session_state
        st.session_state['user_skills'] = user_skills

    with col2:
        user_loc = st.selectbox(
            get_text('loc'), 
            options=["Remote", "Delhi", "Mumbai", "Bangalore", "Chennai"]
        )

    if st.button(get_text('btn')):
        if not user_skills:
            st.warning("Please select at least one skill!")
        else:
            st.markdown("---")
            st.subheader("🎯 Recommended Jobs")
            
            matches = []
            for job in JOBS_DB:
                loc_match = (job['loc'] == user_loc) or (job['loc'] == "Remote")
                skill_match_count = len(set(job['skills']) & set(user_skills))
                
                if loc_match and skill_match_count > 0:
                    score = (skill_match_count / len(job['skills'])) * 100
                    matches.append({
                        **job,
                        "match_score": int(score),
                        "common_skills": list(set(job['skills']) & set(user_skills))
                    })
            
            matches.sort(key=lambda x: x['match_score'], reverse=True)

            if matches:
                for job in matches:
                    with st.container():
                        c1, c2, c3 = st.columns([3, 1, 1])
                        c1.markdown(f"### {job['title']}")
                        c2.metric("Match Score", f"{job['match_score']}%", delta_color="normal")
                        c3.metric("Salary", job['salary'])
                        
                        st.write(f"📍 **Location:** {job['loc']}")
                        st.write(f"✅ **Matching Skills:** {', '.join(job['common_skills'])}")
                        
                        for skill in job['common_skills']:
                            if skill in SCHEMES_DB:
                                st.caption(f"💡 **Scheme Alert:** {SCHEMES_DB[skill]}")
                        
                        st.markdown("---")
            else:
                st.error("No jobs found with this skill set in this location. Try Remote!")

# --- PAGE 2: SKILL QUIZ ---
elif menu == "Skill Quiz":
    st.title(f"📝 {get_text('quiz')}")
    
    questions = {
        "Python": {"q": "What is the output of 'print(type([]))'?", "options": ["list", "tuple", "dict", "set"], "a": "list"},
        "SEO": {"q": "What does SEO stand for?", "options": ["Search Engine Output", "Search Engine Optimization", "Social Engine Operation", "Sell Engine Online"], "a": "Search Engine Optimization"},
        "Excel": {"q": "Which function is used to sum a range?", "options": ["AVG", "SUM", "TOTAL", "ADD"], "a": "SUM"}
    }
    
    category = st.selectbox("Choose Skill to Test", list(questions.keys()))
    q_data = questions[category]
    
    st.write(f"**Question:** {q_data['q']}")
    answer = st.radio("Options", q_data['options'])
    
    if st.button("Submit Answer"):
        if answer == q_data['a']:
            st.success("🎉 Correct! You are ready for the job.")
        else:
            st.error("❌ Incorrect. Keep learning!")

# --- PAGE 3: RESUME GENERATOR ---
elif menu == "Resume Generator":
    st.title(f"📄 {get_text('resume')}")
    
    with st.form("resume_form"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Full Name")
        phone = c2.text_input("Phone Number")
        email = st.text_input("Email")
        summary = st.text_area("Professional Summary")
        submit = st.form_submit_button("Generate Resume")
        
    if submit:
        skills = st.session_state.get('user_skills', [])
        
        resume_text = f"""
{name.upper()}
{email} | {phone}

SUMMARY:
{summary}

SKILLS:
{', '.join(skills) if skills else 'Not provided'}

EXPERIENCE:
[User would add this manually in a full form]
"""
        st.success("Resume Generated Successfully!")
        st.text_area("Preview", resume_text, height=300)
        st.download_button("Download .txt", resume_text, file_name="my_resume.txt")