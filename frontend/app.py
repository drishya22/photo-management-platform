import streamlit as st
import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Photo Management Platform",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================
# STYLING
# ======================

st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Header */
    .app-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.25rem;
    }
    .app-subtitle {
        color: #8a8f98;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    /* Metric cards in sidebar */
    div[data-testid="stMetric"] {
        background: rgba(120, 120, 140, 0.08);
        border: 1px solid rgba(120, 120, 140, 0.15);
        border-radius: 10px;
        padding: 12px 14px;
    }

    /* Category pill badges */
    .cat-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        background: rgba(99, 102, 241, 0.15);
        color: #818cf8;
        margin-bottom: 6px;
    }

    /* Image cards */
    .img-card {
        border: 1px solid rgba(120, 120, 140, 0.18);
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 14px;
        background: rgba(120, 120, 140, 0.04);
        transition: border-color 0.15s ease;
    }
    .img-card:hover {
        border-color: rgba(99, 102, 241, 0.5);
    }
    .img-filename {
        font-size: 0.82rem;
        font-weight: 600;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-top: 4px;
    }
    .img-meta {
        font-size: 0.75rem;
        color: #8a8f98;
    }

    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        color: #8a8f98;
    }
    .empty-state-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    /* Person group header */
    .person-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 1.2rem;
        margin-bottom: 0.6rem;
    }
    .person-count {
        background: rgba(99, 102, 241, 0.15);
        color: #818cf8;
        padding: 2px 9px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ======================
# HELPERS
# ======================

def api_get(path, params=None, timeout=10):
    """GET with a consistent error contract: returns (data, error_str)."""
    try:
        r = requests.get(f"{BASE_URL}{path}", params=params, timeout=timeout)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Backend not reachable. Is the FastAPI server running on :8000?"
    except requests.exceptions.Timeout:
        return None, "Request timed out."
    except requests.exceptions.HTTPError as e:
        return None, f"Server error: {e}"
    except Exception as e:
        return None, f"Unexpected error: {e}"


def load_images(force=False):
    if force or "images_data" not in st.session_state:
        data, err = api_get("/images")
        st.session_state["images_data"] = data
        st.session_state["images_err"] = err
    return st.session_state["images_data"], st.session_state["images_err"]


def load_faces(force=False):
    if force or "faces_data" not in st.session_state:
        data, err = api_get("/faces")
        st.session_state["faces_data"] = data
        st.session_state["faces_err"] = err
    return st.session_state["faces_data"], st.session_state["faces_err"]


def empty_state(icon, title, subtitle=""):
    st.markdown(f"""
    <div class="empty-state">
        <div class="empty-state-icon">{icon}</div>
        <div style="font-weight:600; font-size:1.05rem;">{title}</div>
        <div>{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


CATEGORY_ICONS = {
    "document": "📄", "documents": "📄",
    "prescription": "💊", "prescriptions": "💊",
    "receipt": "🧾", "receipts": "🧾",
    "people": "🧑‍🤝‍🧑", "person": "🧑",
    "travel": "✈️",
    "pet": "🐾", "pets": "🐾",
    "other": "🗂️", "unknown": "❔",
}


def cat_icon(category):
    return CATEGORY_ICONS.get((category or "unknown").lower(), "🗂️")


# ======================
# SIDEBAR
# ======================

with st.sidebar:
    st.markdown("### 📊 Platform Stats")

    if st.button("🔄 Refresh stats", use_container_width=True):
        load_images(force=True)

    data, err = load_images()

    if err:
        st.error(err)
    elif data:
        st.metric("Total Images", data.get("total_images", 0))

        categories = {}
        for image in data.get("images", []):
            c = image.get("category", "unknown")
            categories[c] = categories.get(c, 0) + 1

        if categories:
            st.markdown("**Categories**")
            for category, count in sorted(categories.items(), key=lambda x: -x[1]):
                st.markdown(
                    f"{cat_icon(category)} {category.title()} &nbsp; "
                    f"<span class='person-count'>{count}</span>",
                    unsafe_allow_html=True
                )
        else:
            st.caption("No images yet.")

    st.divider()
    st.caption(f"Backend: `{BASE_URL}`")
    st.caption(datetime.now().strftime("Last loaded %H:%M:%S"))


# ======================
# HEADER
# ======================

st.markdown('<div class="app-header"><h1>📸 AI Photo Management Platform</h1></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Duplicate detection · Auto-categorization · Face grouping · Natural-language search</div>',
    unsafe_allow_html=True
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "⬆️ Upload",
        "🔍 Search",
        "🖼️ Gallery",
        "🧑‍🤝‍🧑 Faces",
        "☁️ Google Photos"
    ]
)

# ======================
# UPLOAD
# ======================

with tab1:
    st.subheader("Upload a photo")

    col_upload, col_preview = st.columns([1, 1])

    with col_upload:
        uploaded_file = st.file_uploader(
            "Drag and drop or browse",
            type=["jpg", "jpeg", "png"],
            help="JPG or PNG. Duplicate and near-duplicate images are flagged automatically."
        )
        upload_clicked = st.button("Upload Image", type="primary", disabled=uploaded_file is None)

    with col_preview:
        if uploaded_file:
            st.image(uploaded_file, caption="Preview", width=300)

    if upload_clicked and uploaded_file is not None:
        with st.spinner("Processing image — hashing, classifying, checking faces..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                response = requests.post(f"{BASE_URL}/upload", files=files, timeout=30)
                response.raise_for_status()
                result = response.json()
            except requests.exceptions.ConnectionError:
                st.error("Backend not reachable. Is the FastAPI server running on :8000?")
                result = None
            except Exception as e:
                st.error(f"Upload failed: {e}")
                result = None

        if result:
            if result.get("is_duplicate"):
                st.warning("⚠️ Exact duplicate detected — this image already exists in the library.")
                with st.expander("Details"):
                    st.json(result)
            elif result.get("is_near_duplicate"):
                st.warning("⚠️ Near-duplicate detected — a visually similar image already exists.")
                with st.expander("Details"):
                    st.json(result)
            else:
                st.success("✅ Image uploaded and processed successfully")
                st.balloons()
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"**Filename**\n\n{result.get('filename', '—')}")
                c2.markdown(f"**Category**\n\n{cat_icon(result.get('category'))} {result.get('category', '—')}")
                person_id = result.get("person_id")
                c3.markdown(f"**Person ID**\n\n{person_id if person_id else 'No face detected'}")
                st.caption(f"Hash: `{result.get('hash', '')[:24]}...`")

                # invalidate caches so gallery/faces reflect the new upload
                st.session_state.pop("images_data", None)
                st.session_state.pop("faces_data", None)

# ======================
# SEARCH
# ======================

with tab2:
    st.subheader("Semantic image search")

    col_q, col_btn = st.columns([4, 1])
    with col_q:
        query = st.text_input(
            "Describe what you're looking for",
            placeholder="e.g. \"receipt from a grocery store\" or \"photo of a dog at the beach\"",
            label_visibility="collapsed"
        )
    with col_btn:
        search_clicked = st.button("Search", type="primary", use_container_width=True)

    if search_clicked:
        if not query.strip():
            st.info("Enter a description to search.")
        else:
            with st.spinner("Searching..."):
                results, err = api_get("/search", params={"query": query})

            if err:
                st.error(err)
            else:
                items = results.get("results", [])
                if not items:
                    empty_state("🔍", "No matches found", "Try a broader or different description.")
                else:
                    st.success(f"Found {len(items)} result{'s' if len(items) != 1 else ''}")
                    cols = st.columns(3)
                    for idx, image in enumerate(items):
                        with cols[idx % 3]:
                            st.markdown('<div class="img-card">', unsafe_allow_html=True)
                            st.image(f"{BASE_URL}{image['image_url']}", use_container_width=True)
                            st.markdown(f'<div class="img-filename">{image["filename"]}</div>', unsafe_allow_html=True)
                            dist = image.get("distance")
                            if dist is not None:
                                similarity = max(0, round((2 - dist) * 50, 1))

                                st.markdown(
                                    f'<div class="img-meta">Match Score: {similarity}%</div>',
                                    unsafe_allow_html=True
                                )
                            st.markdown('</div>', unsafe_allow_html=True)

# ======================
# GALLERY
# ======================

with tab3:
    top = st.columns([3, 1])
    with top[0]:
        st.subheader("Photo gallery")
    with top[1]:
        if st.button("🔄 Reload gallery", use_container_width=True):
            load_images(force=True)

    data, err = load_images()

    if err:
        st.error(err)
    elif not data or not data.get("images"):
        empty_state("🖼️", "No images yet", "Upload some photos to see them here.")
    else:
        images = data["images"]
        all_cats = sorted({img.get("category", "unknown") for img in images})
        selected_cats = st.multiselect("Filter by category", options=all_cats, default=[])

        filtered = [img for img in images if not selected_cats or img.get("category") in selected_cats]

        st.caption(f"Showing {len(filtered)} of {len(images)} images")

        cols = st.columns(3)
        for idx, image in enumerate(filtered):
            with cols[idx % 3]:
                st.markdown('<div class="img-card">', unsafe_allow_html=True)
                st.image(f"{BASE_URL}{image['image_url']}", use_container_width=True)
                st.markdown(f'<div class="img-filename">{image["filename"]}</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<span class="cat-badge">{cat_icon(image.get("category"))} '
                    f'{image.get("category", "unknown").title()}</span>',
                    unsafe_allow_html=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

# ======================
# FACES
# ======================

with tab4:
    top = st.columns([3, 1])
    with top[0]:
        st.subheader("Face groups")
    with top[1]:
        if st.button("🔄 Reload faces", use_container_width=True):
            load_faces(force=True)

    faces, err = load_faces()

    if err:
        st.error(err)
    elif not faces:
        empty_state("🧑‍🤝‍🧑", "No face groups found", "Face groups appear here once people are detected in uploaded photos.")
    else:
        for person_id, pdata in faces.items():
            imgs = list(set(pdata.get("images", [])))
            st.markdown(
                f'<div class="person-header">'
                f'<span style="font-size:1.1rem; font-weight:700;">👤 {person_id}</span>'
                f'<span class="person-count">{len(imgs)} photo{"s" if len(imgs) != 1 else ""}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

            cols = st.columns(4)
            for idx, image_name in enumerate(imgs):
                with cols[idx % 4]:
                    st.image(f"{BASE_URL}/images/{image_name}", use_container_width=True)
                    st.caption(image_name)



st.divider()

st.caption(
    "AI Photo Management Platform • Semantic Search • Face Grouping • Duplicate Detection • FastAPI + Streamlit"
)

# ======================
# GOOGLE PHOTOS
# ======================

with tab5:

    st.subheader("Google Photos Integration")

    st.write(
        "Connect your Google Photos account "
        "to import photos into the platform."
    )

    if st.button("Check Connection Status"):

        response = requests.get(
            f"{BASE_URL}/google-photos/status"
        )

        st.json(response.json())

    st.markdown(
        f"""
        <a href="{BASE_URL}/google-photos/connect"
           target="_blank">
            <button style="
                padding:10px;
                font-size:16px;
                cursor:pointer;">
                Connect Google Photos
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    session_id = st.text_input(
        "Google Photos Session ID"
    )

    if st.button("Load Selected Photos"):

        response = requests.get(
            f"{BASE_URL}/google-photos/media-items/{session_id}"
        )

        data = response.json()

        media_items = data.get("mediaItems", [])

        if len(media_items) == 0:
            st.warning("No photos found")
        else:

            st.success(
                f"Found {len(media_items)} selected photos"
            )

            for item in media_items:

                file_info = item["mediaFile"]

                st.image(
                    file_info["baseUrl"],
                    width=250
                )

                st.write(
                    f"📸 {file_info['filename']}"
                )

                st.caption(
                    f"{file_info['mimeType']}"
                )

                st.divider()