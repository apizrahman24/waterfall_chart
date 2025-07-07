#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
from openpyxl import Workbook

# --- Password Authentication ---
PASSWORD = "your_secret_password"
st.session_state["authenticated"] = st.session_state.get("authenticated", False)

if not st.session_state["authenticated"]:
    with st.form("login_form", clear_on_submit=True):
        password_input = st.text_input("Enter Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if password_input == PASSWORD:
                st.session_state["authenticated"] = True
                st.success("Access granted!")
            else:
                st.error("Incorrect password.")
    st.stop()

st.set_page_config(page_title="Stacked Waterfall Chart", layout="centered")
st.title("📊 Stacked Waterfall Chart with Editable Color Codes")

st.markdown("Each row represents a component (sub-part of a stage). You can type or paste hex color codes directly in the **Color** column (e.g., `#FFA07A`).")

# --- Step 1: Editable Input Table WITH Color column as free text ---
default_data = pd.DataFrame({
    "Stage": ["Base", "Base", "Feature A", "Feature A", "Feature B", "Feature B", "Feature C"],
    "Component": ["Base A", "Base B", "A1", "A2", "B1", "B2", "C1"],
    "Value": [100.00, 100.00, 30.50, 20.25, -10.75, -20.60, 15.30],
    "Color": ["#808080", "#A9A9A9", "#90EE90", "#228B22", "#FFA07A", "#FF4500", "#87CEEB"]
})

edited_df = st.data_editor(
    default_data,
    num_rows="dynamic",
    use_container_width=True,
    key="stacked_input"
)

# --- Sidebar: Helpful color reference note ---
with st.sidebar:
    st.markdown("## 💡 Tip Bar")
    st.markdown("### 🎨 Common Color Codes")
    st.markdown("""
Use these hex color codes in the **Color** column:

| Name                     | Code      |
|--------------------------|-----------|
| PETRONAS Emerald Green   | `#00B1A9` |
| PETRONAS Solid White     | `#FFFFFF` |
| PETRONAS Purple          | `#763F98` |
| PETRONAS Blue            | `#20419A` |
| PETRONAS Yellow          | `#FDB924` |
| PETRONAS Lime Green      | `#BFD730` |
| Black                    | `#000000` |
| Dark Gray                | `#A9A9A9` |
| Red                      | `#FF0000` |
| Default Gray             | `#888888` |

📋 Copy any of these and paste them into the **Color** column.
""")

    st.markdown("---")
    st.markdown("📌 **Tip:** Right-click the chart → **Save image as...** to download it.")

# --- Step 2: Prepare DataFrame, fallback default color if invalid or empty ---
def clean_color_code(code):
    if isinstance(code, str) and code.startswith("#") and len(code) in (7, 4):
        return code
    else:
        return "#888888"  # fallback gray color

df = edited_df.copy()
df["Color"] = df["Color"].apply(clean_color_code)
df["Stage"] = df["Stage"].astype(str)
df["Component"] = df["Component"].astype(str)

stage_list = df["Stage"].unique().tolist()
base_components = df[df["Stage"] == "Base"]

# --- Step 3: Compute base total and prepare bars ---
base_value = base_components["Value"].sum()

bars = []

# Plot Base subcomponents
bottom = 0
for _, row in base_components.iterrows():
    bars.append(go.Bar(
        name=row["Component"],
        x=["Base"],
        y=[row["Value"]],
        base=bottom,
        marker_color=row["Color"],
        customdata=[[row["Component"]]],
        hovertemplate="%{x}<br>Component: %{customdata[0]}<br>Value: %{y:.2f}<extra></extra>",
        text=[row["Value"]],
        textposition="outside",
        texttemplate="%{text:.2f}",
        textfont=dict(size=12)
    ))
    bottom += row["Value"]

# Plot other stages
non_base_stages = [s for s in stage_list if s != "Base"]

current_cumulative = base_value
for stage in non_base_stages:
    sub_df = df[df["Stage"] == stage]
    bottom = current_cumulative
    for _, row in sub_df.iterrows():
        bars.append(go.Bar(
            name=row["Component"],
            x=[stage],
            y=[row["Value"]],
            base=bottom,
            marker_color=row["Color"],
            customdata=[[row["Component"]]],
            hovertemplate="%{x}<br>Component: %{customdata[0]}<br>Value: %{y:.2f}<extra></extra>",
            text=[row["Value"]],
            textposition="outside",
            texttemplate="%{text:.2f}",
            textfont=dict(size=12)
        ))
        bottom += row["Value"]
    current_cumulative = bottom

# Final bar for cumulative total
bars.append(go.Bar(
    name="Final",
    x=["Final"],
    y=[current_cumulative],
    marker_color="#00B1A9",
    customdata=[["Total"]],
    hovertemplate="%{x}<br>Component: %{customdata[0]}<br>Value: %{y:.2f}<extra></extra>",
    text=[current_cumulative],
    textposition="outside",
    texttemplate="%{text:.2f}",
    textfont=dict(size=12)
))

# --- Step 4: Plot chart ---
fig = go.Figure(data=bars)
fig.update_layout(
    barmode="stack",
    title="Custom Stacked Waterfall Chart",
    yaxis_title="Value",
    xaxis_title="Stage",
    showlegend=True,
    plot_bgcolor="white",    # chart area background
    paper_bgcolor="white"    # full figure background
)

st.plotly_chart(fig, use_container_width=True)

# --- Step 5: Excel Export WITHOUT Chart Image ---
def create_excel_without_chart(df: pd.DataFrame) -> io.BytesIO:
    wb = Workbook()
    ws = wb.active
    ws.title = "Waterfall Data"
    ws.append(["Stage", "Component", "Value", "Color"])
    for _, row in df.iterrows():
        ws.append(row.tolist())

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output

# --- Step 6: Download Button ---
if st.button("📥 Download Excel Data"):
    excel_file = create_excel_without_chart(df)
    st.download_button(
        label="Download Excel File",
        data=excel_file,
        file_name="stacked_waterfall_data_only.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# In[ ]:




