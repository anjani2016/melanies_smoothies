# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(f" :cup_with_straw: Customise your smoothies! :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruit you want for your smoothie
  """
)

smoothie_name = st.text_input("Name your smoothie")
st.write("The name of your smoothie will be", smoothie_name)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose upto 5 fruits as ingredients:",
    my_dataframe,
        max_selections=5
)

# tab and 4 spaces - prefer 4 spaces
if ingredients_list:
    st.write("You selected:", ingredients_list)
    st.text( ingredients_list)
    #st.text("You selected:", ingredients_list) did not work
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen
    st.write("You selected:", ingredients_string)
    
    NAME_ON_ORDER = smoothie_name

    my_insert_stmt = """ insert into smoothies.public.ORDERS(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + NAME_ON_ORDER + """')"""
   
    st.write(my_insert_stmt)
    
    #insert button

    time_to_insert = st.button('submit order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


#new section to disply smoothie frooti
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)



