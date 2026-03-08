import { buildRoute, normalizeSlug } from "./router";

export class PageController {
  renderPage(rawSlug: string): string {
    const slug = normalizeSlug(rawSlug);
    return buildRoute(slug);
  }

  trackPageView(slug: string): void {
    sendMetric(slug);
  }
}

export function sendMetric(slug: string): void {
  console.log(`metric:${slug}`);
}
