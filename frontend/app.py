# import streamlit as st 
# import requests 


# BASE_URL="http://localhost:8000"

# st.set_page_config(page_title="Library Management System",page_icon="📚")

# st.title("Library Management System")

# st.sidebar.header("ADD NEW BOOK")
# with st.sidebar.form("BOOK_FORM"):
#     title=st.text_input("Title")
#     author=st.text_input("Author")
#     isbn=st.text_input("ISBN")
#     submitted=st.form_submit_button("Add Book")
    
#     if submitted:
#         book_data={
#             "title":title,
#             "author":author,
#             "isbn":isbn,
#             "is_available":True
#         }

#         response=requests.post(f"{BASE_URL}/books/",json=book_data)

#         if response.status_code==200:
#             st.success("Book added successfully!")
#         else:
#             st.error("Failed to add book.")


# st.subheader("BOOKS IN LIBRARY")

# try:
#     response=requests.get(f"{BASE_URL}/books/")
#     response.raise_for_status()
#     books=response.json()
#     for book in books:
#         st.table(books)
# except requests.RequestException as e:
#     st.error(f"Error fetching books: {e}")






import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://localhost:8000"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style="text-align:center; color:white;">📚 Library Management System</h1>
    <p style="text-align:center; color:white">
        Manage your library books easily
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("➕ Add New Book")

with st.sidebar.form("book_form", clear_on_submit=True):
    title = st.text_input("📖 Book Title")
    author = st.text_input("✍️ Author Name")
    isbn = st.text_input("🔢 ISBN Number")

    submitted = st.form_submit_button("Add Book")

    if submitted:
        if not title or not author or not isbn:
            st.sidebar.warning("⚠️ Please fill all fields")
        else:
            book_data = {
                "title": title,
                "author": author,
                "isbn": isbn,
                "is_available": True
            }

            try:
                response = requests.post(f"{BASE_URL}/books/", json=book_data)
                if response.status_code == 200:
                    st.sidebar.success("✅ Book added successfully!")
                else:
                    st.sidebar.error("❌ Failed to add book")
            except requests.RequestException:
                st.sidebar.error("🚨 Backend not running")

# ---------------- MAIN SECTION ----------------
st.subheader("📚 Books in Library")

col1, col2 = st.columns([2, 1])

with col1:
    search = st.text_input("🔍 Search by Title or Author")

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    refresh = st.button("🔄 Refresh List")

# ---------------- FETCH BOOKS ----------------
try:
    response = requests.get(f"{BASE_URL}/books/")
    response.raise_for_status()
    books = response.json()

    if not books:
        st.info("No books available in the library.")
    else:
        df = pd.DataFrame(books)

        # Search filter
        if search:
            df = df[
                df["title"].str.contains(search, case=False, na=False)
                | df["author"].str.contains(search, case=False, na=False)
            ]

        # Rename columns
        df = df.rename(columns={
            "id": "ID",
            "title": "Title",
            "author": "Author",
            "isbn": "ISBN",
            "is_available": "Available"
        })

        # Availability labels
        df["Available"] = df["Available"].apply(
            lambda x: "Available" if x else "Issued"
        )

        # ---------------- TABLE VIEW ----------------
        st.markdown("### 📋 Table View")
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        # ---------------- CARD VIEW ----------------
        st.markdown("### 📘 Book Card View")

        for _, book in df.iterrows():
            st.markdown(
                f"""
                <div style="
                    background-color:#f5f5f5;
                    border:1px solid #cfcfcf;
                    border-radius:12px;
                    padding:16px;
                    margin-bottom:12px;
                    color:#000;
                ">
                    <h4 style="margin-bottom:8px; color:#000;">
                        📖 {book['Title']}
                    </h4>
                    <p style="margin:2px 0; color:#000;">
                        <b>Author:</b> {book['Author']}
                    </p>
                    <p style="margin:2px 0; color:#000;">
                        <b>ISBN:</b> {book['ISBN']}
                    </p>
                    <p style="margin:2px 0; color:#000;">
                        <b>Status:</b> {book['Available']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

except requests.RequestException as e:
    st.error(f"🚨 Error fetching books: {e}")

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <p style="text-align:center; color:#444;">
        Built with ❤️ using Streamlit & FastAPI
    </p>
    """,
    unsafe_allow_html=True
)
