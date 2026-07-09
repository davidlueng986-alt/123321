import { bumpFinanceDataVersion } from "@/lib/redis/cache";

/** Invalidate Redis-backed dashboard and insights caches after financial writes. */
export async function invalidateFinancialCache(): Promise<void> {
  await bumpFinanceDataVersion();
}
