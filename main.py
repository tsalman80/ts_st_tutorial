import streamlit as st


def main():
    pg = st.navigation(
        [
            st.Page("pages/login.py", title="Login", url_path="login", default=True),
            st.Page("pages/home.py", title="Home", url_path="home"),
            st.Page("pages/logout.py", title="Logout", url_path="logout"),
        ],
        position="hidden",
    )
    pg.run()


if __name__ == "__main__":
    main()
