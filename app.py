import streamlit as st
import pandas as pd
from amazon_price import get_amazon_price

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Smart Laptop Recommender",
    page_icon="💻",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("laptops.csv")

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "💻 Recommendation", "🔄 Compare Laptops"]
)

# ---------------- HOME ----------------
if page == "🏠 Home":
    st.markdown(
        """
        <h1 style="text-align:center;color:#1F618D;">
        Smart Laptop Recommendation System
        </h1>
        <p style="text-align:center;font-size:18px;">
        Live Amazon price • Compare laptops • Buy links
        </p>
        <hr>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    col1.info("🎓 Students")
    col2.success("💼 Professionals")
    col3.warning("🎮 Gamers")

# ---------------- RECOMMENDATION ----------------
elif page == "💻 Recommendation":
    st.header("💻 Laptop Recommendation")

    usage = st.selectbox("Select Usage", df["Usage"].unique())

    if st.button("🔍 Recommend"):
        results = df[df["Usage"] == usage]

        for _, row in results.iterrows():
            col1, col2 = st.columns([1, 2])

            with col1:
                st.image(row["Image"], width=180)

            with col2:
                st.subheader(row["Model"])
                st.write(f"💾 RAM: {row['RAM']}")
                st.write(f"📦 Storage: {row['Storage']}")

                live_price = get_amazon_price(row["ASIN"])
                st.write(f"💰 **Live Amazon Price:** {live_price}")

                st.markdown(
                    f"""
                    <a href="{row['Amazon']}" target="_blank">
                    <button style="background:#FF9900;color:white;padding:8px;border:none;border-radius:5px;">
                    Amazon
                    </button></a>
                    &nbsp;
                    <a href="{row['Flipkart']}" target="_blank">
                    <button style="background:#2874F0;color:white;padding:8px;border:none;border-radius:5px;">
                    Flipkart
                    </button></a>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown("---")

# ---------------- COMPARE ----------------
elif page == "🔄 Compare Laptops":
    st.header("🔄 Compare Laptops")

    l1 = st.selectbox("Laptop 1", df["Model"])
    l2 = st.selectbox("Laptop 2", df["Model"], index=1)

    if st.button("⚖ Compare"):
        a = df[df["Model"] == l1].iloc[0]
        b = df[df["Model"] == l2].iloc[0]

        col1, col2 = st.columns(2)

        for col, lap in zip([col1, col2], [a, b]):
            with col:
                st.image(lap["Image"], width=220)
                st.subheader(lap["Model"])
                st.write(f"💾 {lap['RAM']} | {lap['Storage']}")
                st.write(f"💰 Live Price: {get_amazon_price(lap['ASIN'])}")
