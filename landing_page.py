# app.py
import streamlit as st

st.set_page_config(page_title="📊 Chart Dashboard", layout="centered")

st.title("📊 Welcome to the Chart Dashboard")
st.markdown("### 👋 Hello!")

st.markdown("""
Welcome to your interactive charting dashboard.

Use the **sidebar** on the left to navigate between pages:

- 📉 **Stacked Waterfall Chart**: Visualize project cost components or performance stages.
- 🌞 **Sunburst Chart**: Explore hierarchical data with customizable colors.

---

🛠 Built with Streamlit + Plotly + Pandas
""")

st.markdown("📌 Need help or ideas? Drop a message below ⬇️")
