import streamlit as st
import requests
from PIL import Image,ImageDraw,ImageFont
import io

st.title('顔認識アプリ')

subscription_key='13d5c6284db24f1389fd0f6d7476a159'
assert subscription_key
face_api_url='https://20210503-shinya-y.cognitiveservices.azure.com/face/v1.0/detect'

uploaded_file = st.file_uploader("Choose an image...", type='jpg')
if uploaded_file is not None:
    img = Image.open(uploaded_file)

    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue()

    headers = {
        'Content-type':'application/octet-stream',
        'Ocp-Apim-Subscription-Key':subscription_key}

    params = {
        'returnFaceId':'true',
        'returnFaceAttributes':'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion'
    }

    res = requests.post(face_api_url,params=params,headers=headers,data=binary_img)
    results = res.json()
    font = ImageFont.truetype("meiryo.ttc", 25)

    for result in results:
        rect = result['faceRectangle']
        attr = result['faceAttributes']
        ag = str(attr['age'])
        gd = attr['gender']
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'],rect['top']),(rect['left']+rect['width'],rect['top']+rect['height'])],fill=None,outline='green',width=5)
        draw.text((rect['left'],rect['top']-60),ag,font=font,fill=(255,255,0,0))
        draw.text((rect['left'],rect['top']-30),gd,font=font,fill=(255,255,0,0))

    st.image(img, caption='Uploaded Image.', use_column_width=True)
