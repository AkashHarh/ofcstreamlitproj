
Course Management System
A Full-Stack CRUD Application for Managing Courses and Enrollments

========================================================================================

🛠 FEATURES
========================================================================================

📚 Course Management
• View all courses in a clean, organized table
• Add new courses with unique Course IDs
• Update course details completely (PUT) or partially (PATCH)
• Delete courses safely with confirmation prompts
• Display success messages and celebratory balloons
• Automatic validation for required fields

👥 Enrollment Management
• Add students to courses with unique Enrollment IDs
• View all enrollments with detailed information
• Delete enrollments with ease
• Automatic validation for non-existent IDs

📊 Charts & Visualizations
Course Charts:
• Bar chart showing active vs inactive course status
• Duration distribution bar chart
• Line chart displaying courses added over time

Enrollment Charts:
• Bar chart for enrollments per course
• Student enrollment distribution chart

🔌 API Features
• Full RESTful API with GET, POST, PUT, PATCH, DELETE endpoints
• Proper HTTP status codes and response messages
• JSON responses for easy integration
• Auto-generated API documentation at /docs

========================================================================================

🗂 PROJECT STRUCTURE
========================================================================================

course-management/
│
├── app.py                    # Streamlit frontend application
├── main.py                   # FastAPI backend with API endpoints
├── db.py                     # SQLite database connection & setup
├── models.py                 # Pydantic models for data validation
├── course_management.db      # SQLite database (auto-created)
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation

========================================================================================

⚡ INSTALLATION & SETUP
========================================================================================

1. Clone the Repository
   git clone https://github.com/yourusername/course-management.git
   cd course-management

2. Create a Virtual Environment
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows

3. Install Dependencies
   pip install -r requirements.txt

4. Initialize the Database
   python db.py

5. Run the FastAPI Backend
   python main.py
   # Or: uvicorn main:app --reload
   
   Backend: http://127.0.0.1:8000
   API Docs: http://127.0.0.1:8000/docs

6. Run the Streamlit Frontend
   streamlit run app.py
   
   Frontend: http://localhost:8501

========================================================================================

🧩 HOW IT WORKS
========================================================================================

Component    | Technology | Responsibility
-------------|------------|-----------------------------------------------
Frontend     | Streamlit  | User interface, forms, tables, charts
Backend      | FastAPI    | CRUD operations, validation, JSON responses
Database     | SQLite     | Data persistence, ID management
Models       | Pydantic   | Data validation, type checking

========================================================================================

📝 USAGE TIPS
========================================================================================

⚠️ Important:
• Always verify IDs before updating or deleting
• Course names must be at least 3 characters
• Use refresh buttons to reload latest data
• Confirmation required before deleting records

========================================================================================

🚀 API ENDPOINTS
========================================================================================

Method  | Endpoint         | Description
--------|------------------|--------------------------------
GET     | /courses         | Retrieve all courses
GET     | /courses/{id}    | Get specific course by ID
POST    | /courses         | Create a new course
PUT     | /courses/{id}    | Full update (replace all fields)
PATCH   | /courses/{id}    | Partial update (specific fields)
DELETE  | /courses/{id}    | Delete a course

========================================================================================

💡 FUTURE IMPROVEMENTS
========================================================================================

🔍 Search and filter functionality
📊 Export data to CSV/Excel
🔐 User authentication (admin/student roles)
📈 Advanced analytics and reporting
📧 Email notifications
📱 Mobile-responsive design
🌐 Multi-language support

========================================================================================

💻 TECH STACK
========================================================================================

• Python 3.10+
• FastAPI
• Streamlit
• SQLite
• Pydantic
• Uvicorn
• Pandas
• Matplotlib

========================================================================================

📦 DEPENDENCIES
========================================================================================

fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
streamlit==1.28.0
requests==2.31.0
pandas==2.1.3
matplotlib==3.8.2

========================================================================================

🛡 LICENSE
========================================================================================

This project is open-source and free to use under the MIT License.
Feel free to modify, improve, and distribute as needed.

========================================================================================

👏 ACKNOWLEDGEMENTS
========================================================================================

FastAPI: https://fastapi.tiangolo.com
Streamlit: https://docs.streamlit.io
SQLite: https://www.sqlite.org
Pydantic: https://docs.pydantic.dev


