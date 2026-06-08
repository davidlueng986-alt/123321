import { auth, currentUser } from "@clerk/nextjs/server"
import { prisma } from "./prisma"
import { UserRole } from "@prisma/client"

// ─── Get Current User with DB data ──────────────────────────
export async function getCurrentUser() {
  const { userId } = await auth()
  if (!userId) return null

  const clerkUser = await currentUser()
  if (!clerkUser) return null

  // Upsert user in our database
  const user = await prisma.user.upsert({
    where: { clerkId: userId },
    update: {
      email: clerkUser.emailAddresses[0]?.emailAddress ?? "",
      firstName: clerkUser.firstName ?? "",
      lastName: clerkUser.lastName ?? "",
      imageUrl: clerkUser.imageUrl,
      lastLoginAt: new Date(),
    },
    create: {
      clerkId: userId,
      email: clerkUser.emailAddresses[0]?.emailAddress ?? "",
      firstName: clerkUser.firstName ?? "",
      lastName: clerkUser.lastName ?? "",
      imageUrl: clerkUser.imageUrl,
    },
    include: {
      memberships: {
        include: {
          organization: true,
        },
      },
    },
  })

  return user
}

// ─── Get Current Organization ────────────────────────────────
export async function getCurrentOrganization(orgId?: string) {
  const { userId, orgId: clerkOrgId } = await auth()
  if (!userId) return null

  const targetOrgId = orgId ?? clerkOrgId
  if (!targetOrgId) return null

  const org = await prisma.organization.findUnique({
    where: { clerkOrgId: targetOrgId },
  })

  return org
}

// ─── Check User Permission ───────────────────────────────────
export async function checkPermission(
  userId: string,
  organizationId: string,
  allowedRoles: UserRole[]
): Promise<boolean> {
  const membership = await prisma.organizationMember.findUnique({
    where: {
      organizationId_userId: {
        organizationId,
        userId,
      },
    },
  })

  if (!membership || !membership.isActive) return false
  return allowedRoles.includes(membership.role)
}

// ─── Require Auth ────────────────────────────────────────────
export async function requireAuth() {
  const { userId } = await auth()
  if (!userId) {
    throw new Error("Unauthorized: Authentication required")
  }
  return userId
}

// ─── Require Organization ────────────────────────────────────
export async function requireOrganization() {
  const { userId, orgId } = await auth()
  if (!userId) throw new Error("Unauthorized: Authentication required")
  if (!orgId) throw new Error("No organization selected")

  const org = await prisma.organization.findUnique({
    where: { clerkOrgId: orgId },
  })

  if (!org) throw new Error("Organization not found")
  return { userId, orgId, org }
}

// ─── Log Audit Event ─────────────────────────────────────────
export async function logAuditEvent({
  organizationId,
  userId,
  action,
  resource,
  resourceId,
  oldValues,
  newValues,
  ipAddress,
  userAgent,
  metadata,
}: {
  organizationId: string
  userId?: string | null
  action: "CREATE" | "UPDATE" | "DELETE" | "VIEW" | "LOGIN" | "LOGOUT" | "EXPORT" | "IMPORT" | "SHARE"
  resource: string
  resourceId?: string
  oldValues?: Record<string, unknown>
  newValues?: Record<string, unknown>
  ipAddress?: string
  userAgent?: string
  metadata?: Record<string, unknown>
}) {
  try {
    await prisma.auditLog.create({
      data: {
        organizationId,
        userId,
        action,
        resource,
        resourceId,
        oldValues: oldValues as object,
        newValues: newValues as object,
        ipAddress,
        userAgent,
        metadata: metadata as object,
      },
    })
  } catch (error) {
    // Non-blocking audit log
    console.error("Failed to log audit event:", error)
  }
}
