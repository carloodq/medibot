import os
import streamlit as st
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
import pandas as pd
# from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.document_loaders import CSVLoader
from dotenv import load_dotenv

def csv_to_vs(path_to_corpus, oaikey):
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = oaikey
    loader = CSVLoader(file_path = path_to_corpus, source_column="filename", encoding='utf-8')
    data = loader.load()
    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_documents(data, embeddings)
    docsearch.save_local("circolari_1")
    return None




def get_top_4(myquery, tag = [], destinatari = [] , creazione = []):
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local("circolari_1" , embeddings, allow_dangerous_deserialization=True)
    # retriever = docsearch.as_retriever(search_kwargs={"k": k})
    # docs = retriever.get_relevant_documents(query)

    import pandas as pd
    df = pd.read_csv("sept1.csv")
        
    results_with_scores = db.similarity_search_with_score(myquery, k=int(len(df)), fetch_k=int(len(df)) )
    search_results = []

    # # if there are no categories selected, then don't apply a filter
    # if len(my_categories) == 0:
    #     my_categories  = ['OPL', 'TRB', 'CBA', 'GEN', 'JOA', 'F2'] 
    # if len(my_lines) == 0:
    #     my_lines  = ['F1', 'J1', 'JP', 'F3', 'OPTIMA', 'GEN', 'JOA', 'F2']
    # if len(my_areas) == 0:
    #     my_areas  = ['A', 'B', 'C', 'D', 'E', 'Colle', 'GEN', 'JOA', 'F2', "noline", "TUTTE", "LINEA", "IMPIANTI"] # noline is for entries with no data on area
 
    # def line_included(line_is_included, my_lines):
    #     line_in = False
    #     try:
    #         new_lines = line_is_included.split('-') # sometimes if associated with many lines they are separated with dash
    #     except:
    #         new_lines = []
    #     for l in new_lines:
    #         if l.upper() in my_lines:
    #             line_in = True
    #             break
    #     return line_in

    # def filter_df(my_categories, my_lines, my_areas):
    #     filter_df = ( (df['Categoria'].isin(my_categories)) & (df['Area'].isin(my_areas)) & (df['Linea'].map(lambda line_is_included: line_included(line_is_included, my_lines))  ) )
    #     return list(df[filter_df].index)


    # ok_indeces = filter_df(my_categories, my_lines, my_areas)

    for doc, score in results_with_scores:
        res = {'Content': doc.page_content, 'Metadata': doc.metadata, 'Score': score}
        # if doc.metadata['row'] in ok_indeces:
        #     search_results.append(res)
        search_results.append(res)


    return search_results[:4]





def gen_reply(query, context, chat_history):
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import (
        HumanMessage
    )
    model_name = "gpt-3.5-turbo"
    chat = ChatOpenAI(model_name=model_name, temperature=0)
    question = f"""Sei un chatbot che sta avendo una conversazione con un essere umano.

                    Dati i seguenti estratti e una domanda, crea una risposta finale.

                    Contesto:{context}

                    Conversazione:
                    {chat_history}

                    Umano: {query}
                    AI:
"""

    response = chat([HumanMessage(content=question)]).content

    chat_history += f'''\nHuman: {query}\nAI:{response}'''
        

    return response, chat_history


def summarize(context):
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import (
        HumanMessage
    )
    model_name = "gpt-3.5-turbo"
    chat = ChatOpenAI(model_name=model_name, temperature=0)
    question = f"""Riassumi in 30 parole il seguente testo.

                    Testo:{context}"""

    response = chat([HumanMessage(content=question)]).content

    return response


def doc2event(context):
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import (
        HumanMessage
    )
    model_name = "gpt-3.5-turbo"
    chat = ChatOpenAI(model_name=model_name, temperature=0)
    question = f"""estrai tutti gli eventi in questo documento e restituiscili come testo json. Per ogni evento indica date_ora (%d %B %Y %H:%M) e titolo. Restituisci solo il json e nient'altro. La lista di eventi si chiama eventi.

                    Testo:{context}"""

    response = chat([HumanMessage(content=question)]).content

    return response




