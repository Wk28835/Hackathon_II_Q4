// phase_ii/web/lib/auth.ts
import { betterAuth } from "better-auth";
import { nextCookies } from "better-auth/next-js";
import { Pool } from "pg";

// Retrieve secret explicitly
const secret = process.env.BETTER_AUTH_SECRET;
if (!secret) {
  throw new Error("BETTER_AUTH_SECRET is not defined");
}

// Get database URL
const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) {
  throw new Error("DATABASE_URL is not defined");
}

// Create PostgreSQL pool for Neon
const pool = new Pool({
  connectionString: databaseUrl,
  ssl: {
    rejectUnauthorized: false,
  },
});

export const auth = betterAuth({
  secret: secret,
  baseURL: process.env.BETTER_AUTH_URL,
  plugins: [nextCookies()],
  
  // Enable email and password authentication
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 6,
  },
  
  // Use Neon PostgreSQL database
  database: pool,

  session: {
    expiresIn: 24 * 60 * 60, // 30 days
    updateAge: 24 * 60 * 60, // 24 hours
  },
});
