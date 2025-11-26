# 🐙 Real GitHub PRs for Testing

## Use these REAL GitHub Pull Requests to test the GitHub PR Review feature

---

## 🎯 **RECOMMENDED TEST PRs (Small & Safe)**

### **1. octocat/Hello-World PR #1** ⭐ (BEST FOR DEMO)

**Repository Owner:** `octocat`  
**Repository Name:** `Hello-World`  
**Pull Request Number:** `1`  
**GitHub Token:** Leave empty (public repo)

**What it is:**
- Simple README change
- Small, quick to analyze
- Always available (GitHub's test repo)

**Expected Results:**
- Files Changed: 1
- Total Issues: 10-15
- All 4 agents will review
- Analysis time: 10-15 seconds

**Why use this:**
- ✅ Always works (it's GitHub's official test repo)
- ✅ Fast analysis
- ✅ No token needed
- ✅ Safe for demo

---

### **2. facebook/react (Real React PR)** ⭐

**Repository Owner:** `facebook`  
**Repository Name:** `react`  
**Pull Request Number:** `28495`  
**GitHub Token:** Leave empty (public repo)

**What it is:**
- Real production React code changes
- Multiple file modifications
- Professional code review scenario

**Expected Results:**
- Files Changed: Multiple
- Total Issues: Varies (15-30+)
- Shows how agents analyze React/JavaScript
- Analysis time: 20-40 seconds

**Why use this:**
- ✅ Real production code from Facebook
- ✅ Shows multi-file PR analysis
- ✅ Demonstrates React/JavaScript review capabilities
- ✅ Great for showing different agent insights
- ✅ No token required

---

### **3. tensorflow/tensorflow (Small Documentation PR)**

**Repository Owner:** `tensorflow`  
**Repository Name:** `tensorflow`  
**Pull Request Number:** Find a recent closed PR with 1-2 files (check GitHub)  
**GitHub Token:** Leave empty or use yours

**What it is:**
- Real open source project
- Shows working with large projects
- Usually documentation or small fixes

**Expected Results:**
- Varies by PR
- Shows real-world usage

**Why use this:**
- ✅ Famous project
- ✅ Shows real-world capability
- ✅ Impressive for demo

---

### **3. microsoft/vscode (Recent Small PR)**

**Repository Owner:** `microsoft`  
**Repository Name:** `vscode`  
**Pull Request Number:** Check recent PRs (look for small ones)  
**GitHub Token:** Recommended

**What it is:**
- Real VS Code repository
- Professional codebase
- Real code reviews

**Expected Results:**
- Professional code
- May find real issues or confirm code quality

**Why use this:**
- ✅ Well-known project
- ✅ Shows working with production code
- ✅ Impressive for recruiters

---

## 🔍 **HOW TO FIND GOOD TEST PRs:**

### **Method 1: Use Small PRs from Popular Repos**

Visit GitHub and search for:
- Repos with lots of stars
- Look for "closed" PRs
- Filter by "1 file changed"
- Pick recent ones

**Good repositories:**
- `facebook/react`
- `nodejs/node`
- `python/cpython`
- `rust-lang/rust`

### **Method 2: Use Your Own Repos**

If you have PRs in your own repositories:
- Use your own repo owner name
- Use your repo name
- Use any PR number
- Add your GitHub token

---

## ⚠️ **IMPORTANT NOTES:**

### **About GitHub Tokens:**

**When you DON'T need a token:**
- ✅ Public repositories
- ✅ Small PRs
- ✅ Not rate-limited

**When you NEED a token:**
- ❌ Private repositories
- ❌ If you hit rate limits (after many requests)
- ❌ Large organizations

### **How to get a GitHub Token:**

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name: "PR Review Agent"
4. Select scopes:
   - `repo` (for private repos)
   - OR just `public_repo` (for public only)
5. Generate and copy the token
6. Paste it in the "GitHub Token" field

---

## 🎬 **FOR YOUR DEMO VIDEO:**

### **Recommended Approach:**

**Option A: Safe & Simple (No Token)**
```
Repository Owner: octocat
Repository Name: Hello-World
PR Number: 1
GitHub Token: (leave empty)
```

**Why:** Always works, no setup needed, perfect for demo

---

**Option B: Impressive (With Token)**
```
Repository Owner: tensorflow
Repository Name: tensorflow
PR Number: (recent closed PR)
GitHub Token: (your token)
```

**Why:** Shows working with real open source projects

---

## 🎯 **WHAT TO SAY IN DEMO:**

### **When testing GitHub PR feature:**

**Before clicking Analyze:**
> "The system can also review GitHub pull requests directly. Let me test it with a real PR from GitHub's test repository."

**While it's analyzing:**
> "It's fetching the PR from GitHub, analyzing all the changed files, and running all 4 AI agents..."

**When results appear:**
> "Great! It successfully analyzed the PR, reviewed all files, and provided feedback from all 4 specialized agents. This is perfect for code review automation in teams or open source projects."

---

## 💡 **PRO TIPS:**

### **For Demo Success:**

1. **Test beforehand** - Make sure the PR still exists
2. **Use small PRs** - Faster analysis
3. **Have backup** - Keep octocat/Hello-World as fallback
4. **If it fails** - Don't panic, just mention "This needs a GitHub token" and move on

### **If You Get Errors:**

**Error: "Bad credentials"**
- Solution: Add your GitHub token OR use octocat/Hello-World

**Error: "Not Found"**
- Solution: Check the repo owner/name spelling
- Solution: Try a different PR number

**Error: "Rate limit"**
- Solution: Add GitHub token to get higher limits

---

## ✅ **TESTING CHECKLIST:**

Before your demo:

- [ ] Test with octocat/Hello-World PR #1
- [ ] Verify it returns results in 10-15 seconds
- [ ] Check that all 4 agents provide feedback
- [ ] (Optional) Get GitHub token if you want to test private repos
- [ ] (Optional) Test with another repo to have variety

---

## 🚀 **QUICK TEST NOW:**

**Go to your browser:** http://127.0.0.1:8000

**Click:** "Review GitHub PR"

**Enter:**
```
Repository Owner: octocat
Repository Name: Hello-World
Pull Request Number: 1
```

**Click:** "Analyze Pull Request"

**Wait 10-15 seconds**

**You should see:** ✅ PR Title, Files Changed, Issues Found, Reviews from all 4 agents

---

**This feature shows your app can integrate with real GitHub workflows!** 🎉
