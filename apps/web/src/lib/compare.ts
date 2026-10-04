// IDs were reassigned when the obsolete catalog was replaced by Datahouse.
export const COMPARED_STORAGE_KEY = "compare-listings:datahouse-b859bab1";

export function readCompared(): number[] {
  try {
    localStorage.removeItem("compare-listings");
    const data: unknown = JSON.parse(
      localStorage.getItem(COMPARED_STORAGE_KEY) || "[]",
    );
    return Array.isArray(data)
      ? [
          ...new Set(
            data.filter(
              (id): id is number => Number.isSafeInteger(id) && id > 0,
            ),
          ),
        ].slice(0, 3)
      : [];
  } catch {
    return [];
  }
}
