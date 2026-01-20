-- StoryForge Database Schema
-- AI-Powered Children's Reading Platform

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users/Students Table
CREATE TABLE IF NOT EXISTS students (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    age INTEGER,
    reading_level INTEGER DEFAULT 50 CHECK (reading_level >= 0 AND reading_level <= 100),
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_students_student_id ON students(student_id);
CREATE INDEX idx_students_reading_level ON students(reading_level);

-- Stories Table
CREATE TABLE IF NOT EXISTS stories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(500) NOT NULL,
    story_text TEXT NOT NULL,
    story_type VARCHAR(50) NOT NULL,
    reading_level VARCHAR(50) NOT NULL,
    length VARCHAR(20) NOT NULL,
    vocabulary_words TEXT[],
    word_count INTEGER,
    estimated_reading_time INTEGER,
    moral_lesson TEXT,
    characters TEXT[],
    student_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE INDEX idx_stories_student_id ON stories(student_id);
CREATE INDEX idx_stories_story_type ON stories(story_type);
CREATE INDEX idx_stories_reading_level ON stories(reading_level);
CREATE INDEX idx_stories_created_at ON stories(created_at DESC);

-- Vocabulary Lookups Table
CREATE TABLE IF NOT EXISTS vocabulary_lookups (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    word VARCHAR(255) NOT NULL,
    definition TEXT NOT NULL,
    simple_explanation TEXT,
    examples TEXT[],
    synonyms TEXT[],
    antonyms TEXT[],
    reading_level VARCHAR(50) NOT NULL,
    explanation_style VARCHAR(50) NOT NULL,
    student_id VARCHAR(255) NOT NULL,
    context TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE INDEX idx_vocab_word ON vocabulary_lookups(word);
CREATE INDEX idx_vocab_student_id ON vocabulary_lookups(student_id);
CREATE INDEX idx_vocab_created_at ON vocabulary_lookups(created_at DESC);

-- Comprehension Questions Table
CREATE TABLE IF NOT EXISTS comprehension_questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL,
    story_id UUID,
    student_id VARCHAR(255) NOT NULL,
    student_answer TEXT,
    is_correct BOOLEAN,
    hints TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    answered_at TIMESTAMP,
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE SET NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE INDEX idx_comp_questions_student_id ON comprehension_questions(student_id);
CREATE INDEX idx_comp_questions_story_id ON comprehension_questions(story_id);
CREATE INDEX idx_comp_questions_type ON comprehension_questions(question_type);

-- Progress Tracking Table
CREATE TABLE IF NOT EXISTS student_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id VARCHAR(255) NOT NULL,
    metric_type VARCHAR(100) NOT NULL,
    metric_value FLOAT NOT NULL,
    metadata JSONB DEFAULT '{}',
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE INDEX idx_progress_student_id ON student_progress(student_id);
CREATE INDEX idx_progress_metric_type ON student_progress(metric_type);
CREATE INDEX idx_progress_recorded_at ON student_progress(recorded_at DESC);

-- Router Statistics Table
CREATE TABLE IF NOT EXISTS router_stats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id VARCHAR(255) NOT NULL,
    query TEXT NOT NULL,
    routed_to VARCHAR(50) NOT NULL,
    engagement_level VARCHAR(50) NOT NULL,
    confidence FLOAT NOT NULL,
    pattern_match BOOLEAN DEFAULT FALSE,
    requires_adaptation BOOLEAN DEFAULT FALSE,
    processing_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE INDEX idx_router_stats_student_id ON router_stats(student_id);
CREATE INDEX idx_router_stats_routed_to ON router_stats(routed_to);
CREATE INDEX idx_router_stats_engagement ON router_stats(engagement_level);
CREATE INDEX idx_router_stats_created_at ON router_stats(created_at DESC);

-- Reading Sessions Table
CREATE TABLE IF NOT EXISTS reading_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id VARCHAR(255) NOT NULL,
    session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_end TIMESTAMP,
    stories_read INTEGER DEFAULT 0,
    words_looked_up INTEGER DEFAULT 0,
    questions_answered INTEGER DEFAULT 0,
    questions_correct INTEGER DEFAULT 0,
    engagement_summary JSONB DEFAULT '{}',
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE INDEX idx_sessions_student_id ON reading_sessions(student_id);
CREATE INDEX idx_sessions_start ON reading_sessions(session_start DESC);

-- Agent Performance Metrics Table
CREATE TABLE IF NOT EXISTS agent_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_name VARCHAR(100) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value FLOAT NOT NULL,
    metadata JSONB DEFAULT '{}',
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_agent_metrics_agent ON agent_metrics(agent_name);
CREATE INDEX idx_agent_metrics_name ON agent_metrics(metric_name);
CREATE INDEX idx_agent_metrics_recorded_at ON agent_metrics(recorded_at DESC);

-- Create update trigger for students table
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_students_updated_at BEFORE UPDATE ON students
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample student for testing
INSERT INTO students (student_id, name, age, reading_level, preferences)
VALUES ('test_user_001', 'Test Student', 8, 50, '{"favorite_genre": "adventure", "difficulty": "medium"}')
ON CONFLICT (student_id) DO NOTHING;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO storyforge_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO storyforge_user;

-- Views for analytics

-- Student performance overview
CREATE OR REPLACE VIEW student_performance_overview AS
SELECT
    s.student_id,
    s.name,
    s.reading_level,
    COUNT(DISTINCT st.id) as total_stories_read,
    COUNT(DISTINCT vl.id) as total_words_looked_up,
    COUNT(cq.id) as total_questions_answered,
    SUM(CASE WHEN cq.is_correct THEN 1 ELSE 0 END) as correct_answers,
    ROUND(
        CAST(SUM(CASE WHEN cq.is_correct THEN 1 ELSE 0 END) AS FLOAT) /
        NULLIF(COUNT(cq.id), 0) * 100,
        2
    ) as accuracy_percentage,
    MAX(rs.session_start) as last_active
FROM students s
LEFT JOIN stories st ON s.student_id = st.student_id
LEFT JOIN vocabulary_lookups vl ON s.student_id = vl.student_id
LEFT JOIN comprehension_questions cq ON s.student_id = cq.student_id
LEFT JOIN reading_sessions rs ON s.student_id = rs.student_id
GROUP BY s.student_id, s.name, s.reading_level;

-- Router effectiveness metrics
CREATE OR REPLACE VIEW router_effectiveness AS
SELECT
    routed_to as agent,
    COUNT(*) as total_queries,
    AVG(confidence) as avg_confidence,
    COUNT(CASE WHEN pattern_match THEN 1 END) as pattern_matches,
    COUNT(CASE WHEN requires_adaptation THEN 1 END) as adaptation_required,
    AVG(processing_time_ms) as avg_processing_time_ms,
    COUNT(DISTINCT student_id) as unique_students
FROM router_stats
GROUP BY routed_to
ORDER BY total_queries DESC;

-- Engagement trends
CREATE OR REPLACE VIEW engagement_trends AS
SELECT
    DATE_TRUNC('day', created_at) as date,
    engagement_level,
    COUNT(*) as occurrence_count,
    AVG(confidence) as avg_confidence
FROM router_stats
GROUP BY DATE_TRUNC('day', created_at), engagement_level
ORDER BY date DESC, occurrence_count DESC;

COMMENT ON TABLE students IS 'Student profiles with reading levels and preferences';
COMMENT ON TABLE stories IS 'Generated stories with metadata and vocabulary';
COMMENT ON TABLE vocabulary_lookups IS 'Word definitions and explanations requested by students';
COMMENT ON TABLE comprehension_questions IS 'Questions and answers for reading comprehension';
COMMENT ON TABLE student_progress IS 'Time-series tracking of student progress metrics';
COMMENT ON TABLE router_stats IS 'Query routing decisions and engagement detection';
COMMENT ON TABLE reading_sessions IS 'Reading session summaries and engagement data';
COMMENT ON TABLE agent_metrics IS 'Performance metrics for specialist agents';
