/**
 * Server-side auth abstraction layer.
 * 
 * In DEMO_MODE, returns a fixed demo user without calling Clerk.
 * In production, delegates to Clerk's auth().
 */

const DEMO_USER_ID = "demo_user_001"
const DEMO_ORG_ID = null

export async function getAuth() {
  if (process.env.NEXT_PUBLIC_DEMO_MODE === "true") {
    return {
      userId: DEMO_USER_ID as string | null,
      orgId: DEMO_ORG_ID as string | null,
      sessionId: "demo_session_001" as string | null,
    }
  }

  // Real Clerk auth
  const { auth } = await import("@clerk/nextjs/server")
  const result = await auth()
  return {
    userId: result.userId,
    orgId: result.orgId,
    sessionId: result.sessionId,
  }
}
