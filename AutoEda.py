import streamlit as st
import pandas as pd
import numpy as np
import base64 
from pandas_profiling import ProfileReport
import time
import streamlit.components.v1 as components  # Import Streamlit
timestr = time.strftime("%Y%m%d-%H%M%S")
import codecs
import os


def Report_downloader():
	csvfile = codecs.open("EDA.html", 'r')
	b64 = base64.b64encode(csvfile.encode()).decode()
	new_filename = "Report_{}_.html".format(timestr)
	st.markdown("#### Download File ###")
	href = f'<a href="data:file/html;base64,{b64}" download="{new_filename}">Scarica il Report</a>'
	st.markdown(href,unsafe_allow_html=True)

st.set_page_config(page_title="AUTO Analisi Esplorativa ( EDA ) by I.A. Italia", page_icon=None, layout='wide', initial_sidebar_state='auto')

st.markdown("<center><h1> AUTO EDA <small>by I. A. ITALIA</small></h1>", unsafe_allow_html=True)
st.write('<p style="text-align: center;font-size:15px;" >Non <bold>sei stanco di dover scrivere del codice per fare una semplice ANALISI ESPLORATIVA </bold> dei i tuoi dati <bold>  ?</bold><p>', unsafe_allow_html=True)

dataframe = pd.DataFrame()

file_caricato =  st.file_uploader("SCEGLI UN FILE CSV", type="CSV", accept_multiple_files=False)
if file_caricato is not None:
	dataframe = pd.read_csv(file_caricato)
	st.markdown("<br><br>", unsafe_allow_html=True)	
	
	colonne = list(dataframe.columns)
	options = st.multiselect("Colonne Selezionate per il REPORT",colonne,colonne)
	dataframe = dataframe[options]


	try:
	    with st.beta_expander("VISUALIZZA DATASET"):
	        st.write(dataframe)
	    with st.beta_expander("STATISICA DI BASE"):
	        st.write(dataframe.describe())
	except:
	    print("")
	 
	st.markdown("<br><br>", unsafe_allow_html=True)	
	
	
	
	problemi = ["COMPLETO", "MINIMAL" ]
	tipo_di_problema = st.selectbox('Seleziona che tipo di Report Desideri', problemi)



	if(st.button("Aiutami a Capire questi dati")):
		if(tipo_di_problema == "COMPLETO"):
			profile = ProfileReport(dataframe,title='Pandas Profiling Report',html={'style': {'full_width': True}}, sort=None)
			profile.to_file("EDA.html")
		if(tipo_di_problema == "MINIMAL"):
			profile = ProfileReport(dataframe,title='Pandas Profiling Report',html={'style': {'full_width': True}}, sort=None,minimal=True)
			profile.to_file("EDA.html")
		
if(os.path.exists('EDA.html')):
	with st.spinner(text="Dacci un attimo per analizzare e studiare i dati..."):
		HtmlFile = open("EDA.html", 'r', encoding='utf-8')
		source_code = HtmlFile.read() 
		#print(source_code)
		st.balloons()
		components.html(source_code, height=10000)
		os.remove("EDA.html")
		
	
