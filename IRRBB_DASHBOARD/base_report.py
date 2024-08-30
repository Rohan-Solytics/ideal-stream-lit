import streamlit as st
import base64
from artifacts import Base_Report_data

# Custom CSS style for the container and table header
custom_css = """
<style>
    .custom-container {
        max-height: 400px;
        overflow-y: scroll;
        position: relative;
        border-radius: 10px;
        border: 1px solid #ccc;
    }
    th, td {
        font-size: 14px;
        padding: 8px; /* Add padding for better readability */
        text-align: left; /* Align text to the left */
    }
    .download-button {
        position: absolute;
        top: -10px;
        right: 10px;
        font-size: 18px;
    }
    thead {
        position: sticky;
        top: 0;
        background-color: #005f69;
        color: white;
    }
</style>
"""

def app():
    # Inject custom CSS into the Streamlit app
    st.markdown(custom_css, unsafe_allow_html=True)

    cols_slider = st.slider("Number of Columns to Display", min_value=1, max_value=len(Base_Report_data.columns), value=len(Base_Report_data.columns))
    displayed_data = Base_Report_data.iloc[:, :cols_slider]

    # Rename the index column to "Row_Id"
    displayed_data.index.name = "Row_Id"

    # Create HTML table with custom header row
    html_table = f'<div class="custom-container"><table class="dataframe">'
    html_table += '<thead><tr>'
    html_table += '<th>Row_Id</th>'  # Add the custom index column header
    for col_name in displayed_data.columns:
        html_table += f'<th>{col_name}</th>'
    html_table += '</tr></thead>'

    # Add table rows with concatenated values
    for _, row in displayed_data.iterrows():
        html_table += '<tr>'
        html_table += f'<td>{row.name}</td>'  # Display the index name
        for col_value in row.values:
            html_table += f'<td>{col_value}</td>'
        html_table += '</tr>'

    html_table += '</table></div>'

    # Add a download button with a custom download icon in a square box
    st.markdown('<div class="download-button"><a href="data:file/csv;base64,{}" download="table.csv">⬇️</a></div>'.format(
        base64.b64encode(displayed_data.to_csv(index=True, encoding='utf-8').encode()).decode()),
        unsafe_allow_html=True
    )

    # Display the HTML table
    st.markdown(html_table, unsafe_allow_html=True)
