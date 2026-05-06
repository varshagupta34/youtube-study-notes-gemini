📚 YouTube Study Notes Generator (Gemini Pro + LangChain)
YouTube Study Notes Generator is a Streamlit web app that turns any YouTube video with English captions into clean, exam‑ready study notes in seconds. It pulls the video transcript, chunks it intelligently with LangChain, and uses Google’s Gemini Pro to generate structured summaries tailored to different use cases.

Paste a YouTube URL, pick your style, and the app gives you:

A comprehensive study guide with main topics, key concepts, details, and critical insights

A technical documentation view focused on methods, tools, and implementation details

An interview prep view with core ideas, likely questions, and quick reference notes

A short bullet‑point summary for quick revision

Behind the scenes, the app uses:

YouTube Transcript API to fetch and clean subtitles

LangChain text splitters to handle long transcripts without losing context

Gemini Pro for high‑quality, style‑aware summarization

Streamlit for a responsive, shareable front‑end

This project showcases end‑to‑end LLM application design: prompt‑engineering for multiple summary styles, an extensible summarization module, and a simple but production‑ready UI that can plug into other products or pipelines.

