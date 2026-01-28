import { getAudience, getAudienceSlugs } from '$lib/data/audiences';
import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = ({ params }) => {
  const audience = getAudience(params.audience);

  if (!audience) {
    throw error(404, 'Audience not found');
  }

  return {
    audience
  };
};

// Pre-render all audience pages
export const prerender = true;

export function entries() {
  return getAudienceSlugs().map(slug => ({ audience: slug }));
}
