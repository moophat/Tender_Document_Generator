import streamlit as st
import os
from utils import *
import yaml

# @st.experimental_dialog("Add variable")
# def vote(data):
#         type=st.selectbox("Type",["SVTECH_INFO","BID_OWNER","BID_INFO"])
#         variable=st.text_input("Variable")
#         if st.button("CREATE"):
#             if variable in data.loc[data['Type']==type]['Variable'].to_list():
#                 st.error("Duplicate variable!!!")
#             else:
#                 st.session_state['current_schema']=pd.concat([data, pd.DataFrame([{'Type':type, 'Variable':variable,'Delete?':False}])])
#                 st.rerun()

def load_schema_data():
    yaml_data_file_path = os.path.normpath(
                            os.path.join(
                                os.path.dirname(os.path.abspath(__file__)),
                                ".." , 
                                "data/input_data_schema.yaml")
    )
    with open(yaml_data_file_path) as f:
        current_schema=yaml.safe_load(f)
    current_schema=pd.DataFrame([(key, value) for key, values in current_schema.items() for value in values], 
                  columns=['Type', 'Variable'])
    return current_schema

def write_schema_data(new_data):
    yaml_data_file_path = os.path.normpath(
                            os.path.join(
                                os.path.dirname(os.path.abspath(__file__)),
                                ".." , 
                                "data/input_data_schema.yaml")
    )
    with open(yaml_data_file_path,'w') as f:
        yaml.dump(new_data, f, default_flow_style=False, sort_keys=False)

def change_update_button_state():
    st.session_state['create_button_disabled']=False

with st.sidebar:
    TerminalOutput, LoggingOutput= init_logging_popup_button()
variable_options=[]
with st_stdout("code",TerminalOutput, cache_data=True), st_stderr("code",LoggingOutput, cache_data=True):
    st.header("VARIABLES MANAGEMENT")
    update_button=st.button("UPDATE", disabled=st.session_state.get("create_button_disabled", True))
    st.markdown("""
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    height: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)
    current_schema=load_schema_data()
    new_schema=st.data_editor(current_schema, num_rows="dynamic", on_change= change_update_button_state())
    if update_button:
        new_schema = new_schema.groupby('Type')['Variable'].apply(list).to_dict()
        write_schema_data(new_schema)
        st.rerun()