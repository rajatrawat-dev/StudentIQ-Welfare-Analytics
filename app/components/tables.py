"""Styled dataframes and status badges."""

import streamlit as st
import pandas as pd

def render_styled_dataframe(df: pd.DataFrame, height: int = 400):
    st.dataframe(df, use_container_width=True, height=height, hide_index=True)