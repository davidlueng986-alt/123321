#!/bin/bash
# FinSight AI - Persistent Dev Server Startup Script
# Uses 'tail -f /dev/null' pipe to keep stdin open indefinitely
# so Next.js 16 doesn't exit on stdin EOF in non-TTY environments

export NEXT_TELEMETRY_DISABLED=1
export DATABASE_URL="postgresql://finsight:finsight123@localhost:5432/finsight_ai?schema=public"
export NEXT_PUBLIC_DEMO_MODE=true
export NEXT_PUBLIC_APP_URL=http://localhost:3000
export OPENAI_API_KEY="${OPENAI_API_KEY:-sk-demo-placeholder-key}"
export JWT_SECRET="demo_jwt_secret_key_at_least_32_chars_long"
export ENCRYPTION_KEY="demo_32_char_encryption_key_here!"
export NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY="pk_test_demo_key_placeholder"
export CLERK_SECRET_KEY="sk_test_demo_key_placeholder"

cd /home/user/webapp

echo "Starting FinSight AI dev server (webpack mode)..."

# Use tail -f /dev/null to keep stdin open forever
# This prevents Next.js from detecting stdin EOF and exiting
exec tail -f /dev/null | node_modules/.bin/next dev --webpack --port 3000
