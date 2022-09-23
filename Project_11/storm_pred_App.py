import streamlit as st
import datetime
from datetime import date
from datetime import timedelta
import plotly.figure_factory as ff
import numpy as np
import tensorflow as tf
import pandas as pd
from PIL import Image
import requests
from matplotlib import pyplot as plt

# liberaries for tensorflow and for calling models
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image
from keras.models import load_model

import warnings
warnings.filterwarnings("ignore")

#try:
#######################################################################
# Getting all function for image resisizing
def image_resizing(image_path):
    """
    This function resizes an input image to 224 X 224
    """
    img = image.load_img(image_path, target_size=(224,224))
    return img

 
def image_preprocessing(resized_image):
    """
    This function preprocesses the input image for MobileNetV2
    """
    pic_array = image.img_to_array(resized_image)
    image_batch = np.expand_dims(pic_array, axis=0)
    processed_image = preprocess_input(image_batch)
    return processed_image

def image_classification(preprocessed_image, model):
    probs = model.predict(preprocessed_image)[0].tolist()
    zipped = sorted(list(zip(classes, probs)), key=lambda x: x[1], reverse=True)
    image_class = [zipped[i][0] for i in range(len(zipped))]
    probability  = [zipped[i][1]*100 for i in range(len(zipped))]
    df = pd.DataFrame(data={'image_class':image_class, 'probability(%)': probability})
    return df

################################################################

# "MobileNetV2_solar_pred82.h5" === developed model name

# preprocess an image

resized_image = image_resizing('./im/sample_image1.jpg')
preprocessed_img = image_preprocessing(resized_image)


# these are the flare classes 
classes=['B_class', 'C_class']


model_name = load_model("my_model6.h5")
run_prediction = False

c_class= ""
b_class= ""
#m_class= ""

###############################################################







st.set_page_config(layout="wide")

#st.sidebar.markdown("# Find the Image")

st.subheader("Geomagnetic Storm Forecast")
st.subheader('24 - 48 hrs Earth Geo-Storm Awareness Plartform [EGAP]')

# set a dummy variable to hold or reset the prediction



# first row of columns with Date, Time and Date-Picker+Button

part1,part2,part3 = st.columns([1,1,2])

with part1: 
    date = date.today()

    st.error(f''' Today' Date
    ### {date}
    ''')
    
with part2: 
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")

    st.error(f''' Today's Time
    ### {time}
    ''')
    
with part3: 
    
    date_select = st.date_input('Pick a date!', max_value=date.today()) 
    if st.button('Predict Storm!'): 
        run_prediction = True

if run_prediction ==True:
    # Prediction output (in DataFrame) using the model
    tf.autograph.experimental.do_not_convert
    df=image_classification(preprocessed_img, model_name)
    df=df.sort_values(by= "image_class").reset_index(drop=True)


    
    b_class = df.iloc[0,1].round(decimals=3)
    c_class = df.iloc[1,1].round(decimals=3)
    #m_class = df.iloc[2,1].round(decimals=3)
    
               
        
        
# The second row of columns: 2 columns with static pictures, 1 column for the picture picked by the date + Table, #1 column for the Charts and the Comment 
    
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('#### Upper chromosphere')
    st.image('https://metro.co.uk/wp-content/uploads/2015/02/the-sun.jpg?quality=90&strip=all&zoom=1&resize=480%2C461',  use_column_width=True)
    
with col2:
    st.markdown('#### Upper corona')
    st.image('https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2022/03/the_sun_in_high_resolution/24010613-1-eng-GB/The_Sun_in_high_resolution_pillars.jpg', use_column_width=True)
    

with col3:
    st.markdown('#### Current Sun surface')
    
    if run_prediction == True:
        
        d1 = date_select.strftime("%Y/%m/%d")
        d2=d1.replace("/","")
        uri=f'https://sdo.gsfc.nasa.gov/assets/img/browse/{d1}/{d2}_014500_1024_HMIIF.jpg'

        response = requests.get(uri) ## Making a variable to get image.
        file = open("./im/sample_image1.jpg", "wb") ## Creates the file for image
        file.write(response.content) ## Saves file content
        file.close()
        
        st.image(uri, use_column_width=True)
        
        st.table(df)
        
        #st.markdown(f'''|Solar flare class| B_Class | C_class |     
#|:---:| :---: | :---: |  
#|Flare count % |{b_class} |{c_class}|
#''')
    
with col4:
    st.markdown('#### Geo-storm Probability')
    if run_prediction == True:
        
        # creating chrt plot 
        x = df['image_class']
        y = df ["probability(%)"]

       

        fig, ax = plt.subplots(figsize=(4, 5))
       # plt.figure(figsize=(4, 8))
        ax.bar(x, y, color=['green', 'darkorange'])
        # Setting the x-acis label and its size
        plt.xlabel("Solar Flare Class", size=15)
        # Setting the y-axis label and its size
        plt.ylabel("Earth Geo-storm Event_Prob.", size=15)
        #ax.set_title('XY Stock')
        
        st.pyplot(fig)
        
        
        
        if c_class>b_class:
            st.error("### Strong or Medium Geo-storm warning !!!")
            
        
       # elif c_class>b_class:
            st.error("### A Geo-storm warning !")
       # elif c_class>50:
          #  st.warning("### A Geo-storm warning !")
        else:
            st.success("### No storm, Dorothy can play outside ! ")

with st.expander("### Validate"):
    date_next= date_select+ timedelta(days=1) ## nLine
    d3=date_next.strftime("%Y/%m/%d")
    d4=date_next.strftime("%Y/%m/%d").replace("/","")
    mm = date_next.strftime("%m")
    dd = date_next.strftime("%d")
    yy = date_next.strftime("%Y")

    st.markdown("### Sun Astronomy dispaly for validation")
    st.markdown(f" ##### Diagram of the solar flare activity on {d3}")

    st.image(f'https://tesis.xras.ru/en/upload_test/files/flares_{d4}.png')
    st.markdown(f"https://tesis.xras.ru/en/sun_flares.html?m={mm}&d={dd}&y={yy}")
    
# Just a Dummy button to reset the flow 
st.button("## RESET")
#except:        


  



    