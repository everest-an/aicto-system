-- database_supervision.sql
-- PM全访问账户创建
CREATE USER pm_supervisor WITH PASSWORD 'encrypted_secure_password';
GRANT ALL PRIVILEGES ON DATABASE your_project TO pm_supervisor;

-- 监督专用表
CREATE TABLE pm_supervision_log (
    id SERIAL PRIMARY KEY,
    feature_name VARCHAR(255),
    completion_percentage INTEGER,
    missing_components TEXT[],
    audit_timestamp TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50)
);

CREATE TABLE development_milestones (
    id SERIAL PRIMARY KEY,
    project_id INTEGER,
    milestone_name VARCHAR(255),
    expected_completion DATE,
    actual_completion DATE,
    blockers TEXT[],
    assigned_developer VARCHAR(100)
);

CREATE TABLE pm_intervention_required (
    id SERIAL PRIMARY KEY,
    feature_name VARCHAR(255),
    missing_components TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

-- 自动化监督函数
CREATE OR REPLACE FUNCTION check_feature_completion()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.completion_percentage < 100 THEN
        INSERT INTO pm_intervention_required (feature_name, missing_components)
        VALUES (NEW.feature_name, NEW.missing_components);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 创建触发器
CREATE TRIGGER feature_completion_check
AFTER INSERT OR UPDATE ON pm_supervision_log
FOR EACH ROW
EXECUTE FUNCTION check_feature_completion();

