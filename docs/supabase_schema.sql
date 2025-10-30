-- Supabase Database Schema for Arabic AI Agents Evaluation
-- Run this SQL in your Supabase SQL Editor to create the required tables

-- ============================================================================
-- TABLE 1: Conversations
-- Stores metadata about each conversation
-- ============================================================================
CREATE TABLE IF NOT EXISTS conversations (
  id BIGSERIAL PRIMARY KEY,
  conversation_id TEXT UNIQUE NOT NULL,
  scenario_id TEXT NOT NULL,
  agent_type TEXT NOT NULL,
  model_name TEXT NOT NULL,
  customer_persona TEXT,
  customer_goal TEXT,
  total_turns INTEGER,
  success BOOLEAN,
  end_reason TEXT,
  total_tokens INTEGER,
  total_latency FLOAT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_conversations_scenario ON conversations(scenario_id);
CREATE INDEX IF NOT EXISTS idx_conversations_model ON conversations(model_name);
CREATE INDEX IF NOT EXISTS idx_conversations_agent ON conversations(agent_type);
CREATE INDEX IF NOT EXISTS idx_conversations_created ON conversations(created_at DESC);

-- ============================================================================
-- TABLE 2: Conversation Turns
-- Stores individual messages in each conversation
-- ============================================================================
CREATE TABLE IF NOT EXISTS conversation_turns (
  id BIGSERIAL PRIMARY KEY,
  conversation_id TEXT NOT NULL,
  turn_number INTEGER NOT NULL,
  customer_message TEXT,
  agent_message TEXT,
  customer_tokens INTEGER,
  agent_tokens INTEGER,
  turn_latency FLOAT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_turns_conversation ON conversation_turns(conversation_id);
CREATE INDEX IF NOT EXISTS idx_turns_number ON conversation_turns(conversation_id, turn_number);

-- ============================================================================
-- TABLE 3: Evaluations
-- Stores evaluation scores for conversations
-- ============================================================================
CREATE TABLE IF NOT EXISTS evaluations (
  id BIGSERIAL PRIMARY KEY,
  conversation_id TEXT,
  scenario_id TEXT NOT NULL,
  model_name TEXT NOT NULL,
  task_completion FLOAT CHECK (task_completion >= 0 AND task_completion <= 10),
  empathy FLOAT CHECK (empathy >= 0 AND empathy <= 10),
  clarity FLOAT CHECK (clarity >= 0 AND clarity <= 10),
  cultural_fit FLOAT CHECK (cultural_fit >= 0 AND cultural_fit <= 10),
  problem_solving FLOAT CHECK (problem_solving >= 0 AND problem_solving <= 10),
  overall_score FLOAT CHECK (overall_score >= 0 AND overall_score <= 10),
  evaluator_notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_evaluations_conversation ON evaluations(conversation_id);
CREATE INDEX IF NOT EXISTS idx_evaluations_scenario ON evaluations(scenario_id);
CREATE INDEX IF NOT EXISTS idx_evaluations_model ON evaluations(model_name);

-- ============================================================================
-- VIEWS: Useful queries for analysis
-- ============================================================================

-- View: Average scores by model
CREATE OR REPLACE VIEW model_performance AS
SELECT 
  c.model_name,
  COUNT(DISTINCT e.conversation_id) as total_conversations,
  AVG(e.task_completion) as avg_task_completion,
  AVG(e.empathy) as avg_empathy,
  AVG(e.clarity) as avg_clarity,
  AVG(e.cultural_fit) as avg_cultural_fit,
  AVG(e.problem_solving) as avg_problem_solving,
  AVG(e.overall_score) as avg_overall_score,
  AVG(c.total_turns) as avg_turns,
  AVG(c.total_tokens) as avg_tokens,
  AVG(c.total_latency) as avg_latency
FROM evaluations e
JOIN conversations c ON e.conversation_id = c.conversation_id
GROUP BY c.model_name
ORDER BY avg_overall_score DESC;

-- View: Scenario difficulty (by completion rates)
CREATE OR REPLACE VIEW scenario_analysis AS
SELECT 
  scenario_id,
  COUNT(*) as total_attempts,
  SUM(CASE WHEN success THEN 1 ELSE 0 END) as successful_completions,
  ROUND(100.0 * SUM(CASE WHEN success THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate,
  AVG(total_turns) as avg_turns,
  AVG(total_tokens) as avg_tokens
FROM conversations
GROUP BY scenario_id
ORDER BY success_rate DESC;

-- View: Recent conversations summary
CREATE OR REPLACE VIEW recent_conversations AS
SELECT 
  c.conversation_id,
  c.scenario_id,
  c.model_name,
  c.total_turns,
  c.success,
  c.total_tokens,
  c.total_latency,
  e.overall_score,
  c.created_at
FROM conversations c
LEFT JOIN evaluations e ON c.conversation_id = e.conversation_id
ORDER BY c.created_at DESC
LIMIT 100;

-- ============================================================================
-- ROW LEVEL SECURITY (Optional - Enable if needed)
-- ============================================================================

-- Enable RLS
-- ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE conversation_turns ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE evaluations ENABLE ROW LEVEL SECURITY;

-- Create policies (adjust as needed)
-- CREATE POLICY "Enable read access for all users" ON conversations FOR SELECT USING (true);
-- CREATE POLICY "Enable insert access for all users" ON conversations FOR INSERT WITH CHECK (true);

-- ============================================================================
-- FUNCTIONS: Useful utilities
-- ============================================================================

-- Function to get conversation with all turns
CREATE OR REPLACE FUNCTION get_full_conversation(conv_id TEXT)
RETURNS JSON AS $$
DECLARE
  result JSON;
BEGIN
  SELECT json_build_object(
    'conversation', (
      SELECT row_to_json(c)
      FROM conversations c
      WHERE c.conversation_id = conv_id
    ),
    'turns', (
      SELECT json_agg(t ORDER BY t.turn_number)
      FROM conversation_turns t
      WHERE t.conversation_id = conv_id
    ),
    'evaluation', (
      SELECT row_to_json(e)
      FROM evaluations e
      WHERE e.conversation_id = conv_id
    )
  ) INTO result;
  
  RETURN result;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- SAMPLE QUERIES
-- ============================================================================

-- Get model performance comparison
-- SELECT * FROM model_performance;

-- Get all conversations for a specific scenario
-- SELECT * FROM conversations WHERE scenario_id = 'A1_late_delivery' ORDER BY created_at DESC;

-- Get average scores by agent type
-- SELECT agent_type, AVG(overall_score) as avg_score
-- FROM conversations c
-- JOIN evaluations e ON c.conversation_id = e.conversation_id
-- GROUP BY agent_type;

-- Get conversation with full details
-- SELECT get_full_conversation('A1_late_delivery_gemini_20251027_143022');

-- ============================================================================
-- NOTES
-- ============================================================================
-- 1. Make sure to enable Realtime if you want live updates in your dashboard
-- 2. Configure RLS policies if you need access control
-- 3. Adjust indexes based on your query patterns
-- 4. Monitor table sizes and consider partitioning for large datasets

-- ✅ Schema created successfully!
-- Now you can use STORAGE_MODE=supabase or STORAGE_MODE=both in your .env file

