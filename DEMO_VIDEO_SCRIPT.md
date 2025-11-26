# 🎬 PR Review Agent - Demo Video Script

## 🎯 Video Overview
**Duration:** 3-5 minutes  
**Goal:** Showcase the PR Review Agent's capabilities and value proposition

---

## 📝 SCRIPT

### Scene 1: Introduction (30 seconds)

**[Screen: Show project title slide or IDE with project open]**

**Narration:**
> "Hi! Today I'm going to demonstrate the PR Review Agent - an AI-powered code review system built with LangChain and Groq AI. This tool uses 4 specialized AI agents to automatically review code changes and identify security vulnerabilities, performance issues, code quality problems, and logic errors."

**Show on screen:**
- Project title: "PR Review Agent"
- Tech stack: LangChain + Groq AI + FastAPI
- 4 AI Agents icons

---

### Scene 2: Architecture Overview (30 seconds)

**[Screen: Show the codebase structure or architecture diagram]**

**Narration:**
> "The system is built using LangChain for multi-agent orchestration, Groq's llama-3.3-70b-versatile model for fast and cost-effective AI analysis, and FastAPI for the backend. It features a user-friendly web interface and REST API."

**Highlight:**
- `app/agents/` - 4 specialized agents
- `app/main.py` - FastAPI backend
- `static/index.html` - Web interface
- `.env` - Groq API configuration

**Key Points to Mention:**
- ✅ Uses Groq (faster & cheaper than OpenAI)
- ✅ LangChain for agent orchestration
- ✅ Tracks token usage and costs
- ✅ Production-ready with error handling

---

### Scene 3: Starting the Application (20 seconds)

**[Screen: Terminal]**

**Actions:**
```powershell
# Show starting the server
python -m uvicorn app.main:app --reload --port 8000
```

**Narration:**
> "Let me start the application. You can see all 4 agents initializing with Groq - the Security Analyst, Performance Reviewer, Code Quality Inspector, and Logic Analyzer."

**Show in logs:**
```
Initializing Security Analyst with Groq (faster & cheaper!)
Initializing Performance Reviewer with Groq (faster & cheaper!)
Initializing Code Quality Inspector with Groq (faster & cheaper!)
Initializing Logic Analyzer with Groq (faster & cheaper!)
Application startup complete
```

---

### Scene 4: Web Interface Tour (30 seconds)

**[Screen: Browser at http://localhost:8000]**

**Narration:**
> "Here's the web interface. We have three main features: Review GitHub PR for analyzing pull requests directly from GitHub, Review Diff for analyzing code changes without GitHub, and View Agents to see all our AI reviewers."

**Actions:**
- Click through each tab to show them
- Highlight the clean, professional UI

---

### Scene 5: Demo - Review Diff Feature (90 seconds)

**[Screen: Review Diff tab]**

**Narration:**
> "Let's test the Review Diff feature with a code sample that has security vulnerabilities. I'll paste a login function that uses SQL string concatenation - a classic security risk."

**Actions:**
1. Click "Review Diff" tab
2. Paste this code:
```diff
diff --git a/auth.py b/auth.py
--- a/auth.py
+++ b/auth.py
@@ -1,5 +1,8 @@
 def login(username, password):
-    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
-    result = db.execute(query)
-    return result
+    # Using string concatenation for SQL query
+    user_data = database.query("SELECT * FROM users WHERE name=" + username)
+    if user_data and user_data['password'] == password:
+        session['user'] = username
+        return True
+    return False
```
3. Click "Analyze Diff"

**Narration while waiting:**
> "The system is now analyzing this code with all 4 AI agents. Each agent has a specific focus area and uses Groq's llama model to identify issues."

**When results appear:**
> "Excellent! The system found 15 issues - 4 critical, and 11 informational. Let's look at what each agent found:"

**Actions:**
- **Scroll through results** showing different colored severity badges
- **Click/highlight a Critical issue** from Security Analyst about SQL injection
- **Show a suggestion** with the fix recommendation

**Narration:**
> "The Security Analyst correctly identified the SQL injection vulnerability and suggested using parameterized queries. The Performance Reviewer flagged efficiency concerns, the Code Quality Inspector noted missing error handling, and the Logic Analyzer found edge case issues. Each review includes the severity level, detailed description, and specific fix recommendations."

---

### Scene 6: Demo - GitHub PR Review (60 seconds)

**[Screen: Review GitHub PR tab]**

**Narration:**
> "Now let's try the GitHub PR review feature. I'll review a real pull request from GitHub."

**Actions:**
1. Click "Review GitHub PR" tab
2. Enter:
   - Repository Owner: `octocat`
   - Repository Name: `Hello-World`
   - PR Number: `1`
3. Click "Analyze Pull Request"

**Narration:**
> "The system is fetching the PR from GitHub, analyzing the changes, and generating reviews from all 4 agents."

**When results appear:**
> "Great! The review completed successfully. It analyzed 1 file and found multiple issues across different categories. This works with any public GitHub repository, or private ones if you provide a GitHub token."

**Show:**
- Summary statistics
- A few review comments
- Different severity levels

---

### Scene 7: View Agents (20 seconds)

**[Screen: View Agents tab]**

**Narration:**
> "In the Agents tab, we can see all 4 specialized reviewers and their focus areas. Each agent is an expert in its domain, providing comprehensive code analysis."

**Show:**
- All 4 agent cards
- Their descriptions

---

### Scene 8: Technical Highlights (30 seconds)

**[Screen: Show code or terminal with logs]**

**Narration:**
> "Some technical highlights: The system uses LangChain for agent orchestration, tracks token usage and costs for each review, implements rate limiting for production use, and handles errors gracefully. All reviews are powered by Groq's llama-3.3-70b-versatile model, which provides fast responses at low cost."

**Show on screen:**
- Logs showing token counts
- Cost tracking ($0.0000 for demonstration)
- Fast response times (8-10 seconds)

---

### Scene 9: API Documentation (20 seconds)

**[Screen: http://localhost:8000/docs]**

**Narration:**
> "The system also provides a full REST API with automatic Swagger documentation. Developers can integrate this into CI/CD pipelines, GitHub Actions, or any automated workflow."

**Show:**
- FastAPI Swagger UI
- Available endpoints
- Try out the `/health` endpoint

---

### Scene 10: Conclusion & Use Cases (30 seconds)

**[Screen: Summary slide or back to web interface]**

**Narration:**
> "This PR Review Agent is perfect for:
> - **Teams** wanting automated code reviews
> - **CI/CD pipelines** for quality gates
> - **Open source maintainers** reviewing contributions
> - **Developers** learning best practices from AI feedback
>
> The system is production-ready, fully configurable, and can be deployed to any cloud platform. All code is available, and it's ready to use!"

**Show on screen:**
- ✅ 4 Specialized AI Agents
- ✅ Security, Performance, Quality, Logic Analysis
- ✅ GitHub Integration
- ✅ Fast & Cost-Effective (Groq)
- ✅ Production-Ready
- ✅ REST API

**End screen:**
> "Thank you for watching! Questions? Check the documentation or try it yourself!"

---

## 🎥 FILMING TIPS

### Preparation:
1. **Clean up desktop** - close unnecessary windows
2. **Increase font size** in terminal and browser (125-150%)
3. **Use a good microphone** - clear audio is critical
4. **Record in 1080p** minimum
5. **Test run** everything before recording

### During Recording:
1. **Speak clearly and not too fast**
2. **Pause between sections** (easier to edit)
3. **Show, don't just tell** - click through features
4. **Keep cursor movements smooth**
5. **Zoom in on important text** when needed

### Editing:
1. **Add text overlays** for key points
2. **Use transitions** between scenes
3. **Add background music** (low volume)
4. **Include captions** for accessibility
5. **Export in MP4** format (H.264)

---

## 🎨 VISUAL ELEMENTS TO INCLUDE

### Graphics/Overlays:
- Title slide with project name
- Tech stack icons (LangChain, Groq, FastAPI, Python)
- Agent icons/avatars for 4 agents
- Arrows/highlights pointing to important UI elements
- "Loading..." animation during AI analysis
- Checkmarks ✅ for successful operations

### Screen Recordings:
- Terminal showing server startup
- Browser with web interface
- Code editor showing project structure
- API documentation
- Test results

### B-Roll (Optional):
- GitHub logo when discussing PR review
- Code snippets scrolling
- Architecture diagrams

---

## 📊 METRICS TO HIGHLIGHT

During the demo, emphasize:
- ⚡ **Speed**: "Analysis completes in 10-15 seconds"
- 💰 **Cost**: "Uses Groq - much cheaper than OpenAI"
- 🎯 **Accuracy**: "Found 15 issues including critical SQL injection"
- 🔄 **Scalability**: "Handles PRs of any size"
- 🛡️ **Coverage**: "4 specialized agents for comprehensive review"

---

## 🎬 POST-PRODUCTION CHECKLIST

- [ ] Trim dead air and long pauses
- [ ] Add intro/outro slides
- [ ] Include background music
- [ ] Add captions/subtitles
- [ ] Color grade for consistency
- [ ] Add text overlays for key points
- [ ] Include call-to-action at end
- [ ] Export in multiple formats (YouTube, MP4, etc.)
- [ ] Create thumbnail image
- [ ] Write video description with links

---

## 📤 PUBLISHING

### YouTube Description Template:
```
🤖 PR Review Agent - AI-Powered Code Review System

Automated code review using 4 specialized AI agents powered by LangChain and Groq AI.

✨ Features:
• Security vulnerability detection
• Performance optimization suggestions
• Code quality analysis
• Logic error identification
• GitHub PR integration
• Fast & cost-effective (Groq AI)

🛠️ Tech Stack:
• LangChain for agent orchestration
• Groq AI (llama-3.3-70b-versatile)
• FastAPI backend
• Python 3.10+

📊 Demo Includes:
✅ Live code review demonstration
✅ GitHub PR analysis
✅ Real-time issue detection
✅ API documentation

🔗 Links:
• GitHub Repository: [Your Link]
• Documentation: [Your Link]
• Groq AI: https://groq.com

⏱️ Timestamps:
0:00 - Introduction
0:30 - Architecture Overview
1:00 - Starting the Application
1:30 - Review Diff Demo
3:00 - GitHub PR Review
4:00 - Technical Highlights
4:30 - Conclusion

#AI #CodeReview #LangChain #Groq #Python #FastAPI #MachineLearning
```

---

## ✅ FINAL CHECKLIST

Before recording:
- [ ] Server starts without errors
- [ ] All 4 agents initialize correctly
- [ ] Web interface loads properly
- [ ] Review Diff returns results
- [ ] GitHub PR review works
- [ ] Test code samples ready
- [ ] GitHub token configured (if using PR feature)
- [ ] Font sizes increased for readability
- [ ] Desktop cleaned up
- [ ] Recording software tested

**You're ready to create an amazing demo video! 🎉**
