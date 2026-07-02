import streamlit as st
from auth import signup


def show_signup():

    st.markdown(
        """
        <h1 style="text-align:center;">
            🧠 LeetRecall AI
        </h1>
        <h4 style="text-align:center;color:gray;">
            Create Your Account
        </h4>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    with st.form("signup_form"):

        username = st.text_input(
            "Username"
        )

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )

    if submitted:

        if not username or not email or not password:
            st.error("Please fill all fields.")
            return

        result = signup(
            username,
            email,
            password
        )

        if result.get("success"):

            st.success("🎉 Account created successfully!")

            st.info("You can now login with your credentials.")

        else:

            st.error(
                result.get(
                    "message",
                    "Signup Failed."
                )
            )