CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

--------------------------------------------------
-- USERS
--------------------------------------------------

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--------------------------------------------------
-- QUESTIONS
--------------------------------------------------

CREATE TABLE questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    title VARCHAR(255) NOT NULL,

    platform VARCHAR(50) NOT NULL,

    topic VARCHAR(100) NOT NULL,

    pattern VARCHAR(100) NOT NULL,

    difficulty VARCHAR(20) NOT NULL,

    tags TEXT,

    url TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--------------------------------------------------
-- SOLVES
--------------------------------------------------

CREATE TABLE solves (

    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    user_id UUID NOT NULL,

    question_id UUID NOT NULL,

    solved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    time_taken_minutes INTEGER,

    wrong_attempts INTEGER DEFAULT 0,

    hints_used INTEGER DEFAULT 0,

    confidence_score FLOAT,

    CONSTRAINT fk_solves_user
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_solves_question
        FOREIGN KEY(question_id)
        REFERENCES questions(id)
        ON DELETE CASCADE
);

--------------------------------------------------
-- REVISIONS
--------------------------------------------------

CREATE TABLE revisions (

    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    user_id UUID NOT NULL,

    question_id UUID NOT NULL,

    revised_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    revision_quality FLOAT,

    CONSTRAINT fk_revision_user
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_revision_question
        FOREIGN KEY(question_id)
        REFERENCES questions(id)
        ON DELETE CASCADE
);

--------------------------------------------------
-- RECOMMENDATIONS
--------------------------------------------------

CREATE TABLE recommendations (

    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    user_id UUID NOT NULL,

    question_id UUID NOT NULL,

    recommendation_score FLOAT,

    forget_probability FLOAT,

    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_recommendation_user
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_recommendation_question
        FOREIGN KEY(question_id)
        REFERENCES questions(id)
        ON DELETE CASCADE
);



CREATE INDEX idx_solves_user
ON solves(user_id);

CREATE INDEX idx_solves_question
ON solves(question_id);

CREATE INDEX idx_revision_user
ON revisions(user_id);

CREATE INDEX idx_recommendation_user
ON recommendations(user_id);

CREATE INDEX idx_question_topic
ON questions(topic);

CREATE INDEX idx_question_pattern
ON questions(pattern);