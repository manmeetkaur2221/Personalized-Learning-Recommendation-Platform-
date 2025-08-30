import pandas as pd
import matplotlib.pyplot as plt
try:
    import seaborn as sns
    sns.set_style("whitegrid")
except Exception:
    sns = None
from datetime import datetime, timedelta
import random
from IPython.display import display, HTML, clear_output

# ---------- Pastel theme ----------
pastel_green = "#A8E6CF"
pastel_pink = "#FFB6B9"
accent = "#F6F1FF"
plt.rcParams["figure.facecolor"] = "#ffffff"
plt.rcParams["axes.facecolor"] = "#ffffff"
plt.rcParams["font.size"] = 11

# If seaborn isn't available, fall back to matplotlib defaults
if sns is None:
    print("Note: seaborn not found. Plots will use matplotlib defaults. To install: !pip install seaborn")

# ---------- Sample Data ----------
students = pd.DataFrame({
    "StudentID": range(1, 21),
    "Name": [
        "Aisha","Bilal","Charu","Deep","Esha","Farhan","Gita","Hardeep","Ira","Jatin",
        "Kavya","Amrit","Manmeet","Gaganpreet","Prabhjot","Vansh","Anamika","Harkirat","Gurjot","Sifat"
    ],
    "LearningStyle": [
        "Visual","Kinesthetic","Auditory","Visual","Reading","Visual","Kinesthetic","Auditory","Reading","Visual",
        "Kinesthetic","Auditory","Visual","Kinesthetic","Auditory","Visual","Reading","Visual","Kinesthetic","Auditory"
    ],
    "Interests": [
        "Math, Data","Robotics, Coding","History, Literature","Data, AI","Art, Design","Coding, Games",
        "Biology, Chemistry","Languages, Drama","Math, Physics","AI, ML",
        "Design, UX","Economics, Finance","Cybersecurity, Networking","Astronomy, Space Science",
        "Philosophy, Psychology","Sports, Fitness","Music, Audio Production","Geography, Geopolitics",
        "Film, Animation","Environmental Science, Sustainability"
    ],
    "GradeLevel": [6,8,7,11,9,10,8,7,12,11,9,10,7,8,9,7,10,9,8,6]
})


courses = pd.DataFrame({
    "CourseID": range(1, 21),
   "CourseName": ["Intro to Python","Data Science Basics","Fundamentals of AI","Creative Design","Robotics 101","Biology Essentials","World History",
                  "Mathematics Olympiad Prep","Physics Concepts","Public Speaking","Economics for Teens","UX & Product Design",
                  "Cybersecurity Basics","Astronomy & Space Exploration","Philosophy & Critical Thinking",
                  "Sports Science & Fitness","Music Theory & Composition","Global Geography","Film & Animation Fundamentals",
                  "Environmental Science & Sustainability"
                  ],

   "Subject" : [ "Coding","Data","AI","Design","Robotics","Biology","Math","Physics","Design",
                "Chemistry","Astronomy","Engineering","Literature","Art","Music","Ethics","Business",
                 "Law","Cybersecurity","Game Development"
                 ],

   "Difficulty": ["Beginner", "Beginner", "Intermediate", "Beginner", "Intermediate", "Beginner","Beginner","Advanced",
                                "Intermediate", "Beginner", "Intermediate", "Intermediate","Intermediate", "Beginner", "Advanced",
                                "Intermediate", "Beginner", "Advanced","Intermediate", "Beginner"
                                ],
   "Description": [
  "Hands-on Python programming for beginners",
  "Introductory data skills: spreadsheets, basic plots, stats",
  "Machine learning concepts and simple models",
  "Visual design basics: color, typography, layout",
  "Build and program simple robots and sensors",
  "Core concepts in biology with fun labs",
  "A journey through major world events",
  "Advanced problem solving for math competitions",
  "Foundational physics ideas with experiments",
  "Communication skills, presentations, debate",
  "Principles of supply & demand, markets",
  "User research, prototyping, and usability testing",
  "Explore chemical reactions and molecular structures",
  "Discover the universe: stars, planets, and galaxies",
  "Understand human behavior and mental processes",
  "Big questions, logic, and the roots of knowledge",
  "How societies function and change over time",
  "Maps, landforms, and human-environment interaction",
  "Climate, ecosystems, and sustainability topics",
  "Government systems, policies, and global politics"
  ],

})

# Create some sample enrollments (some completed, some ongoing)
enrollments = []
for _ in range(60):
    sid = int(random.choice(students["StudentID"]))
    cid = int(random.choice(courses["CourseID"]))
    start = pd.Timestamp(year=2024, month=random.randint(1,12), day=random.randint(1,25))
    if random.random() < 0.75:
        # completed
        comp = start + pd.Timedelta(days=random.randint(5,60))
        score = round(random.uniform(50,100),1)
    else:
        comp = pd.NaT
        score = pd.NA
    enrollments.append({"StudentID": sid, "CourseID": cid, "StartDate": start, "CompletionDate": comp, "Score": score})

enrollments = pd.DataFrame(enrollments)

# ---------- Helper UI ----------
def kpi_cards(total_students, total_courses, active_enrollments, avg_completion_rate):
    # Luxury theme colors
    gold_light = "#FFD700"
    gold_dark = "#B8860B"
    navy = "#0B1D39"
    deep_red = "#8B0000"
    emerald = "#006400"
    charcoal = "#1C1C1C"

    html = f"""
    <div style="display:flex; gap:18px; font-family:Arial, sans-serif; margin-bottom:12px;">

      <div style="background:linear-gradient(135deg,{gold_light},{gold_dark}); padding:18px; border-radius:12px; width:240px; box-shadow: 0 6px 20px rgba(0,0,0,0.4);">
        <div style="font-size:12px; color:{charcoal}; font-weight:600;">👩‍🎓 Total Students</div>
        <div style="font-size:22px; font-weight:700; color:{charcoal};">{total_students}</div>
      </div>

      <div style="background:linear-gradient(135deg,{navy},#102C54); padding:18px; border-radius:12px; width:240px; box-shadow: 0 6px 20px rgba(0,0,0,0.4);">
        <div style="font-size:12px; color:{gold_light}; font-weight:600;">📚 Total Courses</div>
        <div style="font-size:22px; font-weight:700; color:{gold_light};">{total_courses}</div>
      </div>

      <div style="background:linear-gradient(135deg,{emerald},#228B22); padding:18px; border-radius:12px; width:240px; box-shadow: 0 6px 20px rgba(0,0,0,0.4);">
        <div style="font-size:12px; color:{gold_light}; font-weight:600;">📈 Active Enrollments</div>
        <div style="font-size:22px; font-weight:700; color:{gold_light};">{active_enrollments}</div>
      </div>

      <div style="background:linear-gradient(135deg,{deep_red},#B22222); padding:18px; border-radius:12px; width:240px; box-shadow: 0 6px 20px rgba(0,0,0,0.4);">
        <div style="font-size:12px; color:{gold_light}; font-weight:600;">✅ Avg Completion %</div>
        <div style="font-size:22px; font-weight:700; color:{gold_light};">{avg_completion_rate:.1f}%</div>
      </div>

    </div>
    """
    display(HTML(html))


def styled_table(df, max_rows=10):
    return df.head(max_rows).style.set_table_styles([
        {'selector': 'th','props': [('background-color', accent), ('color','#222'), ('font-weight','700')]} ,
        {'selector': 'td','props': [('padding','8px')]}]).set_properties(**{'border-radius':'6px'})

# ---------- Core Metrics ----------
def compute_metrics():
    total_students = students.shape[0]
    total_courses = courses.shape[0]
    active_enrollments = enrollments[enrollments['CompletionDate'].isna()].shape[0]
    completed = enrollments[~enrollments['CompletionDate'].isna()]
    if len(completed) > 0:
        avg_completion_rate = (completed['Score'].notna().sum() / len(enrollments)) * 100
    else:
        avg_completion_rate = 0.0
    return total_students, total_courses, active_enrollments, avg_completion_rate

# ---------- Visuals ----------
def students_by_grade_chart():
    grp = students['GradeLevel'].value_counts().sort_index()
    plt.figure(figsize=(8,3.5))
    plt.bar(
        grp.index.astype(str),
        grp.values,
        color="#FFD700",       # gold fill
        edgecolor="black",     # black border
        linewidth=1.2          # slightly thicker border
    )
    plt.title('Students by Grade Level', fontsize=13, weight='bold')
    plt.xlabel('Grade')
    plt.ylabel('Number of Students')
    plt.tight_layout()
    plt.show()

def popular_courses_chart(n=8):
    top = enrollments['CourseID'].value_counts().head(n).reset_index()
    top.columns = ['CourseID','Enrollments']
    top = top.merge(courses[['CourseID','CourseName']], on='CourseID', how='left')

    # Luxury jewel-tone colors
    luxury_colors = [
        "#0F52BA",  # Royal Blue
        "#800020",  # Burgundy
        "#FFD700",  # Gold
        "#2E8B57",  # Emerald Green
        "#4B0082",  # Indigo
        "#C0C0C0",  # Silver
        "#8B4513",  # Saddle Brown
        "#708090"   # Slate Gray
    ][:len(top)]

    plt.figure(figsize=(9, 4))
    plt.barh(
        top['CourseName'],
        top['Enrollments'],
        color=luxury_colors,
        edgecolor="black",   # Black border
        linewidth=1.2        # Border thickness
    )
    plt.title('Popular Courses', fontsize=13, weight='bold')
    plt.tight_layout()
    plt.show()

def monthly_enrollment_trend():
    df = enrollments.copy()
    df['Month'] = df['StartDate'].dt.to_period('M').dt.to_timestamp()
    idx = pd.date_range(start=df['Month'].min(), end=df['Month'].max(), freq='MS')
    monthly = df.groupby('Month').size().reindex(idx, fill_value=0)
    plt.figure(figsize=(9,3))
    plt.plot(monthly.index, monthly.values, marker='o')
    plt.title('Monthly Enrollment Trend')
    plt.tight_layout()
    plt.show()

def top_students_chart(n=6):
    comp = enrollments[~enrollments['CompletionDate'].isna() & enrollments['Score'].notna()]
    avg_scores = comp.groupby('StudentID')['Score'].mean().sort_values(ascending=False).head(n).reset_index()
    avg_scores = avg_scores.merge(students[['StudentID','Name']], on='StudentID', how='left')

    # Luxury jewel-tone colors
    luxury_colors = [
        "#0F52BA",  # Royal Blue
        "#800020",  # Burgundy
        "#FFD700",  # Gold
        "#2E8B57",  # Emerald Green
        "#4B0082",  # Indigo
        "#C0C0C0"   # Silver
    ][:len(avg_scores)]

    plt.figure(figsize=(8, 3))
    plt.barh(
        avg_scores['Name'],
        avg_scores['Score'],
        color=luxury_colors,
        edgecolor="black",   # Black border
        linewidth=1.2        # Border thickness
    )
    plt.title('Top Performing Students', fontsize=13, weight='bold')
    plt.tight_layout()
    plt.show()


# ---------- Recommendation Engine (simple)
def recommend_courses(student_id, top_n=5):
    # Basic scoring: match interests -> subject/description, prefer difficulty based on grade & learning style
    student = students[students['StudentID'] == student_id]
    if student.empty:
        return []
    interests = str(student.iloc[0]['Interests']).lower()
    grade = student.iloc[0]['GradeLevel']
    style = student.iloc[0]['LearningStyle']

    # map learning style to preferred course keywords (naive)
    style_pref = {
        'Visual': ['design','visual','ux','art'],
        'Kinesthetic': ['robot','lab','experiment','hands'],
        'Auditory': ['speaking','communication','debate','languages'],
        'Reading': ['history','economics','literature']
    }
    pref_keywords = style_pref.get(style, [])

    scores = []
    for _, row in courses.iterrows():
        score = 0
        text = (row['CourseName'] + ' ' + row['Subject'] + ' ' + row['Description']).lower()
        # interest match
        for tok in interests.split(','):
            tok = tok.strip()
            if tok and tok in text:
                score += 30
        # style preference match
        for k in pref_keywords:
            if k in text:
                score += 10
        # grade/difficulty preference (simple heuristic)
        if grade <= 8 and row['Difficulty'].lower() == 'beginner':
            score += 8
        if grade >= 11 and row['Difficulty'].lower() == 'advanced':
            score += 8
        # small random tie-breaker
        score += random.random()
        scores.append((row['CourseID'], row['CourseName'], score))

    scored = sorted(scores, key=lambda x: x[2], reverse=True)
    return scored[:top_n]

# ---------- Search + Utility ----------
def search_students(keyword):
    kw = str(keyword).lower()
    out = students[students['Name'].str.lower().str.contains(kw) | students['Interests'].str.lower().str.contains(kw)]
    if out.empty:
        print('No students found.')
    else:
        display(styled_table(out, max_rows=20))

def search_courses(keyword):
    kw = str(keyword).lower()
    out = courses[courses['CourseName'].str.lower().str.contains(kw) | courses['Subject'].str.lower().str.contains(kw) | courses['Description'].str.lower().contains(kw)]
    if out.empty:
        print('No courses found.')
    else:
        display(styled_table(out, max_rows=20))

# ---------- Management functions ----------
def view_students():
    display(styled_table(students, max_rows=50))

def add_student():
    clear_output()
    print('➕ Add a new student')
    name = input('Name: ').strip()
    style = input('Learning style (Visual/Kinesthetic/Auditory/Reading): ').strip() or 'Visual'
    interests = input('Interests (comma separated): ').strip()
    grade = int(input('Grade level (number): ').strip() or 10)
    new_id = int(students['StudentID'].max()) + 1
    students.loc[len(students)] = [new_id, name, style, interests, grade]
    print('✅ Student added.')

def remove_student():
    clear_output()
    name_input = input('Enter Student Name to remove: ').strip().lower()
    global students, enrollments

    # Find matching students (case-insensitive)
    matched_students = students[students['Name'].str.lower() == name_input]

    if matched_students.empty:
        print(f"⚠️ No student found with the name '{name_input}'.")
    else:
        sids_to_remove = matched_students['StudentID'].tolist()

        # Remove from both dataframes
        students = students[~students['StudentID'].isin(sids_to_remove)].reset_index(drop=True)
        enrollments = enrollments[~enrollments['StudentID'].isin(sids_to_remove)].reset_index(drop=True)

        print(f"✅ Removed {len(sids_to_remove)} student(s) named '{name_input}' and their enrollments.")


def view_courses():
    display(styled_table(courses, max_rows=50))

def add_course():
    clear_output()
    print('➕ Add a new course')
    name = input('Course name: ').strip()
    subject = input('Subject: ').strip()
    difficulty = input('Difficulty (Beginner/Intermediate/Advanced): ').strip() or 'Beginner'
    desc = input('Short description: ').strip()
    new_id = int(courses['CourseID'].max()) + 1
    courses.loc[len(courses)] = [new_id, name, subject, difficulty, desc]
    print('✅ Course added.')

def enroll_student():
    clear_output()
    print('📥 Enroll a student into a course')
    sid = int(input('StudentID: ').strip())
    cid = int(input('CourseID: ').strip())
    start = pd.Timestamp.now()
    enrollments.loc[len(enrollments)] = [sid, cid, start, pd.NaT, pd.NA]
    print('✅ Enrolled.')

def complete_course():
    clear_output()
    print('✅ Mark course completed')
    sid = int(input('StudentID: ').strip())
    cid = int(input('CourseID: ').strip())
    idx = enrollments[(enrollments['StudentID']==sid) & (enrollments['CourseID']==cid) & (enrollments['CompletionDate'].isna())].index
    if len(idx) > 0:
        score = float(input('Score (0-100): ').strip() or 75)
        enrollments.loc[idx, 'CompletionDate'] = pd.Timestamp.now()
        enrollments.loc[idx, 'Score'] = score
        print('Marked as completed.')
    else:
        print('No active enrollment found for that student and course.')

# ---------- Dashboard view ----------
def show_dashboard():
    clear_output(wait=True)
    ts, tc, active, avgc = compute_metrics()
    kpi_cards(ts, tc, active, avgc)
    print('➡️ Quick Views:')
    display(HTML("<div style='display:flex; gap:8px;'><div style='flex:1'></div></div>"))
    print('\nPopular Courses:')
    top_c = enrollments['CourseID'].value_counts().head(7).reset_index()
    top_c.columns = ['CourseID','Enrollments']
    top_c = top_c.merge(courses[['CourseID','CourseName']], on='CourseID', how='left')
    display(styled_table(top_c[['CourseName','Enrollments']], max_rows=7))
    students_by_grade_chart()
    popular_courses_chart(7)
    monthly_enrollment_trend()
    top_students_chart(6)

# ---------- Fancy menu ----------
def menu():
    while True:
        print('\n===== 🌸 Personalized Learning Recommendation Platform =====')
        print('1️⃣  View Dashboard')
        print('2️⃣  View Students')
        print('3️⃣  Add Student')
        print('4️⃣  Remove Student')
        print('5️⃣  View Courses')
        print('6️⃣  Add Course')
        print('7️⃣  Enroll Student')
        print('8️⃣  Complete Course')
        print('9️⃣  Search Students')
        print('🔟  Search Courses')
        print('Ⓡ  Recommendations for a Student')
        print('0️⃣  Exit')
        choice = input('Enter choice: ').strip().lower()
        if choice == '1':
            show_dashboard()
        elif choice == '2':
            clear_output()
            view_students()
        elif choice == '3':
            add_student()
        elif choice == '4':
            remove_student()
        elif choice == '5':
            clear_output()
            view_courses()
        elif choice == '6':
            add_course()
        elif choice == '7':
            enroll_student()
        elif choice == '8':
            complete_course()
        elif choice == '9':
            q = input('Search keyword (name/interest): ').strip()
            clear_output()
            search_students(q)
        elif choice == '10' or choice == '🔟':
            q = input('Search keyword (course/subject): ').strip()
            clear_output()
            search_courses(q)
        elif choice == 'r':
            sid = int(input('StudentID for recommendations: ').strip())
            recs = recommend_courses(sid, top_n=6)
            clear_output()
            if len(recs) == 0:
                print('No recommendations found or invalid student.')
            else:
                print('📋 Recommendations: (Course - score)')
                for cid, name, sc in recs:
                    print(f"{cid} - {name}  (score: {sc:.2f})")
        elif choice == '0':
            print('👋 Bbye!')
            break
        else:
            print('⚠️ Invalid choice. Try again.')

# If run as a script in Jupyter, show the menu
if __name__ == '__main__':
    menu()





