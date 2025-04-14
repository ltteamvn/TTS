import edge_tts
import asyncio

async def text_to_speech(text, voice_code, output_file, rate="+0%", pitch="+0Hz"):
    # Tạo đối tượng Communicate với các tham số rate và pitch đã được định dạng
    tts = edge_tts.Communicate(
        text=text,
        voice=voice_code,
        rate=rate,    # Ví dụ: "+100%", "+50%", "+0%", "-50%", "-100%"
        pitch=pitch   # Ví dụ: "+100Hz", "+50Hz", "+0Hz", "-50Hz", "-100Hz"
    )
    await tts.save(output_file)
    return output_file

def convert_text_to_speech(text, voice_code, output_file, rate_value=0, pitch_value=0):
    """
    Chuyển đổi văn bản thành file giọng nói.
    
    Tham số:
    - text: văn bản cần chuyển đổi.
    - voice_code: mã giọng (ví dụ: 'vi-VN-NamMinhNeural').
    - output_file: đường dẫn file mp3 để lưu kết quả.
    - rate_value, pitch_value: giá trị số (trong khoảng -100 đến 100) tương ứng với tốc độ và cao độ.
    
    Ví dụ:
    - rate_value = 100 → "+100%"
    - rate_value = 50  → "+50%"
    - rate_value = 0   → "+0%"
    - rate_value = -50 → "-50%"
    - rate_value = -100→ "-100%"
    
    Tương tự cho pitch_value với đơn vị "Hz".
    """
    def to_percent_str(value):
        # Nếu value bằng 0, luôn trả về "+0%" để khớp định dạng của edge_tts.
        if value == 0:
            return "+0%"
        elif value > 0:
            return f"+{value}%"
        else:
            return f"{value}%"
    
    def to_hz_str(value):
        if value == 0:
            return "+0Hz"
        elif value > 0:
            return f"+{value}Hz"
        else:
            return f"{value}Hz"
    
    rate_str = to_percent_str(rate_value)
    pitch_str = to_hz_str(pitch_value)
    
    # Gọi hàm bất đồng bộ chuyển đổi văn bản thành giọng nói
    asyncio.run(text_to_speech(text, voice_code, output_file, rate=rate_str, pitch=pitch_str))
    return output_file
