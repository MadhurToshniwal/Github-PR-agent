# Architecture Documentation

## System Overview

The PR Review Agent is a production-grade, multi-agent AI system designed to analyze GitHub pull requests and provide comprehensive code reviews across multiple dimensions: security, performance, code quality, and logic correctness.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Client Layer                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │ Web UI   │  │ REST API │  │ GitHub Webhooks      │  │
│  └──────────┘  └──────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  API Gateway Layer                       │
│                   (FastAPI)                              │
│  • Request Validation                                    │
│  • Rate Limiting                                         │
│  • Authentication                                        │
│  • Error Handling                                        │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                Service Layer                             │
│  ┌──────────────────┐      ┌────────────────────────┐  │
│  │ GitHub Service   │      │  Review Service        │  │
│  │ • Fetch PRs      │      │  • Orchestrate Review  │  │
│  │ • Parse Diffs    │      │  • Aggregate Results   │  │
│  └──────────────────┘      └────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Multi-Agent Orchestrator                    │
│  • Coordinate agent execution                            │
│  • Manage parallel processing                            │
│  • Deduplicate findings                                  │
│  • Prioritize issues                                     │
└─────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Security    │  │ Performance  │  │ Code Quality │
│  Analyst     │  │  Reviewer    │  │  Inspector   │
│  Agent       │  │  Agent       │  │  Agent       │
└──────────────┘  └──────────────┘  └──────────────┘
          │               │               │
          └───────────────┼───────────────┘
                          ▼
                  ┌──────────────┐
                  │ Logic        │
                  │ Analyzer     │
                  │ Agent        │
                  └──────────────┘
                          │
                          ▼
              ┌─────────────────────┐
              │    LLM Provider     │
              │  (OpenAI GPT-4)     │
              └─────────────────────┘
```

## Component Details

### 1. API Gateway Layer (FastAPI)

**Responsibilities:**
- HTTP request/response handling
- Input validation using Pydantic
- Rate limiting per IP/user
- CORS management
- API documentation (Swagger/ReDoc)
- Error handling and logging

**Key Files:**
- `app/main.py` - FastAPI application
- `app/schemas.py` - Request/Response models
- `app/config.py` - Configuration management

### 2. Service Layer

#### GitHub Service
**Responsibilities:**
- Authenticate with GitHub API
- Fetch PR information
- Parse file changes and diffs
- Extract code context

**Key Features:**
- Token-based authentication
- Rate limit handling
- Language detection
- Diff parsing with hunk analysis

**File:** `app/services/github_service.py`

#### Review Service
**Responsibilities:**
- Coordinate review workflow
- Prepare data for agents
- Aggregate agent results
- Format final output

**File:** `app/services/review_service.py`

### 3. Multi-Agent System

#### Agent Orchestrator
**Responsibilities:**
- Initialize and manage agents
- Execute agents in parallel
- Deduplicate findings
- Sort by severity and confidence
- Generate summary statistics

**Algorithm:**
1. Receive file changes
2. For each file:
   - Launch all agents in parallel
   - Collect results asynchronously
3. Deduplicate using similarity matching
4. Sort by severity and confidence
5. Generate summary metrics

**File:** `app/agents/orchestrator.py`

#### Specialized Agents

Each agent extends `BaseReviewAgent` and implements:
- `get_system_prompt()` - Agent's expertise definition
- `get_analysis_prompt()` - Task-specific instructions
- `_get_category()` - Issue categorization

##### Security Analyst Agent
**Focus Areas:**
- SQL Injection
- XSS vulnerabilities
- Authentication issues
- Secrets in code
- Insecure APIs
- CSRF risks

**Prompt Engineering:**
- Chain-of-thought reasoning
- Example-based learning
- Severity classification
- Exploit scenario generation

##### Performance Reviewer Agent
**Focus Areas:**
- Algorithmic complexity
- Database query efficiency
- Memory usage
- Caching opportunities
- Resource leaks

**Analysis Approach:**
- Big-O complexity analysis
- Pattern matching for anti-patterns
- Resource usage estimation

##### Code Quality Inspector Agent
**Focus Areas:**
- SOLID principles
- DRY violations
- Naming conventions
- Code complexity
- Documentation

**Evaluation Criteria:**
- Cyclomatic complexity
- Function length
- Nesting depth
- Readability metrics

##### Logic Analyzer Agent
**Focus Areas:**
- Logic errors
- Edge cases
- Null safety
- Off-by-one errors
- Type mismatches

**Detection Methods:**
- Control flow analysis
- Boundary condition checking
- Type inference

**File:** `app/agents/base_agent.py`

### 4. LLM Integration

**Provider:** OpenAI GPT-4 Turbo Preview

**Configuration:**
- Temperature: 0.1 (deterministic)
- Max tokens: 2000
- Model: gpt-4-turbo-preview

**Prompt Strategy:**
- System prompt: Define agent role and expertise
- User prompt: Provide code context and analysis task
- Response parsing: Extract structured findings

## Data Flow

### PR Review Flow

```
1. Client Request
   └─> POST /api/v1/review/pr
       {repo_owner, repo_name, pr_number, github_token}

2. API Gateway
   └─> Validate request
   └─> Check rate limit
   └─> Forward to Review Service

3. Review Service
   └─> Fetch PR from GitHub
   └─> Parse file changes
   └─> Extract diffs

4. Orchestrator
   └─> For each file:
       ├─> Launch Security Analyst
       ├─> Launch Performance Reviewer
       ├─> Launch Code Quality Inspector
       └─> Launch Logic Analyzer
   └─> Await all results
   └─> Deduplicate findings
   └─> Sort by priority

5. Response Formatting
   └─> Generate summary statistics
   └─> Structure review comments
   └─> Add metadata

6. Client Response
   └─> Return JSON with:
       ├─> review_summary
       ├─> reviews (array)
       └─> metadata
```

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- No session management
- Redis for shared rate limiting (optional)
- Load balancer compatible

### Performance Optimization
- Parallel agent execution
- Async I/O operations
- Connection pooling
- Response caching (planned)

### Resource Management
- Request timeout: 300 seconds
- Max PR size: 1000 files
- Max file size: 500KB
- Rate limit: 60 req/min per IP

## Security Architecture

### Input Validation
- Pydantic models for type safety
- Request size limits
- Sanitized error messages

### API Security
- Rate limiting
- GitHub token encryption
- Environment-based secrets
- CORS restrictions

### Code Execution
- No arbitrary code execution
- Sandboxed LLM calls
- Timeout protection

## Error Handling Strategy

### Error Categories
1. **Client Errors (4xx)**
   - Validation errors
   - Authentication failures
   - Rate limit exceeded

2. **Server Errors (5xx)**
   - LLM API failures
   - GitHub API errors
   - Internal processing errors

### Error Response Format
```json
{
  "error": "Brief error message",
  "detail": "Detailed explanation",
  "timestamp": "ISO 8601 timestamp"
}
```

### Logging Strategy
- INFO: Normal operations
- WARNING: Recoverable issues
- ERROR: Failures with stack trace
- Structured JSON logging (production)

## Testing Strategy

### Unit Tests
- Agent prompt generation
- Diff parsing logic
- Comment deduplication
- Severity classification

### Integration Tests
- API endpoint validation
- GitHub service mocking
- End-to-end review flow

### Performance Tests
- Concurrent request handling
- Large PR processing
- Rate limiting accuracy

## Deployment Architecture

### Container Strategy
- Docker multi-stage build
- Non-root user execution
- Health check endpoints
- Graceful shutdown

### Cloud Deployment
- Platform: Railway/Render/AWS
- Auto-scaling: Based on CPU/memory
- Monitoring: Health checks
- Logging: Centralized

### CI/CD Pipeline
- GitHub Actions
- Automated testing
- Docker build and push
- Deployment on merge to main

## Future Enhancements

### Planned Features
1. **Caching Layer**
   - Redis for review caching
   - PR metadata caching
   - Rate limit storage

2. **Background Processing**
   - Celery task queue
   - Async webhook handling
   - Scheduled re-reviews

3. **Advanced Analytics**
   - Historical trend analysis
   - Team metrics dashboard
   - Custom rule engine

4. **Multi-Platform Support**
   - GitLab integration
   - Bitbucket support
   - Azure DevOps

5. **Enhanced AI Features**
   - Auto-fix code generation
   - Learning from feedback
   - Custom agent training
   - Multi-language LLM support

## Performance Metrics

### Target SLAs
- API response time: <30s for typical PR
- Concurrent requests: 100+
- Uptime: 99.9%
- Error rate: <1%

### Monitoring
- Health check endpoint
- Request/response logging
- Error tracking (Sentry optional)
- Usage statistics endpoint
