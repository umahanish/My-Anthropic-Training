# Working With Claude — Student Lab Guide
### Session 2: From First Chat to Connected Workflows

This is your copy — labs only, no lecture. Every lab is something you actually do, live, in Claude. Work through the **Core** labs in each module first; if you finish early, move to **Stretch** labs rather than waiting on the group.

**Legend:** 🟢 Core (everyone does this) · 🔵 Stretch (bonus — dig in if you have time)

Every lab below has a ready-to-use example so you're never staring at a blank message box. Use the example as-is if you don't have your own real task handy, or swap in your own real material — either way works.

**Before you start:** A few labs today need a paid plan (Pro, Max, Team, or Enterprise) and a couple of features are still in beta or rolling out. If a tab or feature mentioned below isn't visible to you, that's expected, not a mistake on your end — flag it to your facilitator and move to the next lab rather than getting stuck.

**Sample files:** A few labs use ready-made sample files instead of requiring your own real material, so you're never blocked without something real to work on:
- `IT_Expenses_Sample.xlsx` — Lab 1.2
- `Email_Thread_Database_Migration.docx` — Lab 2.1
- `sample-repo-failing-test.zip` — Lab 2.1
- `Slack_Activity_Sample_Yesterday.docx` — Lab 2.1
- Five files starting with `Contract_...docx` — Labs 2.1, 2.2, 5.2
- `Project_Timeline_Infrastructure_Modernization.docx` — Lab 3.3

All are fictional, built for this course, and safe to use even if you'd rather not upload real company data. Several connect to the same running scenario (a cloud migration to "Nimbus Cloud Services") — if a detail looks familiar from an earlier lab, that's intentional, not a mistake.

---

## Module 1 — What is Claude? First Conversations & Getting Better Results

### 🟢 Lab 1.1 — Your First Real Conversation *(10 min)*
1. Ask Claude something real. No real task handy? Use:
   ```
   Draft a short status update for my manager on a project that's about
   two weeks behind schedule due to a vendor delay. Keep it factual and
   not defensive.
   ```
2. Don't ask a new question — **iterate** on what came back:
   ```
   Make this more concise, and add one sentence proposing a revised
   delivery date.
   ```
3. Iterate once more:
   ```
   Good, now rewrite the tone slightly more confident — right now it
   reads a little apologetic.
   ```
   By message three, notice how much closer this is to something you'd actually send.

### 🟢 Lab 1.2 — Upload & Ask *(8 min)*
1. Upload one real file — a document, spreadsheet, or image.
2. Ask something specific about it, e.g.:
   ```
   Looking at this spreadsheet, which three expense categories grew the
   fastest over the last two quarters, and by how much?
   ```
3. Now ask Claude the same kind of question **without** the file:
   ```
   In general, which expense categories tend to grow fastest for a
   mid-size IT team over two quarters?
   ```
   Compare the two answers — one is grounded in your real numbers, one is a generic guess. Notice the gap.

### 🔵 Lab 1.3 — Build on a Past Chat *(7 min)*
1. In a new conversation, ask Claude to pull in something from an earlier chat:
   ```
   Pull up our conversation from earlier today about the deployment
   checklist, and add a "rollback steps" section to it.
   ```
2. If it can't find the right conversation, be more specific:
   ```
   I mean the chat where we listed pre-deployment steps for the auth
   service update — that one.
   ```

---

## Module 2 — Claude Desktop: Chat, Cowork, Code

### 🟢 Lab 2.1 — Route the Task *(12 min, pairs)*
For each task, decide **Chat**, **Cowork**, or **Code**, and write one sentence why. Sample material is provided for each so you can actually run your decision, not just guess at it.
1. `"Summarize this one email thread for me."` — use `Email_Thread_Database_Migration.docx`.
2. `"Read every contract in this folder and flag which ones expire in the next 90 days."` — use the same Contracts folder from Lab 2.2 *(answer: 3 of the 5 contracts fall within 90 days of August 1, 2026)*.
3. `"Fix the failing test in this repository."` — use `sample-repo-failing-test.zip` (unzip it first; run `pytest -v` yourself to see the failure before handing it to Claude).
4. `"Set up a task that emails me a summary of yesterday's Slack activity every morning."` — use `Slack_Activity_Sample_Yesterday.docx` as a stand-in for "yesterday's activity" if you don't have a live Slack connector set up.

Compare answers with your partner — where did you disagree, and why?

### 🟢 Lab 2.2 — Same Task, Two Modes *(10 min)*
1. Save the 5 sample contract files (`Contract_Nimbus_Cloud_Services.docx`, `Contract_BrightPath_Security.docx`, `Contract_Vertex_Networking.docx`, `Contract_Alderwood_Office_Supplies.docx`, `Contract_FixedTerm_Consulting.docx`) into a folder named "Contracts" on your computer.
2. In **Chat**, ask:
   ```
   Read the vendor contracts in my "Contracts" folder and tell me which
   ones auto-renew in the next 60 days. Assume today's date is August 1,
   2026.
   ```
   (Chat can't actually read your folder — notice it will ask you to paste content in instead. That's the point.)
3. Now run the exact same request in **Cowork**, pointed at that real folder.
4. Compare: what did Cowork do that Chat couldn't — reading the folder directly, producing a saved summary file, showing you a plan? Was that extra depth worth it for this task?

*(Answer to check yourself against: only one contract auto-renews within 60 days of August 1, 2026 — see if what you got matches, and if not, why not.)*

### 🔵 Lab 2.3 — Peek at Code *(10 min, if you have Code tab access)*
1. Open a small local project (or any sandbox repo).
2. In **Ask** mode, request a small, low-risk change:
   ```
   Add input validation to the login form so it rejects empty passwords,
   and show a clear error message instead of failing silently.
   ```
3. Review the visual diff Claude proposes before approving anything — read it the way you'd read a colleague's pull request.

---

## Module 3 — Introduction to Projects, Artifacts & Skills

### 🔧 One-Time Setup Check *(do this before Lab 3.2 or 3.3)*
Artifacts and Skills both require one setting to be turned on first. Check it now so you're not stuck mid-lab:
1. Click your name or initials in the **bottom-left corner** of the Claude window.
2. Click **Settings**.
3. Click **Capabilities** (Team/Enterprise: your admin sets this in *Organization settings > Capabilities* — ask your facilitator if you don't see it).
4. Confirm **"Code execution and file creation"** is toggled **ON**. If it's off, artifacts won't appear and Skills won't run — this is the single most common reason those two labs seem broken.

---

### 🟢 Lab 3.1 — Build Your Project *(15 min)*
**What a Project actually is:** a dedicated folder that holds instructions and files, so every chat inside it already knows your context — you stop re-explaining yourself from scratch every time.

**Step 1 — Create the Project**
1. Look at the left sidebar and click **Projects**. (Using a browser instead of the app? Go directly to `claude.ai/projects`.)
2. Click **"+ New project"** in the upper-right corner.
3. In the **Name** field, type: `Q3 Infrastructure Review` (or a real one you're actually working on).
4. In the **Description** field, type one line, e.g.: `Planning and risk tracking for this quarter's infrastructure review.`
5. If you're on a Team/Enterprise plan, you'll be asked to choose visibility — select **"Keep it private"** for this lab.
6. Click **"Create project."** You're now inside your new, empty Project.

**Step 2 — Add Instructions**
1. Inside the Project, find and click **"Set project instructions."**
2. Type this into the box:
   ```
   When answering questions in this project, assume I'm presenting to
   non-technical stakeholders. Avoid jargon, and always include a
   one-line "so what" takeaway.
   ```
3. Click **"Save instructions."**

**Step 3 — Add Files**
1. On the right side of the Project's main page, find the project knowledge panel and click the **"+"** button.
2. Upload 1–2 real files relevant to that work — or use `IT_Expenses_Sample.xlsx` from Lab 1.2 if you don't have one handy.
3. Claude processes this in the background — you'll see it listed once it's ready. You do not need to re-upload it in future chats inside this Project.

**Step 4 — Start a Chat and Test It**
1. Click **"New chat"** from inside the Project.
2. Ask:
   ```
   Based on the documents I've shared, what are the two biggest
   infrastructure risks we should flag this quarter?
   ```
3. Check the answer against what you'd expect from your own file/instructions — does it actually reflect what you gave it, or does it feel generic? If generic, the fix is almost always Step 2 (your instructions) or Step 3 (your file didn't finish uploading) — not a Claude problem.

---

### 🟢 Lab 3.2 — Generate & Iterate an Artifact *(12 min)*
**What an Artifact actually is:** when Claude produces something substantial — code, a document, a diagram, an interactive tool — it opens in its own panel next to the conversation instead of getting buried as plain chat text, so you can keep working with it directly.

**Step 1 — Ask for Something Substantial**
1. In any chat (inside or outside your Project), type:
   ```
   Build me a simple interactive calculator that estimates monthly cloud
   hosting cost based on instance type, hours running, and storage size.
   ```
2. Watch the right side of your screen — instead of code appearing as text in the chat, a **separate panel opens**. That panel is the Artifact. You should see a working, clickable calculator inside it, not just code.

**Step 2 — Iterate on It**
1. In the same conversation (don't start a new one), type:
   ```
   Add a toggle for on-demand vs. reserved pricing, and update the
   estimate live when it's switched.
   ```
2. Watch the Artifact panel update **in place** — same panel, new version — rather than a second panel appearing. That's the difference between iterating and starting over.

**Step 3 — Explore the Controls**
1. Look at the **lower-right corner of the Artifact window** — you'll find options to copy, download, or publish it.
2. If a conversation ever has more than one Artifact in it, use the **slider/chat-controls icon in the upper right** of the panel to switch between them.

---

### 🔵 Lab 3.3 — Trigger a Skill on Purpose *(12 min)*
**What a Skill actually is:** pre-packaged instructions Claude loads automatically for a specific kind of task — like producing a properly formatted Word document — so you get real formatting instead of plain text stuffed into a file extension.

**Step 1 — Confirm Skills Are On**
1. Click your name/initials (bottom-left) → **Settings** → **Customize** → **Skills** (Team/Enterprise: your admin enables this org-wide first, in *Organization settings > Skills*).
2. You'll see a list of built-in example Skills (Excel, PowerPoint, Word, PDF creation, etc.) — these are already toggled **on** by default. You don't need to configure anything else to use them.

**Step 2 — Trigger One**
1. Upload `Project_Timeline_Infrastructure_Modernization.docx` (or a real project doc of your own).
2. Type:
   ```
   Turn this project timeline into a polished PowerPoint, one slide per
   phase, using a clean and simple design.
   ```
3. You did **not** need to say "use the PowerPoint skill" — Claude recognized the task and loaded it automatically. That automatic recognition is the whole point of a Skill.

**Step 3 — Check the Result**
1. Open the resulting file and check formatting quality — real slide layout and structure, not text dumped onto blank slides.
2. That polish is the Skill at work. What phrase in your request do you think triggered it — "PowerPoint," "polished," "one slide per phase"?



---

## Module 4 — Connecting Tools: Enterprise Search & Research Mode

### 🟢 Lab 4.1 — Ask Your Org *(10 min)*
1. Open the "Ask [Your Org]" project (if set up).
2. Ask something that spans tools:
   ```
   What's our current process for requesting a new vendor security
   review, and who approved the most recent one?
   ```
3. Check: did the answer pull from more than one source? Can you trace each claim back to where it came from?

*(Not set up yet? Watch your facilitator demo this live, then move to Lab 4.2.)*

### 🟢 Lab 4.2 — Turn On Research *(12 min)*
1. Confirm web search is on — Research needs it to function.
2. Turn on Research mode and ask:
   ```
   What are the current best practices for securing a Kubernetes cluster
   in a multi-tenant environment, and how do the leading approaches
   compare?
   ```
3. Watch what it checks along the way. When done, click into one citation and confirm it actually says what Claude claims.

### 🔵 Lab 4.3 — Steer Research *(8 min)*
1. Run a Research query where an obvious source might get missed, e.g. the same Kubernetes question above.
2. If it skips a source you expected, steer it directly:
   ```
   Also pull relevant context from the official Kubernetes documentation
   specifically, not just third-party blog posts.
   ```
3. Notice how much the answer improves with one targeted nudge.

---

## Module 5 — Claude Cowork: Standing Context, Plugins & Team Sharing

### 🟢 Lab 5.1 — Set Global Instructions *(10 min)*
1. Go to Settings > Cowork > Global instructions and write something like:
   ```
   I'm a systems architect. Default to technical precision over
   simplified explanations. When producing documents, use a formal tone
   and always include a summary section at the top.
   ```
2. Run a quick task afterward and see whether the output reflects it.

### 🟢 Lab 5.2 — Create a Cowork Project (and Test Its Memory) *(12 min)*
1. Create a Cowork Project pointed at your "Contracts" folder from Lab 2.2 (same 5 sample contracts). Add instructions, e.g.:
   ```
   This project is for our Q3 vendor renewal review. Always cross-check
   dates against the contracts in this folder before answering. Assume
   today's date is August 1, 2026.
   ```
2. Run a first task:
   ```
   Which contracts require cancellation notice within the next 30 days
   to avoid auto-renewal?
   ```
   *(Answer to check yourself against: exactly two of the five contracts have a cancellation-notice deadline that falls within the next 30 days.)*
3. A few minutes later, run a related follow-up in the same Project:
   ```
   For the ones you just flagged, draft a short cancellation notice
   email for each.
   ```
   Does it reference the earlier list without you re-explaining it? That's memory working.

### 🔵 Lab 5.3 — Install & Try a Plugin *(8 min)*
1. Browse available plugins in the Cowork interface and install one relevant to your role (e.g., an Enterprise Search or engineering plugin).
2. Run one task with it active:
   ```
   Search across our connected tools for any open tickets related to the
   payment gateway outage last week.
   ```
3. Run a similar task without the plugin active and compare what changed.

---

## Module 6 — Claude in Chrome & Microsoft 365 Integration

### 🟢 Lab 6.1 — Supervised Browser Task *(12 min)*
1. Open Claude in Chrome (confirm it's approved for use first).
2. Try a real, low-stakes task:
   ```
   Go to these three competitor pages and pull their published pricing
   for the standard tier into a simple comparison table.
   ```
3. Before approving any action Claude proposes, actually read what it's about to do — don't reflexively click approve.
4. Save it as a shortcut once it works.

### 🟢 Lab 6.2 — One Office Edit *(10 min)*
Pick whichever app you use most and try the matching prompt:
- **Word:**
  ```
  Reformat this section to match our standard heading style, and fix
  the numbered list that's currently out of order.
  ```
- **Excel:**
  ```
  Build a formula in column F that flags TRUE if the contract end date
  in column D is within 90 days of today.
  ```
- **PowerPoint:**
  ```
  Restructure this slide to fit our template's two-column layout without
  changing the wording.
  ```
Check the result properly: in Word, read the tracked change before accepting; in Excel, check the actual formula, not just the displayed value.

### 🔵 Lab 6.3 — Cross-App Handoff *(8 min)*
1. Open an Excel workbook with real data and a PowerPoint file side by side.
2. From either sidebar, ask:
   ```
   Pull the Q3 revenue-by-region numbers from this workbook into a new
   slide titled "Regional Performance," using our template's chart style.
   ```
3. Confirm it happened without you copying or pasting anything manually.

---

*Facilitator tip: Core labs alone fill each module's scheduled time comfortably. Stretch labs are there so fast finishers keep building instead of sitting idle — they're optional, not a second required pass.*
