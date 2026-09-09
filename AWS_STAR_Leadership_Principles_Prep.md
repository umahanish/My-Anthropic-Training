# AWS-Style STAR & Leadership Principles Prep
For AWS interviews specifically, and any company that has adopted the AWS-style behavioral format (increasingly common across tech, especially cloud-heavy orgs)

---

## Why this format exists, and how to think about it

AWS interviews are built around **16 Leadership Principles (LPs)**. You typically won't be asked "tell me about Ownership" directly — instead you'll get a situational question ("tell me about a time you took on something outside your job description") and the interviewer is silently scoring which LP(s) it demonstrates. A **Bar Raiser** (a trained interviewer from outside the hiring team, present specifically to protect the hiring bar) will usually dig 2–3 follow-up levels deeper than a normal interviewer — "what exactly did *you* do, not the team," "what did you consider and reject," "what would you do differently."

**STAR structure, kept tight (aim for ~90 seconds to 2 minutes per story before follow-ups):**
- **Situation** — one or two sentences of context. Don't over-explain the business background.
- **Task** — what specifically was your responsibility or the problem you owned.
- **Action** — the majority of your airtime goes here. Use "I," not "we" — the interviewer needs to isolate *your* contribution from the team's.
- **Result** — quantified where possible, plus what you learned or would do differently. AWS interviewers specifically like a closing reflection ("what I'd do differently" or "what I learned") — it demonstrates Learn and Be Curious even inside a different principle's story.

**Story bank strategy:** you don't need 16 different stories. 5–6 well-chosen projects, each of which demonstrates 2–3 principles depending on which facet you emphasize, is enough — but you must be able to *recognize which principle a question is really asking about* and pull the right facet out. That mapping is what most of this document is for.

---

## Recognizing the principle behind the question (the skill that actually matters)

| If they ask... | They're probing... |
|---|---|
| "Tell me about a time you did something outside your job scope" | Ownership |
| "Tell me about the most complex problem you've solved" | Dive Deep / Invent and Simplify |
| "Tell me about a time you disagreed with your manager/client" | Have Backbone; Disagree and Commit |
| "Tell me about a time you had to learn something quickly" | Learn and Be Curious |
| "Tell me about a time you missed a deadline or made a mistake" | Ownership / Deliver Results (recovery matters more than the mistake) |
| "Tell me about a time you simplified something complex" | Invent and Simplify |
| "Tell me about your proudest achievement" | Deliver Results / Think Big |
| "Tell me about a time you had incomplete information but had to act" | Bias for Action / Are Right, A Lot |
| "Tell me about a time you built trust with a skeptical stakeholder" | Earn Trust |
| "Tell me about a time you pushed for a higher quality bar than others wanted" | Insist on the Highest Standards |

---

## Your STAR story bank, mapped to Leadership Principles

### 1. Ownership
*"Own it. Think long term and don't sacrifice long-term value for short-term results. Act on behalf of the entire company, beyond just your own team."*

**Story: BT Project — 200+ application migration to microservices/APIs on AWS DCP**
- **Situation:** The BT project needed 200+ legacy applications migrated to a microservices/API architecture on the AWS DCP platform — a scope that touched infrastructure, application teams, and cost governance well beyond a typical architect's assigned lane.
- **Task:** I was responsible for the migration architecture, but the $10M in savings only happens if the migration actually gets adopted across every application team, not just designed on paper.
- **Action:** I didn't stop at handing over a reference architecture. I personally worked with individual application teams to unblock migration-specific issues, tracked adoption progress across all 200+ applications rather than treating my job as "done" once the pattern was published, and escalated resourcing gaps early rather than letting stalled applications quietly miss the program timeline.
- **Result:** The migration delivered $10M in savings — a number that depended on near-complete adoption across the application portfolio, not just a good design sitting in a document.
- **Reflection if pushed:** What I'd do differently now is build the adoption-tracking dashboard on day one rather than a few months in — I initially underestimated how much visibility into per-team progress would matter for keeping the program on track.

### 2. Invent and Simplify
*"Expect and require innovation. Are external aware, look for new ideas everywhere. Are not limited by 'not invented here.' Accept that we may be misunderstood for long periods of time."*

**Story: WebCheck-In Fastpass — deliberately NOT building a full agentic system**
- **Situation:** Fastpass self-service check-in had manual verification steps slowing passengers down, in an environment where the broader program was heavily investing in agentic AI (AskHR, Loyalty bot).
- **Task:** There was implicit pressure to build this as another sophisticated multi-agent system, matching the pattern of the other AI work on the program.
- **Action:** I made the call to simplify instead of match the trend — I broke the workflow into a deterministic state machine (identity verify, document check, seat/bag validation, boarding pass issue) and scoped the LLM to exactly one step where genuine unstructured judgment was needed (document image validation), resisting the urge to make the rest "agentic" for the sake of technical consistency with the rest of the program.
- **Result:** This reduced manual verification steps and sped up check-in, and it's meaningfully easier to debug and audit than a conversational agent would have been for a pure business-rules problem, since 90% of it stayed deterministic.
- **Reflection:** The "invention" here wasn't a new technology — it was resisting the instinct to over-apply an exciting new pattern everywhere just because it was available.

### 3. Are Right, A Lot
*"Have strong judgment and good instincts. Seek diverse perspectives and work to disconfirm their beliefs."*

**Story: AskHR — choosing RAG over fine-tuning**
- **Situation:** When architecting AskHR, there were two credible paths: fine-tune a model on HR policy content, or build a RAG pipeline that retrieves from a live knowledge base.
- **Task:** I had to make this call early, since it shapes the whole system, without the benefit of hindsight on how often policies would actually change.
- **Action:** I reasoned from the nature of the content, not from what was trendy — HR policy, payroll cycles, and benefits rules change on a regular cadence, so a fine-tuned model would drift out of date between retraining cycles. I chose RAG specifically so the knowledge base could be re-indexed the moment a policy changed, without touching the model.
- **Result:** This turned out to be the right call — payroll and leave policy updates happened multiple times over the engagement, and each one was a same-day re-ingestion rather than a retraining cycle.
- **Reflection:** I sought out how frequently the underlying content actually changed before deciding, rather than defaulting to whichever approach I'd used most recently — that's the habit I'd point to as "good instincts" here, not luck.

### 4. Learn and Be Curious
*"Never done learning, always seeking to improve. Curious about new possibilities and act to explore them."*

**Story: Transitioning from cloud/infra architecture into agentic AI architecture**
- **Situation:** Most of my career before 2024 was cloud and infrastructure architecture — TOGAF, Kubernetes, Terraform, migrations. Agentic AI/GenAI architecture (LangChain, LangGraph, AutoGen, MCP, Claude) was a genuinely new domain, not an incremental extension of what I'd done.
- **Task:** To lead AskHR and the Loyalty bot credibly, I needed hands-on depth, not just architecture-diagram-level familiarity.
- **Action:** I didn't just read documentation — I built working prototypes of the RAG and multi-agent patterns myself before asking a team to build on top of them, and I've kept doing this since; I recently rebuilt simplified versions of my own production patterns (RAG pipelines, LangGraph multi-agent flows, MCP tool servers) specifically to make sure my hands-on fluency hadn't atrophied behind the architecture-level view.
- **Result:** That hands-on grounding is what let me make credible calls on trade-offs like RAG-vs-fine-tuning and LangGraph-vs-AutoGen, rather than deferring those decisions entirely to the engineering team.
- **Reflection:** The habit I'm proudest of here is treating "I architected it" and "I can still build it" as two different bars, and holding myself to both.

### 5. Insist on the Highest Standards
*"Relentlessly high standards — many people may think these standards are unreasonably high."*

**Story: AstraZeneca — enforcing citation-only answers under GxP**
- **Situation:** The scientific literature/regulatory-intelligence RAG assistant operated under GxP compliance, where every generated answer needed a traceable audit trail back to a specific source document.
- **Task:** A "good enough" RAG system that answers accurately most of the time is not good enough in this context — an ungrounded claim, even if correct, creates a compliance liability.
- **Action:** I insisted on a hard architectural rule: no answer ships without a verified match to a retrieved chunk, and unmatched claims are stripped or flagged for human review rather than shown. This was a stricter bar than the team's initial design, which treated grounding as a soft preference rather than a hard gate — I pushed to make it a validation step that blocks the response, not just a prompt instruction hoping the model complies.
- **Result:** This gave the research and regulatory affairs teams a system they could actually rely on for submission prep, with an audit trail that held up to GxP review.
- **Reflection:** The uncomfortable part of insisting on this was accepting a higher rate of "I don't know" or escalated answers in exchange for zero ungrounded claims — a trade-off worth explaining if asked, since "highest standards" sometimes means accepting less coverage for more reliability.

### 6. Think Big
*"Create and communicate a bold direction that inspires results. Think differently and look around corners."*

**Story: Positioning AskHR/Loyalty patterns as a reusable enterprise platform, not one-off bots**
- **Situation:** Qatar Airways initially needed two separate point solutions — an HR chatbot and a loyalty assistant.
- **Task:** I could have architected each as an independent, bespoke system.
- **Action:** Instead, I architected the retrieval, evaluation (Ragas/LangSmith), and guardrail patterns as reusable components — the ingestion pipeline pattern, the confidence-threshold escalation logic, the safety-filter layering — so that a third or fourth GenAI use case (which did materialize, in the cargo manifest/HR document extraction work) could reuse the foundation rather than starting from zero.
- **Result:** This shaped the program's later AI investments to move faster because the governance and evaluation patterns already existed, rather than each new use case re-litigating "how do we evaluate this" and "what guardrails do we need" from scratch.
- **Reflection:** Thinking big here wasn't about a moonshot feature — it was recognizing that the *governance and evaluation infrastructure* was the actual reusable asset, more than any single chatbot.

### 7. Dive Deep
*"Operate at all levels, stay connected to the details, audit frequently. No task is beneath you."*

**Story: Root-causing a hallucination/confidence-threshold issue in AskHR**
- **Situation:** Early in AskHR's rollout, the escalation-to-human-ticket rate was higher than expected — a symptom that could have several different root causes.
- **Task:** Rather than accepting a surface explanation ("the model isn't good enough"), I needed to find the actual mechanism.
- **Action:** I went down into the retrieval layer specifically — looking at which queries were escalating, and found that a cluster of them were hitting the confidence threshold not because the model was uncertain about the *answer*, but because the retrieval step was returning chunks that were topically related but not actually the right policy section, due to a chunking boundary cutting a policy clause awkwardly. I traced this by manually reviewing retrieved chunks against the queries that escalated, not just looking at aggregate metrics.
- **Result:** Adjusting the chunking strategy (larger chunks with overlap, preserving clause boundaries) measurably reduced the false-escalation rate, without loosening the confidence threshold itself — which would have risked ungrounded answers slipping through instead.
- **Reflection:** The lesson was that "confidence threshold" symptoms often have a root cause upstream in retrieval, not in the generation step — worth diving into the actual data rather than tuning the most visible knob first.

### 8. Have Backbone; Disagree and Commit
*"Have conviction and be tenacious. Do not compromise for the sake of social cohesion. Once a decision is determined, commit wholly."*

**Story: Lloyds — holding the line on read-only bot capability**
- **Situation:** During the banking chatbot's design, there was pressure from parts of the business to extend the bot's capability toward executing simple transactions (e.g., initiating a standing-order change) to further increase call deflection.
- **Task:** I believed this crossed an important risk line, even though it would have produced a better-looking deflection number in the short term.
- **Action:** I pushed back directly, laying out the risk model: the blast radius of an automated transaction error is categorically worse than a slower manual escalation, and the trust cost of one bad automated transaction would likely outweigh the incremental efficiency gain. I didn't just state a preference — I brought a comparison of the failure cost in each scenario to make the trade-off concrete for stakeholders who weren't AI specialists.
- **Result:** The decision landed on keeping the bot strictly read-only/advisory, which is what shipped — and it's part of why compliance and risk teams were able to sign off on the system at all.
- **Reflection:** If the decision had gone the other way after a fair hearing, my approach would have been to commit fully and build the safest possible version of the write-capable design, rather than continuing to relitigate it after the call was made.

### 9. Bias for Action
*"Speed matters in business. Many decisions are reversible and do not need extensive study."*

**Story: Shipping AskHR iteratively rather than waiting for a complete knowledge base**
- **Situation:** At the start of AskHR, the full HR/payroll/benefits knowledge base wasn't fully digitized or ready for ingestion — waiting for 100% document readiness would have delayed the whole program.
- **Task:** Decide whether to wait for complete content coverage or launch with partial coverage.
- **Action:** I chose to launch with the highest-volume policy areas first (the ones generating the most HR tickets), with an explicit and honest "I don't have information on that yet, escalating to HR" fallback for gaps — a reversible decision, since expanding coverage later was low-risk, versus the cost of delaying the entire program for completeness.
- **Result:** This got real usage data and ticket-deflection impact flowing early, which in turn informed which additional policy areas to prioritize for ingestion next, rather than guessing.
- **Reflection:** The bias-for-action call here specifically worked because the "wrong" version of this decision (launching with gaps) was cheap to correct — worth being explicit about that reversibility if asked, since bias for action doesn't mean skipping judgment on irreversible calls.

### 10. Earn Trust
*"Listen attentively, speak candidly, treat others respectfully. Are vocally self-critical."*

**Story: Building trust with compliance/risk teams across Lloyds and AstraZeneca**
- **Situation:** Both engagements involved skeptical compliance/risk/regulatory stakeholders who had every reason to be cautious about GenAI in a regulated function.
- **Task:** Get genuine buy-in, not just a grudging sign-off.
- **Action:** I led with constraints rather than capabilities in every stakeholder conversation — showing what the system explicitly could *not* do (no write access, no ungrounded answers, full audit trail) before showing what it could do, and I proposed phased, read-only rollouts specifically so these teams could observe real behavior before being asked to trust it with more scope.
- **Result:** Both engagements got compliance sign-off, and at Lloyds specifically the read-only design became the basis for the eventual production system rather than a compromise stakeholders tolerated.
- **Reflection:** Earning trust here meant treating the skeptics' caution as valid input to the architecture, not an obstacle to route around.

### 11. Deliver Results
*"Focus on the key inputs and deliver them with the right quality and in a timely fashion."*

**Story: Aggregate outcomes across your portfolio**
- Use this as your "headline" story when asked for your proudest achievement, pulling together: $10M saved (BT project migration), 40% infrastructure cost reduction (Qatar Airways cloud migration), meaningful HR ticket deflection (AskHR), ~30% telephony cost reduction (Lloyds chatbot), and 25% faster deployment (Terraform/CI-CD on AKS/EKS).
- **Action emphasis:** don't just list numbers — pick one and walk through the actual mechanism that produced it (e.g., the 40% cost reduction came from rightsizing + reserved instances + containerization + decommissioning redundant apps, not just "we moved to the cloud").
- **Reflection:** Results at this level came from treating measurement as part of the architecture from day one (defining what "success" meant before building), not something bolted on afterward to justify the project.

---

## Handling Bar Raiser follow-up drilling

Expect these after almost any STAR answer — prepare, don't improvise:

- **"What exactly did *you* do versus the team?"** → Have a one-sentence answer ready that isolates your individual decision or action, separate from what the team executed.
- **"What did you consider and reject?"** → Always have at least one alternative you seriously weighed and can explain why you didn't choose (this is true for every architecture decision in your other prep docs too — reuse those trade-off explanations here).
- **"What would you do differently now?"** → Never answer "nothing" — even a small, honest refinement is expected and valued.
- **"How did the other person/team react?"** → Especially for Disagree-and-Commit or Earn Trust stories — be honest if there was friction, not just a tidy resolution.
- **"What was the hardest part?"** → Usually a good prompt to reveal the real trade-off or emotional/political difficulty, not just the technical one.

---

## Quick-pick reference table (use this in the room)

| Principle | Best story | Backup story |
|---|---|---|
| Ownership | BT project migration | Qatar Airways 200+ app migration |
| Invent and Simplify | Fastpass (resisting over-agentic design) | AskHR RAG-vs-fine-tune |
| Are Right, A Lot | AskHR RAG choice | Loyalty bot live-vs-ingested data split |
| Learn and Be Curious | Cloud→AI architecture transition | Recent hands-on rebuild of production patterns |
| Insist on Highest Standards | AstraZeneca citation-only gate | Lloyds adversarial/red-team testing |
| Think Big | Reusable governance/eval platform | Cargo manifest extraction expansion |
| Dive Deep | AskHR chunking root-cause | — |
| Have Backbone; Disagree and Commit | Lloyds read-only stance | — |
| Bias for Action | AskHR phased knowledge-base launch | — |
| Earn Trust | Lloyds/AstraZeneca compliance buy-in | — |
| Deliver Results | Aggregate portfolio outcomes | Pick any single project's number |

### One last habit worth building
In the actual interview, don't announce which principle you think the question maps to — just answer with the story. If you're wrong about which principle they're probing, a well-told, specific, "I"-focused STAR story with a real trade-off and an honest reflection still scores well on *something*, because good judgment shows up across principles. Being right about the LP label matters far less than being specific and honest in the story itself.
