# 🚀 Framework Implementation Details

## Orchestration Framework: **LangChain**

This PR Review Agent is built using **LangChain** (v0.1.20) as the multi-agent orchestration framework, as requested in the Lyzr AI Backend Engineering Intern Challenge.

---

## 📦 LangChain Components Used

### 1. **LangChain Core** (`langchain-core==0.1.52`)
   - **Purpose**: Foundation library providing core abstractions
   - **Usage**: Message schemas, base classes, callback system
   - **Location**: `app/agents/base_agent.py`

### 2. **LangChain OpenAI** (`langchain-openai==0.1.0`)
   - **Purpose**: OpenAI integration for LangChain
   - **Usage**: `ChatOpenAI` class for GPT-4 Turbo access
   - **Configuration**:
     - Model: `gpt-4-turbo-preview`
     - Temperature: `0.1` (for deterministic code reviews)
     - Max Tokens: `2000` per analysis

### 3. **LangChain Community** (`langchain-community==0.0.38`)
   - **Purpose**: Community-contributed integrations
   - **Usage**: Additional tools and utilities

---

## 🏗️ Architecture with LangChain

```
FastAPI Application
        ↓
    ReviewService
        ↓
  ReviewOrchestrator ← Coordinates all agents
        ↓
    ┌───┴───┬───────┬──────────┐
    ↓       ↓       ↓          ↓
Security Performance Quality Logic
 Agent    Agent     Agent    Agent
    ↓       ↓       ↓          ↓
  LangChain ChatOpenAI (GPT-4)
        ↓
  Structured Review Comments
```

---

## 💻 Code Implementation

### BaseReviewAgent (with LangChain)

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.callbacks import get_openai_callback

class BaseReviewAgent:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        
        # Initialize LangChain LLM
        self.llm = ChatOpenAI(
            model=settings.DEFAULT_LLM_MODEL,      # gpt-4-turbo-preview
            temperature=settings.TEMPERATURE,       # 0.1
            max_tokens=settings.MAX_TOKENS,         # 2000
            openai_api_key=settings.OPENAI_API_KEY
        )
    
    async def analyze(self, file_path, code_diff, language, full_context):
        # Create LangChain messages
        messages = [
            SystemMessage(content=self.get_system_prompt()),
            HumanMessage(content=self.get_analysis_prompt(code_context))
        ]
        
        # Call LLM with token tracking
        with get_openai_callback() as cb:
            response = self.llm.invoke(messages)
            logger.info(f"Tokens: {cb.total_tokens}, Cost: ${cb.total_cost:.4f}")
        
        # Parse response
        analysis_text = response.content
        return self._parse_analysis(analysis_text, file_path)
```

---

## 🎯 Why LangChain?

### Advantages for This Project

1. **Standardized Message Schemas**
   - SystemMessage / HumanMessage for clear role separation
   - Consistent prompt structure across all 4 agents
   
2. **Built-in Token Tracking**
   - `get_openai_callback()` automatically tracks usage
   - Cost calculation included
   - Helps monitor agent efficiency

3. **Easy LLM Swapping**
   - Can switch from OpenAI to Anthropic/Cohere easily
   - Just change `ChatOpenAI` to `ChatAnthropic`
   - All agents adapt automatically

4. **Production-Ready**
   - Error handling built-in
   - Rate limiting support
   - Async/await compatible

5. **Industry Standard**
   - Widely adopted in production systems
   - Strong community support
   - Regular updates and improvements

---

## 🔧 Configuration

### Environment Variables
```bash
# .env file
OPENAI_API_KEY=sk-your-api-key
DEFAULT_LLM_MODEL=gpt-4-turbo-preview
TEMPERATURE=0.1
MAX_TOKENS=2000
```

### LangChain Settings
```python
# app/config.py
class Settings(BaseSettings):
    # LLM Configuration
    DEFAULT_LLM_MODEL: str = "gpt-4-turbo-preview"
    TEMPERATURE: float = 0.1
    MAX_TOKENS: int = 2000
```

---

## 🚦 Multi-Agent Orchestration

### 4 Specialized Agents (All Using LangChain)

1. **SecurityAnalystAgent**
   - Focus: SQL injection, XSS, auth issues
   - LangChain: ChatOpenAI with security prompt

2. **PerformanceReviewerAgent**
   - Focus: Inefficient loops, memory leaks, N+1 queries
   - LangChain: ChatOpenAI with performance prompt

3. **CodeQualityInspectorAgent**
   - Focus: Code smells, maintainability, best practices
   - LangChain: ChatOpenAI with quality prompt

4. **LogicAnalyzerAgent**
   - Focus: Business logic, edge cases, correctness
   - LangChain: ChatOpenAI with logic prompt

### Parallel Execution
```python
# app/agents/orchestrator.py
async def review_changes(self, files):
    # All 4 agents run in parallel using asyncio
    results = await asyncio.gather(
        self.security_agent.analyze(file_path, diff, lang),
        self.performance_agent.analyze(file_path, diff, lang),
        self.quality_agent.analyze(file_path, diff, lang),
        self.logic_agent.analyze(file_path, diff, lang)
    )
```

---

## 📊 Token Usage Tracking

LangChain's `get_openai_callback()` provides automatic tracking:

```python
with get_openai_callback() as cb:
    response = self.llm.invoke(messages)
    
    # Automatically available:
    # - cb.total_tokens
    # - cb.prompt_tokens
    # - cb.completion_tokens
    # - cb.total_cost (in USD)
    
    logger.info(f"Tokens: {cb.total_tokens}, Cost: ${cb.total_cost:.4f}")
```

---

## 🔮 Future Enhancements with LangChain

### Potential Upgrades
1. **Chains**: Use `LLMChain` for complex multi-step reviews
2. **Memory**: Add conversation memory for context-aware reviews
3. **Tools**: Integrate with GitHub API, linters, test runners
4. **Agents**: Use LangChain's Agent framework for autonomous decisions
5. **Callbacks**: Advanced logging, streaming responses

---

## 📝 Comparison: Why Not CrewAI or Lyzr?

### LangChain vs CrewAI
- **LangChain**: Lower-level, more control, better for custom workflows
- **CrewAI**: Higher-level, opinionated, better for role-based teams
- **Choice**: LangChain for flexibility and fine-tuned control

### LangChain vs Lyzr Agent Studio
- **LangChain**: Open-source, extensive documentation, large community
- **Lyzr**: Newer, still evolving, less community resources
- **Choice**: LangChain for stability and production-readiness

---

## ✅ Verification

### Check LangChain Integration
```bash
# Check installed packages
pip show langchain langchain-openai

# Run the application
python -m uvicorn app.main:app --reload --port 8000

# Test API endpoint
curl -X POST http://localhost:8000/api/v1/review/pr \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "owner/repo", "pr_number": 123}'
```

### Expected Output
```
2025-11-26 20:49:07 - SecurityAnalystAgent analyzing file.py using LangChain
2025-11-26 20:49:08 - SecurityAnalystAgent - Tokens: 1250, Cost: $0.0125
2025-11-26 20:49:08 - PerformanceReviewerAgent analyzing file.py using LangChain
2025-11-26 20:49:09 - PerformanceReviewerAgent - Tokens: 980, Cost: $0.0098
...
```

---

## 🎓 Key Takeaways

1. ✅ **LangChain is the orchestration framework** used in this project
2. ✅ **ChatOpenAI** class manages all LLM interactions
3. ✅ **SystemMessage/HumanMessage** for structured prompts
4. ✅ **get_openai_callback()** for automatic token tracking
5. ✅ **4 agents** running in parallel with asyncio
6. ✅ **Production-ready** with error handling and logging

---

## 📚 References

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [LangChain OpenAI Integration](https://python.langchain.com/docs/integrations/platforms/openai)
- [ChatOpenAI API Reference](https://api.python.langchain.com/en/latest/chat_models/langchain_openai.chat_models.base.ChatOpenAI.html)
- [LangChain Callbacks](https://python.langchain.com/docs/modules/callbacks/)

---

**Built for the Lyzr AI Backend Engineering Intern Challenge** 🚀
