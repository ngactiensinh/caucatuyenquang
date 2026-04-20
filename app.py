import streamlit as st
import requests
import pandas as pd

# Cấu hình trang
st.set_page_config(page_title="Tuyên Quang Fishing Weather", page_icon="🎣")

st.title("🎣 Dự Báo Thời Tiết Câu Cá - Tuyên Quang")
st.write("Dành riêng cho cần thủ săn Chép, Rô phi, Trôi.")

# Nhập API Key (Bạn có thể dán trực tiếp hoặc dùng Secret của Streamlit)
api_key = "YOUR_API_KEY_HERE" 
city = "Tuyen Quang"

def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=vi"
    response = requests.get(url)
    return response.json()

if api_key != "YOUR_API_KEY_HERE":
    data = get_weather(city, api_key)
    
    if data.get("cod") == 200:
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        wind_speed = data['wind']['speed']
        
        # Hiển thị thông số cơ bản
        col1, col2, col3 = st.columns(3)
        col1.metric("Nhiệt độ", f"{temp}°C")
        col2.metric("Độ ẩm", f"{humidity}%")
        col3.metric("Gió", f"{wind_speed} m/s")
        
        st.info(f"Trạng thái: {description.capitalize()}")

        # Logic đánh giá cho từng loại cá
        st.subheader("📊 Đánh giá khả năng lên cá")
        
        results = []
        
        # Cá Chép
        if 15 <= temp <= 25:
            results.append({"Loại cá": "Cá Chép", "Đánh giá": "Tuyệt vời", "Lưu ý": "Thời tiết mát mẻ, chép đi ăn mạnh."})
        else:
            results.append({"Loại cá": "Cá Chép", "Đánh giá": "Trung bình", "Lưu ý": "Tránh lúc nắng gắt hoặc quá lạnh."})
            
        # Cá Rô Phi
        if temp > 25 and humidity > 60:
            results.append({"Loại cá": "Cá Rô Phi", "Đánh giá": "Rất tốt", "Lưu ý": "Rô phi thích nắng ấm và độ ẩm cao."})
        elif temp < 18:
            results.append({"Loại cá": "Cá Rô Phi", "Đánh giá": "Kém", "Lưu ý": "Cá lười ăn do nước lạnh."})
        else:
            results.append({"Loại cá": "Cá Rô Phi", "Đánh giá": "Ổn", "Lưu ý": "Câu ở tầng nước nông."})

        # Cá Trôi
        if 22 <= temp <= 30:
            results.append({"Loại cá": "Cá Trôi", "Đánh giá": "Tốt", "Lưu ý": "Cá trôi ưa ấm, thích hợp câu lục hoặc đài."})
        else:
            results.append({"Loại cá": "Cá Trôi", "Đánh giá": "Trung bình", "Lưu ý": "Cá nhát mồi khi nhiệt độ biến động."})

        df = pd.DataFrame(results)
        st.table(df)
        
    else:
        st.error("Không tìm thấy dữ liệu thời tiết. Vui lòng kiểm tra lại API Key.")
else:
    st.warning("Vui lòng nhập OpenWeatherMap API Key để bắt đầu!")
