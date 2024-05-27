import streamlit as st
import language_tool_python
import pandas as pd

def correct_text(text):
    my_tool = language_tool_python.LanguageTool('en-US')
    matches = my_tool.check(text)
    corrected_text = my_tool.correct(text)
    misspelled_words = [text[match.offset:match.offset + match.errorLength] for match in matches]
    corrected_words = [match.replacements[0] if match.replacements else '' for match in matches]
    misspelled_and_corrected = [(word, corrected) for word, corrected in zip(misspelled_words, corrected_words) if word != corrected]
    return corrected_text, misspelled_and_corrected

def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            text = uploaded_file.getvalue().decode("utf-8")
            return correct_text(text)
        else:
            st.warning("Please upload a text file (.txt).")
            return None, None

def main():
    st.title("WriteRight")
    st.write("Enter a sentence or upload a text file (.txt) to check grammar and spelling.")

    st.subheader("Enter your sentence:")
    input_text = st.text_area("", height=350)

    st.subheader("Upload a text file (.txt):")
    uploaded_file = st.file_uploader("", type=['txt'])

    if st.button("Correct"):
        if input_text:
            corrected_text, misspelled_and_corrected = correct_text(input_text)
            st.header("Original Text:")
            st.write(input_text)
            st.header("Corrected Text:")
            st.write(corrected_text)
            if misspelled_and_corrected:
                df = pd.DataFrame(misspelled_and_corrected, columns=["Misspelled Word", "Correct Spelling"])
                st.header("Misspelled Words and Corrections:")
                st.dataframe(df)
        elif uploaded_file:
            corrected_text, misspelled_and_corrected = process_uploaded_file(uploaded_file)
            if corrected_text:
                st.header("Corrected Text:")
                st.write(corrected_text)
                if misspelled_and_corrected:
                    df = pd.DataFrame(misspelled_and_corrected, columns=["Misspelled Word", "Correct Spelling"])
                    st.header("Misspelled Words and Corrections:")
                    st.dataframe(df)
        else:
            st.warning("Please enter a sentence or upload a text file.")

if __name__ == "__main__":
    main()
