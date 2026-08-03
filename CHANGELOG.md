# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.4.0] - 2026-07-10
### Added
- **Transition Performance (C1)**: Removed artificial 380ms transition delay on local navigation for instant page switching.
- **Dynamic RFQ Mailto Flow (C2)**: Redesigned the static RFQ form to dynamically construct a `mailto:` URL and automatically trigger default email clients pre-filled with clipboard contents, ensuring 100% honesty and seamless operation.
- **Mobile Dropdowns & Drawers (C4, C6)**: Re-engineered headers to use touch/click toggle behaviors, and copied language link selectors + catalog download buttons directly into the side drawers of all 12 localized pages.
- **Search Optimization (H1)**: Debounced keyup events in product search by 250ms to prevent heavy DOM reconstructions on every keystroke.

## [v2.3.0] - 2026-07-10
### Added
- **Site-Wide Search Engine**: Added a live instant search bar to the catalog page sidebar in all language versions, allowing users to query by SKU, name, description, or subcategory.
- **Image Restoration**: Restored 120 high-quality 3D design mockups for dining and lounge chairs to replace empty "Image Pending" boxes.
- **Translation Alignment**: Synchronized category naming definitions (such as translating Japanese dining category to "ダイニングチェア" and Chinese to "設計師餐椅").

## [v2.2.0] - 2026-07-10
### Added
- **Global Database Cleanup**: Released 101 previously hidden products (Dining, Stools, Lounge) and categorized them dynamically.
- **Sidebar Dropdown Menus**: Redesigned categories with clean gold-accented accordion dropdowns and item counters.
- **Stal Kimtar Merge**: Merged steel-framed design chairs directly into main Dining Chairs and Lounge Chairs categories.
- **Header Visibility Fixes**: Added transparent header style overrides for white text and borders, fixing visibility on dark hero section backgrounds.
- **Language Switcher Visibility**: Enhanced contrast, size, and layout of the header language dropdown selector.

## [v2.1.0] - 2026-07-10
### Added
- **Office Furniture Support**: Implemented a new data processing pipeline (`process_office_furniture.py`) to parse new Office Chairs and Office Furniture product data from Excel.
- **Dynamic Image Sync**: Successfully merged 600+ new product images into the `Product_Images/01_Office_Furniture` asset repository.
- **Office Preview Page**: Created `office.html` to preview the newly integrated office categories separately.
- **Email Notification Script**: Added `scripts/notify_update.py` for sending update emails to stakeholders.
- **Site Versioning**: Added automatic site version injection (`SITE_VERSION`) in the footer of all localized pages.

## [v2.0.0] - 2026-07-03
### Changed
- Refactored frontend to feature exactly 10 featured items per category across EN/TW/JP.
- Unified navigation headers, footers, mobile drawers, and language selectors across all pages.
- Integrated 201 real Canva product images.
