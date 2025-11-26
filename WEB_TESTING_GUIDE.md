# 🎯 Web Interface Testing Guide

## ✅ Your Setup is Ready!
- Groq API Key: Added ✅
- Server: Running at http://127.0.0.1:8000 ✅
- All 4 Agents: Initialized with Groq ✅

---

## 🖥️ How to Test with Web Interface

### Step 1: Open the Web UI
Visit: **http://127.0.0.1:8000**

You'll see a beautiful interface with 3 tabs:
1. **Review Pull Request** - For GitHub PRs
2. **Review Code Diff** - For direct code review ⭐ START HERE!
3. **Agents Info** - See your 4 agents

---

## 🧪 Test Case 1: Security Vulnerability (SQL Injection)

### Click "Review Code Diff" Tab

**File Path:** 
```
app/database.py
```

**Code Diff:** (Copy and paste this exactly)
```
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id={user_id}"
    return database.execute(query)

def delete_user(user_id):
    query = f"DELETE FROM users WHERE id={user_id}"
    return database.execute(query)
```

**Language:**
```
python
```

**Click "Review Code"** → Wait 2-3 seconds ⚡

### Expected Result:
🔒 **Security Agent** will flag:
- Critical: SQL Injection vulnerability
- Suggestion: Use parameterized queries

---

## 🧪 Test Case 2: Performance Issue

**File Path:**
```
app/utils.py
```

**Code Diff:**
```
def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            if items[i] == items[j]:
                duplicates.append(items[i])
    return duplicates
```

**Language:**
```
python
```

**Click "Review Code"**

### Expected Result:
⚡ **Performance Agent** will flag:
- High: O(n²) algorithm
- Suggestion: Use set for O(n) complexity

---

## 🧪 Test Case 3: Code Quality Improvement

**File Path:**
```
app/handlers.py
```

**Code Diff:**
```
def process_request(request):
    if request.method == 'GET' or request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':
        result = handle(request)
        if result != None:
            if result.status == 200:
                return result
    return None
```

**Language:**
```
python
```

**Click "Review Code"**

### Expected Result:
✨ **Quality Agent** will flag:
- Medium: Use `in` operator instead of chained `or`
- Medium: Use `if result is not None`
- Low: Improve readability with early returns

---

## 🧪 Test Case 4: Logic Error

**File Path:**
```
app/validation.py
```

**Code Diff:**
```
def calculate_discount(price, discount_percent):
    discount = price * discount_percent / 100
    final_price = price - discount
    return final_price

def apply_bulk_discount(items):
    total = 0
    for item in items:
        total += item.price
    if len(items) > 10:
        total = total * 0.9
    return total
```

**Language:**
```
python
```

**Click "Review Code"**

### Expected Result:
🧠 **Logic Agent** will flag:
- Medium: No validation for discount_percent (could be >100 or <0)
- Medium: No validation for negative prices
- Low: Consider bulk discount threshold as config

---

## 🎨 What You'll See

### Review Results Display:
```
┌─────────────────────────────────────┐
│  🔒 Security Analyst                │
│  Severity: CRITICAL                  │
│  Line: 2                             │
│  Issue: SQL Injection vulnerability  │
│  Suggestion: Use parameterized...    │
│  Confidence: 95%                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  ⚡ Performance Reviewer             │
│  Severity: HIGH                      │
│  ...                                 │
└─────────────────────────────────────┘
```

---

## 🎯 Quick Tips

### ✅ DO:
- Use simple, complete code snippets
- Include full function bodies
- Use realistic variable names
- Test one issue at a time first

### ❌ DON'T:
- Don't use git diff format with `@@` markers (just paste code)
- Don't worry about line numbers
- Don't mix multiple languages

---

## 🚀 Testing Different Languages

### JavaScript Example:
**File Path:** `api/routes.js`
**Language:** `javascript`
**Code:**
```javascript
app.get('/user/:id', (req, res) => {
    const query = `SELECT * FROM users WHERE id=${req.params.id}`;
    db.query(query, (err, result) => {
        res.send(result);
    });
});
```

### Java Example:
**File Path:** `UserController.java`
**Language:** `java`
**Code:**
```java
public User getUser(String userId) {
    String query = "SELECT * FROM users WHERE id=" + userId;
    return database.executeQuery(query);
}
```

### Go Example:
**File Path:** `handler.go`
**Language:** `go`
**Code:**
```go
func GetUser(userId string) (*User, error) {
    query := fmt.Sprintf("SELECT * FROM users WHERE id=%s", userId)
    return db.Query(query)
}
```

---

## 📊 Understanding the Results

### Severity Levels:
- 🔴 **Critical**: Security issues, data loss risks
- 🟠 **High**: Performance issues, major bugs
- 🟡 **Medium**: Code quality, maintainability
- 🟢 **Low**: Minor improvements, style

### Confidence Scores:
- **90-100%**: Very confident
- **70-89%**: Likely correct
- **50-69%**: Suggestion, review carefully
- **<50%**: Low confidence, validate

---

## 🎮 Interactive Features

### In the Web UI:
1. **Color-coded cards** for each agent
2. **Severity badges** (Critical/High/Medium/Low)
3. **Line numbers** for precise location
4. **Specific suggestions** for fixes
5. **Confidence scores** for transparency

---

## 🐛 If Something Goes Wrong

### "No reviews found"
→ Make sure code has actual issues
→ Try a test case from above

### "Error reviewing"
→ Check the code is valid syntax
→ Make sure language is correct
→ Try simpler code first

### Server not responding
→ Check terminal - look for errors
→ Groq API key should be valid
→ Server should show "Application startup complete"

---

## 🎯 Best Practices for Testing

### Start Simple:
1. Test with SQL injection example first
2. See all 4 agents respond
3. Try other test cases
4. Then try your own code

### For Demos:
1. Use the SQL injection case (most impressive!)
2. Show the performance O(n²) case
3. Highlight real-time responses (Groq is FAST!)
4. Show all 4 agents working together

---

## 🌟 Advanced: Review a GitHub PR

### If you have a GitHub token:

1. Click **"Review Pull Request"** tab
2. Fill in:
   - **Repository:** `octocat/Hello-World`
   - **PR Number:** `1`
3. Click **"Review PR"**

This will fetch the actual PR from GitHub and review all changed files!

---

## 📸 What Success Looks Like

After clicking "Review Code", you should see:

✅ Loading indicator appears
✅ 2-3 seconds later (Groq is FAST!)
✅ 4 colored cards appear (one per agent)
✅ Each shows severity, line number, issue, suggestion
✅ Summary at top shows total issues found

---

## 🚀 Ready to Test!

1. **Open:** http://127.0.0.1:8000
2. **Click:** "Review Code Diff" tab
3. **Copy:** SQL injection test case from above
4. **Paste:** Into the form
5. **Click:** "Review Code"
6. **Watch:** The magic happen! ✨

The agents analyze in parallel and return in ~2 seconds thanks to Groq!

---

**Your app is ready! Start with the SQL injection test case for the best demo!** 🎉
