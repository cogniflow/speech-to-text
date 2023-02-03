import streamlit as st
import streamlit.components.v1 as components
from st_custom_components import st_audiorec
import base64
from cogniflow_utils import cogniflow_request_audio

st.set_page_config(
    page_title="Cogniflow Speech-to-text",
    page_icon="https://uploads-ssl.webflow.com/60510407e7726b268293da1c/60ca08f7a2abc9c7c79c4dac_logo_ico256x256.png"
)

st.title('Speech-to-Text')
st.markdown("Powered by [Cogniflow](https://www.cogniflow.ai)")

model = st.secrets["model_url"]
api_key = st.secrets["api_key"]

audio_file = st.file_uploader("Upload an audio", type=['wav', 'ogg', 'mp3'])

st.caption("Or")

with st.expander("Record Audio"):
    audio_bytes = st_audiorec()

placeholder = st.empty()
audio_bytes_sel = None

if audio_bytes:
    with placeholder.container():
        st.write("Audio to transcribe:")
        st.audio(audio_bytes, format="audio/wav")
    audio_format = "wav"
    audio_bytes_sel = audio_bytes

if audio_file:
    with placeholder.container():
        st.write("Audio to transcribe:")
        st.audio(audio_file, format=audio_file.type)
    audio_format = audio_file.type.replace("audio/","")
    audio_bytes_sel = audio_file.getvalue()

text = st.text_area("(Optional) Enter the content of the audio to get the Word Error Rate")

click = st.button("✨ Get transcription")

if click:
    if audio_bytes_sel is not None and model != "" and api_key != "":    
        audio_b64 = base64.b64encode(audio_bytes_sel).decode()

        with st.spinner("Predicting..."):
            result = cogniflow_request_audio(model, api_key, audio_b64, audio_format, text)        

        st.session_state['result'] = result['result']
        st.session_state['wer'] = result['wer']

    else:
        st.warning("Record or upload an audio first")

if 'result' in st.session_state:

    st.header("Output")
    st.success(st.session_state.result)  
    st.download_button('📄 Download transcription to file', st.session_state.result)
    
    if st.session_state.wer != -1:
        st.metric(label="WER", value=st.session_state.wer, help="0.25 means that 75 percent of the transcription was correct")
        
