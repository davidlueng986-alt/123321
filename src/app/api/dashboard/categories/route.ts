import { getAuth } from "@/lib/server-auth"
import { prisma } from "@/lib/prisma"
import { apiSuccess, apiError } from "@/lib/rate-limit"
import { getExpensesByCategory } from "@/lib/financial-calculations"

export async function GET() {
  try {
    const { userId, orgId } = await getAuth()
    if (!userId) return apiError("Unauthorized", 401)

    const org = orgId
      ? await prisma.organization.findUnique({ where: { clerkOrgId: orgId } })
      : await prisma.organization.findFirst({ where: { clerkOrgId: `personal_${userId}` } })

    if (!org) return apiSuccess([])

    const categories = await getExpensesByCategory(org.id)
    return apiSuccess(categories)
  } catch (error) {
    console.error("Categories API error:", error)
    return apiError("Failed to fetch categories", 500)
  }
}
