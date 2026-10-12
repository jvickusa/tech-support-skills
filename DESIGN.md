---
name: Tech Support Skills Reports
description: The website's readable evidence surfaces, adapted to standalone troubleshooting documents.
colors:
  canvas: "#f2f6fd"
  surface: "#fff"
  ink: "#14294b"
  muted: "#526580"
  line: "#d3deee"
  blue: "#2457d6"
  soft: "#e5edfe"
  yellow: "#f4c84a"
  conclusion: "#173b91"
  on-conclusion: "#f4f7ff"
  confidence: "#d0ddf6"
  dark-canvas: "#101d35"
  dark-surface: "#1a2d4a"
  dark-ink: "#edf4ff"
  dark-muted: "#b6c7df"
  dark-line: "#354a68"
  dark-blue: "#8fb4ff"
  dark-soft: "#233c64"
typography:
  display:
    fontFamily: "Barlow Condensed, Arial Narrow, sans-serif"
    fontSize: "clamp(2.75rem, 6vw, 4.5rem)"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.018em"
  headline:
    fontFamily: "Barlow Condensed, Arial Narrow, sans-serif"
    fontSize: "2rem"
    fontWeight: 700
    lineHeight: 1.1
  title:
    fontFamily: "Barlow Condensed, Arial Narrow, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 700
    lineHeight: 1.1
  body:
    fontFamily: "Atkinson, Segoe UI, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
  secondary:
    fontFamily: "Atkinson, Segoe UI, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.6
rounded:
  appendix: "6px"
  next: "10px"
  conclusion: "14px"
spacing:
  small: "8px"
  compact: "12px"
  paragraph: "16px"
  inset: "20px"
  group: "24px"
  section: "32px"
components:
  conclusion:
    backgroundColor: "{colors.conclusion}"
    textColor: "{colors.on-conclusion}"
    rounded: "{rounded.conclusion}"
    padding: "28px 32px"
  next-actions:
    backgroundColor: "{colors.soft}"
    textColor: "{colors.ink}"
    rounded: "{rounded.next}"
    padding: "24px 28px"
  evidence-appendix:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.appendix}"
    padding: "20px"
---

# Design System: Tech Support Skills Reports

## Overview

Inherits Why Is My Internet Crap?'s condensed headings, readable body type, cool reading surfaces, and blue evidence panel. Report mode uses one continuous document: conclusion first, supporting evidence beneath, practical actions clearly marked. No separate visual identity.

Source: `skills/internet-diagnostics/assets/report.html`; identity reference: sibling `crap-internet/DESIGN.md`. HTML and Markdown share semantic hierarchy; HTML supplies visual tokens. Sections adapt to each investigation rather than imposing a measurement schema.

## Colors

### Primary

Blue identifies links and the conclusion panel. Conclusion foreground and confidence colors stay paired with their fixed blue surface in both screen themes. Yellow appears in text selection, inherited from the website's action accent.

### Neutral

Canvas surrounds the reading sheet. Ink carries evidence, muted text carries metadata and limitations, lines separate groups, and soft tint marks next actions. System dark mode replaces the neutral and link tokens together. Print restores white paper and dark text, including the conclusion.

**Evidence rule.** Written labels distinguish observations, comparisons, hypotheses, confidence, and unknowns. Color alone never carries evidentiary status.

## Typography

Barlow Condensed Bold gives headings the website's direct voice. Atkinson Hyperlegible Regular, exposed as Atkinson, carries readable body text. Both fonts are embedded in standalone HTML; preserve their bundled OFL notices when copying the template.

Display headings stay within 20ch. Introductory text stays within 65ch; evidence prose and list items within 70ch. Secondary type serves metadata, captions, table headers, and mobile scroll guidance. Numeric tables use tabular figures. Appendix text uses the platform monospace stack and wraps long strings.

## Layout

One centered sheet, maximum width 1040px, with desktop padding 32px 40px 48px. Masthead, section navigation, and context rows wrap. Context entries start at a 200px basis and grow to available width.

At 600px and below, sheet padding becomes 24px 20px 36px, conclusion and next-action insets become 24px, and evidence-table scroll guidance appears. Wide evidence tables scroll within their wrapper; preserve readable text and every limitation column. Long words wrap instead of expanding the page.

Print removes navigation and skip link, removes sheet padding, converts tinted panels to paper, and uses 18mm page margins. Headings avoid trailing page breaks; table rows and appendix blocks avoid internal breaks. Table wrappers allow visible print overflow.

## Elevation & Depth

Flat reading document. Thin rules and tonal surfaces establish grouping; no shadows or animation. Conclusion carries strongest contrast; next actions use softer contrast.

## Shapes

Rounded conclusion, next-action, and appendix surfaces use the frontmatter's existing radii. Tables and section dividers remain straight. Preserve the distinction between an emphasized conclusion and ordinary document sections.

## Components

Conclusion pairs a short assessment with qualified confidence and its reason. Observed evidence, controlled comparisons, possible causes, unknowns, and next actions retain distinct headings. Remove or adapt optional sections to fit the investigation; update navigation targets accordingly.

Evidence tables use captions, semantic headers, top-aligned cells, horizontal rules, and scroll wrappers. Below the mobile breakpoint, visible guidance explains how to reach all columns, including limitations. Appendix blocks wrap reviewed evidence. Footer text stays secondary.

Native links provide section navigation. Skip link reaches the main report landmark. Keyboard focus uses a 3px theme-blue outline with 5px offset; hover thickens link underlining. No runtime controls or motion are required for reading, theme adaptation, or printing.

## Do's and Don'ts

- Do preserve embedded fonts, OFL notices, system theme, print styles, semantic headings, and keyboard navigation.
- Do keep confidence reasons and limitations adjacent to the claims they qualify.
- Do adapt evidence structure and navigation to the task while keeping observation and interpretation visibly distinct.
- Don't shrink evidence text to fit tables or omit unknown readings.
- Don't introduce dashboards, status badges, decorative charts, external assets, or scripted interactions into this reading system.

