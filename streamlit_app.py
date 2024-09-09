import streamlit as st
import numpy as np
from PIL import Image
import base64
import io

# 이미지 업로드
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # 이미지를 PIL로 열기
    img = Image.open(uploaded_file)
    img_array = np.array(img)

    # 이미지를 base64로 인코딩
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    # HTML과 JavaScript로 캔버스 생성 및 색상 추출 구현
    html_code = f"""
    <canvas id="canvas" width="{img.width}" height="{img.height}"></canvas>
    <script>
        var canvas = document.getElementById('canvas');
        var ctx = canvas.getContext('2d');
        var img = new Image();
        img.src = 'data:image/png;base64,{img_base64}';
        img.onload = function() {{
            ctx.drawImage(img, 0, 0);
        }};
        
        canvas.addEventListener('click', function(event) {{
            var rect = canvas.getBoundingClientRect();
            var x = event.clientX - rect.left;
            var y = event.clientY - rect.top;
            var pixel = ctx.getImageData(x, y, 1, 1).data;
            var rgb = 'rgb(' + pixel[0] + ',' + pixel[1] + ',' + pixel[2] + ')';
            document.getElementById('colorDisplay').textContent = '선택한 색상: ' + rgb;
            document.getElementById('colorBlock').style.backgroundColor = rgb;
        }});
    </script>
    <p id="colorDisplay">선택한 색상: </p>
    <div id="colorBlock" style="width: 100px; height: 100px; background-color: #FFFFFF;"></div>
    """

    # Streamlit에서 HTML 코드 실행
    st.components.v1.html(html_code, height=img.height + 150)
