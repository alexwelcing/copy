/**
 * Conversion Tracking and Analytics
 *
 * Unified tracking for:
 * - Google Analytics 4 (GA4)
 * - Google Ads conversion tracking
 * - Meta/Facebook Pixel
 * - LinkedIn Insight Tag
 * - Twitter Pixel
 */

import { browser } from '$app/environment';

// Types for tracking events
export interface ConversionEvent {
  event: string;
  category?: string;
  label?: string;
  value?: number;
  currency?: string;
  // Audience segmentation
  audience_type?: string;
  // UTM attribution
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  utm_content?: string;
  // Custom dimensions
  skill_used?: string;
  plan_type?: string;
}

// =============================================================================
// UTM PARAMETER HANDLING
// =============================================================================

export function getStoredUTM(): Record<string, string> {
  if (!browser) return {};

  const params: Record<string, string> = {};
  const utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];

  utmKeys.forEach(key => {
    const value = sessionStorage.getItem(key);
    if (value) params[key] = value;
  });

  return params;
}

export function storeUTMFromURL(): void {
  if (!browser) return;

  const params = new URLSearchParams(window.location.search);
  const utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];

  utmKeys.forEach(key => {
    const value = params.get(key);
    if (value) {
      sessionStorage.setItem(key, value);
    }
  });

  // Also store landing page
  if (!sessionStorage.getItem('landing_page')) {
    sessionStorage.setItem('landing_page', window.location.pathname);
  }
}

// =============================================================================
// GOOGLE ANALYTICS 4
// =============================================================================

declare global {
  interface Window {
    gtag?: (...args: any[]) => void;
    dataLayer?: any[];
    fbq?: (...args: any[]) => void;
    _linkedin_data_partner_ids?: string[];
    lintrk?: (...args: any[]) => void;
    twq?: (...args: any[]) => void;
  }
}

export function trackGA4Event(event: ConversionEvent): void {
  if (!browser || typeof window.gtag !== 'function') return;

  const utm = getStoredUTM();

  window.gtag('event', event.event, {
    event_category: event.category,
    event_label: event.label,
    value: event.value,
    currency: event.currency,
    audience_type: event.audience_type,
    skill_used: event.skill_used,
    plan_type: event.plan_type,
    // Attribution
    ...utm
  });
}

// =============================================================================
// GOOGLE ADS CONVERSIONS
// =============================================================================

export interface GoogleAdsConversion {
  conversionId: string;
  conversionLabel: string;
  value?: number;
  currency?: string;
}

// Conversion IDs (set these in environment)
export const GOOGLE_ADS_CONVERSIONS = {
  signup: {
    conversionId: 'AW-XXXXXXXXX',
    conversionLabel: 'XXXXXXXX'
  },
  skill_used: {
    conversionId: 'AW-XXXXXXXXX',
    conversionLabel: 'XXXXXXXX'
  },
  lead_captured: {
    conversionId: 'AW-XXXXXXXXX',
    conversionLabel: 'XXXXXXXX'
  }
};

export function trackGoogleAdsConversion(
  conversion: GoogleAdsConversion
): void {
  if (!browser || typeof window.gtag !== 'function') return;

  window.gtag('event', 'conversion', {
    send_to: `${conversion.conversionId}/${conversion.conversionLabel}`,
    value: conversion.value,
    currency: conversion.currency || 'USD'
  });
}

// =============================================================================
// META/FACEBOOK PIXEL
// =============================================================================

export function trackMetaEvent(
  event: string,
  params?: Record<string, any>
): void {
  if (!browser || typeof window.fbq !== 'function') return;

  window.fbq('track', event, params);
}

// Standard Meta events
export const MetaEvents = {
  pageView: () => trackMetaEvent('PageView'),
  lead: (value?: number) => trackMetaEvent('Lead', { value, currency: 'USD' }),
  signup: () => trackMetaEvent('CompleteRegistration'),
  startTrial: () => trackMetaEvent('StartTrial'),
  subscribe: (value: number) => trackMetaEvent('Subscribe', { value, currency: 'USD' })
};

// =============================================================================
// LINKEDIN INSIGHT TAG
// =============================================================================

export function trackLinkedInConversion(conversionId: string): void {
  if (!browser || typeof window.lintrk !== 'function') return;

  window.lintrk('track', { conversion_id: conversionId });
}

// LinkedIn conversion IDs
export const LINKEDIN_CONVERSIONS = {
  signup: 'XXXXXXX',
  demo_request: 'XXXXXXX',
  content_download: 'XXXXXXX'
};

// =============================================================================
// TWITTER PIXEL
// =============================================================================

export function trackTwitterEvent(
  event: string,
  params?: Record<string, any>
): void {
  if (!browser || typeof window.twq !== 'function') return;

  window.twq('event', event, params);
}

// Twitter events
export const TwitterEvents = {
  pageView: () => trackTwitterEvent('PageView'),
  signup: () => trackTwitterEvent('tw-XXXXX-XXXXX'),
  lead: () => trackTwitterEvent('tw-XXXXX-XXXXX')
};

// =============================================================================
// UNIFIED CONVERSION TRACKING
// =============================================================================

export type ConversionType =
  | 'page_view'
  | 'signup'
  | 'skill_used'
  | 'lead_captured'
  | 'cta_click'
  | 'demo_request'
  | 'plan_selected';

export function trackConversion(
  type: ConversionType,
  data?: Partial<ConversionEvent>
): void {
  if (!browser) return;

  const utm = getStoredUTM();
  const fullData: ConversionEvent = {
    event: type,
    ...data,
    ...utm
  };

  // GA4
  trackGA4Event(fullData);

  // Google Ads
  if (type === 'signup' && GOOGLE_ADS_CONVERSIONS.signup) {
    trackGoogleAdsConversion(GOOGLE_ADS_CONVERSIONS.signup);
  }
  if (type === 'skill_used' && GOOGLE_ADS_CONVERSIONS.skill_used) {
    trackGoogleAdsConversion(GOOGLE_ADS_CONVERSIONS.skill_used);
  }
  if (type === 'lead_captured' && GOOGLE_ADS_CONVERSIONS.lead_captured) {
    trackGoogleAdsConversion(GOOGLE_ADS_CONVERSIONS.lead_captured);
  }

  // Meta
  if (type === 'page_view') MetaEvents.pageView();
  if (type === 'signup') MetaEvents.signup();
  if (type === 'lead_captured') MetaEvents.lead(data?.value);

  // LinkedIn
  if (type === 'signup') trackLinkedInConversion(LINKEDIN_CONVERSIONS.signup);
  if (type === 'demo_request') trackLinkedInConversion(LINKEDIN_CONVERSIONS.demo_request);

  // Twitter
  if (type === 'page_view') TwitterEvents.pageView();
  if (type === 'signup') TwitterEvents.signup();
  if (type === 'lead_captured') TwitterEvents.lead();

  // Console log in development
  if (import.meta.env.DEV) {
    console.log('[Tracking]', type, fullData);
  }
}

// =============================================================================
// AUDIENCE-SPECIFIC TRACKING
// =============================================================================

export function trackAudiencePageView(audience: string): void {
  trackConversion('page_view', {
    category: 'audience_page',
    label: audience,
    audience_type: audience
  });
}

export function trackSkillUsed(skill: string, audience?: string): void {
  trackConversion('skill_used', {
    category: 'engagement',
    label: skill,
    skill_used: skill,
    audience_type: audience
  });
}

export function trackCTAClick(
  cta: string,
  location: string,
  audience?: string
): void {
  trackConversion('cta_click', {
    category: 'engagement',
    label: `${location}:${cta}`,
    audience_type: audience
  });
}

export function trackLeadCaptured(
  source: string,
  audience?: string
): void {
  trackConversion('lead_captured', {
    category: 'conversion',
    label: source,
    audience_type: audience
  });
}
