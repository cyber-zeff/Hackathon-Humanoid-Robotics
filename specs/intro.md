---
title: Docusaurus 5-Minute Tutorial Introduction
spec_version: 1.0
author: Gemini
date: 2025-12-16
---

# Specification for: Tutorial Intro

## 1. Objective

This document should serve as a quick-start guide for new Docusaurus users. The goal is to get them to a running Docusaurus site in less than 5 minutes. It should be concise, actionable, and focus on the immediate first steps.

## 2. Target Audience

- Beginner developers new to Docusaurus.
- Users who want to quickly evaluate the framework.

## 3. Content Structure & Key Points

### Section 1: Introduction
- **Headline:** "Tutorial Intro"
- **Opening Statement:** A welcoming sentence that states the goal: discovering Docusaurus in less than 5 minutes.
- **Emphasis:** Bold the phrase "Docusaurus in less than 5 minutes".

### Section 2: Getting Started
- **Sub-headline:** "Getting Started"
- **Primary Call-to-Action:** Mention creating a new site.
- **Secondary Call-to-Action:** Provide a direct, bolded link to **[docusaurus.new](https://docusaurus.new)** for an immediate trial.

### Section 3: Prerequisites
- **Sub-headline:** "What you'll need"
- **Requirement:** List Node.js version 20.0 or above.
  - Include a link to the Node.js download page: `https://nodejs.org/en/download/`
  - Add a note about checking dependencies during installation.

### Section 4: Site Generation
- **Sub-headline:** "Generate a new site"
- **Instruction:** Explain that the classic template is used.
- **Code Block:** Provide the command to generate a new site.
  - **Language:** `bash`
  - **Command:** `npm init docusaurus@latest my-website classic`
- **Explanation:** Briefly describe what the command does (creates the site, installs dependencies).

### Section 5: Running the Site
- **Sub-headline:** "Start your site"
- **Instruction:** Explain how to start the development server.
- **Code Block:** Provide the commands to navigate into the new directory and start the server.
  - **Language:** `bash`
  - **Commands:**
    ```bash
    cd my-website
    npm run start
    ```
- **Explanation:**
  - Describe what `cd` and `npm run start` do.
  - Mention the local server URL: `http://localhost:3000/`.
  - Explain the auto-reloading feature when a file like `docs/intro.md` is edited.
