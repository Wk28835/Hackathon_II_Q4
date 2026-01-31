// phase_ii/web/lib/auth.ts
import { betterAuth } from "better-auth";
import { nextCookies } from "better-auth/next-js";
import { Pool } from "pg";

// Explicitly check for secret to prevent hidden crashes
if (!process.env.BETTER_AUTH_SECRET) throw new Error("Missing BETTER_AUTH_SECRET");

// Singleton for DB Pool
const globalForPool = globalThis as unknown as { pool: Pool };
const pool = globalForPool.pool || new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});
if (process.env.NODE_ENV !== 'production') globalForPool.pool = pool;

// Singleton for Auth Instance
const globalForAuth = globalThis as unknown as { auth: any };

export const auth = globalForAuth.auth || betterAuth({
  database: pool,
  secret: process.env.BETTER_AUTH_SECRET,
  baseURL: process.env.BETTER_AUTH_URL,
  plugins: [nextCookies()], // Keep this as the ONLY plugin for now
  emailAndPassword: { enabled: true },
});

if (process.env.NODE_ENV !== 'production') globalForAuth.auth = auth;