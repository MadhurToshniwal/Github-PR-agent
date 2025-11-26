# 🚀 Quick Start Guide - PR Review Agent

## ⚡ For Demo Video Recording

### 1. Start the Server (30 seconds)

```powershell
# Open PowerShell in D:\lyzr
cd D:\lyzr

# Start server
python -m uvicorn app.main:app --reload --port 8000
```

**Wait for this output:**
```
✅ Initializing Security Analyst with Groq (faster & cheaper!)
✅ Initializing Performance Reviewer with Groq (faster & cheaper!)
✅ Initializing Code Quality Inspector with Groq (faster & cheaper!)
✅ Initializing Logic Analyzer with Groq (faster & cheaper!)
✅ Application startup complete
```

### 2. Open Web Interface

```powershell
# Open browser
start http://localhost:8000
```

### 3. Test Review Diff (Use This Code)

**Click "Review Diff" tab, paste this:**

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

**Click "Analyze Diff"**

**Expected Results (10-15 seconds):**
- ✅ Total Issues: 15-20
- ✅ Critical: 4
- ✅ High: 0-1
- ✅ Medium: 0
- ✅ Low: 0-1
- ✅ Info: 10-11

### 4. Test GitHub PR Review

**Click "Review GitHub PR" tab, enter:**
- Repository Owner: `octocat`
- Repository Name: `Hello-World`
- Pull Request Number: `1`
- GitHub Token: (leave empty or use yours)

**Click "Analyze Pull Request"**

**Expected Results (10-15 seconds):**
- ✅ PR Title shown
- ✅ Files Changed: 1
- ✅ Issues found: 10-15
- ✅ Reviews from all 4 agents

### 5. View Agents

**Click "View Agents" tab**

**You'll see:**
- 🔒 Security Analyst
- ⚡ Performance Reviewer
- ✅ Code Quality Inspector
- 🧠 Logic Analyzer

---

## 🎬 Recording Tips

### Before Recording:
1. Close all unnecessary windows
2. Increase browser zoom to 125%
3. Increase terminal font size
4. Clear browser cache
5. Test run once

### During Recording:
1. Speak clearly
2. Wait for animations to complete
3. Highlight important numbers/results
4. Show the different severity badges (colors)
5. Scroll through some review comments

### After Recording:
1. Add text overlays for key points
2. Include captions
3. Add music (low volume)
4. Create thumbnail

---

## 📊 What to Highlight

### In Demo:
✨ **Speed:** "Results in 10-15 seconds!"  
💰 **Cost:** "Using Groq - faster & cheaper than OpenAI"  
🎯 **Accuracy:** "Found critical SQL injection vulnerability"  
🤖 **Intelligence:** "4 specialized AI agents working together"  
⚡ **Technology:** "LangChain + Groq AI"  

---

## 🎯 Key Talking Points

1. **Multi-Agent System**
   - Not just one AI, but 4 specialized agents
   - Each focuses on different aspects
   - Security, Performance, Quality, Logic

2. **Production Ready**
   - Error handling
   - Rate limiting
   - Scalable architecture
   - REST API

3. **Cost Effective**
   - Uses Groq instead of OpenAI
   - Faster inference
   - Lower costs
   - Token tracking built-in

4. **Easy Integration**
   - GitHub PR reviews
   - Direct diff analysis
   - REST API for CI/CD
   - Webhook support ready

---

## ✅ Final Checklist Before Demo

- [ ] Server starts without errors
- [ ] All 4 agents initialize
- [ ] Web UI loads at localhost:8000
- [ ] Review Diff returns results with Critical issues
- [ ] GitHub PR review works (optional, needs token)
- [ ] View Agents shows all 4
- [ ] Desktop is clean
- [ ] Browser zoom is 125%
- [ ] Terminal font is large enough
- [ ] Microphone tested
- [ ] Recording software ready

---

## 🆘 Quick Troubleshooting

**Server won't start?**
```powershell
Get-Process -Name python | Stop-Process -Force
python -m uvicorn app.main:app --reload --port 8000
```

**No results in review?**
- Check .env has `DEFAULT_LLM_MODEL=llama-3.3-70b-versatile`
- Check GROQ_API_KEY is valid

**GitHub PR fails?**
- Normal if no token provided
- Skip this demo part or add token

---

## 🎉 YOU'RE READY!

Everything is tested and working perfectly.  
Just follow the DEMO_VIDEO_SCRIPT.md for the complete narration.

**Good luck with your demo! 🚀**
