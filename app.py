"""
app.py - Daily Routine Tracker Web Application
Framework: Streamlit
Author: College Project
"""

import streamlit as st
import pandas as pd
from datetime import date, datetime
import database as db
import analytics

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Daily Routine Tracker",
    page_icon="⏰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- CUSTOM CSS -----------------
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #64748B;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #F8FAFC;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge-high {
        background-color: #FEE2E2;
        color: #DC2626;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-med {
        background-color: #FEF3C7;
        color: #D97706;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-low {
        background-color: #DCFCE7;
        color: #16A34A;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .category-tag {
        background-color: #EFF6FF;
        color: #2563EB;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- INITIALIZE DATABASE -----------------
db.init_db()

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.image("https://cdn-icons-png.flantiq.com/512/3247/3247310.png", width=70)
    st.title("Routine Tracker")
    st.caption("College Mini-Project | Python & Streamlit")
    
    st.divider()
    
    # User Profile / Student details
    student_name = st.text_input("👤 Student Name", value="Student")
    st.markdown(f"**Welcome, {student_name}!**")
    
    # Date display
    today_date = date.today()
    st.markdown(f"📅 **Today:** `{today_date.strftime('%A, %d %B %Y')}`")
    
    st.divider()
    
    # Motivational quote
    quote = analytics.get_random_quote()
    st.info(f"{quote}")
    
    # Export data button
    st.divider()
    all_logs = db.get_all_logs_data()
    if all_logs:
        df_export = pd.DataFrame(all_logs)
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Logs to CSV",
            data=csv_data,
            file_name=f"routine_logs_{today_date.isoformat()}.csv",
            mime="text/csv",
            use_container_width=True
        )

# ----------------- MAIN HEADER -----------------
st.markdown('<div class="main-title">⏰ Daily Routine & Habit Tracker</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Stay disciplined, track college tasks, build consistency, and hit your daily goals.</div>', unsafe_allow_html=True)

# ----------------- TABS NAVIGATION -----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Today's Routine",
    "➕ Manage Routines",
    "📊 Analytics & Streaks",
    "🎓 Project Info & Viva Q&A"
])

# ===================================================
# TAB 1: TODAY'S ROUTINE
# ===================================================
with tab1:
    col_date, col_filter, col_pri = st.columns([2, 2, 2])
    
    with col_date:
        selected_date = st.date_input("Select Date to View/Log", value=today_date)
    
    routines_data = db.get_routines_with_status(selected_date)
    
    # Extract unique categories
    categories = sorted(list(set(r["category"] for r in routines_data)))
    with col_filter:
        cat_filter = st.selectbox("Filter by Category", ["All"] + categories)
    
    with col_pri:
        pri_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])

    # Apply filters
    filtered_routines = routines_data
    if cat_filter != "All":
        filtered_routines = [r for r in filtered_routines if r["category"] == cat_filter]
    if pri_filter != "All":
        filtered_routines = [r for r in filtered_routines if r["priority"] == pri_filter]

    # Metrics computation
    total_count = len(routines_data)
    completed_count = sum(1 for r in routines_data if r["completed"] == 1)
    completion_rate = int((completed_count / total_count * 100)) if total_count > 0 else 0
    
    # Streak metrics
    cur_streak, max_streak = analytics.calculate_streaks(all_logs)

    # Top summary cards
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Total Routines", value=total_count)
    m2.metric(label="Completed", value=completed_count)
    m3.metric(label="Completion Rate", value=f"{completion_rate}%")
    m4.metric(label="Current Streak", value=f"🔥 {cur_streak} Days")

    st.write("---")

    # Progress bar
    st.write(f"**Progress for {selected_date.strftime('%b %d, %Y')}**")
    st.progress(completion_rate / 100.0)

    if completion_rate == 100 and total_count > 0:
        st.success("🎉 Amazing! You have completed 100% of your daily routine! Keep it up!")
    elif completion_rate >= 50:
        st.info("💪 Halfway there! Complete the remaining tasks to seal the day.")
    
    st.write("")

    if not filtered_routines:
        st.warning("No routines found matching your filter. Add routines from the 'Manage Routines' tab!")
    else:
        st.subheader("📝 Routine Checklist")
        for r in filtered_routines:
            box_col, details_col, status_col = st.columns([0.5, 4, 1.5])
            
            # Checkbox key must be unique per routine and date
            cb_key = f"chk_{r['id']}_{selected_date.isoformat()}"
            is_done = bool(r["completed"])
            
            with box_col:
                new_state = st.checkbox("", value=is_done, key=cb_key)
                if new_state != is_done:
                    db.set_routine_status(r["id"], selected_date, new_state)
                    st.rerun()

            with details_col:
                # Text formatting with strikethrough if completed
                title_display = f"~~{r['title']}~~" if is_done else f"**{r['title']}**"
                pri_class = f"badge-{r['priority'].lower()[:3]}"
                
                cat_badge = f'<span class="category-tag">📂 {r["category"]}</span>'
                pri_badge = f'<span class="{pri_class}">⚡ {r["priority"]}</span>'
                time_badge = f'⏰ <b>{r["time_slot"]}</b>'
                
                st.markdown(f"{title_display} &nbsp; {time_badge} &nbsp; {cat_badge} &nbsp; {pri_badge}", unsafe_allow_html=True)
                if is_done and r.get("completion_time"):
                    st.caption(f"✅ Marked done on: {r['completion_time']}")

            with status_col:
                if is_done:
                    st.success("Done")
                else:
                    st.warning("Pending")

# ===================================================
# TAB 2: MANAGE ROUTINES
# ===================================================
with tab2:
    st.subheader("➕ Add New Routine / Habit")
    
    with st.form(key="add_routine_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            title = st.text_input("Routine / Task Title*", placeholder="e.g. Solve 3 LeetCode Problems")
            category = st.selectbox("Category", ["Study", "Fitness", "Productivity", "Personal", "Health", "College Work"])
            frequency = st.selectbox("Frequency", ["Daily", "Weekdays", "Weekends"])

        with c2:
            time_slot = st.text_input("Time Slot*", placeholder="e.g. 05:00 PM or Morning")
            priority = st.selectbox("Priority Level", ["High", "Medium", "Low"], index=1)
        
        submit_btn = st.form_submit_button("➕ Add Routine", use_container_width=True)
        if submit_btn:
            if not title.strip() or not time_slot.strip():
                st.error("Please provide both a Title and Time Slot.")
            else:
                db.add_routine(title, category, time_slot, priority, frequency)
                st.success(f"Routine '{title}' added successfully!")
                st.rerun()

    st.write("---")
    st.subheader("📋 Existing Routines")
    all_routines = db.get_all_routines()

    if not all_routines:
        st.info("No routines created yet. Use the form above to add your first daily routine!")
    else:
        for r in all_routines:
            with st.expander(f"⏰ {r['time_slot']} - {r['title']} ({r['category']})"):
                with st.form(key=f"edit_form_{r['id']}"):
                    ec1, ec2 = st.columns(2)
                    with ec1:
                        ed_title = st.text_input("Title", value=r["title"])
                        ed_cat = st.selectbox("Category", ["Study", "Fitness", "Productivity", "Personal", "Health", "College Work"], 
                                              index=["Study", "Fitness", "Productivity", "Personal", "Health", "College Work"].index(r["category"]) if r["category"] in ["Study", "Fitness", "Productivity", "Personal", "Health", "College Work"] else 0)
                        ed_freq = st.selectbox("Frequency", ["Daily", "Weekdays", "Weekends"],
                                               index=["Daily", "Weekdays", "Weekends"].index(r["frequency"]) if r["frequency"] in ["Daily", "Weekdays", "Weekends"] else 0)
                    with ec2:
                        ed_time = st.text_input("Time Slot", value=r["time_slot"])
                        ed_pri = st.selectbox("Priority", ["High", "Medium", "Low"],
                                              index=["High", "Medium", "Low"].index(r["priority"]) if r["priority"] in ["High", "Medium", "Low"] else 1)
                    
                    update_col, delete_col = st.columns([1, 1])
                    with update_col:
                        update_btn = st.form_submit_button("💾 Save Changes")
                    with delete_col:
                        delete_btn = st.form_submit_button("🗑️ Delete Routine", type="secondary")
                    
                    if update_btn:
                        db.update_routine(r["id"], ed_title, ed_cat, ed_time, ed_pri, ed_freq)
                        st.success("Routine updated!")
                        st.rerun()
                    if delete_btn:
                        db.delete_routine(r["id"])
                        st.warning("Routine deleted!")
                        st.rerun()

# ===================================================
# TAB 3: ANALYTICS & STREAKS
# ===================================================
with tab3:
    st.subheader("📊 Analytics, Consistency & Streaks")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.metric("🔥 Current Streak", f"{cur_streak} Consecutive Days")
    col_s2.metric("⭐ Longest Streak", f"{max_streak} Days")
    col_s3.metric("🎯 Total Logged Entries", len(all_logs))

    st.write("---")

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.write("📈 **Past 7 Days Completion Rate (%)**")
        trend_data = analytics.get_weekly_trend(all_logs, days_count=7)
        df_trend = pd.DataFrame(trend_data)
        if not df_trend.empty:
            df_display = df_trend.set_index("Date")[["Completion Rate (%)"]]
            st.bar_chart(df_display, color="#3B82F6")
        else:
            st.info("Log routine activities to see weekly performance trends!")

    with col_chart2:
        st.write("📂 **Routines by Category**")
        cat_counts = analytics.get_category_breakdown(routines_data)
        if cat_counts:
            df_cat = pd.DataFrame(list(cat_counts.items()), columns=["Category", "Total Routines"]).set_index("Category")
            st.bar_chart(df_cat, color="#10B981")
        else:
            st.info("Add routines to view category distribution!")

    st.write("---")
    st.subheader("🏆 Consistency Badges")
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        if cur_streak >= 1:
            st.success("🥉 **Bronze Starter**\n\n1+ Day Streak Achieved!")
        else:
            st.caption("🔒 *Bronze Starter (1 Day Streak)*")
    with b2:
        if cur_streak >= 3:
            st.success("🥈 **Consistency Champ**\n\n3+ Days Streak Achieved!")
        else:
            st.caption("🔒 *Consistency Champ (3 Days Streak)*")
    with b3:
        if cur_streak >= 7:
            st.success("🥇 **Weekly Warrior**\n\n7+ Days Streak Achieved!")
        else:
            st.caption("🔒 *Weekly Warrior (7 Days Streak)*")
    with b4:
        if cur_streak >= 30:
            st.success("👑 **Habit Master**\n\n30 Days Streak Achieved!")
        else:
            st.caption("🔒 *Habit Master (30 Days Streak)*")

# ===================================================
# TAB 4: PROJECT INFO & VIVA Q&A
# ===================================================
with tab4:
    st.subheader("🎓 College Project Details & Viva Q&A Guide")
    st.markdown("""
    This section is designed to help you prepare your project presentation and viva examination for your college teacher!

    ### 📌 Project Overview
    - **Project Title:** Daily Routine & Habit Tracker
    - **Domain:** Personal Productivity / Web Application Development
    - **Frontend:** Streamlit (Python Web Framework)
    - **Backend & Database:** SQLite3 (Embedded Relational Database)
    - **Data Analysis:** Pandas

    ---

    ### 💡 Viva / Oral Exam Q&A (Teacher ke sawalat or unke jawabat)

    **Q1: What is the main objective of this project?**  
    *Answer:* The objective is to provide students and users an automated system to manage daily routines, track completion progress in real-time, maintain habit streaks, and analyze weekly productivity via charts.

    **Q2: Why did you choose Streamlit instead of traditional Django or Flask?**  
    *Answer:* Streamlit is a modern Python framework optimized for data-driven applications. It provides reactive UI components, rapid prototyping, built-in state management, and seamless integration with Pandas and charting libraries without needing separate frontend HTML/CSS/JavaScript files.

    **Q3: Where is the data stored and how is it structured?**  
    *Answer:* The project uses **SQLite3**, a serverless, self-contained relational database stored locally in `routine_tracker.db`. It contains two normalized tables:
    1. `routines`: Stores routine definitions (title, category, time_slot, priority, frequency).
    2. `daily_logs`: Stores completion history linked via foreign key `routine_id` and unique `(routine_id, log_date)` constraints.

    **Q4: How does the Streak Calculation algorithm work?**  
    *Answer:* The algorithm checks unique dates in `daily_logs` where tasks were completed. It sorts the dates chronologically and checks consecutive backwards steps starting from today (or yesterday) to find continuous active days.

    **Q5: What are the future enhancements of this project?**  
    *Answer:* Future enhancements include email or WhatsApp notifications for upcoming routines, AI-driven routine recommendations based on student study schedules, and cloud synchronization.
    """)
