import streamlit as st
import langchain_helper

st.title("Restaurant Generator")

cuisine = st.sidebar.selectbox(
    "Pick a Cuisine",
    (
        "American",
        "Italian",
        "Mexican",
        "Indian",
        "Arabic",
        "French",
        "British",
        "Chinese",
        "Japanese",
        "Korean",
        "Russian",
    ),
)

if cuisine:
    response = langchain_helper.generate_restaurant_name_and_items(cuisine)
    st.header(response["restaurant_name"].content.replace('"', ""))
    menu_items = response["menu_items"].content.split(",")
    st.write("*** Menu Items ***")
    for item in menu_items:
        st.write("-", item)
