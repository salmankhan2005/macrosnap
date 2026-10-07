---
name: MacroSnap
colors:
  surface: '#f9faef'
  surface-dim: '#d9dbd0'
  surface-bright: '#f9faef'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f5e9'
  surface-container: '#edefe4'
  surface-container-high: '#e7e9de'
  surface-container-highest: '#e2e3d9'
  on-surface: '#1a1d16'
  on-surface-variant: '#424843'
  inverse-surface: '#2e312a'
  inverse-on-surface: '#f0f2e7'
  outline: '#727972'
  outline-variant: '#c2c8c1'
  surface-tint: '#456551'
  primary: '#43634f'
  on-primary: '#ffffff'
  primary-container: '#5b7c66'
  on-primary-container: '#f6fff5'
  inverse-primary: '#accfb6'
  secondary: '#44664f'
  on-secondary: '#ffffff'
  secondary-container: '#c3e9cc'
  on-secondary-container: '#486a53'
  tertiary: '#605b51'
  on-tertiary: '#ffffff'
  tertiary-container: '#797469'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#c7ebd1'
  primary-fixed-dim: '#accfb6'
  on-primary-fixed: '#012111'
  on-primary-fixed-variant: '#2e4d3a'
  secondary-fixed: '#c6eccf'
  secondary-fixed-dim: '#aacfb4'
  on-secondary-fixed: '#002110'
  on-secondary-fixed-variant: '#2d4e38'
  tertiary-fixed: '#e9e2d4'
  tertiary-fixed-dim: '#cdc6b8'
  on-tertiary-fixed: '#1e1b13'
  on-tertiary-fixed-variant: '#4b463c'
  background: '#f9faef'
  on-background: '#1a1d16'
  surface-variant: '#e2e3d9'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 3.5rem
    fontWeight: '700'
    lineHeight: 4.25rem
    letterSpacing: -0.03em
  display-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 2.5rem
    fontWeight: '700'
    lineHeight: 3rem
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 2.25rem
    fontWeight: '600'
    lineHeight: 2.75rem
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 1.75rem
    fontWeight: '600'
    lineHeight: 2.25rem
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 1.5rem
    fontWeight: '600'
    lineHeight: 2rem
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 1.25rem
    fontWeight: '600'
    lineHeight: 1.75rem
    letterSpacing: 0em
  title-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 1.125rem
    fontWeight: '500'
    lineHeight: 1.625rem
    letterSpacing: 0em
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 1.125rem
    fontWeight: '400'
    lineHeight: 1.75rem
    letterSpacing: 0em
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 1rem
    fontWeight: '400'
    lineHeight: 1.5rem
    letterSpacing: 0em
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 0.875rem
    fontWeight: '400'
    lineHeight: 1.25rem
    letterSpacing: 0.005em
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 0.875rem
    fontWeight: '600'
    lineHeight: 1.25rem
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 0.75rem
    fontWeight: '600'
    lineHeight: 1rem
    letterSpacing: 0.04em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 2rem
  margin-mobile: 1.25rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system establishes an empathetic, mindful, and editorial wellness presence. It merges the warmth of high-end editorial health publications with the seamless utility of an AI-powered nutrition companion. 

Rather than clinical judgment or aggressive fitness metrics, the interface communicates nourishment, balanced living, and effortless clarity. The aesthetic follows modern organic minimalism: vast warm breathing room, tactile card containers, grounded botanical tones, and human-centric geometric typography. Interactions are smooth, non-punitive, and calm, evoking a feeling of supportive daily guidance.

## Colors

The palette draws directly from muted botanicals and natural linens, eliminating harsh electronic whites and high-contrast blacks in favor of organic warmth.

- **Primary (`#64856F`)**: Calming sage green. Serves as the key brand touchstone, primary action background, active states, and focused accents.
- **Secondary / Deep Accent (`#496B54`)**: Forest sage shade. Used for hover states, deep interactive accents, and high-emphasis focal items.
- **Tertiary / Warm Highlight (`#F3EBDD`)**: Warm linen tone. Dedicated to caloric metrics, nutritional highlights, celebratory badges, and soft feature calls.
- **Surface Canvas (`#F7F7F2`)**: Warm ivory foundation. Grounds all screen surfaces with an organic warmth.
- **Surface Card (`#FFFFFF`)**: Pure crisp white. Elevates primary modular cards and dialogs above the ivory canvas.
- **Accent Surface (`#EDF2EE`)**: Light sage tint. Reserved for chip fills, table headers, visual badges, and quiet tertiary button states.
- **Neutral Primary (`#252821`)**: Soft charcoal timber. Applied across headlines, high-priority labels, and readable body text.
- **Neutral Secondary (`#74796F`)**: Muted moss grey. Dedicated to timestamps, macro subtitles, captions, and de-emphasized metadata.
- **Subtle Border (`#E8E9E1`)**: Warm stone divider. Provides structural definition without introducing visual clutter.

## Typography

Typography relies uniformly on Plus Jakarta Sans to deliver an approachable, geometric clarity with friendly humanist nuances.

- Headings use medium to bold weights (`600` and `700`) paired with subtle negative tracking (`-0.01em` to `-0.03em`), generating an editorial rhythm reminiscent of contemporary culinary and health magazines.
- Numerical macro metrics (calories, protein, carbs, fat) should utilize tabular numeric figures (`font-variant-numeric: tabular-nums`) to prevent jitter across dynamic updates.
- Micro-labels and tag metadata leverage `label-sm` with slight positive tracking to ensure effortless legibility on smaller mobile contexts.

## Layout & Spacing

The layout philosophy centers on a fluid, airy 12-column grid for desktop environments (max container width: `1200px`) transitioning into an adaptive 4-column layout on mobile viewports.

- Generous whitespace is fundamental: meal logging, nutrition charts, and camera captures must never feel cramped. Section containers embrace ample vertical margins (`margin: 2rem` scaling to `1.25rem` on mobile devices).
- Inner component gaps and card padding are strictly driven by the 4px base scale tokens (`space-xs` through `space-xl`).
- High-density lists (such as granular ingredient listings) use `space-sm` for horizontal item separations, while dashboard panels use `space-lg` and `space-xl` to frame distinct meals and analytics.

## Elevation & Depth

Visual hierarchy uses a refined hybrid of soft tonal layering and warm ambient shadows.

- **Level 0 (Base)**: Flat canvas surface (`#F7F7F2`) with zero shadow.
- **Level 1 (Cards & Modules)**: Surfaces (`#FFFFFF`) with a hairline border (`1px solid #E8E9E1`) and a delicate ambient shadow: `0px 2px 8px -2px rgba(37, 40, 33, 0.04), 0px 1px 3px 0px rgba(37, 40, 33, 0.02)`.
- **Level 2 (Hover & Floating Elements)**: Meal cards upon selection, active capture overlays, and floating summary drawers: `0px 8px 24px -4px rgba(37, 40, 33, 0.06), 0px 2px 6px -1px rgba(37, 40, 33, 0.03)`.
- **Level 3 (Modals & Snapped Sheets)**: Camera analysis modals and bottom nutrition sheets: `0px 16px 36px -6px rgba(37, 40, 33, 0.08), 0px 4px 12px -2px rgba(37, 40, 33, 0.04)`.

## Shapes

The shape identity is defined by gentle, welcoming curvature using level 2 roundedness (`0.5rem` / `8px` base).

- Standard interactive controls, inputs, and chips leverage `rounded` (`0.5rem`).
- Modular wellness panels, nutrition breakdown cards, and image snapshot previews scale to `rounded-lg` (`1rem`).
- Bottom sheets, modal containers, and macro summary banners adopt `rounded-xl` (`1.5rem`).
- Pill containers (`rounded-full`) are strictly reserved for progress indicator caps, circular image viewports, and floating action triggers.

## Components

### Buttons
- **Primary**: Solid `#64856F` background with `#FFFFFF` text. Height of `44px` on desktop, `48px` on mobile touch targets. Smooth transition to `#496B54` on hover/active. Border radius is `rounded` (`0.5rem`).
- **Secondary / Soft**: Subtle `#EDF2EE` background with `#252821` text. Transitions to a 10% opacity darkening on hover.
- **Ghost**: Transparent background with `#64856F` text, hovering to `#EDF2EE`.

### Chips & Badges
- **Nutritional Chips**: Background `#EDF2EE`, text `#496B54`, font size `label-sm`. Used for tags like "High Protein", "Gluten-Free", or meal types.
- **Calorie & Highlight Badges**: Background `#F3EBDD`, text `#252821`, bold `0.75rem` numbering. Used for quick-glance daily caloric counts and AI confidence scores.

### Input Fields & Search
- Inputs feature a crisp `#FFFFFF` background, `#252821` text, `#74796F` placeholder, and a `1px solid #E8E9E1` border.
- Active focus smoothly transitions the border to `#64856F` with a soft outer glow (`0 0 0 3px rgba(100, 133, 111, 0.15)`).

### Cards
- Base surface of `#FFFFFF`, wrapped with a subtle border `#E8E9E1` and `rounded-lg` (`1rem`) geometry.
- Content structured with `space-lg` inner padding, segregating meal snapshots, macro progress rings, and textual breakdowns cleanly.

### Checkboxes & Radio Buttons
- Custom square (`rounded: 0.25rem`) and circular forms with an `#E8E9E1` resting border. 
- When selected, fills with `#64856F` displaying a clean `#FFFFFF` checkmark or center pip.

### Domain-Specific Components (AI Macro Tracker)
- **Macro Distribution Bars**: Segmented horizontal progress tracks featuring soft rounded caps. Colors: Protein (Deep Sage `#496B54`), Carbs (Calming Sage `#64856F`), Fat (Warm Linen `#F3EBDD`).
- **Snap Preview Viewfinder**: A translucent camera viewfinder frame utilizing thin `#FFFFFF` corner brackets over camera feeds with a floating `#64856F` AI capture button.