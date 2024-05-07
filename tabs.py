import os
import streamlit as st
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
import pandas as pd
from datetime import datetime
import time
from pathlib import Path
import os
from search_and_gen import get_top_4, gen_reply
from streamlit.runtime import get_instance
from streamlit.runtime.scriptrunner import get_script_run_ctx
import json



def calendario():

    data_df = pd.read_csv("calendario_medi.csv")

    data_df['inizio'] = data_df['inizio'].map(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    data_df['fine'] = data_df['fine'].map(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

    updated_df = st.data_editor(
        data_df,
        column_config={
            "inizio": st.column_config.DatetimeColumn(
                "Inizio",
                min_value=datetime(2023, 6, 1),
                max_value=datetime(2025, 1, 1),
                format="YYYY-MM-DD HH:mm",
                step=60,
            ),
                    "fine": st.column_config.DatetimeColumn(
                "Fine",
                min_value=datetime(2023, 6, 1),
                max_value=datetime(2025, 1, 1),
                format="YYYY-MM-DD HH:mm",
                step=60,
            ),
        },
        hide_index=True,
        num_rows="dynamic"

    )

    if st.button("Salva", type="primary"):
        updated_df = updated_df.dropna()
        updated_df.to_csv("calendario_medi.csv", index = False)
        salvato = st.success('Salvato', icon="✅")
        time.sleep(3) 
        salvato.empty()

    if st.button("Trova sovrapposizioni", type="primary"):
        salvato = st.success('Nessuna sovrapposizione', icon="✅")
        time.sleep(3) 
        salvato.empty()


def upload_docs():
    st.title("Carica PDF")

    uploaded_file = st.file_uploader("Carica una circolare in formato PDF", type=['pdf'])

    if uploaded_file is not None:
        save_folder = "pdfs"  # Replace with your desired folder path
        save_path = Path(save_folder, uploaded_file.name)

        with open(save_path, mode='wb') as f:
            f.write(uploaded_file.getvalue())

        st.success(f"File '{uploaded_file.name}' saved successfully!")
    else:
        st.info("Please upload a PDF file.")


def search_docs():

    # Create a text input for search terms
    search_term = st.text_input("Inserisci i termini della ricerca:")

    # Create a button to trigger the search functionality
    if st.button("Cerca"):
        # Implement your search logic here using the search_term variable
        # This could involve filtering data, displaying search results, etc.
        st.write(f"Ricerca in corso: '{search_term}'")  # Placeholder for search results


        pdf_filenames = []
        for filename in os.listdir('pdfs'):
            if filename.lower().endswith(".pdf"):  # Check for lowercase and uppercase extensions
                pdf_filenames.append(filename)
                
        # Display title
        st.title("Risultati")

        # Loop to display three results
        for i in range(len(pdf_filenames)):
            container = st.container(border=True)

            # Create columns
            col1, col2 = container.columns( [1, 4])  # You can also specify width ratios as a list (e.g., [2, 1])

            # Use the columns for your content
            with col1:
                col1.write(pdf_filenames[i])

            with col2:
                col2.write("*descrizione*")
            
        

def substitute():

    st.markdown("## Ricerca supplente")


    giorni_settimana = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
    day = st.selectbox("Seleziona un giorno:", giorni_settimana)
    hour = st.selectbox('Quale ora:', [1, 2, 3, 4, 5, 6, 7])

    df = pd.read_csv("orari_prof.csv")

    naprofs = df[(df["Giorno"]==day)&(df["Ora"]==hour)]
    naprofs = naprofs['Docente'].unique()

    all_profs = df["Docente"].unique()

    avail_profs = [x for x in all_profs if x not in naprofs]

    st.markdown("### Supplenti disponibili")

    stravprofs = ""

    for p in avail_profs[:-1]:
        stravprofs += p + ", "
    stravprofs += avail_profs[-1]


    st.markdown(stravprofs)


def orari_profs():

    st.markdown("# Modifica orari ")


    data_df = pd.read_csv("orari_prof.csv")
    profsdf = pd.read_csv("profs.csv")
    profs =  list(profsdf['Docente'])
    classidf = pd.read_csv("classi.csv")
    classi = list(classidf['Classe'])


    updated_df = st.data_editor(
        data_df,
        column_config={
            "Ora": st.column_config.NumberColumn(
            "Ora",
            min_value=1,
            max_value=7,
            step=1,
            required=True
                ),


            "Giorno":  st.column_config.SelectboxColumn(
            "Giorno",
            width="medium",
             options=["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"],
            required=True),

            "Docente":  st.column_config.SelectboxColumn(
            "Docente",
            width="medium",
             options=profs,
            required=True),


            "Classe":  st.column_config.SelectboxColumn(
            "Classe",
            width="medium",
             options=classi,
            required=True)
            
            },
        hide_index=True,
        num_rows="dynamic"

    )



    if st.button("Salva Orari", type="primary"):
        updated_df = updated_df.dropna()
        updated_df.to_csv("orari_prof.csv", index = False)
        salvato = st.success('Salvato', icon="✅")
        time.sleep(3) 
        salvato.empty()


    st.markdown("# Modifica professori ")


    updated_df = st.data_editor(
        profsdf,
        hide_index=True,
        num_rows="dynamic"

    )

    if st.button("Salva Professori", type="primary"):
        updated_df = updated_df.dropna()
        updated_df.to_csv("profs.csv", index = False)
        salvato = st.success('Salvato', icon="✅")
        time.sleep(3) 
        salvato.empty()

    st.markdown("# Modifica classi ")


    updated_df = st.data_editor(
        classidf,
        hide_index=True,
        num_rows="dynamic"

    )

    if st.button("Salva Classi", type="primary"):
        updated_df = updated_df.dropna()
        updated_df.to_csv("classi.csv", index = False)
        salvato = st.success('Salvato', icon="✅")
        time.sleep(3) 
        salvato.empty()



def cerca_circ():

    def _get_session():
        runtime = get_instance()
        session_id = get_script_run_ctx().session_id
        session_info = runtime._session_mgr.get_session_info(session_id)
        if session_info is None:
            raise RuntimeError("Couldn't get your Streamlit Session object.")
        return session_id

    def log_message(user, message):
        ts = datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S")
        df = pd.read_csv('conv_log.csv')
        mex = [{'session': _get_session(), 'user': user, 'message': message, 'timestamp': ts}]
        pd.concat([df, pd.DataFrame(mex)], ignore_index = True).to_csv('conv_log.csv', index = False)
        return 0

    st.markdown(f"## Ricerca") 
    # container = st.container(border=True)

    def click_button():
        st.session_state.clicked = True




    col1, col2, col3, col4 = st.columns(4)
    tag = col1.multiselect("Tag", ["Attività extra-sc.", "Corsi docenti", "Gite", "Colloqui"], placeholder="Scegli")
    destinatari = col2.multiselect("Destinatari", ["Docenti", "Studenti", "Genitori"], placeholder="Scegli")
    creazione = col3.multiselect("Creazione", ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno","Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"], placeholder="Scegli")
    ricerca_solo_titolo = col4.toggle("Ricerca solo titolo")


    colbar, colsearch = st.columns([3, 1])
    query = colbar.text_input("Cerca documenti", placeholder="eg corso di Python",  label_visibility = "collapsed")
    ricerca = colsearch.button("Cerca", use_container_width = True, on_click=click_button)


    lorem_ipsum = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'''
    contesto_cont = st.container(border=True)
    add_btns = []
    open_btns = []
    search_r = []

    if 'clicked' not in st.session_state:
        st.session_state.clicked = False
    if 'contesto_dict' not in st.session_state:
        st.session_state.contesto_dict = []


    if st.session_state.clicked:

        try:
            if ricerca_solo_titolo: # se voglio fare una ricerca solo titoli
                search_res = get_top_4_only_title(query, tag, destinatari, creazione)
                if search_res == 'no result': # se non ci sono risultati con la ricerca bm25
                    with st.container(border=True):
                        st.write("Nessun risultato")
                else:
                    for i in range(len(search_res)):
                        with st.container(border=True):
                            title = str(search_res[i].page_content)
                            st.code(title)
                            cont = search_res[i].metadata['content']
                            coltext, coladd = st.columns([4, 1])
                            # coltext.write(cont)
                            cadd = coladd.button("Aggiungi a contesto" , key = 'add' + str(i), use_container_width = True )
                            if cadd:
                                st.session_state.contesto_dict.append({'title': title, 'content': cont})
        except:
            pass
        
        else: 
            search_res = get_top_4(query) #, tipo, linea, area)
            for i in range(len(search_res)):
                with st.container(border=True):
                    title = str(search_res[i]['Metadata']['source'])
                    cont = search_res[i]['Content']

                    def extract_from_content(cont):
                        filename = cont.split('filename:')
                        after_filename = filename[1]

                        filename = after_filename.split('\noggetto:')
                        filename, after_filename = filename[0], filename[1]

                        ogg = after_filename.split('\ndestinatari:')
                        ogg, after_ogg = ogg[0], ogg[1]

                        dest = after_ogg.split('\ndoc:')
                        dest, after_dest = dest[0], dest[1]

                        doc = after_dest.split('\ndoc_30w:')
                        doc, after_doc = doc[0], doc[1]

                        eventi_suggeriti = after_doc.split('\neventi_suggeriti:')
                        doc_30w, eventi_suggeriti  = eventi_suggeriti[0], eventi_suggeriti[1]

                        return filename, ogg, dest, doc, doc_30w, eventi_suggeriti
                    
                    filename, ogg, dest, doc, doc_30w, eventi_suggeriti = extract_from_content(cont)

                    st.markdown(f"**{ogg.strip().capitalize()}**")
                    st.write(f''':gray[{dest}]''')
                    st.markdown(doc_30w)

                    dictionary = json.loads(eventi_suggeriti)

                    title_added = False

                    for e in dictionary['eventi']:
                        if "%" not in e['date_ora'] and len(e['date_ora']) > 8:
                            if not title_added:
                                st.markdown("**Eventi suggeriti**")
                                title_added = True
                            coldt, coltitle, coladd = st.columns([1,3, 1])
                            coldt.markdown(f''':gray[{e['date_ora']}]''')
                            coltitle.markdown(f''':gray[{e['titolo']}]''')
                            cadd = coladd.button("Crea evento" , key = 'cal' + str(e), use_container_width = True )
                        






                    
                    coltext, coladd = st.columns([1, 4])
                    coltext.button("Apri",  key = 'apri' + str(i))

                    cadd = coladd.button("Aggiungi a contesto" , key = 'add' + str(i),  type="primary" )
                    if cadd:
                        st.session_state.contesto_dict.append({'title': title, 'content': cont})

    contesto_cont.write("## Contesto")
    cremove = contesto_cont.button("Resetta contesto" )

    if cremove:
        st.session_state.contesto_dict = []

            
    for e in st.session_state.contesto_dict:    
        contesto_cont.code(e['title'])


    chat_history = ''

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Chiedimi pure.."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        log_message('user', prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})


    # file:///L:/Sistema%20Qualita/13%20-%20OPL/OPL_154%20Salvataggio%20ricette%20J1.xlsx

        # response = rrf.generate_answer(prompt, path_to_corpus).content
        # response = f"{response}"
        def new_mex(st, response):
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            log_message('bot', response)


        # if prompt[:3] == "#da":
        #     df = pd.read_csv("conv_log.csv")
        #     docs = pd.read_csv("trb_opl_cba.csv")
        #     from datetime import datetime
        #     df['ts'] = df.timestamp.map(lambda x: datetime.strptime(x[:10], "%Y/%m/%d"))
        #     st.markdown("Ecco i messaggi totali (bot + user)  per giornata")
        #     st.line_chart(df.groupby("ts").size())
        #     no_idx = df[df.message.map(lambda x : x[:3])  == '#no'].index
        #     before_no_idx = no_idx - 1
        #     fb_no = df.loc[no_idx.append(before_no_idx)].sort_index()[['user', 'message']]
        #     st.markdown("Ecco le risposte con feedback negativo")
        #     st.dataframe(fb_no)
        #     st.markdown("Ecco tutte le risposte")
        #     st.dataframe(df)
        #     st.dataframe(docs)

        if prompt[:3] == "#si":
            new_mex(st, 'Grazie per il feedback 👍')

        elif prompt[:3] == "#no":
            new_mex(st, 'Grazie per il feedback 👍')

        else:
            # response = gen_reply(prompt, docs[0])   # context = str([x[0].page_content for x in st.session_state.contesto_dict])
            context = str([x['content'] for x in st.session_state.contesto_dict])
            response, chat_history = gen_reply(prompt, context, chat_history)
            new_mex(st, response)