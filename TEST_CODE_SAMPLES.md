# 🧪 Test Code Samples for PR Review Agent

## Use these different code samples to test and demonstrate various issue types

---

## 📝 **SAMPLE 1: SQL Injection (Security - CRITICAL)**

**Best for:** Showing security vulnerability detection

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

**Expected Results:**
- Critical: 4 (SQL Injection vulnerability)
- Security Analyst will flag dangerous string concatenation in SQL

---

## 📝 **SAMPLE 2: XSS Vulnerability (Security - HIGH)**

**Best for:** Showing web security issues

```diff
diff --git a/web.py b/web.py
--- a/web.py
+++ b/web.py
@@ -1,6 +1,10 @@
 def render_comment(comment):
-    return f"<div>{comment}</div>"
+    # Display user comment directly
+    user_input = request.form.get('comment')
+    html = "<div class='comment'>" + user_input + "</div>"
+    return html
 
 def display_user_profile(username):
-    return render_template('profile.html', name=username)
+    profile_html = f"<h1>Welcome {username}!</h1>"
+    return profile_html
```

**Expected Results:**
- Critical: 2-3 (XSS vulnerability)
- Security Analyst will detect unescaped user input in HTML

---

## 📝 **SAMPLE 3: Performance Issues (Performance - MEDIUM)**

**Best for:** Showing performance optimization suggestions

```diff
diff --git a/data_processor.py b/data_processor.py
--- a/data_processor.py
+++ b/data_processor.py
@@ -1,8 +1,15 @@
 def process_users(user_ids):
-    return [get_user(id) for id in user_ids]
+    results = []
+    for user_id in user_ids:
+        user = db.query(f"SELECT * FROM users WHERE id={user_id}")
+        results.append(user)
+    return results
 
 def find_duplicates(items):
-    return list(set(items))
+    duplicates = []
+    for i in range(len(items)):
+        for j in range(i+1, len(items)):
+            if items[i] == items[j] and items[i] not in duplicates:
+                duplicates.append(items[i])
+    return duplicates
```

**Expected Results:**
- High: 2-3 (N+1 query problem, O(n²) algorithm)
- Performance Reviewer will suggest batch queries and better algorithms

---

## 📝 **SAMPLE 4: Code Quality Issues (Quality - MEDIUM)**

**Best for:** Showing code smell detection

```diff
diff --git a/utils.py b/utils.py
--- a/utils.py
+++ b/utils.py
@@ -1,10 +1,20 @@
-def calculate_total(items):
-    return sum(item.price for item in items)
+def calc(x):
+    t = 0
+    for i in x:
+        if i.p:
+            t = t + i.p
+        else:
+            t = t + 0
+    return t
 
-def validate_email(email):
-    return '@' in email and '.' in email
+def check(e):
+    if '@' in e:
+        if '.' in e:
+            return True
+        else:
+            return False
+    else:
+        return False
```

**Expected Results:**
- Medium: 5-8 (poor naming, nested if, unnecessary else)
- Code Quality Inspector will suggest better practices

---

## 📝 **SAMPLE 5: Logic Errors (Logic - HIGH)**

**Best for:** Showing bug detection

```diff
diff --git a/calculator.py b/calculator.py
--- a/calculator.py
+++ b/calculator.py
@@ -1,12 +1,18 @@
 def divide_numbers(a, b):
-    return a / b
+    result = a / b
+    return result
 
 def get_discount(price, percentage):
-    return price * (percentage / 100)
+    discount = price * percentage / 100
+    new_price = price - discount
+    return new_price
 
 def is_adult(age):
-    return age >= 18
+    if age >= 18:
+        return True
+    
+def check_password_strength(password):
+    return len(password) > 8
```

**Expected Results:**
- High: 3-4 (division by zero, missing return, weak validation)
- Logic Analyzer will find edge cases and bugs

---

## 📝 **SAMPLE 6: Missing Error Handling (Quality - MEDIUM)**

**Best for:** Showing robustness issues

```diff
diff --git a/file_handler.py b/file_handler.py
--- a/file_handler.py
+++ b/file_handler.py
@@ -1,8 +1,12 @@
 def read_config(filename):
-    with open(filename) as f:
-        return json.load(f)
+    f = open(filename)
+    data = json.load(f)
+    return data
 
 def save_data(data, filename):
-    with open(filename, 'w') as f:
-        json.dump(data, f)
+    file = open(filename, 'w')
+    json.dump(data, file)
+    
+def parse_number(text):
+    return int(text)
```

**Expected Results:**
- Medium: 4-6 (no error handling, resource leaks)
- All agents will flag missing try-except and resource management

---

## 📝 **SAMPLE 7: Hardcoded Credentials (Security - CRITICAL)**

**Best for:** Showing credential exposure

```diff
diff --git a/config.py b/config.py
--- a/config.py
+++ b/config.py
@@ -1,5 +1,10 @@
-DATABASE_URL = os.getenv('DATABASE_URL')
-API_KEY = os.getenv('API_KEY')
+# Database configuration
+DATABASE_URL = "postgresql://admin:password123@localhost/mydb"
+API_KEY = "sk-1234567890abcdef"
+AWS_SECRET = "AKIAIOSFODNN7EXAMPLE"
 
 def connect_db():
-    return psycopg2.connect(DATABASE_URL)
+    connection = psycopg2.connect(
+        host="localhost",
+        user="admin",
+        password="admin123"
+    )
+    return connection
```

**Expected Results:**
- Critical: 5-6 (hardcoded passwords, API keys)
- Security Analyst will strongly flag credential exposure

---

## 📝 **SAMPLE 8: Race Condition (Logic - HIGH)**

**Best for:** Showing concurrency issues

```diff
diff --git a/counter.py b/counter.py
--- a/counter.py
+++ b/counter.py
@@ -1,8 +1,15 @@
+counter = 0
+
 def increment_counter():
-    with lock:
-        counter += 1
+    global counter
+    temp = counter
+    temp = temp + 1
+    counter = temp
 
 def get_balance(account_id):
-    return accounts[account_id]
+    balance = accounts[account_id]
+    time.sleep(0.1)  # Simulate processing
+    return balance
```

**Expected Results:**
- High: 3-4 (race condition, non-atomic operations)
- Logic Analyzer will detect concurrency problems

---

## 🎬 **HOW TO USE THESE SAMPLES IN DEMO:**

### **For Quick Demo (Use Sample 1):**
- Shows CRITICAL security issue (SQL injection)
- Most impressive for demo
- Clear, understandable vulnerability

### **For Comprehensive Demo (Use Samples 1, 3, 5):**
1. **Sample 1** - Security (SQL Injection)
2. **Sample 3** - Performance (N+1 queries)
3. **Sample 5** - Logic (Division by zero)

Shows all different agent types working!

### **For Different Audiences:**

**Security-focused audience:**
- Use Samples 1, 2, 7 (Security issues)

**Performance-focused audience:**
- Use Sample 3 (Performance optimization)

**General developers:**
- Use Samples 1, 4, 6 (Security, Quality, Error handling)

**Teaching/Learning:**
- Use Samples 4, 5, 6 (Code quality and common mistakes)

---

## 🎯 **TESTING EACH SAMPLE:**

**For each sample:**
1. Go to http://127.0.0.1:8000
2. Click "Review Diff"
3. Copy and paste the diff
4. Click "Analyze Diff"
5. Wait 10-15 seconds
6. See results!

**What to look for:**
- Different samples will have different severity distributions
- Some focus on Security (Critical)
- Some focus on Performance (Medium/High)
- Some focus on Logic (High)
- Some focus on Quality (Medium)

---

## ✅ **RECOMMENDED FOR YOUR DEMO:**

**Use Sample 1 (SQL Injection) for your main demo because:**
- ✅ Shows CRITICAL severity (most impressive)
- ✅ Easy to explain (everyone understands "hacking")
- ✅ Clear security risk
- ✅ AI provides excellent fix suggestions
- ✅ All 4 agents find different issues in the same code

**Optional: Add Sample 7 (Hardcoded Credentials) for extra wow factor:**
- Shows multiple CRITICAL issues
- Very obvious security problem
- Great for emphasizing security scanning capabilities

---

## 💡 **PRO TIPS:**

1. **Start with Sample 1** in your demo - it's the most impressive
2. **Have 2-3 samples ready** to show versatility
3. **Explain the vulnerability** before showing AI results
4. **Point out all 4 agents** finding different things
5. **Show the "Fix" suggestions** - not just finding bugs, but solving them

---

**All samples are ready to copy-paste! Just choose which one(s) to demonstrate!** 🚀
