<script lang="ts">
  /**
   * SEO Component
   *
   * Handles all meta tags for search engines and social sharing.
   * Place in <svelte:head> section of any page.
   */

  export let title: string;
  export let description: string;
  export let keywords: string[] = [];
  export let canonical: string = '';
  export let noindex: boolean = false;

  // Open Graph
  export let ogTitle: string = '';
  export let ogDescription: string = '';
  export let ogImage: string = '';
  export let ogImageAlt: string = '';
  export let ogType: 'website' | 'article' | 'product' = 'website';

  // Twitter Card
  export let twitterCard: 'summary' | 'summary_large_image' = 'summary_large_image';
  export let twitterTitle: string = '';
  export let twitterDescription: string = '';
  export let twitterImage: string = '';
  export let twitterSite: string = '@highloera';
  export let twitterCreator: string = '@highera';

  // Structured Data (JSON-LD)
  export let schema: object | null = null;

  // Computed values with fallbacks
  $: computedOgTitle = ogTitle || title;
  $: computedOgDescription = ogDescription || description;
  $: computedTwitterTitle = twitterTitle || ogTitle || title;
  $: computedTwitterDescription = twitterDescription || ogDescription || description;
  $: computedTwitterImage = twitterImage || ogImage;
  $: computedOgImageAlt = ogImageAlt || title;
</script>

<!-- Primary Meta Tags -->
<title>{title}</title>
<meta name="title" content={title} />
<meta name="description" content={description} />

{#if keywords.length > 0}
  <meta name="keywords" content={keywords.join(', ')} />
{/if}

{#if canonical}
  <link rel="canonical" href={canonical} />
{/if}

{#if noindex}
  <meta name="robots" content="noindex, nofollow" />
{:else}
  <meta name="robots" content="index, follow" />
{/if}

<!-- Open Graph / Facebook -->
<meta property="og:type" content={ogType} />
<meta property="og:title" content={computedOgTitle} />
<meta property="og:description" content={computedOgDescription} />

{#if ogImage}
  <meta property="og:image" content={ogImage} />
  <meta property="og:image:alt" content={computedOgImageAlt} />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
{/if}

{#if canonical}
  <meta property="og:url" content={canonical} />
{/if}

<meta property="og:site_name" content="High Era" />

<!-- Twitter Card -->
<meta name="twitter:card" content={twitterCard} />
<meta name="twitter:site" content={twitterSite} />
<meta name="twitter:creator" content={twitterCreator} />
<meta name="twitter:title" content={computedTwitterTitle} />
<meta name="twitter:description" content={computedTwitterDescription} />

{#if computedTwitterImage}
  <meta name="twitter:image" content={computedTwitterImage} />
{/if}

<!-- Structured Data (JSON-LD) -->
{#if schema}
  {@html `<script type="application/ld+json">${JSON.stringify(schema)}</script>`}
{/if}
