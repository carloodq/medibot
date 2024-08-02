import streamlit as st
import datetime
st.write("hey")

if 'rows' not in st.session_state:
    st.session_state['rows'] = []



pressed_new_button = st.button("Aggiungi documento")
if pressed_new_button:
    st.session_state['rows'] += [str(datetime.datetime.now())]



inpts = []
up_files_list = []

for x in st.session_state['rows']:
    inpts.append(st.text_input('yo', key = x))

    uploaded_files = st.file_uploader("Carica una circolare in formato PDF", type=['pdf', 'png', 'jpg', 'jpeg'], accept_multiple_files = True, key = x+'img')
    up_files_list.append(uploaded_files)


        

if st.button('show'):
    for i in inpts:
        st.write(i)


    for uploaded_files in up_files_list:
        for uploaded_file in uploaded_files:
            if uploaded_file is not None:
                uploaded_file[name] += 'hola'
                st.write(uploaded_file.name)
            #     save_folder = "pdfs"  # Replace with your desired folder path
            #     save_path = Path(save_folder, uploaded_file.name)

            #     with open(save_path, mode='wb') as f:
            #         f.write(uploaded_file.getvalue())

            #     st.success(f"File '{uploaded_file.name}' saved successfully!")
            # else:
            #     st.info("Please upload a PDF file.")




