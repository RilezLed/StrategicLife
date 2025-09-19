import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

fig = None
css = """
.st-key-my_custom_container {
    background-color: rgba(28, 30, 46, 0.82); /* Light blue */
    padding: 20px;
    border-radius: .5px;
    border: 15px solid #3c4d78;
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.2);
}
.st-key-my_custom_container2 {
    background-color: rgba(0, 3, 31, 0.82); /* Light blue */
    padding: 20px;
    border-radius: 10px;
    align-items: center;
    box-shadow: 20px 20px 20px rgba(0, 0, 0, 0.9);
}
.st-key-my_custom_container3 {
    background-color: rgba(0, 3, 31, 0.82); /* Light blue */
    padding: 20px;
    border-radius: 10px;
    align-items: center;
    box-shadow: 20px 20px 20px rgba(0, 0, 0, 0.9);
}
.st-key-my_custom_container4 {
    background-color: rgba(0, 3, 31, 0.82); /* Light blue */
    padding: 20px;
    border-radius: 10px;
    align-items: center;
    box-shadow: 20px 20px 20px rgba(0, 0, 0, 0.9);
}
"""

st.markdown(
    """
    <style>
    /* Animate the gradient flowing down-right */
    @keyframes gradientDrift {
        0% {background-position: 0% 0%;}
        100% {background-position: 50% 50%;}
    }

    /* Apply gradient + soft cube overlay */
    .stApp {
        background: linear-gradient(135deg, #07184a, #031036, #01081c, #01030a);
        background-size: 300% 300%;
        animation: gradientDrift 60s linear infinite;

        /* Overlay soft cube pattern */
        background-image:
            linear-gradient(45deg, rgba(163, 163, 163,0.03) 25%, transparent 25%),
            linear-gradient(-45deg, rgba(163, 163, 163,0.03) 25%, transparent 25%),
            linear-gradient(45deg, transparent 75%, rgba(163, 163, 163,0.03) 75%),
            linear-gradient(-45deg, transparent 75%, rgba(163, 163, 163,0.03) 75%);
        background-size: 70px 70px;
        background-blend-mode: overlay;
        filter: blur(0.3px); /* softens the pattern */
    }


    """,
    unsafe_allow_html=True
)


# Inject the CSS into the Streamlit app
st.html(f"<style>{css}</style>")

# --- Base Data ---
baseDf = pd.DataFrame({
    "Strategic Life Area(SLA)": ["Relationships", "Relationships", "Relationships", "Body,Mind & Spirit", "Body,Mind & Spirit", "Body,Mind & Spirit", "Community & Society", "Community & Society", "Jobs, Learning, & Finances", "Jobs, Learning, & Finances", "Jobs, Learning, & Finances", "Interests and Entertainment", "Interests and Entertainment", "Interests and Entertainment", "Basic Needs", "Basic Needs"],
    "Strategic Life Unit(SLU)": ["Significant Other", "Family", "Friends", "Physical Health", "Mental Health", "Spirituality", "Community", "Societal Engagement", "Career", "Education", "Finances", "Hobbies", "Online Entertainment", "Offline Entertainment", "Physiological Needs", "Daily Living Activities"],
    "Time Dedicated(hrs/week)": [0]*16,
    "Importance(1-10)": [0]*16,
    "Satisfaction(1-10)": [0]*16
})

# --- Session State ---
if "df" not in st.session_state:
    st.session_state.df = baseDf.copy()
if "show_chart" not in st.session_state:
    st.session_state.show_chart = False

st.set_page_config(page_title="Strategic Life Planner", page_icon="🧩", layout="wide")
st.write ("# Strategic Life Portfolio")


with st.container(width="stretch", height="content", key="my_custom_container", border=True): # Fixed width, height based on content
    mainCol1, mainCol2 = st.columns([3, 2], gap="large")
    mainCol1.write ("## ♖ Intro")
    mainCol1.write("")
    mainCol1.write("&nbsp;&nbsp;&nbsp;&nbsp; Life is a complex and multifaceted journey, encompassing various domains that contribute to our overall well-being and fulfillment." \
                  " However, many individuals struggle to find balance and alignment across these areas, leading to feelings of dissatisfaction and imbalance. "
                   "How we go about managing and optimizing these domains can significantly impact our happiness and success. Inspired by strategic business frameworks, we can apply similar principles to our personal lives to achieve a more balanced and intentional approach." )
    mainCol1.write("&nbsp;&nbsp;&nbsp;&nbsp; This Strategic Life Planner aims to provide a structured approach to evaluating and optimizing these key life domains, helping individuals to create a more harmonious and fulfilling life experience. This tool was created based on the principles outlined in Rainer Strack's Article 'Use Strategic Thinking to Create the Life You Want' and the accompanying HBR Video.")
    mainCol1.write("&nbsp;&nbsp;&nbsp;&nbsp; The planner consists of three main steps: (1) Taking Inventory of Your Strategic Life Units, (2) Visualizing Your Life Balance with a Quadrant Chart, and (3) Generating Insights and Actionable Steps for Improvement. By following these steps, individuals can gain clarity on their current life balance, identify areas for improvement, and develop a strategic plan to enhance their overall well-being.")
    mainCol1.write("")
    mainCol1.write("")
    mainCol1.link_button("Watch full HBR Video Here", "https://www.youtube.com/watch?v=dbiNhAZlXZk", icon="🔗")
    mainCol1.link_button("Read full HBR Article Here", "https://hbr.org/2023/12/use-strategic-thinking-to-create-the-life-you-want", icon="🔗")

    mainCol2.write("")
    mainCol2.write("")
    mainCol2.image("chess.jpg", caption="Strategic Life Planning is like Chess - think several moves ahead!", use_container_width=True)


with st.container(width="stretch", height="content", key="my_custom_container2"):
    st.write("## Step 1: Your Strategic Life Table", align="left")

    dtCol1, dtCol2, dtCol3 = st.columns([4, 1,3], gap="medium")
    dtCol3.write("### Taking Inventory of Your Strategic Life Units")
    dtCol3.write("&nbsp;&nbsp;&nbsp;&nbsp; To emulate the strategic thinking used in business, we start by taking inventory of the key areas of life. ")
    dtCol3.write("&nbsp;&nbsp;&nbsp;&nbsp; On the left is a table that outlines various Strategic Life Areas (SLAs) and their corresponding Strategic Life Units (SLUs). " \
    "These are meant to represent the major domains of life that contribute to overall well-being and fulfillment. For each SLU, you will assess three key dimensions: Time Dedicated (in hours per week), Importance (on a scale of 1-10), and Satisfaction (on a scale of 1-10). ")
    dtCol3.write("&nbsp;&nbsp;&nbsp;&nbsp; Take a few minutes to fill out the table based on your current life situation by clicking on the individual cells and typing in your values." \
    "Values will be express in whole numbers only. For Importance and Satisfaction, use a scale of 1-10, where 1 is the lowest and 10 is the highest. For Time Dedicated, estimate the average number of hours you spend on each SLU per week. " \
    " Be honest and reflective in your assessments, as this will provide the foundation for the next steps in the strategic life planning process. "
    "Once you are done, navigate to Step 2 and hit Update/Show Graph button to visualize your life balance. "\
        "Afterwards, navigate to Step 3 to generate insights and actionable steps for improvement.")
    dtCol3.write("&nbsp;&nbsp;&nbsp;&nbsp; You can also generate a random portfolio example to see how the chart and insights work, or reset the table to start over. ")
    dtCol3.write("Additonally, by hovering over the top right of the table, you can download your filled out table as a CSV file for your records. ")

    #dtCol1.image("journal.jpg", caption="Reflect on your life balance regularly to make adjustments as needed.", use_container_width=True)
dtCol2.write("")
dtCol2.write("")
dtCol2.write("")
dtCol2.write("")
dtCol2.write("")

if dtCol2.button("🎲 Generate Me a Random Portfolio Example"):
    st.session_state.df["Time Dedicated(hrs/week)"] = np.random.randint(0, 20, size=len(st.session_state.df))       # 0–20 hrs
    st.session_state.df["Importance(1-10)"] = np.random.randint(1, 11, size=len(st.session_state.df))              # 1–10
    st.session_state.df["Satisfaction(1-10)"] = np.random.randint(1, 11, size=len(st.session_state.df))            # 1–10

    st.session_state["edited_df"] = st.session_state.df  # keep it persistent in session
    st.success("✅ Random portfolio generated!")

dtCol2.write("")  # Spacer

if dtCol2.button("🔄 Reset Table", type="secondary", width="stretch"):
    st.session_state.df = baseDf.copy()
    st.session_state.show_chart = False
    st.rerun()  # refresh with reset table
    
    print("Reset clicked")

dtCol2.write("")  # Spacer



st.write("---")
col1, col2 = st.columns([2, 3], gap="large")

def generate_table(df):
    return dtCol1.data_editor(
        df,
        column_config={
            "Time Dedicated(hrs/week)": st.column_config.NumberColumn(
                "Time Dedicated(hrs/week)", min_value=0, max_value=168, step=1, format="%d hrs"
            ),
            "Importance(1-10)": st.column_config.NumberColumn(
                "Importance(1-10)", min_value=1, max_value=10, step=1
            ),
            "Satisfaction(1-10)": st.column_config.NumberColumn(
                "Satisfaction(1-10)", min_value=1, max_value=10, step=1
            ),
        },
        disabled=["Strategic Life Area(SLA)", "Strategic Life Unit(SLU)"],
        hide_index=True,
        height=600,
    )

# --- Chart Function ---
def generate_quadrant_chart(data):
    fig = px.scatter(
        data,
        x="Satisfaction(1-10)",
        y="Importance(1-10)",
        size="Time Dedicated(hrs/week)",
        color="Strategic Life Area(SLA)",
        hover_data=["Strategic Life Unit(SLU)", "Time Dedicated(hrs/week)"]
    )
    fig.add_shape(type="line", x0=5, x1=5, y0=0, y1=10, line=dict(color="black", dash="dash"))
    fig.add_shape(type="line", x0=0, x1=10, y0=5, y1=5, line=dict(color="black", dash="dash"))
    fig.add_shape(type="rect", x0=5, x1=10, y0=5, y1=10,
              fillcolor="green", opacity=.15, line_width=0)
    fig.add_shape(type="rect", x0=0, x1=5, y0=5, y1=10,
              fillcolor="orange", opacity=.15, line_width=0)
    fig.add_shape(type="rect", x0=5, x1=10, y0=0, y1=5,
              fillcolor="blue", opacity=.15, line_width=0)
    fig.add_shape(type="rect", x0=0, x1=5, y0=0, y1=5,
              fillcolor="gray", opacity=.15, line_width=0)
    fig.add_annotation(x=5, y=5, text="↑ Important / Satisfied →", showarrow=False, font=dict(size=12, color="gray"))
    
    fig.update_layout(
        title="Life Balance Quadrant Chart",
        xaxis=dict(title="Satisfaction (1-10)", range=[-1, 11]),
        yaxis=dict(title="Importance (1-10)", range=[-1, 11]),
        template="plotly_white",
        margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    height=800, width=600)
    return fig

with st.container(width="stretch", height="content", key="my_custom_container3"):
    st.write("## Step 2. Your Life Balance Quadrant Chart")



    edited_df = generate_table(st.session_state.df)
    if st.button(" ⬆️ Update/Show Graph", type="secondary"):
        st.session_state.df = edited_df.copy()
        st.session_state.show_chart = True
        st.success("✅ Chart updated!")
        
    with st.expander("ℹ️ Chart Explanation & How to Use It"):
        st.write("")
        st.write("&nbsp;&nbsp;&nbsp;&nbsp; The Quadrant Chart visualizes your Strategic Life Units (SLUs) based on three key dimensions: Satisfaction, Importance, and Time Dedicated. Quadrants in the upper left represent areas that are important to you but where you have low satisfaction, indicating potential areas for improvement. Quadrants in the upper right represent areas where you are both satisfied and consider important, suggesting strengths to maintain. The size of the bubbles indicates the amount of time you dedicate to each SLU, providing insight into how your time allocation aligns with your priorities.")

    # --- Chart Display ---
    if st.session_state.show_chart:
        
        fig = generate_quadrant_chart(st.session_state.df)
        st.plotly_chart(fig, use_container_width=True)

st.write("---")

with st.container(width="stretch", height="content", key="my_custom_container4"):
    
    st.write("## Step 3. Summary  & Insights")
    st.write("")

    if st.button(" 🗒️ Generate Summary", type="secondary"):
        st.write("")
        st.write("")
        # Example rules for insights:
        Icol1, Icol2, Icol3 = st.columns([2,2,2], gap="large")
        high_time = edited_df.sort_values("Time Dedicated(hrs/week)", ascending=False).head(1)
        Icol1.write(f"⏱ You dedicate the most time to **{high_time['Strategic Life Area(SLA)'].values[0]}: {high_time['Strategic Life Unit(SLU)'].values[0]} ** ({high_time['Time Dedicated(hrs/week)'].values[0]} hrs/week).")

        low_satisfaction = edited_df[edited_df["Satisfaction(1-10)"] < 5]
        if not low_satisfaction.empty:
            Icol2.write("⚠️ Areas with low satisfaction:")
            for _, row in low_satisfaction.iterrows():
                Icol2.write(f"- {row['Strategic Life Unit(SLU)']} (Sat: {row['Satisfaction(1-10)']}, Imp: {row['Importance(1-10)']})")

        high_importance_low_time = edited_df[(edited_df["Importance(1-10)"] >= 7) & (edited_df["Time Dedicated(hrs/week)"] < 5)]
        if not high_importance_low_time.empty:
            Icol3.write("📉 Areas you consider important but spend little time on:")
            for _, row in high_importance_low_time.iterrows():
                Icol3.write(f"- {row['Strategic Life Unit(SLU)']} (Imp: {row['Importance(1-10)']}, Time: {row['Time Dedicated(hrs/week)']})")

        print("Generate Summary clicked")
    st.write("")
    st.write("")




