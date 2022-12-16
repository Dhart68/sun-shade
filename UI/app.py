import streamlit as st
import base64
from PIL import Image
import numpy as np
import pandas as pd

st.markdown("""# Sun and Shades for Solar Panels
## Check if it is interesting to implement a solar panel in a given place.
""")

col1, col2 = st.columns(2)

with col1:
    longitude = st.text_input('Longitude', '...  ')
with col2:
    latitude = st.text_input('Latitude', '... ')

col, = st.columns(1)

with col:
    """### Sun Exposition"""
    if longitude == "-73.98530154756561" and latitude == "40.76616942412636":

        image = Image.open('plot.png')
        st.image(image)
        file_ = open("images/png_to_gif.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
        unsafe_allow_html=True,)
        st.success('You can install a solar panel, it is profitable ! ')



    else :
        st.markdown('# Please input coordinates')
