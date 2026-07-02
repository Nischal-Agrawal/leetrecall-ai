import streamlit as st
from auth import login


def show_login():

    st.markdown(
        """
        <h1 style="text-align:center;">
            🧠 LeetRecall AI
        </h1>
        <h4 style="text-align:center;color:gray;">
            Intelligent DSA Revision System
        </h4>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    with st.form("login_form"):

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True
        )

    if submitted:

        if not email or not password:
            st.error("Please fill all fields.")
            return

        result = login(
            email,
            password
        )

        if result.get("success"):

            st.session_state.logged_in = True
            st.session_state.token = result["access_token"]
            st.session_state.username = result["username"]
            st.session_state.email = result["email"]

            st.success("Login Successful!")

            st.rerun()

        else:

            st.error(
                result.get(
                    "message",
                    "Login Failed."
                )
            )