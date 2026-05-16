import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfReader
from docx import Document
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# ================= NLTK DOWNLOADS =================
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="JobConnect AI",
    layout="wide"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>

.stApp{
    background-color:#F3F2EF;
}

/* LOGIN BACKGROUND */

[data-testid="stAppViewContainer"]{
    background-image:url("https://images.unsplash.com/photo-1521791136064-7986c2920216");
    background-size:cover;
    background-position:center;
    background-attachment:fixed;
}

/* LOGIN BOX */

.login-box{
    background:rgba(0,0,0,0.70);
    padding:45px;
    border-radius:20px;
    box-shadow:0px 4px 20px rgba(0,0,0,0.5);
}

/* NAVBAR */

.navbar{
    background:#0A66C2;
    padding:18px;
    border-radius:10px;
    margin-bottom:20px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.2);
}

/* LOGO */

.logo{
    color:white;
    font-size:34px;
    font-weight:bold;
}

/* TITLE */

.title{
    color:white;
    font-size:42px;
    font-weight:bold;
    text-align:center;
}

/* SUBTITLE */

.subtitle{
    color:white;
    font-size:20px;
    text-align:center;
    font-weight:500;
}

/* CARD */

.card{
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.1);
    margin-bottom:20px;
}

/* JOB CARD */

.job-card{
    background:white;
    padding:20px;
    border-radius:15px;
    border-left:6px solid #0A66C2;
    margin-bottom:20px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.1);
}

/* LABELS */

label{
    color:white !important;
    font-size:18px !important;
    font-weight:bold !important;
}

/* INPUTS */

.stTextInput input{
    background-color:white;
    color:black;
    border-radius:10px;
    height:50px;
    font-size:18px;
}

/* BUTTON */

.stButton button{
    background-color:#0A66C2;
    color:white;
    border:none;
    border-radius:10px;
    width:100%;
    height:50px;
    font-size:20px;
    font-weight:bold;
}

/* SIDEBAR */

section[data-testid="stSidebar"]{
    background-color:#0A66C2;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

</style>
""", unsafe_allow_html=True)

# ================= LOGIN STATE =================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# ================= LOGIN PAGE =================
# ================= LOGIN PAGE =================
if not st.session_state.logged_in:

    # LOGIN PAGE BACKGROUND ONLY
    st.markdown("""
    <style>

    [data-testid="stAppViewContainer"]{
        background-image:url("https://images.unsplash.com/photo-1521791136064-7986c2920216");
        background-size:cover;
        background-position:center;
        background-attachment:fixed;
    }

    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1.3,1])

    with col2:

        st.markdown("<br><br><br>", unsafe_allow_html=True)

        st.markdown("<div class='login-box'>", unsafe_allow_html=True)

        st.markdown("""
        <div class='title'>
        Intelligent Skill Analysis and Personalized Job Discovery System
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class='subtitle'>
        AI Powered Platform for Smart Career Guidance and Youth Employment
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

        username = st.text_input("Email or Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Sign In"):

            if username and password:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success("Login Successful")

                st.rerun()

            else:

                st.error("Please Enter Username and Password")

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()
# ================= NAVBAR =================
st.markdown("""
<div class='navbar'>
<span class='logo'>JobConnect AI</span>
</div>
""", unsafe_allow_html=True)

# ================= LOAD JOBS =================
jobs_df = pd.read_csv("jobs.csv")

# ================= CLEAN TEXT =================
def clean_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z ]', '', text)

    words = word_tokenize(text)

    stop_words = set(stopwords.words('english'))

    filtered_words = [
        word for word in words
        if word not in stop_words
    ]

    return ' '.join(filtered_words)

# ================= PDF EXTRACTION =================
def extract_text_from_pdf(uploaded_file):

    text = ""

    pdf_reader = PdfReader(uploaded_file)

    for page in pdf_reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text

# ================= DOCX EXTRACTION =================
def extract_text_from_docx(uploaded_file):

    doc = Document(uploaded_file)

    text = ""

    for para in doc.paragraphs:

        text += para.text

    return text

# ================= SIDEBAR =================
st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Menu",
    [
        "Home",
        "My Profile",
        "Upload Resume",
        "Skill Analysis",
        "Recommended Jobs"
    ]
)

# ================= HOME PAGE =================
# ================= HOME PAGE =================
if menu == "Home":

    st.header("Professional Feed")

    # POST 1
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col1, col2 = st.columns([1,6])

    with col1:

        st.image(
            "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            width=70
        )

    with col2:

        st.subheader("Rahul Sharma")

        st.write("AI Engineer at TechNova")

        st.write(
            "Excited to announce that our AI recruitment platform crossed 1 million users today!"
        )

        st.image(
            "https://images.unsplash.com/photo-1522202176988-66273c2fd55f",
            use_container_width=True
        )

        st.write("👍 1.2K Likes    💬 240 Comments")

    st.markdown("</div>", unsafe_allow_html=True)

    # POST 2
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col1, col2 = st.columns([1,6])

    with col1:

        st.image(
            "https://cdn-icons-png.flaticon.com/512/4140/4140048.png",
            width=70
        )

    with col2:

        st.subheader("Priya Reddy")

        st.write("Data Analyst at Infosys")

        st.write(
            "Sharing free resources for students preparing for Data Science interviews."
        )

        st.image(
            "https://images.unsplash.com/photo-1516321318423-f06f85e504b3",
            use_container_width=True
        )

        st.write("👍 980 Likes    💬 180 Comments")

    st.markdown("</div>", unsafe_allow_html=True)

    # POST 3
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col1, col2 = st.columns([1,6])

    with col1:

        st.image(
            "https://cdn-icons-png.flaticon.com/512/6997/6997662.png",
            width=70
        )

    with col2:

        st.subheader("Arjun Verma")

        st.write("Machine Learning Intern")

        st.write(
            "I recently completed my internship in AI and got placed as ML Engineer."
        )

        st.image(
            "https://images.unsplash.com/photo-1519389950473-47ba0277781c",
            use_container_width=True
        )

        st.write("👍 2K Likes    💬 450 Comments")

    st.markdown("</div>", unsafe_allow_html=True)

    # POST 4
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col1, col2 = st.columns([1,6])

    with col1:

        st.image(
            "https://cdn-icons-png.flaticon.com/512/6997/6997665.png",
            width=70
        )

    with col2:

        st.subheader("Sneha Kapoor")

        st.write("Software Developer")

        st.write(
            "Top 10 websites every engineering student should use for placements."
        )

        st.image(
            "https://images.unsplash.com/photo-1498050108023-c5249f4df085",
            use_container_width=True
        )

        st.write("👍 1.5K Likes    💬 320 Comments")

    st.markdown("</div>", unsafe_allow_html=True)
# ================= PROFILE PAGE =================
# ================= PROFILE PAGE =================
if menu == "My Profile":

    st.header("Create Your Profile")

    # PROFILE PHOTO
    profile_pic = st.file_uploader(
        "Upload Profile Photo",
        type=["png", "jpg", "jpeg"]
    )

    col1, col2 = st.columns([1,2])

    with col1:

        if profile_pic:

            st.image(profile_pic, width=220)

        else:

            st.image(
                "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                width=220
            )

    with col2:

        full_name = st.text_input("Full Name")

        headline = st.text_input(
            "Professional Headline"
        )

        location = st.text_input("Location")

        email = st.text_input("Email")

        phone = st.text_input("Phone Number")

    st.subheader("About")

    about = st.text_area(
        "Write About Yourself"
    )

    st.subheader("Skills")

    skills = st.text_area(
        "Enter Skills"
    )

    st.subheader("Education")

    education = st.text_area(
        "Education Details"
    )

    st.subheader("Projects")

    projects = st.text_area(
        "Project Details"
    )

    st.subheader("Experience")

    experience = st.text_area(
        "Work Experience"
    )

    if st.button("Save Profile"):

        st.success("Profile Saved Successfully")

        st.markdown("<hr>", unsafe_allow_html=True)

        st.header("My LinkedIn Style Profile")

        col3, col4 = st.columns([1,3])

        with col3:

            if profile_pic:

                st.image(profile_pic, width=220)

        with col4:

            st.subheader(full_name)

            st.write(headline)

            st.write("📍", location)

            st.write("📧", email)

            st.write("📞", phone)

        st.subheader("About")

        st.write(about)

        st.subheader("Skills")

        st.write(skills)

        st.subheader("Education")

        st.write(education)

        st.subheader("Projects")

        st.write(projects)

        st.subheader("Experience")

        st.write(experience)
# ================= UPLOAD RESUME =================
if menu == "Upload Resume":

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.header("Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"]
    )

    user_skills = st.text_input(
        "Enter Your Skills"
    )

    if uploaded_file:

        if uploaded_file.name.endswith(".pdf"):

            resume_text = extract_text_from_pdf(uploaded_file)

        else:

            resume_text = extract_text_from_docx(uploaded_file)

        cleaned_resume = clean_text(resume_text)

        st.session_state.resume_text = cleaned_resume

        st.session_state.user_skills = user_skills

        st.success("Resume Uploaded Successfully")

        score = min(
            len(cleaned_resume.split()) / 50,
            5
        )

        st.subheader("Resume Strength")

        st.progress(int(score * 20))

        st.success(
            f"Resume Score: {round(score,2)} / 5"
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ================= SKILL ANALYSIS =================
if menu == "Skill Analysis":

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.header("AI Skill Analysis")

    if 'resume_text' in st.session_state:

        resume = st.session_state.resume_text

        jobs_text = (
            jobs_df['Skills']
            + " "
            + jobs_df['Description']
        )

        corpus = [resume] + jobs_text.tolist()

        tfidf = TfidfVectorizer()

        tfidf_matrix = tfidf.fit_transform(corpus)

        similarity = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:]
        )

        jobs_df['Score'] = similarity[0] * 100

        for i in range(len(jobs_df)):

            st.write(
                jobs_df.iloc[i]['Job Title']
            )

            st.progress(
                int(jobs_df.iloc[i]['Score'])
            )

    else:

        st.warning(
            "Please Upload Resume First"
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ================= RECOMMENDED JOBS =================
if menu == "Recommended Jobs":

    st.header("Recommended Jobs For You")

    if 'resume_text' in st.session_state:

        resume = st.session_state.resume_text

        jobs_text = (
            jobs_df['Skills']
            + " "
            + jobs_df['Description']
        )

        corpus = [resume] + jobs_text.tolist()

        tfidf = TfidfVectorizer()

        tfidf_matrix = tfidf.fit_transform(corpus)

        similarity = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:]
        )

        jobs_df['Similarity'] = similarity[0]

        top_jobs = jobs_df.sort_values(
            by='Similarity',
            ascending=False
        ).head(10)

        # COMPANY NAMES
        companies = [
            "Google",
            "Amazon",
            "Infosys",
            "TCS",
            "Swiggy",
            "Zomato",
            "Reliance",
            "Accenture",
            "Flipkart",
            "Meesho",
            "Tech Mahindra",
            "Byjus",
            "Deloitte",
            "Wipro",
            "Capgemini"
        ]

        # LOCATIONS
        locations = [
            "Hyderabad",
            "Bangalore",
            "Chennai",
            "Pune",
            "Mumbai",
            "Delhi"
        ]

        # SALARIES
        salaries = [
            "₹10,000/month",
            "₹15,000/month",
            "₹20,000/month",
            "₹25,000/month",
            "₹4 LPA",
            "₹6 LPA",
            "₹8 LPA",
            "₹12 LPA"
        ]

        # JOB TYPES
        job_types = [
            "Full Time",
            "Part Time",
            "Internship",
            "Work From Home",
            "Freelance"
        ]

        for i, (index, row) in enumerate(top_jobs.iterrows()):

            st.markdown(
                "<div class='job-card'>",
                unsafe_allow_html=True
            )

            col1, col2 = st.columns([1,4])

            with col1:

                st.image(
                    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                    width=90
                )

            with col2:

                st.subheader(row['Job Title'])

                st.write(
                    f"🏢 Company Hiring: {companies[i % len(companies)]}"
                )

                st.write(
                    f"📍 Location: {locations[i % len(locations)]}"
                )

                st.write(
                    f"💼 Salary: {salaries[i % len(salaries)]}"
                )

                st.write(
                    f"🕒 Job Type: {job_types[i % len(job_types)]}"
                )

                st.write(
                    "🟢 Hiring Status: Actively Hiring"
                )

                st.write(
                    "🛠 Required Skills:"
                )

                st.write(row['Skills'])

                st.write(
                    "📄 Job Description:"
                )

                st.write(row['Description'])

                st.success(
                    f"✅ Match Score: {round(row['Similarity'] * 100,2)}%"
                )

                col3, col4 = st.columns(2)

                with col3:

                    st.button(
                        f"Apply Now {index}"
                    )

                with col4:

                    st.button(
                        f"Save Job {index}"
                    )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    else:

        st.warning(
            "Please Upload Resume First"
        )