# StoryForge - AI-Powered Children's Book Learning Platform
## Hackathon III: Reusable Intelligence Project

> **Your Unique Innovation**: Multi-agent architecture with intelligent content routing based on reading level detection and engagement analysis

---

## 🎯 What Makes StoryForge Different

Unlike generic educational chatbots, StoryForge uses **6 specialized AI agents** coordinated by an intelligent Router Agent that:

1. **Analyzes child's reading level** - Vocabulary, comprehension, age-appropriate content
2. **Detects engagement patterns** - Excited, confused, bored, curious
3. **Routes to specialists** - Each agent excels at specific learning tasks
4. **Adapts content complexity** - Based on reading proficiency (0-100%)
5. **Alerts educators** - Real-time learning difficulty detection

---

## 📊 Architecture Overview

### Multi-Agent System

```
┌─────────────────────────────────────────────────────────────┐
│                    ROUTER AGENT (Port 8001)                  │
│              Intent Classification + Engagement Analysis      │
│                                                              │
│  Routing Logic:                                             │
│  ├─ 20% → Story Agent (Create/Continue stories)            │
│  ├─ 25% → Comprehension Agent (Answer questions)           │
│  ├─ 30% → Vocabulary Agent (Define/Explain words)          │
│  ├─ 10% → Quiz Agent (Generate comprehension tests)        │
│  ├─ 10% → Progress Agent (Track reading levels)            │
│  └─ 5%  → Adaptive (Engagement-based routing)              │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│    STORY     │  │ COMPREHENSION│  │  VOCABULARY  │
│  Agent 8002  │  │  Agent 8003  │  │  Agent 8004  │
│              │  │              │  │              │
│ • Generate   │  │ • Questions  │  │ • Definitions│
│   stories    │  │ • Summaries  │  │ • Context    │
│ • Continue   │  │ • Analysis   │  │ • Examples   │
│   narratives │  │              │  │              │
└──────────────┘  └──────────────┘  └──────────────┘

┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│     QUIZ     │  │   PROGRESS   │  │   EDUCATOR   │
│  Agent 8005  │  │  Agent 8006  │  │  Dashboard   │
│              │  │              │  │              │
│ • Generate   │  │ • Track      │  │ • Alerts     │
│   quizzes    │  │   levels     │  │ • Analytics  │
│ • Auto-grade │  │ • Analyze    │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## 🏗️ Agent Specifications

### 1. Router Agent (Port 8001)
**Role**: Intelligent content router and orchestrator

**Classification Logic**:
```
Intent Detection:
├─ "Tell me a story about..." → Story Agent
├─ "What does X mean?" → Vocabulary Agent
├─ "What happened in the story?" → Comprehension Agent
├─ "Can you quiz me?" → Quiz Agent
└─ "How am I doing?" → Progress Agent

Engagement Detection:
├─ "I don't understand" → Simpler explanation
├─ "This is boring" → More engaging content
├─ Multiple wrong answers → Easier questions
└─ "Tell me more!" → Advanced content
```

---

### 2. Story Agent (Port 8002)
**Role**: Generate and continue age-appropriate stories

**Features**:
- Adapts vocabulary to reading level
- Creates engaging narratives
- Continues user-initiated stories
- Incorporates educational themes

**Reading Level Adaptation**:
| Level | Age | Vocabulary | Sentence Length | Themes |
|-------|-----|-----------|-----------------|--------|
| Beginner (0-40%) | 5-7 | Simple words | 5-8 words | Animals, Family |
| Emerging (41-70%) | 8-10 | Grade-level | 8-12 words | Adventure, Friendship |
| Proficient (71-90%) | 11-13 | Advanced | 12-15 words | Mystery, Science |
| Advanced (91-100%) | 14+ | Complex | 15+ words | Complex themes |

---

### 3. Comprehension Agent (Port 8003)
**Role**: Assess and improve reading comprehension

**Techniques**:
- Summarization requests
- Character analysis
- Plot prediction
- Theme identification
- Cause-effect relationships

**Progressive Questioning**:
```
Level 1: "Who is the main character?"
Level 2: "What problem does the character face?"
Level 3: "How does the setting affect the story?"
Level 4: "What is the author's message?"
Level 5: "How would you change the ending?"
```

---

### 4. Vocabulary Agent (Port 8004)
**Role**: Build vocabulary through context

**Response Format**:
```markdown
📚 **Word**: [word]

**Simple Definition**: [child-friendly]

**In the Story**: [example from context]

**Other Examples**:
- [sentence 1]
- [sentence 2]

**Similar Words**: [synonyms]

**Try Using It**: [practice prompt]
```

---

### 5. Quiz Agent (Port 8005)
**Role**: Generate and auto-grade comprehension quizzes

**Question Types**:
1. Multiple choice (comprehension)
2. True/False (facts)
3. Fill-in-the-blank (vocabulary)
4. Short answer (analysis)
5. Creative (application)

**Difficulty Scaling**:
```python
def generate_quiz(reading_level):
    if reading_level < 40:
        return {
            "type": "multiple_choice",
            "questions": 3,
            "hints": True
        }
    elif reading_level < 70:
        return {
            "type": "mixed",
            "questions": 5,
            "hints": False
        }
    else:
        return {
            "type": "advanced",
            "questions": 8,
            "open_ended": True
        }
```

---

### 6. Progress Agent (Port 8006)
**Role**: Track reading proficiency and growth

**Metrics Tracked**:
- Reading level (0-100%)
- Vocabulary mastery
- Comprehension accuracy
- Engagement score
- Reading streak

**Proficiency Calculation**:
```
Reading Level = (
    Quiz Scores × 40% +
    Vocabulary Tests × 30% +
    Comprehension Accuracy × 20% +
    Engagement Score × 10%
)

Categories:
0-40%   → Beginner (🔵)
41-70%  → Emerging (🟢)
71-90%  → Proficient (🟡)
91-100% → Advanced (🔴)
```

---

## 🚀 Implementation Phases

### Phase 1: Foundation (Current → Week 1)
- [x] Basic Docker setup
- [x] Frontend-Backend connection
- [ ] Router Agent with basic intent classification
- [ ] Database schema for users and progress
- [ ] Story Agent MVP

### Phase 2: Core Agents (Week 1-2)
- [ ] Comprehension Agent
- [ ] Vocabulary Agent
- [ ] Quiz Agent with auto-grading
- [ ] Progress tracking system
- [ ] Kafka event bus setup

### Phase 3: Intelligence (Week 2-3)
- [ ] Engagement detection
- [ ] Reading level adaptation
- [ ] Difficulty adjustment algorithm
- [ ] Struggle detection and alerts
- [ ] WebSocket for real-time updates

### Phase 4: Polish (Week 3-4)
- [ ] Educator dashboard
- [ ] Analytics and reporting
- [ ] Kubernetes deployment
- [ ] Comprehensive testing
- [ ] Documentation site

---

## 📁 Proposed File Structure

```
storyforge/
├── backend/
│   ├── router_agent/        # Port 8001 - Main router
│   ├── story_agent/         # Port 8002 - Story generation
│   ├── comprehension_agent/ # Port 8003 - Comprehension
│   ├── vocabulary_agent/    # Port 8004 - Vocabulary
│   ├── quiz_agent/          # Port 8005 - Quiz generation
│   ├── progress_agent/      # Port 8006 - Progress tracking
│   └── shared/
│       ├── models.py
│       ├── database.py
│       └── kafka_client.py
├── frontend/
│   ├── app/
│   │   ├── (child)/
│   │   │   ├── story/       # Story reading interface
│   │   │   ├── quiz/        # Quiz interface
│   │   │   └── progress/    # Child dashboard
│   │   └── (educator)/
│   │       ├── dashboard/   # Class overview
│   │       └── alerts/      # Difficulty alerts
│   └── components/
├── docker-compose.yml       # All 6 agents + Kafka + DB
├── k8s/                     # Kubernetes manifests
└── docs/                    # Docusaurus documentation
```

---

## 🎯 Key Differentiators

### 1. **Reading Level Detection**
Not just age - actual comprehension ability

### 2. **Engagement-Based Routing**
Detects boredom, confusion, excitement

### 3. **Progressive Difficulty**
Content adapts in real-time

### 4. **Educational Value**
Every interaction teaches something

### 5. **Educator Insights**
Real-time alerts when children struggle

---

## 🔄 Data Flow Examples

### Example 1: Child Asks "What is a brave?"
```
User → Router Agent
    ├─ Classify: Vocabulary question
    ├─ Detect: Neutral engagement
    └─ Route → Vocabulary Agent (8004)
             ├─ Generate definition
             ├─ Find story context
             ├─ Create examples
             └─ Suggest practice
    → Return to user
    → Publish to Kafka: vocabulary.query
    → Update progress DB
```

### Example 2: Struggle Detection
```
Child fails quiz 3 times
    │
    ▼
Quiz Agent detects repeated failure
    │
    ├─ Easier questions to child
    │
    └─ Publish to Kafka: struggle.comprehension
              │
              ▼
    Kafka Consumer (Educator Alert Service)
              │
              ▼
    WebSocket to Educator Dashboard
              │
              ▼
    Alert: "⚠️ Emma struggling with story comprehension"
```

---

## 📊 Success Metrics

### Technical Metrics
- Router accuracy: >95%
- Response time: <500ms p95
- Agent availability: >99.5%
- Kafka throughput: 1000 msg/sec

### Educational Metrics
- Reading level improvement
- Quiz completion rate
- Vocabulary growth
- Engagement score
- Time spent reading

---

## 🎨 Unique Features

1. **Story Continuation**: Children can co-create stories with AI
2. **Context-Aware Vocabulary**: Words explained using the current story
3. **Adaptive Quizzes**: Difficulty adjusts based on performance
4. **Reading Streak Rewards**: Gamification for daily reading
5. **Parent/Educator Portal**: See child's growth over time

---

## Next Steps

1. **Review this design** - Does this align with your vision?
2. **Choose a focus** - Which agents to build first?
3. **Set up infrastructure** - Kafka, PostgreSQL, multi-service Docker
4. **Start coding** - Begin with Router Agent

---

**Would you like me to start implementing this architecture?** I can begin with:

A) Router Agent with intent classification
B) Story Agent for generating age-appropriate content
C) Database schema and models
D) Docker Compose setup for all 6 agents

Let me know which component you'd like to tackle first!
