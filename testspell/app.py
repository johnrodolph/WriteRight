import streamlit as st
import language_tool_python
import pandas as pd

def correct_text(text):
    my_tool = language_tool_python.LanguageTool('en-US')
    matches = my_tool.check(text)
    corrected_text = my_tool.correct(text)
    
    misspelled_words = []
    corrected_words = []
    grammar_errors = []

    for match in matches:
        error_text = text[match.offset:match.offset + match.errorLength]
        if match.replacements:
            correction = match.replacements[0]
        else:
            correction = ''
        
        if match.ruleIssueType == 'misspelling':
            misspelled_words.append((error_text, correction))
        else:
            grammar_errors.append((error_text, correction, match.message))

    return corrected_text, misspelled_words, grammar_errors

def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            text = uploaded_file.getvalue().decode("utf-8")
            return correct_text(text)
        else:
            st.warning("Please upload a text file (.txt).")
            return None, None, None

def main():
    st.title("WriteRight")
    st.write("Enter a sentence or upload a text file (.txt) to check grammar and spelling.")
    
    input_text_col, file_upload_col = st.columns(2)

    with input_text_col:
        st.subheader("Enter your sentence:")
        input_text = st.text_area("", height=350)

    with file_upload_col:
        st.subheader("Upload a text file (.txt):")
        uploaded_file = st.file_uploader("", type=['txt'])

    if st.button("Correct"):
        with st.spinner('Processing...'):
            if input_text:
                corrected_text, misspelled_words, grammar_errors = correct_text(input_text)
                st.header("Original Text:")
                st.write(input_text)
                st.header("Correct Grammar and Spelling:")
                st.write(corrected_text)
                
                if misspelled_words:
                    misspelled_df = pd.DataFrame(misspelled_words, columns=["Misspelled Word", "Correct Spelling"])
                    st.header("Misspelled Words and Corrections:")
                    st.dataframe(misspelled_df)
                
                if grammar_errors:
                    grammar_df = pd.DataFrame(grammar_errors, columns=["Error", "Correction", "Message"])
                    st.header("Grammatical Errors and Corrections:")
                    st.dataframe(grammar_df)
                    
            elif uploaded_file:
                corrected_text, misspelled_words, grammar_errors = process_uploaded_file(uploaded_file)
                if corrected_text:
                    st.header("Correct Grammar and Spelling:")
                    st.write(corrected_text)
                    
                    if misspelled_words:
                        misspelled_df = pd.DataFrame(misspelled_words, columns=["Misspelled Word", "Correct Spelling"])
                        st.header("Misspelled Words and Corrections:")
                        st.dataframe(misspelled_df)
                    
                    if grammar_errors:
                        grammar_df = pd.DataFrame(grammar_errors, columns=["Error", "Correction", "Message"])
                        st.header("Grammatical Errors and Corrections:")
                        st.dataframe(grammar_df)
            else:
                st.warning("Please enter a sentence or upload a text file.")
    
 

if __name__ == "__main__":
    main()
