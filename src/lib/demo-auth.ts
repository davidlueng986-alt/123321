/**
 * Demo Authentication Module
 * 
 * This module provides a Clerk-compatible auth interface that works without
 * real Clerk credentials. Used for local development and testing.
 * 
 * When NEXT_PUBLIC_DEMO_MODE=true, all auth functions return a fixed demo user.
 */

export const DEMO_USER_ID = "demo_user_001"
export const DEMO_ORG_ID = null // Solo user mode - no org (uses personal org)

export interface DemoAuthResult {
  userId: string | null
  orgId: string | null
  sessionId: string | null
}

export function getDemoAuth(): DemoAuthResult {
  return {
    userId: DEMO_USER_ID,
    orgId: DEMO_ORG_ID,
    sessionId: "demo_session_001",
  }
}

export const isDemoMode = () => process.env.NEXT_PUBLIC_DEMO_MODE === "true"
