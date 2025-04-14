import asyncio
import edge_tts

async def async_text_to_speech(text, voice_code, output_file, rate="+0%", pitch="+0Hz"):
    tts = edge_tts.Communicate(
        text=text,
        voice=voice_code,
        rate=rate,
        pitch=pitch
    )
    await tts.save(output_file)
    return output_file

def text_to_speech(text, voice_code, output_file, rate="+0%", pitch="+0Hz"):
    asyncio.run(async_text_to_speech(text, voice_code, output_file, rate, pitch))
    return output_file

def convert_text_to_speech(text, voice_code, output_file, rate_value=0, pitch_value=0):
    def to_percent_str(value):
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
    text_to_speech(text, voice_code, output_file, rate=rate_str, pitch=pitch_str)
    return output_file
