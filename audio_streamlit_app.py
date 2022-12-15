import streamlit as st
from audio_recorder_streamlit import audio_recorder
import base64
from cogniflow_utils import cogniflow_request_audio
#import sounddevice as sd

st.set_page_config(
    page_title="Cogniflow Speech-to-text",
    page_icon="https://uploads-ssl.webflow.com/60510407e7726b268293da1c/60ca08f7a2abc9c7c79c4dac_logo_ico256x256.png"
)

def _max_width_():
    max_width_str = f"max-width: 900px;"
    st.markdown(
        f"""
    <style>
    .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

_max_width_()

st.title('Speech Recognition')
st.markdown("Powered by [Cogniflow](https://www.cogniflow.ai)")

model = st.secrets["model_url"]
api_key = st.secrets["api_key"]

col_audio1, col_audio2 = st.columns(2)

with col_audio1:
    audio_bytes = audio_recorder()

with col_audio2:
    audio_file = st.file_uploader("Or Upload an audio", type=['wav', 'ogg', 'mp3'])

placeholder = st.empty()

audio_bytes_sel = None

if audio_bytes:
    placeholder.audio(audio_bytes, format="audio/wav")
    audio_format = "wav"
    audio_bytes_sel = audio_bytes

if audio_file:
    placeholder.empty()
    placeholder.audio(audio_file, format=audio_file.type)
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
    col1, col2 = st.columns(2, gap="large")   
    col1.header("Output")
    col1.success(st.session_state.result)  
    
    if st.session_state.wer != -1:
        col2.header("Word Error Rate")
        col2.metric(label="WER", value=st.session_state.wer, help="0.25 means that 75 percent of the transcription was correct")    
    
    col2.download_button('📄 Download transcription to file', st.session_state.result)

