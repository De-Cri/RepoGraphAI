export function normalizeSlug(value: string): string {
  return value.trim().toLowerCase().replace(/\s+/g, "-");
}

export function buildRoute(slug: string): string {
  return withPrefix(slug);
}

function withPrefix(slug: string): string {
  return `/pages/${slug}`;
}
