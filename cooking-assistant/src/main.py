from groq import Groq
import base64
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client with API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_ingredient(image_bytes):
    """Gửi ảnh đến mô hình Vision để nhận diện nguyên liệu"""
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    response = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",  # Use the correct model name
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "Hãy nhận diện nguyên liệu trong ảnh này và trả về tên nguyên liệu bằng tiếng Việt, ngăn cách bởi dấu phẩy."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }],
        stream=False,
        temperature=1,
        max_tokens=1024,
        top_p=1,
    )

    return response.choices[0].message.content

def suggest_recipe(ingredients):
    """Dựa vào nguyên liệu đã nhận diện, đề xuất một công thức nấu ăn bằng tiếng Việt"""
    response = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",  # Use the correct model name
        messages=[{
            "role": "user",
            "content": f"Đề xuất một công thức nấu ăn sử dụng các nguyên liệu sau: {ingredients}. Hãy trả lời bằng tiếng Việt."
        }]
    )
    return response.choices[0].message.content

# Giao diện Streamlit
st.title("🍳 AI- Cooking Assistant")

uploaded_files = st.file_uploader("📸 Tải lên ảnh món ăn", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

if uploaded_files:
    ingredients_list = []

    for uploaded_file in uploaded_files:
        image_bytes = uploaded_file.read()
        ingredients = analyze_ingredient(image_bytes)
        ingredients_list.append(ingredients)
        st.write(f"✅ {uploaded_file.name}: {ingredients}")

    if ingredients_list:
        all_ingredients = ", ".join(ingredients_list)
        st.subheader("📋 Tất cả nguyên liệu gợi ý:")
        st.write(all_ingredients)

        recipe = suggest_recipe(all_ingredients)
        st.subheader("👨‍🍳 Công thức nấu ăn gợi ý:")
        st.write(recipe)
