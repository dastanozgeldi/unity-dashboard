from collections import Counter
import pandas as pd
import requests
import streamlit as st
from datetime import datetime

st.title("Unity Dashboard")
name = st.text_input("Enter your name", max_chars=50)

if name:
    BASE_URL = "http://127.0.0.1:8000/dashboard/get_distractions"
    url = f"{BASE_URL}?name={name}"
    r = requests.get(url)

    data = r.json()["distractions"]
    # sample 2023-07-01T16:54:36.920Z
    now = datetime.now()
    distracted_hours = [
        distraction["time"].split("T")[1][0:2]
        for distraction in data
        # Showing for today
        if distraction["time"][0:10] == str(now)[0:10]
    ]

    distraction_count = Counter(distracted_hours)

    # distraction_count = get_data(name)
    data = {
        "Hour": distraction_count.keys(),
        "Number of Distractions": distraction_count.values(),
    }
    df = pd.DataFrame(data)

    st.write(f"## {name}")

    # Plot the histogram using st.bar_chart
    st.bar_chart(df, y="Number of Distractions", x="Hour")
    st.write(df)
