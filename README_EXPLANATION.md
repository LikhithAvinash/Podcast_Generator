# Project Setup & How to Change Podcast Length

Hey there! Here is a simple explanation of what we did to keep the project running smoothly without hitting those annoying API limits, and how you can change the length of your podcast.

## 🛡️ Precautions Taken to Avoid API Limits

To make sure we don't use up all the free API credits or get blocked for asking too fast, we added a few safety nets:

1. **Short & Sweet Instructions:** We told the AI to keep everything extremely short. We limited the research to just 2 facts, the summary to 150 words, and the final script to just 6 lines of dialogue. Less words = fewer tokens used = less chance of hitting the limit.
2. **Word Count Caps (Token Limits):** We put a hard limit on how many "words" (tokens) the AI is allowed to spit out for each task (like 300, 400, or 500 max). This forces the AI to stop if it talks too much.
3. **Speed Limits (Max RPM):** We added a "speed limit" of 10 requests per minute. This stops the program from spamming the API all at once.
4. **Smart Retries:** Sometimes the API gets busy or briefly blocks us. We taught the program to recognize this, wait patiently for 30 to 60 seconds, and try again automatically instead of just crashing. 
5. **No Endless Loops:** We limited how many times the AI can try to rethink a problem (only 2 or 3 times per task). This stops it from getting stuck in an infinite loop and eating up your credits.

---

## 🎧 How to Adjust the Length of the Podcast

If you want the podcast to be longer (or shorter), it's actually really easy! You don't need to know how to code, you just need to change a few words in three simple text files. 

Here is exactly what you do:

**Step 1: Open `src/podcaster/config/tasks.yaml`**
Look for the `scripting_task` section at the bottom. You will see it says "exactly 6 lines of dialogue". 
* **Change it:** Just change the number `6` to whatever you want (like `10` or `20`).

**Step 2: Open `src/podcaster/config/agents.yaml`**
Look for the `scriptwriter` section at the bottom. You will see "6-dialogue podcast script" and "6 lines of dialogue".
* **Change it:** Update those numbers to match what you put in Step 1.

**Step 3: Open `src/podcaster/crew.py`**
Look for the `scriptwriter` section (around line 47). You'll see a line that says `max_tokens=500`. This is the maximum length the AI is allowed to write. 
* **Change it:** If you asked for a much longer script (like 20 lines), you need to give the AI more room to write so it doesn't get cut off. Try changing `500` to `1000` or `1500`.

Save those files, run your program again, and your podcast will be the new length!
