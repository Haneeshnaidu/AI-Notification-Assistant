# import os
# import streamlit as st
# import pandas as pd
# from sqlalchemy import create_engine
# from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# engine = create_engine(DATABASE_URL)

# st.title("AI Notification Assistant")

# df = pd.read_sql("SELECT * FROM notifications ORDER BY created_at DESC", engine)

# priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])

# if priority_filter != "All":
#     df = df[df["priority"] == priority_filter]

# st.dataframe(df)


import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL)

st.title("AI Notification Assistant")

# Auto refresh every 10 seconds
st_autorefresh(interval=10000, key="datarefresh")

# Load data
df = pd.read_sql("SELECT * FROM notifications ORDER BY created_at DESC", engine)

# Metrics section
col1, col2, col3 = st.columns(3)

col1.metric("High Priority", len(df[df["priority"] == "High"]))
col2.metric("Medium Priority", len(df[df["priority"] == "Medium"]))
col3.metric("Low Priority", len(df[df["priority"] == "Low"]))

st.divider()

# Filter section
priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])

if priority_filter != "All":
    df = df[df["priority"] == priority_filter]

# Display table
st.dataframe(df)


# import os
# import requests
# import streamlit as st
# import pandas as pd
# from sqlalchemy import create_engine
# from dotenv import load_dotenv
# from streamlit_autorefresh import st_autorefresh

# load_dotenv()

# DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# engine = create_engine(DATABASE_URL)

# st.title("AI Notification Assistant")

# # Auto refresh every 10 seconds
# st_autorefresh(interval=10000, key="datarefresh")

# # Load data
# df = pd.read_sql("SELECT * FROM notifications ORDER BY created_at DESC", engine)

# # Metrics section
# col1, col2, col3 = st.columns(3)

# col1.metric("High Priority", len(df[df["priority"] == "High"]))
# col2.metric("Medium Priority", len(df[df["priority"] == "Medium"]))
# col3.metric("Low Priority", len(df[df["priority"] == "Low"]))

# st.divider()

# # Priority chart
# st.subheader("Notification Priority Distribution")
# priority_counts = df["priority"].value_counts()
# st.bar_chart(priority_counts)

# st.divider()

# # Daily AI Summary
# st.subheader("Daily AI Summary")

# if st.button("Generate Summary"):
#     try:
#         response = requests.get("http://127.0.0.1:8000/daily-summary")
#         summary = response.json()["summary"]
#         st.success(summary)
#     except:
#         st.error("Could not fetch summary from API")

# st.divider()

# # Filter section
# priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])

# if priority_filter != "All":
#     df = df[df["priority"] == priority_filter]

# # Display table
# st.subheader("Notifications")
# st.dataframe(df)