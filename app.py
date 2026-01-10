import streamlit as st
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Laptop Recommendation", layout="wide")

# ---------------- LOAD DATA ----------------
users = pd.read_csv("users.csv")
df = pd.read_csv("laptops.csv")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- AUTH FUNCTIONS ----------------
def login(username, password):
    return not users[(users.username == username) & (users.password == password)].empty

def signup(username, password):
    global users
    if username in users.username.values:
        return False
    users.loc[len(users)] = [username, password]
    users.to_csv("users.csv", index=False)
    return True

# ---------------- LOGIN / SIGNUP ----------------
if not st.session_state.logged_in:
    st.title("🔐 Laptop Recommendation System")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            if login(u, p):
                st.session_state.logged_in = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        su = st.text_input("New Username")
        sp = st.text_input("New Password", type="password")
        if st.button("Create Account"):
            if signup(su, sp):
                st.success("Account created. Login now.")
            else:
                st.error("Username already exists")

# ---------------- MAIN WEBSITE ----------------
else:
    st.sidebar.success("Logged in")
    page = st.sidebar.radio("Menu", ["🏠 Home", "🔍 Search Laptop", "💻 Recommend", "🔄 Compare"])

    # ---------- HOME ----------
    if page == "🏠 Home":
        st.markdown("<h1 style='color:#0A58CA'>Laptop Recommendation System</h1>", unsafe_allow_html=True)
        st.write("Search, compare and find best laptops easily.")

    # ---------- SEARCH ----------
    elif page == "🔍 Search Laptop":
        st.header("🔍 Search Your Laptop")

        query = st.text_input("Enter laptop model name")

        if query:
            results = df[df["Model"].str.contains(query, case=False)]

            if results.empty:
                st.warning("No laptop found")
            else:
                for _, row in results.iterrows():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.image(row["Image"], width=160)
                    with col2:
                        st.subheader(row["Model"])
                        st.write(f"💰 ₹{row['Price']}")
                        st.write(f"💾 {row['RAM']} | {row['Storage']}")
                        st.markdown(
                            f"""
                            <a href="{row['Amazon']}" target="_blank">
                            <button style="background:#FF9900;color:white;padding:8px;border:none;border-radius:5px;">Amazon</button>
                            </a>
                            &nbsp;
                            <a href="{row['Flipkart']}" target="_blank">
                            <button style="background:#2874F0;color:white;padding:8px;border:none;border-radius:5px;">Flipkart</button>
                            </a>
                            """,
                            unsafe_allow_html=True
                        )
                        st.markdown("---")

    # ---------- RECOMMEND ----------
    elif page == "💻 Recommend":
        st.header("💻 Laptop Recommendations")
        usage = st.selectbox("Select usage", df["Usage"].unique())
        recs = df[df["Usage"] == usage]

        for _, row in recs.iterrows():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(row["Image"], width=160)
            with col2:
                st.subheader(row["Model"])
                st.write(f"💰 ₹{row['Price']}")
                st.write(f"💾 {row['RAM']} | {row['Storage']}")
                st.markdown(
                    f"""
                    <a href="{row['Amazon']}" target="_blank">
                    <button style="background:#FF9900;color:white;padding:8px;border:none;border-radius:5px;">Amazon</button>
                    </a>
                    &nbsp;
                    <a href="{row['Flipkart']}" target="_blank">
                    <button style="background:#2874F0;color:white;padding:8px;border:none;border-radius:5px;">Flipkart</button>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown("---")

    # ---------- COMPARE ----------
    elif page == "🔄 Compare":
        st.header("🔄 Compare Laptops")
        l1 = st.selectbox("Laptop 1", df["Model"])
        l2 = st.selectbox("Laptop 2", df["Model"], index=1)

        if st.button("Compare"):
            a = df[df["Model"] == l1].iloc[0]
            b = df[df["Model"] == l2].iloc[0]

            c1, c2 = st.columns(2)
            for col, lap in zip([c1, c2], [a, b]):
                with col:
                    st.image(lap["Image"], width=200)
                    st.subheader(lap["Model"])
                    st.write(f"₹{lap['Price']}")
                    st.write(lap["RAM"], lap["Storage"])
