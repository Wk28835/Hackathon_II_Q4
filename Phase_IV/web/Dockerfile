# ========================================
# Stage 1: Dependencies
# ========================================
ARG NODE_VERSION=24.11.1-alpine
FROM node:${NODE_VERSION} AS deps

WORKDIR /app

COPY package*.json ./

RUN npm ci --omit=dev

# ========================================
# Stage 2: Build Dependencies
# ========================================
FROM node:${NODE_VERSION} AS build-deps

WORKDIR /app

COPY package*.json ./

RUN npm ci --omit=dev

# ========================================
# Stage 3: Builder
# ========================================
FROM build-deps AS builder

# Declare ARGs to capture values from --build-arg
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_BETTER_AUTH_URL

# Set build-time environment variables for Next.js to "bake in"
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL} \
    NEXT_PUBLIC_BETTER_AUTH_URL=${NEXT_PUBLIC_BETTER_AUTH_URL}

# Private Secrets (No NEXT_PUBLIC prefix - safe for build stage)
ENV BETTER_AUTH_SECRET="build-time-secret-replace-at-runtime" \
    DATABASE_URL="postgresql://dummy:dummy@localhost:5432/dummy" \
    QDRANT_URL="http://localhost:6333" \
    QDRANT_API_KEY="build-time-key" \
    GEMINI_API_KEY="build-time-key" \
    QDRANT_COLLECTION="dummy" \
    EMBEDDING_PROVIDER="gemini" \
    EMBEDDING_MODEL="text-embedding-004"

COPY . .

# Next.js will now see the todo.test URLs during this command
RUN npm run build

# ========================================
# Stage 4: Production
# ========================================
FROM node:${NODE_VERSION} AS production

WORKDIR /app

# Ensure the production stage also has access to the public URL envs
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_BETTER_AUTH_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL \
    NEXT_PUBLIC_BETTER_AUTH_URL=$NEXT_PUBLIC_BETTER_AUTH_URL

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs

# Set environment for production
ENV NODE_ENV=production \
    NODE_OPTIONS="--max-old-space-size=256 --no-warnings" \
    NPM_CONFIG_LOGLEVEL=silent

# Copy production dependencies
COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=deps --chown=nodejs:nodejs /app/package*.json ./

# Copy built application
COPY --from=builder --chown=nodejs:nodejs /app/.next ./.next
COPY --from=builder --chown=nodejs:nodejs /app/public ./public

# Health check for Kubernetes
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})"

# Switch to non-root user
USER nodejs

EXPOSE 3000

CMD ["node_modules/.bin/next", "start"]