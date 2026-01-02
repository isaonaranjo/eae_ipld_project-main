import streamlit as st
import base64

    
# ----- Page configs (tab title, favicon) -----
st.set_page_config(
    page_title="Isabel Ortiz - Portfolio",
    page_icon="📊",
    layout="wide"
)


def home_page():
    # ----- Left menu -----
    with st.sidebar:
        st.image("eae_img.png", width=200)
        st.header("Introduction to Programming Languages for Data")
        st.write("###")
        st.write("***Final Project - Dec 2025***")
        st.write("**Author:** Maria Isabel Ortiz Naranjo") 
        st.write("**Instructor:** [Enric Domingo](https://github.com/enricd)")

    # ----- Top title -----
    st.html("""<div style="text-align: center;"><h1 style="text-align: center;">👋 Hi! My name is Isabel</h1></div>""")  # TODO: Add your name


    # ----- Profile image file -----
    profile_image_file_path = "isa.png"       # TODO: Upload your profile image to the same folder as this script and update this if it has a different name

    with open(profile_image_file_path, "rb") as img_file:
        img = "data:image/png;base64," + base64.b64encode(img_file.read()).decode()


    # ----- Your Profile Image -----
    st.html(f"""
    <div style="display: flex; justify-content: center;">
        <img src="{img}" alt="Your Name" width="300" height="300" style="border-radius: 50%; object-fit: cover; margin-top: 40px; margin-bottom: 40px;">
    </div>
    """)


    # ----- Personal title or short description -----
    current_role = "Data Analyst and Computer Science Engineer, specializing in Data Analytics and Big Data"

    st.html(f"""<div style="text-align: center;"><h4><i>{current_role}</i></h4></div>""")

    st.write("##")    # Adding some space


    # ----- About me section -----
    st.subheader("About Me")

    # TODO: Modify and adapt the following lines to your info, you can add or remove some details if you want
    st.write("""
    - 🧑‍💻 I am a **Data Analyst and Computer Science Engineer**, currently specializing in **Data Analytics & Big Data**.

    - 🛩️ **Previous experience:** Business Analyst II in Regulatory Compliance, working with fee-schedule data, SQL databases, Python automation, and data validation processes.
             
    - ❤️ **Passionate about:** data-driven decision making, analytics, technology, and continuous learning.

    - 🤖 **Personal projects:** data analysis projects using Python (Pandas, NumPy, Matplotlib), academic assignments, and exploratory data visualizations.

    - 🏂 **Hobbies:** going to the gym, walking by the sea, traveling, and creative writing.

    - 📫 How to reach me: mionaranjo@gmail.com

    - 🏠 **Location:** Barcelona
    """)

    # Feel free to add other points like your Linkedin, Github, Social Media, etc.


# This is ensambling the entire app with the different pages and the navigation menu
pg = st.navigation([
    st.Page(home_page, title="Home", icon="👋"),
    st.Page("pages/01_image_cropper.py", title="Image Cropper", icon="🖼️"),
    st.Page("pages/02_netflix_data_analysis.py", title="Netflix Data Analysis", icon="🎬"),
    st.Page("pages/03_temperatures_dashboard.py", title="Temperatures Dashboard", icon="🌦️"),
])

# ----- Custom CSS (Purple theme) -----
st.markdown("""
<style>
/* Page background */
.stApp {
  background: linear-gradient(180deg, #f7f3ff 0%, #ffffff 70%);
}

/* Reduce top padding (Streamlit default is huge) */
.block-container {
  padding-top: 2rem;
  padding-bottom: 2rem;
  max-width: 1100px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #5e3ea1 0%, #432a78 100%);
}
section[data-testid="stSidebar"] * { color: white !important; }

/* Sidebar nav buttons look nicer */
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] span {
  font-weight: 600;
}
section[data-testid="stSidebar"] a {
  border-radius: 10px;
}

/* Titles */
h1, h2, h3 { color: #3d246c; }
h4 { color: #4b2c82; }

/* “Cards” style for content blocks */
.purple-card {
  background: rgba(255,255,255,0.75);
  border: 1px solid rgba(94, 62, 161, 0.15);
  box-shadow: 0 8px 24px rgba(61, 36, 108, 0.08);
  border-radius: 18px;
  padding: 18px 20px;
}

/* Center hero section tighter */
.hero {
  text-align: center;
  margin-top: 0.5rem;
  margin-bottom: 1.2rem;
}
.role {
  text-align: center;
  font-size: 1.05rem;
  color: #4b2c82;
  margin-top: 0.2rem;
}
</style>
""", unsafe_allow_html=True)

# Run the app
pg.run()