FROM node:22-bookworm-slim AS node_base

WORKDIR /src/frontend

# deps
FROM node_base AS deps

COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* .npmrc* ./
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \
  else echo "Lockfile not found." && exit 1; \
  fi


# builder
FROM node_base AS builder

COPY --from=deps /src/frontend/node_modules ./node_modules
COPY . .

RUN \
  if [ -f yarn.lock ]; then yarn run build; \
  elif [ -f package-lock.json ]; then npm run build; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm run build; \
  else echo "Lockfile not found." && exit 1; \
  fi


# development
FROM node_base AS development

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

COPY --from=deps --chown=node:node /src/frontend/node_modules ./node_modules
COPY --from=builder --chown=node:node /src/frontend/.next ./.next
COPY --chown=node:node . .

USER node

CMD ["npm", "run", "dev"]


# runner
FROM node_base AS runner

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /src/frontend/public ./public
COPY --from=builder --chown=nextjs:nodejs /src/frontend/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /src/frontend/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
