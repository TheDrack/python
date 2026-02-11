-- Migration: Create evolution_rewards table
-- Description: Stores Reinforcement Learning rewards for JARVIS evolution tracking
-- Version: 002
-- Date: 2026-02-11

-- Create the evolution_rewards table
CREATE TABLE IF NOT EXISTS evolution_rewards (
    id SERIAL PRIMARY KEY,
    action_type VARCHAR(100) NOT NULL,
    reward_value FLOAT NOT NULL,
    context_data JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on action_type for faster filtering
CREATE INDEX IF NOT EXISTS idx_rewards_action_type ON evolution_rewards(action_type);

-- Create index on created_at for time-based queries
CREATE INDEX IF NOT EXISTS idx_rewards_created_at ON evolution_rewards(created_at DESC);

-- Create index on reward_value for aggregation queries
CREATE INDEX IF NOT EXISTS idx_rewards_value ON evolution_rewards(reward_value);

-- Comments for documentation
COMMENT ON TABLE evolution_rewards IS 'JARVIS Reinforcement Learning reward tracking for evolution and self-improvement';
COMMENT ON COLUMN evolution_rewards.id IS 'Unique reward entry identifier';
COMMENT ON COLUMN evolution_rewards.action_type IS 'Type of action: pytest_pass, pytest_fail, deploy_success, deploy_fail, roadmap_progress, etc.';
COMMENT ON COLUMN evolution_rewards.reward_value IS 'Reward points (positive for success, negative for failure)';
COMMENT ON COLUMN evolution_rewards.context_data IS 'JSON context about the action (test names, error messages, metrics, etc.)';
COMMENT ON COLUMN evolution_rewards.metadata IS 'Additional metadata (user_id, session_id, deployment_id, etc.)';
COMMENT ON COLUMN evolution_rewards.created_at IS 'Timestamp when the reward was logged';
