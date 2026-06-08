# 🎙️ Podcaster Crew

Welcome to the **Podcaster Crew**, an AI-powered multi-agent system built with [crewAI](https://crewai.com) and Gemini. This project automatically researches a topic, summarizes it, writes a short podcast script, and generates a final audio podcast using Google's Gemini Voice API.

https://github.com/LikhithAvinash/Podcast_Generator/assets/your-asset-id/podcast_gen.mp4

## ✨ Features
- **Multi-Agent Collaboration**: Uses dedicated agents for Research, Reporting, and Scriptwriting.
- **Text-to-Speech Pipeline**: Automatically converts the generated script into an audio file.
- **Free-Tier Optimized**: Carefully configured to stay within API free-tier limits, complete with auto-retry logic for transient errors.

---

## 🚀 Installation & Setup

1. **Install UV** (our package manager):
   ```bash
   pip install uv
   ```

2. **Install Dependencies**:
   Navigate to the project root and run:
   ```bash
   uv sync
   # OR
   crewai install
   ```

3. **Environment Setup**:
   Create a `.env` file in the project root and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   MODEL=gemini/gemini-1.5-flash
   ```
   *(Get your free API key at [Google AI Studio](https://aistudio.google.com/apikey))*

---

## 🏃‍♂️ Running the Project

To start the crew and generate your podcast, run:

```bash
uv run crewai run
```

When it finishes, your research report and podcast script will be saved in the `outputs/` folder, and the generated `.mp3` / `.wav` audio file will be placed wherever the TTS tool exports it.

To change the podcast **topic**, open `src/podcaster/main.py` and change the `TOPIC` variable at the top of the file!

---

## 🎧 How to Adjust the Length of the Podcast

By default, the script is set to exactly 6 lines of dialogue to save API tokens. To make the podcast longer or shorter, simply update these three files:

1. **`src/podcaster/config/tasks.yaml`**: Look for the `scripting_task` section at the bottom. Change `"exactly 6 lines of dialogue"` to your desired length (e.g., 10 or 15).
2. **`src/podcaster/config/agents.yaml`**: Look for the `scriptwriter` section at the bottom. Change the mentions of `"6-dialogue podcast script"` to match your new length.
3. **`src/podcaster/crew.py`**: Find the `scriptwriter` agent configuration (around line 47). You will see `max_tokens=500`. Increase this number (e.g., `1000` or `1500`) to give the AI more room to write so the longer script doesn't get cut off.

---

## 🛡️ Free-Tier API Precautions

If you are using a free API key, you might normally hit rate limits (Error 429) very quickly. We built several safety nets into this project to prevent that:

1. **Strict Token Caps:** We enforce a hard limit on how many words the AI can output per task using `max_tokens`.
2. **Short & Concise Instructions:** Prompts are engineered to ask for brief summaries (e.g., 2 bullet points, 150 words) to minimize generation costs.
3. **Speed Limits (Max RPM):** The crew operates with `max_rpm=10` to stop the program from spamming the API all at once.
4. **Smart Auto-Retries:** Powered by LiteLLM, if the API gets busy or briefly blocks the request, the program recognizes the transient error and patiently waits 30-60 seconds before automatically retrying. It will try up to 5 times instead of crashing.
5. **Limited Iterations:** Agents are capped at 2-3 `max_iter` limit to prevent them from getting stuck in an expensive infinite loop.

---

## 🛠️ Customization
- Modify `src/podcaster/config/agents.yaml` to change agent personas.
- Modify `src/podcaster/config/tasks.yaml` to change what the agents are supposed to do.
- Modify `src/podcaster/crew.py` to add new tools or change API settings.
