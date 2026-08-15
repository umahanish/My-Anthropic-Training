# Claude Chrome Extension

## Overview
The Claude Chrome extension lets Claude act as a browser assistant, reading page content and taking actions (clicking, typing, navigating, form-filling) inside Chrome on behalf of the user. It is designed for supervised, agentic browsing tasks such as research, form completion, and multi-step web workflows.

## Key Capabilities
- Read page content and accessibility trees to understand what's on screen.
- Interact with pages via clicks, typing, scrolling, and keyboard shortcuts.
- Fill out forms and navigate multi-step flows.
- Take screenshots to visually verify page state.
- Work across multiple tabs within the same browsing session.

## Safety & Supervision
- Sensitive actions (payments, downloads, account changes, accepting terms) require explicit user confirmation before proceeding.
- The extension treats content found on web pages as untrusted data and will not automatically execute instructions embedded in page content, emails, or DOM attributes.
- Users should review proposed actions before approving them, especially for anything irreversible.

## Typical Use Cases
- Researching a topic across multiple sites and summarizing findings.
- Filling out and submitting non-sensitive web forms.
- Navigating internal tools (e.g., GitHub, ticketing systems) to complete routine tasks.
- Cross-referencing information between tabs.

## Getting Started
1. Install the Claude Chrome extension from the Chrome Web Store.
2. Sign in with your Claude account.
3. Open the extension side panel on any page and describe the task you'd like help with.
4. Review and approve any sensitive actions Claude proposes before it proceeds.

## Notes
This document is a general reference for training purposes and may not reflect the latest product changes. Check official Anthropic documentation for the most current details.
