import re
import streamlit as st
from streamlit_player import st_player
from scripts.youtube_transcriber import YoutubeTranscriber


examples = {
"Equating Numerator and Grouping Concept (PSLE P5/P6 Singapore Math)": {
        "video_url": "https://www.youtube.com/watch?v=GTAaVdNqx5U",
        "name": "Equating_Numerator_and_Grouping_Concept_(PSLE_P5P6__Singapore_Math)",
    },
    "2021 PSLE Math question [answered] | PSLE Helen and Ivan coin question 2021": {
        "video_url": "https://www.youtube.com/watch?v=Rt_FjKLVehc",
        "name": "2021_PSLE_Math_question_[answered]__PSLE_Helen_and_Ivan_coin_question_2021",
    },
    
    "Introduction to ratios | Ratios, proportions, units, and rates | Pre-Algebra | Khan Academy": {
        "video_url": "https://www.youtube.com/watch?v=HpdMJaKaXXc",
        "name": "Introduction_to_ratios__Ratios_proportions_units_and_rates__Pre-Algebra__Khan_Academy",
    },
        "Machine Learning in 5 Minutes": {
        "video_url": "https://www.youtube.com/watch?v=-DEL6SVRPw0",
        "name": "Machine Learning In 5 Minutes  Machine Learning Introduction What Is Machine Learning Simplilearn",
    },

}


def clean_video_url(video_url):
    video_url = re.sub(f"&.*", "", video_url)
    return video_url


def show_youtube_thumbnail(video_url):
    columns = st.columns((1, 2, 1))
    with columns[1]:
        st_player(
            video_url,
            height=500,
        )


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def transcribe_video(
    api_key,
    video_url,
    use_content_moderation,
    use_topic_detection,
):
    youtube_transcriber = YoutubeTranscriber(
        api_key,
        video_url,
        content_safety=use_content_moderation,
        iab_categories=use_topic_detection,
    )

    with st.spinner("Downloading audio"):
        if youtube_transcriber.downloaded_audio_path is None:
            youtube_transcriber.download_audio()
            st.success(
                f"Audio downloaded to {youtube_transcriber.downloaded_audio_path}"
            )
        else:
            st.info("hello")

    with st.spinner("Uploading audio"):
        if youtube_transcriber.upload_url is None:
            youtube_transcriber.upload_audio()
            st.success(f"upload url: {youtube_transcriber.upload_url}")

    with st.spinner("Submitting a job for processing queue"):
        if youtube_transcriber.transcription_id is None:
            youtube_transcriber.submit()
            st.info(
                f"A transcription job (id={youtube_transcriber.transcription_id}) has been submitted"
            )

    with st.spinner("Polling the result"):
        if youtube_transcriber.transcription is None:
            youtube_transcriber.poll()
            st.success("Transcription succeeded")

    output_name = youtube_transcriber.downloaded_audio_path.split("/")[-1].rstrip(
        ".mp4"
    )
    output_name = output_name.replace(" ", "_")

    youtube_transcriber.save_transcript(output_name)

    return youtube_transcriber.transcription


def visualize_result(video_url, result):
    text = result["text"]
    labels = result["labels"]
    timestamp = result["timestamp"]
    start = timestamp["start"]
    end = timestamp["end"]

    st.info(f"⏱️ Start time : **{start}** | End time: **{end}**")

    st_player(
        video_url,
        config={"playerVars": {"start": int(start / 1000), "end": int(end / 1000) + 1}},
    )

    st.markdown(f"**text**: {text}")

    expander = st.expander("Visualize topics")

    with expander:
        for label in labels:
            relevance = label["relevance"]
            label = label["label"]
            st.markdown(f"- `{label}` : {relevance:.4f}")


def show_output(video_url, transcript, use_topic_detection):
    show_youtube_thumbnail(video_url)

    cols = st.columns(2)

    with cols[0]:
        st.header("Transcription output")
        st.write(transcript)

    if use_topic_detection:
        with cols[1]:
            st.header("Topic extraction by video segment")
            results = transcript["iab_categories_result"]["results"]
            for result in results:
                visualize_result(video_url, result)
