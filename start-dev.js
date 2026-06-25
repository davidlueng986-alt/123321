#!/usr/bin/env node
/**
 * Persistent Next.js dev server wrapper
 * Uses --webpack flag to avoid Turbopack's stdin-detection exit
 */
const { spawn } = require('child_process')
const path = require('path')

const nextBin = path.join(__dirname, 'node_modules', '.bin', 'next')

const env = {
  ...process.env,
  DATABASE_URL: 'postgresql://finsight:finsight123@localhost:5432/finsight_ai?schema=public',
  NEXT_PUBLIC_DEMO_MODE: 'true',
  NEXT_PUBLIC_APP_URL: 'http://localhost:3000',
  OPENAI_API_KEY: process.env.OPENAI_API_KEY || 'sk-demo-placeholder-key',
  JWT_SECRET: 'demo_jwt_secret_key_at_least_32_chars_long',
  ENCRYPTION_KEY: 'demo_32_char_encryption_key_here!',
  NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: 'pk_test_demo_key_placeholder',
  CLERK_SECRET_KEY: 'sk_test_demo_key_placeholder',
  NEXT_TELEMETRY_DISABLED: '1',
}

console.log('Starting FinSight AI dev server (webpack mode)...')

const child = spawn(nextBin, ['dev', '--port', '3000', '--webpack'], {
  cwd: __dirname,
  stdio: 'inherit',
  env,
  detached: false,
})

child.on('error', (err) => {
  console.error('Failed to start Next.js:', err)
  process.exit(1)
})

child.on('exit', (code, signal) => {
  console.log(`Next.js exited: code=${code} signal=${signal}`)
  process.exit(code || 0)
})

// Keep the wrapper alive
setInterval(() => {}, 10000)

process.on('SIGTERM', () => { child.kill('SIGTERM'); process.exit(0) })
process.on('SIGINT',  () => { child.kill('SIGINT'); process.exit(0) })
