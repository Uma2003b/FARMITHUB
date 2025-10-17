# TODO: Standardize Header Across AgriConnectHub Pages

## Overview
Standardize the header and navigation across all static HTML pages linked from main.html to ensure UI consistency. Use the full header structure from main.html: .header-nav-wrapper with .uniform-header (brand "Welcome to AgriConnectHub", buttons: calendar, feedback, logout, theme), and static <nav><ul> with all app links. Include necessary scripts (nav.js, theme.js, auth.js). Adjust for page-specific needs (e.g., back/export buttons via JS).

## Steps

### 1. Prepare Styles
- [x] Update theme.css to define colors for buttons matching the image: .calendar-button (green), .feedback-button (yellow), .logout-button (red), .theme-toggle (blue-ish). Ensure green bar for .uniform-header.

### 2. Update Root-Level HTML Files
- [x] Edit about.html: Replace <header> and <nav> with template; add back button logic if needed.
- [x] Edit cropCalendar.html: Replace <header> and <nav>; retain export button in main content.
- [x] Edit disease.html: Replace <header> and <nav>.
- [x] Edit organic.html: Replace <header> and <nav>.
- [x] Edit farmer.html: Replace <header> and <nav>.
- [x] Edit weather.html: Replace <header> and <nav>.
- [x] Edit shopkeeper.html: Replace <header> and <nav>.
- [x] Edit chat.html: Replace <header> and <nav>.
- [x] Edit plantation.html: Replace <header> and <nav>.
- [x] Edit feed-back.html: Replace <header> and <nav>.
- [x] Edit Forum/forum.html: Replace <header> and <nav>.

### 3. Update Subdirectory Templates
- [x] Edit Crop_Planning/templates/cropplan.html: Replace <header> and <nav>.
- [x] Edit Labour_Alerts/templates/labour.html: Replace <header> and <nav>.

### 4. Handle Flask/Sub-Apps (If Applicable)
- [x] Review and update templates in Flask apps (e.g., Crop Recommendation/templates/crop_recommendation.html) for consistency; may require server run for testing.

### 5. Testing and Verification
- [ ] Use browser to launch main.html, navigate to each page, verify consistent header (green bar, welcome text, menu items, colored buttons).
- [ ] Check dark mode toggle and logout functionality across pages.
- [ ] Update any issues found.

### 6. Finalization
- [ ] All steps complete: Headers standardized.
- [ ] Archive or remove this TODO.md if no further changes needed.

Progress: Starting with step 1.
