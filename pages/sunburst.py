# pages/sunburst_chart.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sunburst Chart with Colors", layout="wide")
st.title("🌞 Customizable Sunburst Chart")

st.markdown("""
Manually enter your hierarchy and values. Adjust how many **levels (rings)** the sunburst chart displays, and customize the **color for each row**.
""")

with st.sidebar:
    st.markdown("## 💡 Tip Bar")
    st.markdown("### 🎨 Common Color Codes")
    st.markdown("""
| Name                   | Code      |
|------------------------|-----------|
| Bright Red             | `#FF5733` |
| Fresh Green            | `#33FF57` |
| Sky Blue               | `#3357FF` |
| PETRONAS Emerald Green | `#00B1A9` |
| PETRONAS Blue          | `#20419A` |
| Yellow                 | `#FDB924` |
| Black                  | `#000000` |
| Dark Gray              | `#A9A9A9` |
| Default Gray           | `#888888` |
""")
    st.markdown("---")
    st.markdown("📌 **Tip:** Right-click the chart → **Save image as...** to download it.")

example_data = {
    "Level 1": ["Asia", "Asia", "Europe"],
    "Level 2": ["China", "India", "Germany"],
    "Level 3": ["Beijing", "Mumbai", "Berlin"],
    "Value": [100, 80, 70],
    "Color": ["#FF5733", "#33FF57", "#3357FF"]
}

df_input = st.data_editor(
    pd.DataFrame(example_data),
    num_rows="dynamic",
    use_container_width=True,
    key="sunburst_input"
)

categorical_cols = df_input.select_dtypes(include='object').columns.tolist()
if "Color" in categorical_cols:
    categorical_cols.remove("Color")

numeric_cols = df_input.select_dtypes(include='number').columns.tolist()

if categorical_cols:
    level_count = st.slider("🔁 Number of Levels (Circles) to Show", 1, len(categorical_cols), value=len(categorical_cols))
    levels_to_use = categorical_cols[:level_count]
else:
    levels_to_use = []

if numeric_cols:
    value_col = st.selectbox("🔢 Select Value Column", numeric_cols)
else:
    st.error("⚠️ Please enter at least one numeric column for values.")
    st.stop()

color_map = dict()
if "Color" in df_input.columns:
    for _, row in df_input.iterrows():
        label = " - ".join([str(row[col]) for col in levels_to_use])
        color_map[label] = row["Color"]

if levels_to_use:
    df_input["CustomPath"] = df_input[levels_to_use].agg(" - ".join, axis=1)
else:
    st.warning("⚠️ Please select at least one level to generate the sunburst chart.")
    st.stop()

if levels_to_use and value_col:
    fig = px.sunburst(
        df_input,
        path=levels_to_use,
        values=value_col,
        color="CustomPath",
        color_discrete_map=color_map,
        title=f"🌈 Sunburst Chart with {level_count} Level(s) and Custom Colors"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ Please enter at least one categorical and one numeric column.")
