export function readCompared(): number[] {
  try {
    const data: unknown = JSON.parse(
      localStorage.getItem("compare-listings") || "[]",
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
