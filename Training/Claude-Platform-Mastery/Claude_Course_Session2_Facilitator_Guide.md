# Working With Claude — From First Chat to Connected Workflows
### Session 2 Facilitator Guide

**Audience:** IT Professionals (same cohort as AI Fluency Session 1)
**Format:** Hands-on / Lab / Workshop as marked per module — live, on real accounts, not slides-only
**Grounding:** Content below is checked against current Anthropic documentation (support.claude.com, claude.com) as of this guide's preparation. Product surfaces like this move fast — see the checklist immediately below before you rely on any of it in front of a room.

---

## ⚠️ Do This 48 Hours Before Class — Access Checklist

This is the single biggest risk to "nobody loses this course," and it's not conceptual — it's plan-gating. Several features in this session **require a paid plan (Pro, Max, Team, or Enterprise)**, and a few are still **beta or rolling out**, meaning some students may not see them yet even on a paid plan:

| Feature | Plan requirement | Status to verify |
|---|---|---|
| Claude Desktop app itself | Free+ | Generally available |
| Cowork (desktop) | Pro, Max, Team, Enterprise | Available on desktop app now |
| Cowork (web/mobile) | Max first, more plans rolling out | **Beta — confirm who has it** |
| Code tab (desktop) | Pro, Max, Team, Enterprise | **Still rolling out — may not appear for everyone** |
| Projects, Artifacts, Skills | Free+ (org admin may need to enable Skills org-wide) | Generally available |
| Enterprise Search ("Ask Your Org") | Team, Enterprise | Requires an **org Owner to complete setup first** — do this days in advance |
| Research mode | Pro, Max, Team, Enterprise | Requires web search **turned on** to function |
| Cowork Plugins | Pro, Max, Team, Enterprise | Org owners can restrict which plugins appear |
| Claude in Chrome | Pro, Max, Team, Enterprise | **Beta** — Chrome (and Chromium browsers) only |
| Claude for Microsoft 365 (Word/Excel/PPT/Outlook add-ins) | Pro, Max, Team, Enterprise | Word/Excel/PowerPoint generally available; **Outlook still in beta**; requires the org to allow the "Office agents" cross-app setting for full effect |

**Action items:**
1. Confirm every student is on at least a Pro plan (or your org's Team/Enterprise plan) before the session — a free-tier student will be locked out of half the day.
2. If you plan to demo Enterprise Search, have your org Owner complete the one-time setup (connecting document/chat/email sources) **before** class — it can't be done live in a few minutes.
3. Check whether the Code tab and web/mobile Cowork have reached your students' accounts yet. If not, treat those specific parts as a **trainer-led demo** rather than hands-on, and say so upfront rather than let students discover they're missing a tab.
4. Have a backup plan for Claude in Chrome: if the extension isn't installed org-wide, get IT approval to install it before the session, not during.

Naming this gap explicitly at the start of class is a relief, not a red flag — "if you don't see the Code tab yet, that's expected, here's why" prevents a student from quietly assuming they did something wrong.

---

## Session-Level Learning Objectives

By the end of this session, participants will be able to:
1. Hold an effective first conversation with Claude and iterate toward a better answer
2. Choose correctly between Chat, Cowork, and Code for a given task
3. Set up and use a Project, generate and edit an Artifact, and invoke a Skill
4. Turn on Research mode and use Enterprise Search to pull answers from company knowledge
5. Configure Cowork's standing context (global instructions + a Project) and use a plugin
6. Use Claude in Chrome and the Microsoft 365 add-ins safely, on real browser and Office tasks

## The Narrative Thread — "Your First Day"

Unlike Session 1 (which ran on a cautionary story), this session runs on a **build-up** narrative: you are a new IT hire, and by the end of the day, Claude has gone from "a chat window you type into" to "something running across your tools while you're in a meeting." Each module is a capability upgrade in that same story. Say this explicitly at the open — it gives every module a reason to exist instead of feeling like six disconnected features.

**Cold open (say this before the title slide, same energy as Session 1):**

> "Imagine it's your actual first day. 9am, you open Claude and ask it a question — that's it, that's the whole toolkit. By lunch, you're pulling answers out of company docs you've never opened, doing research that used to take a colleague a week to onboard you on. By 5pm, Claude is working inside a shared folder, checking your team's tools, and editing a slide deck directly in PowerPoint — while you're in a meeting. Nothing about that path requires you to be technical. It requires knowing which tool in the toolbox to reach for, and that's what today is."

Callback opportunity: this cohort already has the 4D vocabulary from Session 1. Use it lightly, not as a second lecture — e.g., "Choosing between Chat and Cowork *is* Delegation" and "everything in Module 6 about approving what Claude does in your browser *is* Discernment and Diligence, just applied somewhere new." Don't over-explain it — a one-line callback lands better than a paragraph.

## Suggested Schedule

| Time | Module | Format |
|---|---|---|
| 0:00–0:50 | Module 1 — What is Claude? First Conversations & Getting Better Results | Hands-on |
| 0:50–1:00 | Break |
| 1:00–2:00 | Module 2 — Claude Desktop: Chat, Cowork, Code | Lab |
| 2:00–2:10 | Break |
| 2:10–3:20 | Module 3 — Introduction to Projects, Artifacts & Skills | Workshop |
| 3:20–4:00 | Lunch |
| 4:00–5:00 | Module 4 — Connecting Tools: Enterprise Search & Research Mode | Lab |
| 5:00–5:10 | Break |
| 5:10–6:10 | Module 5 — Claude Cowork: Standing Context, Plugins & Team Sharing | Lab |
| 6:10–6:20 | Break |
| 6:20–7:10 | Module 6 — Claude in Chrome & Microsoft 365 Integration | Hands-on |

---

# Module 1 — What is Claude? First Conversations & Getting Better Results
**Format: Hands-on · 50 minutes**

### Learning objectives
- Understand what Claude is and how a conversation actually works
- Run a first real conversation and iterate on it live
- Connect "getting better results" directly back to the Description skill from Session 1

### Step-by-step content

**1.1 What Claude actually is (10 min)**
- Claude is a conversational AI assistant: you write a message, it responds, and the conversation continues with full context of everything said so far in that thread.
- It's accessible several ways — the web/app chat at claude.ai, the Claude Desktop and mobile apps, and inside tools like Chrome and Microsoft 365 (today's later modules). All of them are the same underlying assistant; what changes is how much *reach* it has into your files, tools, and browser.
- Claude does not remember previous separate conversations by default the way a person would — each new chat starts fresh unless you're using a Project (Module 3) or Claude's memory/chat search feature, which lets Claude reference relevant past conversations when you ask it to.

**1.2 What makes a first conversation go well (15 min)**
- Be specific about the outcome you want, not just the topic — this is Description from Session 1, and it applies from message one.
- Iterate rather than restart: if the first answer is close but not right, tell Claude specifically what to change. You don't need to re-explain the whole task.
- Give Claude real material to work with — paste the actual email, the actual error, the actual draft — the same "concrete context beats a description of context" principle from Session 1's prompting module.
- Claude can read files you upload (documents, spreadsheets, images, PDFs) directly in a conversation — a first conversation doesn't have to start from typed text alone.

**1.3 Getting better results — the callback (10 min)**
Put this on screen, verbatim, as a bridge from Session 1:
> "Everything we spent a full session on last time — Goal, Context, Constraints, Format — works exactly the same way in a first conversation. The only thing that's new today is *where* you can point Claude, not *how* you talk to it."

### Hands-on Exercise 1 — Your First Real Conversation (15 min)

**Objective:** Run one real first conversation, then deliberately practice iteration instead of restarting.

**Instructions handed to participants:**
1. Open Claude (web, app, or desktop — whichever you'll use most). Ask it something real you actually need today — not a test question.
2. Look at the response. Instead of asking a brand new question, **iterate**: tell Claude specifically what to change, add, or fix about that exact response.
3. Do this once more. By the third message, the response should be noticeably closer to something you'd actually use.
4. Try uploading one real file (a document, spreadsheet, or image) and ask Claude a question about it directly.

**Debrief:** How many of you started your first message with a full Goal/Context/Constraints/Format prompt, versus a plain question you refined afterward? Both are valid — which one felt more natural to you, and why?

---

# Module 2 — Claude Desktop: Chat, Cowork, Code
**Format: Lab · 60 minutes**

### Learning objectives
- Understand the three modes inside the Claude Desktop app and what each is optimized for
- Correctly route a real task to Chat, Cowork, or Code
- Understand what's shared between Cowork and Code "under the hood"

### Step-by-step content

**2.1 One app, three modes (10 min)**
The Claude Desktop app has three tabs at the top: **Chat**, **Cowork**, and **Code**. On the latest app versions, Chat and Cowork share one home — your chats, Cowork sessions, projects, and artifacts all live in one sidebar, and you switch between "Chat" and "Cowork" right from the message box. Code sessions and projects stay in their own separate area.

Cowork and Code actually run on the same underlying engine — both are powered by Claude Code technology under the hood, running locally on your machine, capable of working independently and sustaining longer tasks. Chat does not run that engine; it's optimized for fast back-and-forth instead.

**2.2 Chat (10 min)**
Optimized for: quick exchanges, brainstorming, drafting, iterative back-and-forth — same Claude as claude.ai, plus native-app extras:
- **Quick entry** (Mac): double-tap Option to summon Claude in a compact overlay window without leaving what you're doing
- **Screenshots and window sharing** (Mac): show Claude exactly what's on your screen instead of describing it
- **Dictation** (Mac): talk instead of type
- **Desktop connectors**: local tools and services Claude can reach because it's running natively on your machine

**2.3 Cowork (15 min)**
Optimized for: complex or sustained work — research, analysis, file organization, producing finished documents. Where Chat answers a question, Cowork *does a job*.
- **Folder access**: give Claude a folder on your computer; it reads what's relevant and saves finished work back to that folder
- **Scheduled tasks**: recurring work Claude runs automatically on a cadence you set (a daily briefing, a weekly roundup) — these run remotely and don't need your computer awake
- **Browser use**: paired with Claude in Chrome (Module 6), Cowork can check websites and pull in what it finds as part of a larger task
- **Plugins** (Module 5): give Claude extra capabilities — pulling live data, searching internal knowledge, working within a specific framework
- **Protected environment**: Cowork's work happens in a contained space — it can read/write within folders you've shared, but can't reach outside them
- Cowork is currently a research preview on Pro/Max/Team/Enterprise, with new capabilities added regularly — expect it to look slightly different even a few weeks from now.

**2.4 Code (10 min)**
Optimized for: building software — writing, testing, running, and deploying code, directly in your actual codebase.
- **Ask / Code / Plan modes** control how much Claude does unsupervised: Ask proposes every change and waits for approval; Code applies file changes automatically but checks before running terminal commands; Plan lays out the full approach before touching anything, with a dedicated viewer to review the plan as work progresses
- **Local**: Claude works directly with a folder on your machine, including running a dev server you can preview
- **Remote**: Claude works in a cloud environment connected to a GitHub repo — sessions keep running even if you close the app
- The Code tab is still rolling out to Pro/Max/Team/Enterprise — this is one of the access-checklist items from the top of this guide.

**2.5 Which one, when? (5 min)** — put this comparison on screen:

| | Chat | Cowork | Code |
|---|---|---|---|
| Best for | Quick exchanges, drafting, learning through dialogue | Research, analysis, file organization, finished deliverables | Writing, testing, deploying software |
| Runs where | In the conversation | Contained workspace on your machine | Directly in your project / repo |

### Lab Exercise 2 — Route the Task (30 min, pairs)

**Objective:** Practice choosing the right mode instead of defaulting to Chat for everything (the single most common inefficiency new users have).

**Instructions handed to participants:**
1. Each pair gets 4 task cards (facilitator prepares these, or generate live — see below). Example tasks:
   - "Summarize this one email thread for me."
   - "Read every contract in this folder and flag which ones expire in the next 90 days."
   - "Fix the failing test in this repository."
   - "Set up a task that emails me a summary of yesterday's Slack activity every morning."
2. For each card, decide: Chat, Cowork, or Code — and write one sentence justifying it.
3. If you have access, actually run at least one task in its correct mode and see what the experience feels like versus running it in Chat instead.
4. Compare answers as a group — where did pairs disagree, and why?

**Debrief:** Which task, if you ran it in the *wrong* mode, would have wasted the most time? That's usually the clearest signal of why the mode choice matters.

---

# Module 3 — Introduction to Projects, Artifacts & Skills
**Format: Workshop · 70 minutes**

### Learning objectives
- Set up a Project with real context and instructions
- Generate and iterate on an Artifact
- Understand what a Skill is and see one trigger automatically

### Step-by-step content

**3.1 Projects — solving the "cold start" problem (15 min)**
- Before Projects, every new conversation starts from zero — you re-explain your context every time.
- A Project groups conversations around a shared body of knowledge: upload documents, code, style guides, or past work, and every chat inside that Project can draw on it without you re-pasting anything.
- You can add **custom instructions** per Project — tone, role, format expectations — so Claude behaves consistently for that specific area of work (e.g., "answer as a senior data analyst," "always use our team's terminology").
- Think of Settings as global (shape every conversation), Projects as scoped (shape one area of work — one client, one initiative, one part of the business).

**3.2 Artifacts — working side-by-side, not just reading a reply (15 min)**
- When you ask Claude to generate something substantial — code, a document, a diagram, an interactive tool — it can appear in a dedicated Artifact window next to the conversation, instead of buried in chat text.
- Artifacts support multiple types: code (with live preview for things like web components), documents, SVG images, diagrams, and interactive apps.
- You can keep iterating on an Artifact conversationally — ask for a change, and Claude updates it in place rather than starting over. You can also edit earlier messages to branch into a different version without losing the original.
- This matters for IT work specifically: Artifacts give you a genuinely larger, more reviewable code window than scrolling through chat.

**3.3 Skills — teaching Claude your workflows once (15 min)**
- A Skill is a package of instructions (and optionally scripts) that Claude loads *only when relevant* to the task at hand — this is called progressive disclosure, and it's what keeps Skills from bloating every conversation with irrelevant instructions.
- Two kinds: **Anthropic-built Skills** (available to everyone, invoked automatically — e.g., enhanced document creation for Excel, Word, PowerPoint, PDF), and **custom Skills** your org creates for its own workflows, written in plain Markdown, no coding required for simple ones.
- Team/Enterprise admins can provision Skills organization-wide, so everyone gets consistent behavior without individual setup.
- The practical test: if you or your team do the same kind of task repeatedly with the same conventions, that's a Skill candidate.

### Workshop — Build Your Own Project, Then Watch a Skill Fire (25 min, individual)

**Objective:** Leave with one real, working Project — not a demo you'll forget how to reproduce.

**Instructions handed to participants:**
1. Create a new Project around something real you're actually working on (not a toy example). Give it a name.
2. Add custom instructions — at minimum, one sentence about tone or format you want Claude to default to in this Project.
3. Upload or paste in 1–2 real documents relevant to that work.
4. Inside the Project, ask Claude a question that requires it to use what you just gave it — notice whether the answer actually reflects your documents and instructions, or feels generic. If generic, that's your first real Discernment check of the day (callback to Session 1).
5. Now ask Claude to produce something substantial — for example, "turn this into a formatted Word document" or "build me a simple dashboard for this data." Watch for two things happening at once: an Artifact (or a generated file) appearing, and — if it's a document type — a Skill quietly doing the formatting work in the background.

**Debrief:** Who noticed a moment where Claude clearly used something you gave it in setup versus something that felt like it ignored your instructions? That gap is worth naming out loud — it's usually a Description issue (the instruction was vague) rather than Claude "not working."

---

# Module 4 — Connecting Tools: Enterprise Search & Research Mode
**Format: Lab · 60 minutes**

### Learning objectives
- Understand what connectors are and the difference between local and remote ones
- Use Enterprise Search to query across company tools from one place
- Turn on and use Research mode for a real multi-step question

### Step-by-step content

**4.1 Connectors, briefly (10 min)**
- A connector links Claude to an external tool or data source (e.g., Google Drive, Slack, Jira, a CRM) so Claude can read from — and sometimes act in — that tool during a conversation.
- Desktop connectors reach local tools and services because Claude Desktop runs natively on your machine; remote connectors reach cloud services over the web and work from any surface (web, desktop, mobile).
- This is the plumbing underneath both Enterprise Search and Research mode — worth knowing it exists before using the features built on top of it.

**4.2 Enterprise Search — "ask your org anything" (20 min)**
- Enterprise Search adds a pre-configured project (labeled "Ask [Your Org]") to the sidebar for Team and Enterprise organizations, built specifically for unified search across your company's knowledge sources — chat, email, cloud storage, wikis, and more, from one query.
- Setup is admin-driven: an org Owner connects the sources (at minimum one for documents and one for chat; email is recommended), and after that, it's available to the whole organization.
- Once set up, you just ask it a normal question — "how does our pricing model work?", "who owns the vendor relationship with X?" — and Claude searches across every connected source and synthesizes an answer, rather than you searching each tool separately.
- Good use cases: onboarding ("what do I need to know about Project X"), finding the internal expert on a topic, spotting patterns across customer feedback that live in different systems.

**4.3 Research mode (20 min)**
- Research is a different capability: instead of pulling from your org's connected tools by default, it's built for open-ended questions that need **multiple searches that build on each other** — Claude decides what to investigate next based on what it's already found, across both the web and any of your connected tools (like Google Workspace, if connected).
- **Important:** Research requires web search to be turned on to function at all — check this first if it seems inactive.
- To enable: find the Research toggle in the chat interface (a "+" or dedicated button depending on your app version) — it turns blue/active when on.
- If Research doesn't seem to be actually researching, you can steer it explicitly: "Claude, please use the research tool to..." or "pull relevant context from [specific source]."
- Research sessions use more of your usage allocation than a normal chat, since Claude is running multiple searches and building a comprehensive answer — worth knowing before running it on every question by habit.

### Lab Exercise 3 — Search Your Org, Then Research the World (30 min, individual)

**Objective:** Feel the difference between "search what we already know" and "go find out."

**Instructions handed to participants:**
1. If Enterprise Search is set up for your org, open the "Ask [Your Org]" project and ask a real question you'd normally have to hunt for across multiple tools. If it's not set up yet, ask your facilitator to demo this step live instead.
2. Turn on Research mode in a regular conversation. Confirm web search is enabled first.
3. Ask a genuinely open-ended question relevant to your work — something that would take real digging, not a single-fact lookup (e.g., "what are the current best practices for X, and how do the leading approaches compare?").
4. While it runs, notice: is Claude showing you what it's checking along the way? When it's done, check at least one citation against the actual source — same verification habit from Session 1's Discernment module, just applied to a built-in research tool instead of a plain answer.

**Debrief:** For the task you just ran through Research — would Enterprise Search have answered it faster if the information already lived in your org's tools? That distinction (already-known vs. needs-discovery) is the practical rule for which tool to reach for.

---

# Module 5 — Claude Cowork: Standing Context, Plugins & Team Sharing
**Format: Lab · 60 minutes**

### Learning objectives
- Set up standing context so Cowork doesn't start from zero every session
- Install and use a plugin
- Understand what's safe to share with a team and what stays local

### Step-by-step content

**5.1 Standing context — global instructions and projects (15 min)**
Two layers, don't confuse them:
- **Global instructions**: set once in Settings > Cowork, apply to *every* Cowork session — your preferred tone, output format, background on your role. Set-and-forget.
- **Cowork Projects**: dedicated workspaces for a specific area of work, each with its own folder, instructions, and — importantly — **memory**. Memory is enabled for Cowork Projects, meaning Claude remembers context from past tasks *within that Project* and applies it to future tasks in the same one. This is what actually solves "Cowork forgot everything from last time."
- Practical note: Cowork Projects are desktop-only and stored locally on your computer right now — there's no cloud sync for Project data, and for Team/Enterprise members, Cowork Projects don't currently support sharing the Project itself with teammates (see 5.3 for what *is* shareable).

**5.2 Plugins — encoding your team's expertise (20 min)**
- A plugin bundles skills, connectors, and sub-agents into a single installable package, built around a specific role or workflow (e.g., a finance plugin, a legal plugin, an "enterprise search across everything" plugin).
- You browse and add plugins directly from the Cowork interface to match the task at hand.
- For Team/Enterprise: org owners can build a curated **plugin marketplace**, controlling exactly which plugins appear for their team — useful for keeping everyone using vetted, consistent tools rather than everyone installing whatever they find.
- Practical framing for this room: a plugin is what turns "Cowork, generically" into "Cowork, configured like it was built for our team."

**5.3 Team sharing and safety (15 min)**
- What's shareable: the *output* of what you build — finished documents, a workflow you've validated, results you want a teammate to see. Cowork conversation history itself is stored locally on your machine and isn't centrally managed or exported by admins.
- What's not currently shareable: the Cowork Project itself (its folder/instructions/memory) between teammates — each person's Project is their own workspace right now.
- Safety framing, direct callback to Session 1's Diligence: before sharing anything Claude produced in Cowork with a teammate or wider team, that's exactly the Deployment Diligence question from Session 1 — have *you* verified it, not just Claude.

### Lab Exercise 4 — Set Up Your Standing Context (30 min, individual)

**Objective:** Leave with global instructions and a working Cowork Project set up on real material — the goal is that Monday-morning Cowork already knows who you are.

**Instructions handed to participants:**
1. Go to Settings > Cowork > Global instructions. Write 2–3 sentences that should apply to *everything* Cowork does for you — role, tone, or a standing preference.
2. Create a Cowork Project pointed at a real folder you work in. Add project-specific instructions on top of your global ones.
3. Run one real task inside that Project.
4. Run a second, related task in the *same* Project a few minutes later, and notice whether Claude references anything from the first task without you re-explaining it — that's memory working.
5. If plugins are available to your org, browse what's on offer and install one relevant to your role. Try one task with it active.

**Debrief:** What's one piece of context you had to repeat to Claude constantly before today, that global instructions or a Project will now handle for you permanently?

---

# Module 6 — Claude in Chrome & Microsoft 365 Integration
**Format: Hands-on · 50 minutes**

### Learning objectives
- Understand what Claude in Chrome can and can't safely do
- Use the Microsoft 365 add-ins in at least one Office app
- Apply Session 1's Discernment/Diligence instincts to an agent that takes real actions

### Step-by-step content

**6.1 Claude in Chrome — read, click, navigate (15 min)**
- Claude in Chrome is a browser extension that lets Claude read, click, and navigate websites alongside you, working in a side panel while you browse.
- It's genuinely useful for: multi-tab research (checking pricing across ten competitor sites), extracting data from pages without an API, and saving a working prompt as a reusable **shortcut** you trigger later, including scheduling it to run automatically.
- **This is the safety-critical part of today — say it plainly, don't rush it:** Claude in Chrome can interact directly with websites on your behalf. It has safety classifiers screening for prompt-injection attempts, but Anthropic is explicit that it's still a research preview and carries real risk. Concretely:
  - Avoid it for financial transactions, password management, or anything touching sensitive personal/health/government data.
  - Use a separate browser profile without access to sensitive accounts if possible.
  - Review Claude's proposed actions before approving them, especially on a site you haven't used it on before.
  - You can pre-approve routine actions for trusted workflows, but Claude will still stop and ask before certain irreversible actions, like completing a purchase.
- **This is Discernment and Diligence from Session 1, just relocated:** verifying a claim before trusting it (Discernment) becomes reviewing an action before approving it; owning what ships (Diligence) becomes owning what an agent just did on a real website under your login.

**6.2 Claude for Microsoft 365 (20 min)**
- Native add-ins for Excel, PowerPoint, and Word (generally available on all paid plans), plus Outlook (currently in beta) — Claude works inside a sidebar in each app.
- Per-app behavior worth knowing:
  - **Excel:** reads multi-tab workbooks, builds real formulas (not just static values), and tracks every cell it changes.
  - **PowerPoint:** works inside your existing template — your layouts, fonts, colors — producing native, editable charts rather than pasted images.
  - **Word:** edits land as tracked changes, and Claude can respond to comment threads explaining what it changed and why.
  - **Outlook:** drafts and calendar invites open in Outlook's native compose form and wait for you to click send — Claude does not send on your behalf.
- The standout feature for this audience: Claude can now **work across these apps together** — read data from an open Excel workbook and build a PowerPoint from it, for instance — without you copying and pasting between them. This requires each add-in to be activated at least once, and for Team/Enterprise, an org owner may need to enable the cross-app "Office agents" setting.

### Hands-on Exercise 5 — Supervised Browser Task + One Office Edit (25 min, individual)

**Objective:** Get real, first-hand comfort with both surfaces, under supervision, on low-stakes material.

**Instructions handed to participants:**

*Part A — Claude in Chrome (12 min):*
1. Install/open Claude in Chrome if you haven't already (facilitator: confirm this was pre-approved per the access checklist).
2. Pick a low-stakes, real task: research something for work across 2–3 sites, or extract information from a page you'd normally copy-paste manually.
3. Before approving any action Claude proposes, actually read what it's about to do — don't reflexively click approve. This is the whole exercise.
4. Save the prompt as a shortcut once it works, so you have it for next time.

*Part B — Microsoft 365 (13 min):*
5. Open Word, Excel, or PowerPoint (whichever you use most) and activate the Claude add-in.
6. Give it one real, small edit request — reformat a section, build a formula, restructure a slide to match your template.
7. Check the result the way Session 1 taught you to: in Word, actually read the tracked change before accepting it; in Excel, check the formula, not just the displayed number.

**Debrief (full group):** For the browser task — was there a moment you almost approved something without really reading it? Be honest, that's the whole point of the exercise, same as Session 1's automation-bias lesson. For the Office task — did tracked changes / visible formulas make you trust the result more than a flat "here's your answer" would have?

---

## Closing — Tie It Back

End with the narrative payoff, not a feature recap:

> "This morning, Claude was a text box. By the end of today, it's reading your files, searching your company's tools, running scheduled work in the background, and editing documents directly where you already work. None of that required you to become 'technical' — it required knowing which of six tools to reach for, and that's genuinely it."

Ask for one commitment, same pattern as Session 1: **which one of these six will you actually use this week?** Not all six — one. That's the one that sticks.

---

## Appendix — Quick Reference: Which Tool, When

| You want to... | Reach for |
|---|---|
| Ask a quick question or draft something short | **Chat** |
| Produce a finished deliverable from multiple sources, or run something on a schedule | **Cowork** |
| Write, test, or deploy code in a real project | **Code** |
| Keep persistent context for one area of work | **Project** |
| Get a reviewable document/code/diagram alongside the conversation | **Artifact** |
| Standardize a repeatable workflow across yourself or your team | **Skill** |
| Search everything your company already knows | **Enterprise Search** |
| Investigate an open-ended question across the web (and your tools) | **Research mode** |
| Give Cowork permanent context about you or a workspace | **Global instructions / Cowork Project** |
| Configure Cowork like it was built for your specific role | **Plugin** |
| Have Claude act inside your actual browser | **Claude in Chrome** (approve every action) |
| Edit directly inside Word/Excel/PowerPoint/Outlook | **Claude for Microsoft 365** |

*Facilitator note: verify every rollout-status item in the access checklist again on the morning of the session — beta features and plan gating on these products can change week to week.*
