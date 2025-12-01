import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie
import base64
import os

# ==============================================================================
# 1. CẤU HÌNH HỆ THỐNG & TÀI NGUYÊN
# ==============================================================================
st.set_page_config(
    page_title="Sinh nhật vui vẻ",
    page_icon="🎁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Đường dẫn file cục bộ & online ---
LOTTIE_CAKE_URL = "https://lottie.host/58085714-3644-4669-843e-4e40c106831a/5q7q19497X.json"
IMG_MIFFY_LOCAL = "miffy.png"
IMG_MIFFY_ONLINE = "https://i.pinimg.com/originals/c8/53/39/c853392df283d069dc898d99c4383182.png"
AUDIO_FILE_LOCAL = "happy_birthday.mp3"
AUDIO_URL_ONLINE = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

# ==============================================================================
# 2. CÁC HÀM HỖ TRỢ NÂNG CAO (BACKEND)
# ==============================================================================

@st.cache_data(ttl=3600)
def load_lottie_safe(url):
    """Tải hoạt hình Lottie an toàn"""
    try:
        return requests.get(url, timeout=3).json()
    except:
        return None

def get_base64_of_bin_file(bin_file):
    """Chuyển file (ảnh/nhạc) sang dạng base64 để nhúng trực tiếp vào HTML"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def render_html_image(local_path, online_url, width_px):
    """
    Hàm render ảnh bằng HTML thuần để đảm bảo căn giữa 100%.
    Tự động chọn file local nếu có, ngược lại dùng link online.
    """
    img_src = online_url
    if os.path.isfile(local_path):
        try:
            b64_data = get_base64_of_bin_file(local_path)
            # Xác định loại ảnh (png/jpg)
            ext = local_path.split('.')[-1]
            img_src = f"data:image/{ext};base64,{b64_data}"
        except:
            pass # Nếu lỗi đọc file local thì dùng online
            
    html_code = f"""
        <div style="display: flex; justify-content: center; align-items: center; margin: 20px 0;">
            <img src="{img_src}" width="{width_px}" style="border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

def play_audio_hidden(local_path, online_url):
    """Phát nhạc ẩn, không lặp lại"""
    audio_src = online_url
    if os.path.isfile(local_path):
        try:
            b64_data = get_base64_of_bin_file(local_path)
            audio_src = f"data:audio/mp3;base64,{b64_data}"
        except:
            pass

    # Thuộc tính 'autoplay' và không có 'loop'
    html_code = f"""
        <audio autoplay style="display:none;">
            <source src="{audio_src}" type="audio/mp3">
        </audio>
    """
    st.markdown(html_code, unsafe_allow_html=True)

# ==============================================================================
# 3. THIẾT KẾ GIAO DIỆN CAO CẤP (CSS GLASSMORPHISM)
# ==============================================================================
def inject_pro_css():
    st.markdown(
        """
        <style>
        /* Reset và ẩn các thành phần thừa của Streamlit */
        #MainMenu, footer, header {visibility: hidden;}
        
        /* Nền Gradient đa sắc sang trọng */
        .stApp {
            background: linear-gradient(120deg, #fccb90 0%, #d57eeb 100%);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
        }
        @keyframes gradientBG {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        /* --- GLASS CARD CONTAINER (Tấm kính mờ) --- */
        .glass-container {
            background: rgba(255, 255, 255, 0.25);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 40px;
            text-align: center; /* Căn giữa nội dung text bên trong */
        }

        /* --- TYPOGRAPHY --- */
        .main-title {
            font-family: 'Montserrat', sans-serif;
            font-weight: 800;
            font-size: 55px;
            color: #fff;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.2);
            margin-bottom: 10px;
        }
        .sub-title {
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 20px;
            color: rgba(255,255,255,0.9);
            margin-bottom: 30px;
            font-weight: 300;
        }
        .wish-text {
            font-size: 26px;
            color: #fff;
            font-weight: bold;
            text-shadow: 1px 1px 5px rgba(0,0,0,0.2);
            line-height: 1.5;
        }
        .signature {
             font-size: 16px; color: rgba(255,255,255,0.8); margin-top: 10px;
        }

        /* --- INPUT FIELD & BUTTON STYLING --- */
        /* Tùy chỉnh ô nhập liệu để hòa hợp với nền kính */
        .stTextInput > div > div > input {
            text-align: center; font-size: 22px; padding: 12px;
            border-radius: 25px; border: 2px solid rgba(255,255,255,0.5);
            background-color: rgba(255, 255, 255, 0.6) !important;
            color: #d63384; font-weight: bold;
        }
        /* Tùy chỉnh nút bấm */
        div.stButton > button {
            background: linear-gradient(90deg, #ff8a00, #e52e71);
            color: white; font-size: 20px; font-weight: bold;
            padding: 12px 40px; border-radius: 50px; border: none;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        }
        /* Căn giữa nút bấm */
        div.stButton { display: flex; justify-content: center; }
        </style>
        """,
        unsafe_allow_html=True
    )

# ==============================================================================
# 4. MAIN APP LOGIC
# ==============================================================================
def main():
    inject_pro_css()
    
    # Quản lý trạng thái (Session State)
    if 'stage' not in st.session_state:
        st.session_state.stage = 0 # 0: Màn hình nhập tên, 1: Màn hình chúc mừng

    # Bố cục 3 cột: Nội dung chính nằm ở cột giữa (col2)
    col1, col2, col3 = st.columns([1, 2.5, 1]) # Cột giữa rộng hơn chút

    with col2:
        # Bắt đầu container kính mờ
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)

        # --- PHẦN TIÊU ĐỀ CHUNG ---
        st.markdown('<div class="main-title">HAPPY BIRTHDAY</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-title">MÓN QUÀ ĐẶC BIỆT SIÊU BÍ ẨN </div>', unsafe_allow_html=True)

        # --- GIAI ĐOẠN 1: NHẬP TÊN ---
        if st.session_state.stage == 0:
            st.write("")
            # Ô nhập tên (Đã được CSS căn giữa text bên trong)
            name_input = st.text_input("", placeholder="Nhập tên nhân vật chính...", )
            st.write("")
            st.write("")
            
            # Nút mở quà (Đã được CSS căn giữa)
            if st.button("✨ KHUI QUÀ NGAY ✨"):
                if name_input:
                    st.session_state.name = name_input
                    st.session_state.stage = 1
                    st.rerun()
                else:
                    st.warning("Bạn chưa nhập tên kìa!")

        # --- GIAI ĐOẠN 2: HIỂN THỊ LỜI CHÚC ---
        else:
            # 1. Phát nhạc ẩn
            play_audio_hidden(AUDIO_FILE_LOCAL, AUDIO_URL_ONLINE)
            st.balloons()

            # 2. Hiển thị Bánh kem (Hoạt hình Lottie tự căn giữa tốt)
            lottie_json = load_lottie_safe(LOTTIE_CAKE_URL)
            if lottie_json:
                st_lottie(lottie_json, height=320, key="cake_anim", loop=True, speed=1)
            else:
                # Ảnh tĩnh dự phòng (Dùng HTML wrapper để căn giữa)
                render_html_image("", "https://images.unsplash.com/photo-1578985545062-69928b1d9587", 300)

            st.write("")

            # 3. Hiển thị Miffy (Dùng HTML Wrapper -> CHẮC CHẮN GIỮA)
            render_html_image(IMG_MIFFY_LOCAL, IMG_MIFFY_ONLINE, 180)
            
            # 4. Lời chúc
            st.write("")
            st.markdown(
                f"""
                <div class="wish-text">
                    Chúc Mừng Sinh Nhật {st.session_state.name}! ❤️<br>
                    Tuổi mới rực rỡ, xinh đẹp và hạnh phúc nhé!
                </div>
                <div class="signature">(From: Miffy & Me)</div>
                """,
                unsafe_allow_html=True
            )

            st.write("")
            st.write("")
            # Nút chơi lại
            if st.button("🔄 Xem lại lần nữa"):
                st.session_state.stage = 0
                st.rerun()

        # Kết thúc container kính mờ
        st.markdown('</div>', unsafe_allow_html=True) 

if __name__ == "__main__":

    main()
