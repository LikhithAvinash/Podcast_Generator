import os
import time
import logging
from crewai.tools import BaseTool, tool
from typing import Type
from pydantic import BaseModel, Field
from crewai_tools import FileWriterTool, FileReadTool
from google import genai
from google.genai import types
import wave
import datetime
import base64

logger = logging.getLogger(__name__)

def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)
    

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."

file_writer_tool = FileWriterTool()

# result_1 = file_writer_tool._run('example.txt', 'This is a test content.', 'knowledge/')


file_read_tool = FileReadTool()

# result_2 = FileReadTool(file_path='knowledge/')


@tool
def web_search_tool(query: str) -> str:
    """
    Search the web using DuckDuckGo and return the top results.
    Use this tool to find the latest news, facts, and information on any topic.
    """
    from ddgs import DDGS
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        if not results:
            return "No results found."
        output = []
        for r in results:
            output.append(f"- **{r.get('title', '')}**: {r.get('body', '')} ({r.get('href', '')})")
        return "\n".join(output)
    except Exception as e:
        return f"Search error: {e}"


def _call_gemini_with_retry(client, model, contents, config, max_retries=4, initial_wait=30):
    """
    Calls the Gemini API with exponential backoff on transient errors.
    Handles: 429 rate-limit, 503 high-demand, and unavailable errors.
    Waits 30s -> 60s -> 120s -> 240s between retries.
    """
    for attempt in range(max_retries + 1):
        try:
            return client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )
        except Exception as e:
            error_str = str(e).lower()
            is_transient = (
                "429" in error_str
                or "503" in error_str
                or "resource_exhausted" in error_str
                or "quota" in error_str
                or "rate" in error_str
                or "high demand" in error_str
                or "unavailable" in error_str
            )
            if is_transient and attempt < max_retries:
                wait_time = initial_wait * (2 ** attempt)  # 30, 60, 120, 240 seconds
                print(
                    f"⏳ API error (attempt {attempt + 1}/{max_retries + 1}). "
                    f"Waiting {wait_time}s before retry..."
                )
                time.sleep(wait_time)
            else:
                raise


@tool
def gemini_voice_tool(script: str) -> str:
    """
    Use this tool to generate a voice for the text.
    """
    client = genai.Client(api_key=(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")))
    
    response = _call_gemini_with_retry(
        client=client,
        model="gemini-2.5-flash-preview-tts",
        contents=script,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            temperature=0.5,
            speech_config=types.SpeechConfig(
                multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                    speaker_voice_configs=[
                    types.SpeakerVoiceConfig(
                        speaker='Joe',
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name='Kore',
                            )
                        )
                    ),
                    types.SpeakerVoiceConfig(
                        speaker='Jane',
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name='Puck',
                            )
                        )
                    ),
                    ]
                )
            )
        ),
    )
    
    parts = getattr(response.candidates[0].content, 'parts', [])
    inline = None
    for p in parts:
        maybe_inline = getattr(p, 'inline_data', None)
        if maybe_inline is not None and getattr(maybe_inline, 'data', None):
            inline = maybe_inline
            break

    if inline is None or getattr(inline, 'data', None) is None:
        raise ValueError("Gemini did not return inline audio data.")

    audio_bytes = inline.data
    if isinstance(audio_bytes, str):
        audio_bytes = base64.b64decode(audio_bytes)
    else:
        audio_bytes = bytes(audio_bytes)

    if not audio_bytes:
        raise ValueError("Gemini returned empty audio data.")

    # Ensure output directory exists and create a unique filename
    output_dir = os.path.join(os.getcwd(), "outputs")
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(output_dir, f"podcast-{timestamp}.wav")
    wave_file(filename, audio_bytes)
    return filename
