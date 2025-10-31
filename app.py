import streamlit as st
import joblib
import time

# -------------------------------------------------
# Page config & title
# -------------------------------------------------
st.set_page_config(page_title="Book Recommender System", layout="wide")
st.title("Book Recommender System")

# -------------------------------------------------
# Load model (cached once)
# -------------------------------------------------
@st.cache_resource
def load_model():
    model = joblib.load("model.pkl")
    return {
        "data": model["data"],
        "similarity": model["similarity"],
        "pivot_index": model["pivot_index"],
    }

with st.spinner("Loading model and book catalogue..."):
    model_data = load_model()
    data = model_data["data"]
    similarity = model_data["similarity"]
    pivot_index = model_data["pivot_index"]

st.success(f"Loaded **{len(pivot_index):,}** books successfully!")

# -------------------------------------------------
# Safe image URL
# -------------------------------------------------
def safe_image_url(book_name: str) -> str:
    try:
        url = data[data["book_name"] == book_name].iloc[0]["image_url"]
        return url if url and isinstance(url, str) and url.strip() else "https://via.placeholder.com/120x180?text=No+Image"
    except:
        return "https://via.placeholder.com/120x180?text=No+Image"

# -------------------------------------------------
# Recommend 7 books
# -------------------------------------------------
def recommend(book_name: str):
    if book_name not in pivot_index:
        st.error("Book not found in the similarity dataset!")
        return []

    book_idx = pivot_index.index(book_name)
    distances = similarity[book_idx]
    similar_items = sorted(
        enumerate(distances), key=lambda x: x[1], reverse=True
    )[1:8]  # Top 7 (skip itself)

    recs = []
    for idx, _ in similar_items:
        title = pivot_index[idx]
        img = safe_image_url(title)
        recs.append((title, img))
    return recs

# -------------------------------------------------
# UI: Book selector
# -------------------------------------------------
book_name = st.selectbox(
    "Select a book:",
    options=pivot_index,
    index=None,
    placeholder="Start typing or choose a book..."
)

# -------------------------------------------------
# Recommend button
# -------------------------------------------------
if st.button("Recommend"):
    if not book_name:
        st.warning("Please select a book first!")
    else:
        st.subheader("Recommended Books:")
        with st.spinner("Finding 7 similar books..."):
            time.sleep(0.6)  # Optional: makes spinner visible
            recommendations = recommend(book_name)

        if recommendations:
            # Force image height to 180px
            st.markdown(
                """
                <style>
                .book-img img {
                    height: 180px !important;
                    width: auto !important;
                    object-fit: contain;
                    border-radius: 8px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            # 7 columns
            cols = st.columns(7, gap="medium")
            for i, (title, img_url) in enumerate(recommendations):
                with cols[i]:
                    st.markdown(
                        f'<div class="book-img"><img src="{img_url}"></div>',
                        unsafe_allow_html=True,
                    )
                    st.caption(title, unsafe_allow_html=True)
        else:
            st.info("No recommendations found.")