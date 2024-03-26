import streamlit as st
from PyPDF2 import PdfReader
import io
import re  # Import the regex module

def pdf_to_text(pdf_file):
    """Converts PDF file content to text using PyPDF2, excluding lines containing 'DocuSign' or version numbers."""
    text = ""
    reader = PdfReader(pdf_file)
    version_pattern = re.compile(r'\bv?\d+(\.\d+)+\b')  # Regular expression to match version numbers (e.g., 1.0.0, v2.1.3)
    for page in reader.pages:
        page_text = page.extract_text() if page.extract_text() else ""
        filtered_text = "\n".join(line for line in page_text.splitlines() if "docusign" not in line.lower() and not version_pattern.search(line))
        text += filtered_text + "\n"
    return text.strip()

def highlight_differences(text1, text2):
    """Generates HTML to display differing lines from two texts, highlighting differences and including line numbers."""
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    
    max_len = max(len(lines1), len(lines2))
    lines1.extend(["Not in document"] * (max_len - len(lines1)))
    lines2.extend(["Not in document"] * (max_len - len(lines2)))
    
    diff_html = ''
    differences_found = False
    for i, (line1, line2) in enumerate(zip(lines1, lines2), start=1):
        if line1 != line2:
            differences_found = True
            cell1 = line1 if line1 else "Not in document"
            cell2 = line2 if line2 else "Not in document"
            diff_html += f'<tr><td>Line {i}</td>' \
                         f'<td style="background-color: #ffa07a; padding: 4px; width:45%;">{cell1}</td>' \
                         f'<td style="background-color: #98fb98; padding: 4px; width:45%;">{cell2}</td></tr>'
    if differences_found:
        diff_html = '<table style="width:100%;">' + diff_html + '</table>'
    return diff_html, differences_found

st.title('Unwanted change checker')

st.write("Intended to be used to compare two contracts that should be identical. Lines with 'DocuSign' and version numbers are ignored in the comparison.")

# Use session state to manage the unique keys for file uploaders
if 'upload_key' not in st.session_state:
    st.session_state.upload_key = 0

# Add a refresh button
if st.button('Refresh App'):
    # Increment the key to reset the uploaders
    st.session_state.upload_key += 1

col1, col2 = st.columns(2)

with col1:
    st.write("PDF 1:")
    pdf1 = st.file_uploader("Upload PDF 1", type=['pdf'], key=f"pdf1_{st.session_state.upload_key}")

with col2:
    st.write("PDF 2:")
    pdf2 = st.file_uploader("Upload PDF 2", type=['pdf'], key=f"pdf2_{st.session_state.upload_key}")

if pdf1 and pdf2:
    pdf1_bytes = io.BytesIO(pdf1.getvalue())
    pdf2_bytes = io.BytesIO(pdf2.getvalue())

    text1 = pdf_to_text(pdf1_bytes)
    text2 = pdf_to_text(pdf2_bytes)
    diff_html, differences_found = highlight_differences(text1, text2)
    
    if not differences_found:
        st.write("'100%' identical excluding lines that are generated by 'DocuSign' and version numbers.")
    else:
        st.write("Differences Found (excluding 'DocuSign' and version numbers):")
        st.markdown(diff_html, unsafe_allow_html=True)
   

