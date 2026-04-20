import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Fishing Tuyên Quang", page_icon="🎣")

st.title("🎣 Dự Báo Thời Tiết Câu Cá - Tuyên Quang")
st.write("Cập nhật dữ liệu thời gian thực cho cần thủ chuyên nghiệp.")

# Nhập API Key của bạn tại đây
api_key = "469e873ece82bed4e2c8f188bd979816" 
# Nếu vẫn lỗi, hãy thử nhập "Tuyen Quang,VN"
city = "Tuyen Quang,VN"

def get_weather(city, api_key):
    # Sử dụng đúng endpoint và thêm tham số để lấy áp suất
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=vi"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return None

if api_key:
    data = get_weather(city, api_key)
    
    if data and data.get("cod") == 200:
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure'] # Áp suất khí quyển
        description = data['weather'][0]['description']
        wind_speed = data['wind']['speed']
        
        # Hiển thị thông số đẹp mắt
        st.subheader(f"📍 Địa điểm: {data['name']}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Nhiệt độ", f"{temp}°C")
        c2.metric("Độ ẩm", f"{humidity}%")
        c3.metric("Áp suất", f"{pressure} hPa")
        c4.metric("Gió", f"{wind_speed}m/s")
        
        st.success(f"Bầu trời: {description.capitalize()}")

        # Phân tích kỹ thuật cho dân chuyên
        st.divider()
        st.subheader("📋 Tư vấn kỹ thuật cho cần thủ")
        
        advice = []
        
        # Logic Cá Chép (Nhạy cảm với áp suất)
        if 1010 <= pressure <= 1020:
            chep_stt = "✅ Rất tốt"
            chep_note = "Áp suất ổn định, cá Chép đi tuần tra tìm mồi mạnh."
        else:
            chep_stt = "⚠️ Cẩn thận"
            chep_note = "Áp suất biến động, Chép có thể lửng, khó chạm đáy."

        # Logic Cá Rô Phi
        if temp >= 25:
            ro_stt = "🔥 Cực sung"
            ro_note = "Trời ấm, Rô phi phàm ăn, thích hợp mồi cám thơm."
        else:
            ro_stt = "🧊 Chậm"
            ro_note = "Nước lạnh Rô phi lười di chuyển."

        # Logic Cá Trôi
        if 22 <= temp <= 28 and humidity > 70:
            troi_stt = "✅ Thuận lợi"
            troi_note = "Thời tiết oi nóng trước mưa, Trôi thường đè mồi mạnh."
        else:
            troi_stt = "⏳ Bình thường"
            troi_note = "Cá Trôi ăn lai rai, cần xả ổ bền bỉ."

        df = pd.DataFrame([
            {"Loại cá": "Cá Chép", "Trạng thái": chep_stt, "Lời khuyên": chep_note},
            {"Loại cá": "Cá Rô Phi", "Trạng thái": ro_stt, "Lời khuyên": ro_note},
            {"Loại cá": "Cá Trôi", "Trạng thái": troi_stt, "Lời khuyên": troi_note}
        ])
        
        st.table(df)
        
    elif data and data.get("cod") == 401:
        st.error("Lỗi: API Key chưa được kích hoạt. Bạn vui lòng đợi khoảng 30-60 phút để OpenWeather xác nhận mã này.")
    else:
        st.warning("Đang kết nối dữ liệu... Nếu đợi quá lâu, hãy kiểm tra lại kết nối internet hoặc thử lại sau ít phút.")
