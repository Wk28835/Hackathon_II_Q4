-- Better Auth Required Tables for PostgreSQL/Neon
-- Run this SQL in Neon console or via psql

-- User table
CREATE TABLE IF NOT EXISTS "user" (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    "emailVerified" BOOLEAN DEFAULT FALSE,
    image TEXT,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Session table
CREATE TABLE IF NOT EXISTS "session" (
    id TEXT PRIMARY KEY,
    "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    token TEXT NOT NULL UNIQUE,
    "expiresAt" TIMESTAMP NOT NULL,
    "ipAddress" TEXT,
    "userAgent" TEXT,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Account table (for OAuth and credentials)
CREATE TABLE IF NOT EXISTS "account" (
    id TEXT PRIMARY KEY,
    "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    "accountId" TEXT NOT NULL,
    "providerId" TEXT NOT NULL,
    "accessToken" TEXT,
    "refreshToken" TEXT,
    "accessTokenExpiresAt" TIMESTAMP,
    "refreshTokenExpiresAt" TIMESTAMP,
    "scope" TEXT,
    "idToken" TEXT,
    password TEXT,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Verification table
CREATE TABLE IF NOT EXISTS "verification" (
    id TEXT PRIMARY KEY,
    identifier TEXT NOT NULL,
    value TEXT NOT NULL,
    "expiresAt" TIMESTAMP NOT NULL,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_session_user ON "session"("userId");
CREATE INDEX IF NOT EXISTS idx_session_token ON "session"(token);
CREATE INDEX IF NOT EXISTS idx_account_user ON "account"("userId");
CREATE INDEX IF NOT EXISTS idx_user_email ON "user"(email);
