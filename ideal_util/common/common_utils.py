#/usr/bin/env python3

import uuid
import streamlit as st

# Initialize an unique ID for the user session and store it in session state
# This ID is passed to the @st.cache_data decorated function as an extra argument. 
# It is not used inside the function but is used to differentiate between different users.
# We use this mechanism to ensure user-specific data cached are only accessible to one user.
def get_session_id():
    if 'SESSION_ID' not in st.session_state:
        session_id = str(uuid.uuid4())
        st.session_state["SESSION_ID"] = session_id
    else:
        session_id = st.session_state["SESSION_ID"] 
    return session_id
