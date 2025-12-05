# import streamlit as st
# import requests
# import pandas as pd
# from typing import Dict, Any

# API_BASE_URL = "http://127.0.0.1:8000"

# st.set_page_config(
#     page_title="Course Management System",
#     layout="wide",
#     page_icon="🎓",
#     initial_sidebar_state="expanded"
# )

# st.markdown("""
#     <style>
#     .main-header {
#         font-size: 3rem;
#         font-weight: bold;
#         color: #1f77b4;
#     }
#     .stButton>button {
#         width: 100%;
#     }
#     </style>
# """, unsafe_allow_html=True)

# def show_response(resp: requests.Response, method: str, endpoint: str):
#     st.info(f"➡️ **{method} {endpoint}**")
#     if 200 <= resp.status_code < 300:
#         st.success(f"✅ Status: {resp.status_code}")
#     else:
#         st.error(f"❌ Status: {resp.status_code}")
#     try:
#         data = resp.json()
#         st.json(data)
#     except Exception:
#         st.text(resp.text)

# def make_api_call(method: str, endpoint: str, data: Dict[Any, Any] = None):
#     try:
#         url = f"{st.session_state.api_url}{endpoint}"
#         if method == "GET":
#             return requests.get(url)
#         elif method == "POST":
#             return requests.post(url, json=data)
#         elif method == "PUT":
#             return requests.put(url, json=data)
#         elif method == "PATCH":
#             return requests.patch(url, json=data)
#         elif method == "DELETE":
#             return requests.delete(url)
#     except Exception as e:
#         st.error(f"❌ Error connecting to API: {e}")
#         return None

# if "api_url" not in st.session_state:
#     st.session_state.api_url = API_BASE_URL

# st.markdown('<p class="main-header">🎓 Course Management System</p>', unsafe_allow_html=True)
# st.caption(
#     "Full-stack CRUD application | FastAPI + SQLite + Streamlit | "
#     "Supports GET / POST / PUT / PATCH / DELETE"
# )

# st.sidebar.header("📋 Navigation")
# operation = st.sidebar.radio(
#     "Select an operation",
#     [
#         "📊 View All Courses",
#         "🔍 Get Course by ID",
#         "➕ Add New Course",
#         "✏️ Update Course (PUT)",
#         "🔧 Partial Update (PATCH)",
#         "🗑️ Delete Course",
#     ],
# )

# # st.sidebar.markdown("---")
# # st.sidebar.subheader("⚙️ Settings")
# # st.session_state.api_url = st.sidebar.text_input("FastAPI Base URL", value=st.session_state.api_url)

# # st.sidebar.markdown("---")
# # st.sidebar.info(
# #     "💡 Quick Start:\n\n"
# #     "1. Run FastAPI: uvicorn main:app --reload\n"
# #     "2. Run Streamlit: streamlit run app.py"
# # )
# # st.sidebar.markdown("---")
# # st.sidebar.caption("📚 Course Management System v1.0")

# if operation == "📊 View All Courses":
#     st.header("📊 View All Courses")
#     col1, col2, col3 = st.columns([2, 1, 1])
#     with col2:
#         if st.button("🔄 Refresh", type="primary", use_container_width=True):
#             st.rerun()
#     st.markdown("---")
#     resp = make_api_call("GET", "/courses")
#     if resp and resp.status_code == 200:
#         courses = resp.json()
#         if courses:
#             st.success(f"✅ Found {len(courses)} course(s)")
#             df = pd.DataFrame(courses)
#             order = ["course_id", "course_name", "duration", "is_active", "created_at", "description"]
#             df = df[order]
#             st.dataframe(df, use_container_width=True, hide_index=True)
#             with st.expander("📄 View Raw JSON Response"):
#                 st.json(courses)
#         else:
#             st.warning("⚠️ No courses found.")
#     elif resp:
#         show_response(resp, "GET", "/courses")

# elif operation == "🔍 Get Course by ID":
#     st.header("🔍 Get Course by ID")
#     course_id = st.number_input("Enter Course ID", min_value=1, step=1, format="%d")
#     if st.button("🔍 Search Course", type="primary", use_container_width=True):
#         endpoint = f"/courses/{int(course_id)}"
#         resp = make_api_call("GET", endpoint)
#         if resp and resp.status_code == 200:
#             course = resp.json()
#             st.success("✅ Course found!")
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.metric("📋 Course ID", course["course_id"])
#                 st.metric("📚 Course Name", course["course_name"])
#             with col2:
#                 st.metric("⏱️ Duration", course["duration"] or "N/A")
#                 st.metric("🔄 Status", course["is_active"])
#             with col3:
#                 st.metric("📅 Created At", course["created_at"])
#             st.markdown("---")
#             st.subheader("📝 Description")
#             st.write(course["description"] or "_No description provided_")
#             with st.expander("📄 View Raw JSON"):
#                 st.json(course)
#         elif resp:
#             show_response(resp, "GET", endpoint)

# elif operation == "➕ Add New Course":
#     st.header("➕ Add New Course")
#     with st.form("create_course_form", clear_on_submit=True):
#         col1, col2 = st.columns(2)
#         with col1:
#             course_name = st.text_input("Course Name *", placeholder="e.g., Python Programming")
#             duration = st.text_input("Duration", placeholder="e.g., 3 Months")
#         with col2:
#             is_active = st.selectbox("Active Status *", options=["Yes", "No"], index=0)
#         description = st.text_area("Description", height=150)
#         submitted = st.form_submit_button("➕ Create Course", type="primary", use_container_width=True)
#         if submitted:
#             if not course_name:
#                 st.error("❌ Course name is required!")
#             else:
#                 payload = {
#                     "course_name": course_name,
#                     "description": description if description else None,
#                     "duration": duration if duration else None,
#                     "is_active": is_active,
#                 }
#                 with st.expander("📤 Request Payload"):
#                     st.json(payload)
#                 resp = make_api_call("POST", "/courses", payload)
#                 if resp and resp.status_code == 201:
#                     st.success("✅ Course created successfully!")
#                     st.balloons()
#                     st.info(f"🆔 New Course ID: {resp.json()['course_id']}")
#                 elif resp:
#                     show_response(resp, "POST", "/courses")

# elif operation == "✏️ Update Course (PUT)":
#     st.header("✏️ Update Course (Full Replace)")
#     st.warning("⚠️ This will replace ALL fields.")
#     course_id = st.number_input("Course ID to Update", min_value=1, step=1, format="%d")
#     with st.form("update_course_form"):
#         col1, col2 = st.columns(2)
#         with col1:
#             course_name = st.text_input("New Course Name *")
#             duration = st.text_input("New Duration")
#         with col2:
#             is_active = st.selectbox("Active Status *", options=["Yes", "No"], index=0)
#         description = st.text_area("New Description", height=150)
#         submitted = st.form_submit_button("✏️ Update Course", type="primary", use_container_width=True)
#         if submitted:
#             if not course_name:
#                 st.error("❌ Course name is required!")
#             else:
#                 payload = {
#                     "course_name": course_name,
#                     "description": description if description else None,
#                     "duration": duration if duration else None,
#                     "is_active": is_active,
#                 }
#                 endpoint = f"/courses/{int(course_id)}"
#                 with st.expander("📤 Request Payload"):
#                     st.json(payload)
#                 resp = make_api_call("PUT", endpoint, payload)
#                 if resp and resp.status_code == 200:
#                     st.success("✅ Course updated successfully!")
#                     with st.expander("📄 View Updated Course"):
#                         st.json(resp.json())
#                 elif resp:
#                     show_response(resp, "PUT", endpoint)

# elif operation == "🔧 Partial Update (PATCH)":
#     st.header("🔧 Partial Update Course")
#     course_id = st.number_input("Course ID to Update", min_value=1, step=1, format="%d")
#     st.subheader("Select fields to update:")
#     payload = {}
#     col1, col2 = st.columns(2)
#     with col1:
#         update_name = st.checkbox("✏️ Update Course Name")
#         if update_name:
#             name = st.text_input("New Course Name")
#             if name:
#                 payload["course_name"] = name
#         update_duration = st.checkbox("⏱️ Update Duration")
#         if update_duration:
#             dur = st.text_input("New Duration")
#             if dur:
#                 payload["duration"] = dur
#     with col2:
#         update_status = st.checkbox("🔄 Update Status")
#         if update_status:
#             status = st.selectbox("New Status", ["Yes", "No"])
#             payload["is_active"] = status
#         update_desc = st.checkbox("📝 Update Description")
#         if update_desc:
#             desc = st.text_area("New Description", height=100)
#             if desc:
#                 payload["description"] = desc
#     st.markdown("---")
#     if st.button("🔧 Apply Partial Update", type="primary", use_container_width=True):
#         if not payload:
#             st.warning("⚠️ No fields selected to update!")
#         else:
#             endpoint = f"/courses/{int(course_id)}"
#             with st.expander("📤 Request Payload"):
#                 st.json(payload)
#             resp = make_api_call("PATCH", endpoint, payload)
#             if resp and resp.status_code == 200:
#                 st.success("✅ Course updated successfully!")
#                 with st.expander("📄 View Updated Course"):
#                     st.json(resp.json())
#             elif resp:
#                 show_response(resp, "PATCH", endpoint)

# elif operation == "🗑️ Delete Course":
#     st.header("🗑️ Delete Course")
#     st.error("⚠️ This action cannot be undone!")
#     course_id = st.number_input("Course ID to Delete", min_value=1, step=1, format="%d")
#     st.markdown("---")
    
#     col1, col2 = st.columns([1, 3])
    
#     with col1:
#         confirm = st.checkbox("I understand")
    
#     with col2:
#         if st.button("🗑️ Delete Course", type="primary", disabled=not confirm, use_container_width=True):
#             endpoint = f"/courses/{int(course_id)}"
#             resp = make_api_call("DELETE", endpoint)
            
#             if resp and resp.status_code == 200:
#                 st.success("🎉 Course deleted successfully!")
#                 st.balloons()
                
#                 with st.expander("📄 View Response"):
#                     st.write("✔️ The course was removed from the system.")
#                     st.json(resp.json())
            
#             elif resp:
#                 show_response(resp, "DELETE", endpoint)


# st.markdown("---")
# st.caption("🎓 Course Management System | FastAPI + SQLite + Streamlit")
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

#API_BASE = "http://127.0.0.1:8000"
API_BASE = "https://ofcstreamlitproj.onrender.com"
st.session_state.api_url = API_BASE.rstrip("/")

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
    /* Pointer cursor for dropdowns */
    div[data-baseweb="select"] {
        cursor: pointer !important;
    }
    div[data-baseweb="select"] > div {
        cursor: pointer !important;
    }
    /* Pointer cursor for selectbox */
    .stSelectbox > div > div {
        cursor: pointer !important;
    }
    /* Pointer cursor for radio buttons */
    .stRadio > div {
        cursor: pointer !important;
    }
    /* Pointer cursor for buttons */
    .stButton>button {
        cursor: pointer !important;
        width: 100%;
    }
    /* Main header styling */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
    }
    /* NEW: Sidebar header styling */
    .sidebar .sidebar-content {
        background-color: #f0f2f6; /* Subtle background color for the sidebar */
    }
    .sidebar-title {
        color: #0c4c84; /* Deep blue color for the title */
        font-weight: 900;
        padding: 10px 0 10px 0;
        text-align: center;
        border-bottom: 2px solid #0c4c84;
        margin-bottom: 20px;
    }
    /* Styling for the Navigation Radio Buttons */
    .stRadio > label {
        font-size: 1.1em !important;
        font-weight: 500 !important;
    }
    /* Custom Styling for Metrics in Dashboard */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e6e6e6;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)


def api_call(method, endpoint, data=None):
    url = f"{st.session_state.api_url}{endpoint}"
    try:
        if method=="GET": 
            return requests.get(url)
        if method=="POST": 
            return requests.post(url,json=data)
        if method=="PUT": 
            return requests.put(url,json=data)
        if method=="PATCH": 
            return requests.patch(url,json=data)
        if method=="DELETE": 
            return requests.delete(url)
    except Exception as e:
        st.error(f"Network error: {e}")
        return None

def show_response(resp):
    if resp and resp.content: # Check if response object exists and has content
        with st.expander("📄 Response JSON"):
            try: 
                st.json(resp.json())
            except: 
                st.text(resp.text)
    elif resp:
         with st.expander("📄 Response Details"):
             st.text(f"Status: {resp.status_code}. No JSON content.")
def handle_api_response(resp, success_message, error_message_key="detail"):
    if resp is None:
        st.error("❌ No response received from API.")
        return

    # SUCCESS → 200 or 201
    if resp.status_code in (200, 201):
        st.success(success_message)
        st.balloons()

    # EXPECTED ERRORS → 400, 404, 409
    elif resp.status_code in (400, 404, 409):
        try:
            error_detail = resp.json().get(error_message_key, "Unknown error occurred")
        except:
            error_detail = f"Could not parse error message (Status {resp.status_code})"

        st.error(f"❌ {error_detail}")

    # ANY OTHER ERROR
    else:
        st.error(f"❌ API Failed: Status Code {resp.status_code}")

    # OPTIONAL: Show full API response below
    show_response(resp)


with st.sidebar:
    st.markdown("<h1 class='sidebar-title'>📘 CMS Dashboard</h1>", unsafe_allow_html=True)
    st.write("---")
    
    # Updated Navigation
    menu = st.radio(
        "🚀 **Navigation**", 
        ["🏠 Dashboard", "📚 Course Operations & Charts", "📋 Enrollment & Charts", "🔍 Student Search"],
        key="main_navigation"
    )
    

st.title("🎓 Course Management System")


if menu=="🏠 Dashboard":
    st.header(" Dashboard 🏠:Overview")
    
    # --- Metrics Section ---
    st.subheader("Key Performance Indicators")
    resp_summary = api_call("GET","/dashboard/summary")
    
    if resp_summary and resp_summary.status_code == 200:
        summary = resp_summary.json()
        
        col1, col2, col3 = st.columns(3)
        
        # Total Courses Metric
        with col1:
            st.metric(
                label="Total Courses 📚", 
                value=summary.get("total_courses", "N/A"),
                delta=f'{summary.get("active_courses", "N/A")} Active'
            )
        
        # Total Enrollments Metric
        with col2:
            st.metric(
                label="Total Enrollments 🧑‍🎓", 
                value=summary.get("total_enrollments", "N/A"),
            )
        
        # Active Courses Metric
        with col3:
            total_courses = summary.get("total_courses", 0)
            active_courses = summary.get("active_courses", 0)
            try:
                active_percent = f"{round((active_courses / total_courses) * 100)}%" if total_courses > 0 else "0%"
                st.metric(
                    label="Active Course Rate ✅", 
                    value=active_percent
                )
            except:
                 st.metric(
                    label="Active Course Rate ✅", 
                    value="N/A"
                )
        
        st.markdown("---")
        
        # --- Interactive Chart Widget ---
        st.subheader("Interactive Course Enrollment Distribution")
        
        resp_enroll = api_call("GET","/enrollments")
        resp_course = api_call("GET","/courses")
        
        if (resp_enroll and resp_enroll.status_code==200 and 
            resp_course and resp_course.status_code==200):
            
            df_enroll = pd.DataFrame(resp_enroll.json())
            df_course = pd.DataFrame(resp_course.json())
            
            if not df_enroll.empty and not df_course.empty:
                
                enroll_counts = df_enroll['course_id'].value_counts().reset_index()
                enroll_counts.columns = ['course_id', 'EnrollmentCount']
                
                df_course['course_id'] = pd.to_numeric(df_course['course_id'], errors='coerce')
                
                merged_df = pd.merge(enroll_counts, df_course[['course_id', 'course_name', 'is_active']], 
                                     on='course_id', how='left')
                merged_df['CourseLabel'] = merged_df['course_name'].fillna('Unknown Course') 

                # Filter options for the chart
                active_filter_chart = st.selectbox(
                    "Filter Courses by Status for Chart:", 
                    ["All", "Yes", "No"], 
                    key="dashboard_chart_filter"
                )
                
                chart_df = merged_df.copy()
                if active_filter_chart != "All":
                    chart_df = chart_df[chart_df['is_active'] == active_filter_chart]

                if not chart_df.empty:
                    fig_plotly = px.bar(
                        chart_df,
                        x='CourseLabel',
                        y='EnrollmentCount',
                        title=f'Total Enrollments per Course (Status: {active_filter_chart})',
                        labels={'CourseLabel': 'Course Name', 'EnrollmentCount': 'Number of Enrollments'},
                        color='EnrollmentCount',
                        hover_data={'course_id': True, 'is_active': True},
                        color_continuous_scale=px.colors.sequential.Tealgrn
                    )
                    fig_plotly.update_layout(xaxis={'categoryorder':'total descending'}, title_x=0.5)
                    st.plotly_chart(fig_plotly, use_container_width=True)
                else:
                    st.info("No courses found for the selected chart filter.")
            else:
                st.info("Enrollment or Course data is empty. Cannot display interactive chart.")
        else:
            st.warning("Failed to load enrollment or course data for the chart.")

        with st.expander("API Responses for Dashboard Data"):
            if resp_summary: st.json({"summary": resp_summary.json()})
            if resp_enroll: st.json({"enrollments": resp_enroll.json()})
            if resp_course: st.json({"courses": resp_course.json()})

    else:
        st.error("Could not load dashboard summary from API.")
        if resp_summary:
            show_response(resp_summary)


elif menu=="📚 Course Operations & Charts":
    operation = st.selectbox("Operation", ["View All (Filtered)", "Add", "Update (Full)", "Update (Partial)", "Delete", "Charts"])
    
    if operation=="View All (Filtered)":
        st.subheader("Filter and Search Courses")
        
        col_search, col_filter = st.columns([3, 1])
        with col_search:
            search_term = st.text_input("Search Name or Description", key="course_search_term")
        with col_filter:
            active_filter = st.selectbox("Status Filter", ["All", "Yes", "No"], key="course_active_filter")
        
        
        params = {}
        if active_filter != "All":
            params["is_active"] = active_filter
        if search_term:
            params["search"] = search_term
            
        resp = api_call("GET","/courses", data=None) 
        if resp and resp.status_code==200:
        
            resp = requests.get(f"{st.session_state.api_url}/courses", params=params)
            
            if resp and resp.status_code==200:
                df = pd.DataFrame(resp.json())
                if not df.empty: 
                    st.dataframe(df.sort_values("course_id"))
                else:
                    st.info("No courses found matching the criteria.")
            
        show_response(resp)
    
    elif operation=="Add":
        cid = st.number_input("Course ID", min_value=1, step=1)
        name = st.text_input("Name")
        dur = st.number_input("Duration (hr)", min_value=1,  format="%d")

        desc = st.text_area("Description")
        active = st.selectbox("Active",["Yes","No"])
        if st.button("Add Course"):
            payload={"course_id":cid,"course_name":name,"duration":dur,"description":desc,"is_active":active}
            resp = api_call("POST","/courses",payload)
            handle_api_response(resp, 
                                success_message=f"🎉 Course {name} added",
                                error_message_key="detail")
    
    # elif operation=="Update (Full)":
    #     st.warning("⚠️ Full Update (PUT) - All fields will be replaced")
    #     cid = st.number_input("Course ID to Update",min_value=1,step=1)
    #     name = st.text_input("New Name")
    #     dur = st.text_input("New Duration")
    #     desc = st.text_area("New Description")
    #     active = st.selectbox("Active",["Yes","No"])
    #     if st.button("Update Course (PUT)"):
    #         payload={"course_id":cid,"course_name":name,"duration":dur,"description":desc,"is_active":active}
    #         resp = api_call("PUT",f"/courses/{cid}",payload)
    #         handle_api_response(resp, 
    #                             success_message=f"✅ Updated Course {cid}",
    #                             error_message_key="detail")

    elif operation == "Update (Full)":
        st.warning("⚠️ Full Update (PUT) - All fields will be replaced")
        cid = st.number_input("Course ID to Update", min_value=1, step=1)
        name = st.text_input("New Name")
        dur = st.number_input("Duration (hr)", min_value=1,  format="%d")
        desc = st.text_area("New Description")
        active = st.selectbox("Active", ["Yes", "No"])

        if st.button("Update Course (PUT)"):

            payload = {
                "course_id": cid,
                "course_name": name,
                "duration": dur,
                "description": desc,
                "is_active": active
            }

            resp = api_call("PUT", f"/courses/{cid}", payload)

            # NEW - Handle 404 before calling handler
            if resp.status_code == 404:
                st.error(f"❌ Course ID {cid} not found.")
            else:
                handle_api_response(
                    resp,
                    success_message=f"✅ Updated Course {cid}",
                    error_message_key="detail"
                )


    
    elif operation=="Update (Partial)":
        st.info("💡 Partial Update (PATCH) - Update only selected fields")
        cid = st.number_input("Course ID to Update",min_value=1,step=1)
        
        st.subheader("Select fields to update:")
        payload = {}
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.checkbox("Update Name"):
                new_name = st.text_input("New Name")
                if new_name:
                    payload["course_name"] = new_name
            
            if st.checkbox("Update Duration"):
                new_dur = st.number_input("Duration (hr)", min_value=1,  format="%d")
                if new_dur:
                    payload["duration"] = new_dur
        
        with col2:
            if st.checkbox("Update Status"):
                new_active = st.selectbox("New Status", ["Yes","No"])
                payload["is_active"] = new_active
            
            if st.checkbox("Update Description"):
                new_desc = st.text_area("New Description")
                if new_desc:
                    payload["description"] = new_desc
        
        if st.button("Apply Partial Update (PATCH)"):
            if not payload:
                st.warning("⚠️ No fields selected to update!")
            else:
                resp = api_call("PATCH",f"/courses/{cid}",payload)
                # handle_api_response(resp, 
                #                     success_message=f"✅ Partially Updated Course {cid}",
                #                     error_message_key="detail")
                if resp.status_code == 404:
                    st.error(f"❌ Course ID {cid} not found.")
                else:
                    handle_api_response(
                        resp,
                        success_message=f"✅ Partially Updated Course {cid}",
                        error_message_key="detail"
                    )

    

            
    elif operation=="Delete":
        cid = st.number_input("Course ID to Delete",min_value=1,step=1)
        if st.button("Delete Course"):
            resp = api_call("DELETE",f"/courses/{cid}")
            if resp and resp.status_code==200:
                json_resp = resp.json()
                if json_resp.get("success"): 
                    st.success(json_resp.get("message"))
                else: 
                    st.error(json_resp.get("message"))
            elif resp:
                handle_api_response(resp, "", error_message_key="detail") 
            show_response(resp)

    elif operation=="Charts":
        resp = api_call("GET","/courses")
        if resp and resp.status_code==200:
            df = pd.DataFrame(resp.json())
            if not df.empty:
                
                st.subheader("🥧 Course Status Distribution (Interactive Pie Chart)")
                status_counts = df['is_active'].value_counts().reset_index()
                status_counts.columns = ['Status', 'Count']

                fig_pie = px.pie(
                    status_counts, 
                    values='Count', 
                    names='Status', 
                    title='Course Active Status Breakdown',
                    color_discrete_sequence=px.colors.sequential.Teal
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
                
                st.subheader("📊 Course Duration Distribution")
                dur_counts = df['duration'].fillna("Unknown").value_counts()
                
                fig, ax = plt.subplots(figsize=(8, 5))
                dur_counts.plot(kind='bar', ax=ax, color='skyblue')
                ax.set_title('Course Duration Breakdown', fontsize=16)
                ax.set_xlabel('Duration', fontsize=12)
                ax.set_ylabel('Count', fontsize=12)
                ax.tick_params(axis='x', rotation=45)
                ax.grid(axis='y', linestyle=':', alpha=0.6)
                st.pyplot(fig)

                st.subheader("📈 Number of Courses Added Over Time")
                df['created_at'] = pd.to_datetime(df['created_at'])
                time_counts = df.groupby(df['created_at'].dt.date).size()
                
                fig, ax = plt.subplots()
                time_counts.plot(kind='line', ax=ax, marker='o', color='green')
                ax.set_title('Courses Added Over Time', fontsize=16)
                ax.set_xlabel('Date', fontsize=12)
                ax.set_ylabel('New Courses', fontsize=12)
                ax.tick_params(axis='x', rotation=45)
                ax.grid(True, linestyle='--', alpha=0.7)
                st.pyplot(fig)

elif menu=="📋 Enrollment & Charts":
    section = st.selectbox("Section", ["Enrollment Operations", "Charts"])
    
    if section=="Enrollment Operations":
        op = st.selectbox("Enrollment Operation", ["View All", "Add", "Delete"])
        if op=="View All":
            resp = api_call("GET","/enrollments")
            if resp and resp.status_code==200:
                df = pd.DataFrame(resp.json())
                if not df.empty: st.dataframe(df.sort_values("enrollment_id"))
            show_response(resp)
        elif op=="Add":
            eid = st.number_input("Enrollment ID", min_value=1, step=1)
            cid = st.number_input("Course ID", min_value=1, step=1)
            name = st.text_input("Student Name")
            if st.button("Add Enrollment"):
                payload={"enrollment_id":eid,"course_id":cid,"student_name":name}
                resp = api_call("POST","/enrollments",payload)
                handle_api_response(resp, 
                                    success_message=f"🎉 Enrollment added", 
                                    error_message_key="detail") 
        elif op=="Delete":
            eid = st.number_input("Enrollment ID to Delete", min_value=1, step=1)
            if st.button("Delete Enrollment"):
                resp = api_call("DELETE",f"/enrollments/{eid}")
                if resp and resp.status_code==200:
                    json_resp = resp.json()
                    if json_resp.get("success"): st.success(json_resp.get("message"))
                    else: st.error(json_resp.get("message"))
                elif resp:
                    handle_api_response(resp, "", error_message_key="detail")
                show_response(resp)
    
    elif section=="Charts":
        resp_enroll = api_call("GET","/enrollments")
        resp_course = api_call("GET","/courses")
        
        if resp_enroll and resp_enroll.status_code==200 and resp_course and resp_course.status_code==200:
            df_enroll = pd.DataFrame(resp_enroll.json())
            df_course = pd.DataFrame(resp_course.json())
            
            if not df_enroll.empty:
                
                st.subheader("📊 Enrollments per Course (Interactive)")
                
                enroll_counts = df_enroll['course_id'].value_counts().reset_index()
                enroll_counts.columns = ['course_id', 'EnrollmentCount']
                
                df_course['course_id'] = pd.to_numeric(df_course['course_id'], errors='coerce')
                
                merged_df = pd.merge(enroll_counts, df_course[['course_id', 'course_name']], 
                                     on='course_id', how='left')
                merged_df['CourseLabel'] = merged_df['course_name'].fillna('Unknown Course') + ' (ID: ' + merged_df['course_id'].astype(str) + ')'

                fig_plotly = px.bar(
                    merged_df,
                    x='CourseLabel',
                    y='EnrollmentCount',
                    title='Total Enrollments per Course',
                    labels={'CourseLabel': 'Course', 'EnrollmentCount': 'Number of Enrollments'},
                    color='EnrollmentCount',
                    color_continuous_scale=px.colors.sequential.Viridis
                )
                fig_plotly.update_layout(xaxis={'categoryorder':'total descending'})
                st.plotly_chart(fig_plotly, use_container_width=True)

                st.subheader("📊 Enrollments by Students")
                student_counts = df_enroll['student_name'].value_counts()
                
                fig, ax = plt.subplots(figsize=(8, 5))
                student_counts.plot(kind='barh', ax=ax, color='purple')
                ax.set_title('Enrollments per Student', fontsize=16)
                ax.set_xlabel('Number of Enrollments', fontsize=12)
                ax.set_ylabel('Student Name', fontsize=12)
                ax.grid(axis='x', linestyle=':', alpha=0.6)
                st.pyplot(fig)
            else:
                st.info("No enrollment data available for charts.")


# elif menu == "🔍 Student Search":
#     st.header("🔍 Student Enrollment History")
#     student_name_search = st.text_input("Enter Student Name to Search")
    
#     if st.button("Search Enrollments"):
#         if student_name_search:
#             search_url = f"{st.session_state.api_url}/students/{student_name_search}/enrollments"
#             resp = requests.get(search_url)
            
#             if resp and resp.status_code == 200:
#                 data = resp.json()
#                 df = pd.DataFrame(data)
                
#                 st.subheader(f"Results for: **{student_name_search}**")
                
#                 display_df = df[['enrollment_id', 'course_id', 'enrolled_at']].copy()
#                 st.dataframe(display_df.sort_values("enrolled_at", ascending=False))
                
#                 st.success(f"Found {len(df)} enrollments for {student_name_search}")
#             elif resp:
#                 st.subheader("Search Failed")
#                 handle_api_response(resp, "", error_message_key="detail")
#             show_response(resp)
#         else:
#             st.warning("Please enter a student name.")
elif menu == "🔍 Student Search":
    st.header("🔍 Student Enrollment History")
    student_name_search = st.text_input("Enter Student Name to Search")

    if st.button("Search Enrollments"):
        if student_name_search:
            search_url = f"{st.session_state.api_url}/students/{student_name_search}/enrollments"
            resp = requests.get(search_url)

            # 🔴 Student NOT FOUND → backend returns 404
            if resp.status_code == 404:
                st.error(resp.json().get("detail", "Student not found"))
                show_response(resp)
                st.stop()

            # 🟡 Student exists but ZERO enrollments → backend returns 204
            if resp.status_code == 204:
                st.warning(resp.json().get("detail", "No enrollments found"))
                show_response(resp)
                st.stop()

            # 🟢 Student exists WITH enrollments → 200 OK
            if resp.status_code == 200:
                data = resp.json()
                df = pd.DataFrame(data)

                st.subheader(f"Results for: **{student_name_search}**")

                display_df = df[['enrollment_id', 'course_id', 'enrolled_at']].copy()
                st.dataframe(display_df.sort_values("enrolled_at", ascending=False))

                st.success(f"Found {len(df)} enrollments for {student_name_search}")
                show_response(resp)
                st.stop()

            # ❗ Any other unexpected response
            st.error(f"Unexpected error ({resp.status_code})")
            show_response(resp)
        else:
            st.warning("Please enter a student name.")
