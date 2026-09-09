# TOGAF / Enterprise Architecture Perspective
How to walk an interviewer through each project using the TOGAF ADM — for when the conversation shifts from "architecture" in the general sense to "Enterprise Architecture" specifically.

---

## Why this matters and how it's different from your other prep

Everything in your other prep docs answers "what did you build and why." This document answers a different question interviewers sometimes deliberately ask once they see "TOGAF Certified" on your resume: **"okay, but did you actually run this like an Enterprise Architect, or did you just design a system?"** That's a real distinction — TOGAF is a governance and stakeholder-alignment discipline as much as a design method, and a Principal/Enterprise Architect interviewer will specifically probe whether you used it as a framework for decisions and governance, not just a certification you hold.

**Quick ADM refresher (say these phase names naturally when narrating, don't recite them like a script):**

| Phase | What it covers |
|---|---|
| Preliminary | Establish architecture principles, capability, and governance framework |
| A — Architecture Vision | Stakeholders, business drivers, scope, high-level target state |
| B — Business Architecture | Capabilities, value streams, organizational impact |
| C — Information Systems Architecture | Data Architecture + Application Architecture |
| D — Technology Architecture | Infrastructure, platforms, technology standards |
| E — Opportunities & Solutions | Gap analysis, build-vs-buy, work packages |
| F — Migration Planning | Roadmap, sequencing, risk-based prioritization |
| G — Implementation Governance | Architecture contracts, compliance reviews, sign-off gates |
| H — Architecture Change Management | Monitoring, drift detection, triggers for re-architecture |
| Requirements Management (center of the cycle) | Continuous — requirements captured and traced across every phase |

---

## The one thing to say early if asked "how does TOGAF even apply to agentic AI, given the framework predates GenAI"

*"TOGAF's ADM is technology-agnostic by design — it doesn't need to know about LLMs to still be the right way to move from a business driver to a governed, phased rollout. Where I did have to adapt it was in the Preliminary phase's architecture principles — I added AI-specific principles (no ungrounded answers ship, every agent tool call must be scoped and auditable, guardrails are non-negotiable, not optional) and in Phase H, where change management cadence had to be much faster than traditional IT, because a prompt or retrieval change is a much lower-risk, higher-frequency change than a typical application change — so the governance gate needed to be lightweight enough not to block that pace, while still catching the things that actually matter, like a change that weakens a guardrail."* That answer shows you're not reciting the framework — you actually adapted it.

---

# 1. QATAR AIRWAYS — treated as one Enterprise AI program (AskHR + Loyalty + Fastpass + cargo extraction + cloud migration)

**Preliminary Phase:** Established AI-specific architecture principles alongside Qatar Airways' existing EA principles — e.g., "no generated answer ships without grounding," "every agent tool call is scoped and logged," "cloud-native on the client's existing Azure landing zone unless a documented technical reason justifies otherwise." Defined (or plugged into) an Architecture Review Board with representation from IT, HR, Commercial/Loyalty, and Security — this board is the governance backbone referenced in Phase G below.

**Phase A — Architecture Vision:** Stakeholders: HR leadership (ticket volume pain), Commercial/Loyalty (customer experience), IT Operations, Security/Compliance. Business drivers: reduce HR ticket load, improve premium customer self-service, speed up passenger check-in. Produced a Statement of Architecture Work scoping the AI program (which use cases, in what sequence, with what success metrics) and a high-level Architecture Vision showing the target state — a shared agentic AI platform capability, not three unrelated bots.

**Phase B — Business Architecture:** Mapped the affected business capabilities — Employee Self-Service, Customer Loyalty Management, Passenger Processing — and modeled the value streams before/after (e.g., "Resolve Employee HR Query": before = raise ticket → wait → HR responds; after = ask AskHR → grounded answer or escalate). This is where I identified the organizational impact: HR's role shifts from first-line query response toward reviewing escalations and maintaining the policy content that feeds the knowledge base — a real operating-model change worth naming if asked "what changed for the business, not just the technology."

**Phase C — Information Systems Architecture:**
- *Data Architecture:* defined the data domains (HR policy/payroll content, membership/mileage data, cargo manifest data) with sensitivity classification (PII in HR data, financial-adjacent data in loyalty) driving what could be ingested into a shared vector store versus what had to remain a live, access-controlled API call.
- *Application Architecture:* the LangChain/LangGraph agent applications, MCP tool-integration layer, and Azure AI Foundry model-serving layer as reusable application components — deliberately designed so the second and third use case could reuse the retrieval, guardrail, and evaluation components rather than each project building its own.

**Phase D — Technology Architecture:** Azure landing zone (APIM, AKS, Azure AI Foundry, Azure DevOps) as the primary technology standard; GCP (Vertex AI Custom Models, Cloud Run, GKE) formally documented as an approved exception for the cargo-manifest extraction workload specifically, not an ungoverned deviation — this is an important distinction if asked "how did a second cloud get introduced without breaking your standards."

**Phase E — Opportunities & Solutions:** Gap analysis between current state (manual HR ticketing, no self-service; static loyalty FAQ with no personalized real-time answers) and target state. Build-vs-buy assessment — evaluated vendor chatbot platforms versus a custom-built RAG/agent solution, and justified build specifically because of the grounding, audit, and guardrail requirements a generic vendor product couldn't guarantee. Grouped the work into transition architecture packages: AskHR (Increment 1), Loyalty bot (Increment 2), Fastpass (Increment 3), cargo extraction (Increment 4).

**Phase F — Migration Planning:** Sequenced by a mix of value and risk — AskHR first (highest ticket volume, lowest technical/data-integration complexity, fastest win to build program credibility), then the Loyalty bot (higher complexity — live system integration via MCP, financial-adjacent data), then Fastpass and cargo extraction. This sequencing itself is a good answer if asked "how did you prioritize" — value-per-unit-of-risk, not just business demand order.

**Phase G — Implementation Governance:** Each increment went through Architecture Review Board sign-off before production release, using an Architecture Contract with the delivery team that made specific guardrail and evaluation requirements non-negotiable conditions of go-live (not just recommendations) — e.g., AskHR could not launch without the confidence-threshold escalation logic in place, regardless of delivery timeline pressure.

**Phase H — Architecture Change Management:** Established a lighter-weight but still governed change path for prompt/retrieval changes (fast cadence, automated eval gate) versus a heavier path for anything touching guardrails, data classification, or introducing a new cloud/technology (goes back through the Review Board). This split is what let the program move fast on iteration while still catching the changes that actually mattered — the cargo-manifest GCP decision went through the heavier path.

---

# 2. ASTRAZENECA

**Preliminary Phase:** Architecture principles here were shaped directly by GxP/21 CFR Part 11 requirements — traceability, validation, and auditability weren't optional principles, they were regulatory constraints baked into the principle set from day one.

**Phase A — Architecture Vision:** Stakeholders: research scientists (the actual users), Regulatory Affairs, Quality/Compliance, IT. Vision: accelerate literature review and regulatory submission prep without compromising GxP compliance — the vision statement explicitly named "citation-grounded, audit-ready" as a target-state property, not an implementation detail decided later.

**Phase B — Business Architecture:** Mapped to the Clinical Research and Regulatory Submission Preparation value streams — showing where in the existing (slow, manual) literature-review process an AI-assisted step would sit, and which roles (research scientists, regulatory reviewers) interact with the new capability.

**Phase C — Information Systems Architecture:**
- *Data Architecture:* clinical trial documents, regulatory filings, and literature treated as a versioned, classified data domain — critically, a document taxonomy that preserved version history rather than overwriting, since GxP audit may need to reference what was known at a specific past date.
- *Application Architecture:* the RAG assistant (Bedrock Knowledge Bases + Claude/Bedrock generation) and the SageMaker-based ML pipeline as two distinct application components serving different workload types (conversational retrieval vs. model training) under one MLOps governance umbrella.

**Phase D — Technology Architecture:** AWS-native stack (API Gateway, Bedrock, SageMaker, EKS) — chosen partly because AstraZeneca's existing AWS investment and partly because SageMaker's model governance/versioning capabilities directly supported the GxP validation requirements from the Preliminary phase principles.

**Phase E — Opportunities & Solutions:** Gap analysis between fully manual literature review and an AI-assisted process; the solution option analysis is where the "citation-or-nothing" architectural constraint was decided — evaluated as a hard validation gate rather than a soft prompt instruction, specifically because a "best effort" grounding approach wouldn't pass GxP scrutiny.

**Phase F — Migration Planning:** Phased rollout starting with a single research group as a validated pilot before wider rollout — deliberately slower than a typical enterprise software rollout, because each phase required its own GxP validation evidence package, not just user acceptance testing.

**Phase G — Implementation Governance:** GxP validation *is* the architecture governance gate in this context — model/prompt promotion from dev to production required a documented validation protocol with sign-off, functionally equivalent to a TOGAF Architecture Contract but framed in regulatory validation language for the client's compliance team.

**Phase H — Architecture Change Management:** Any change to the underlying model, prompt, or retrieval logic triggers a re-validation requirement — this is Architecture Change Management operating at a stricter cadence than Qatar Airways' lighter-weight prompt-change path, and worth contrasting the two explicitly if asked how governance differs by regulatory context.

---

# 3. LLOYDS BANKING GROUP

**Preliminary Phase:** Architecture principles driven by banking risk appetite — no unauthorized write/transaction actions from an AI system, strict data residency and access-boundary requirements, and an assumption that any AI-facing component must coexist with, not replace, existing regulated core-banking integration.

**Phase A — Architecture Vision:** Stakeholders: Customer Service operations, Risk/Compliance, the Core Banking platform team, IT. Vision: deflect toll-free call volume while explicitly preserving the existing risk posture — the vision document named "read-only, advisory-only" as a target-state constraint upfront, not a compromise negotiated later under pressure.

**Phase B — Business Architecture:** Mapped to the Customer Service value stream, with the Core Banking Integration capability treated as an already-mature, non-negotiable capability to integrate with rather than modernize — an important call: not every legacy capability needs re-architecting just because a new AI capability is being introduced next to it.

**Phase C — Information Systems Architecture:**
- *Data Architecture:* FAQ/policy content as one classified data domain (ingestible, RAG-appropriate); account/transaction data as a separate, strictly access-controlled domain that is never ingested, only queried live.
- *Application Architecture:* the chatbot/NLU application on GCP Vertex AI, IVR integration components, and the dual-gateway pattern (IBM API Connect for core banking, Apigee for the new AI-facing surface) as distinct, clearly bounded application components.

**Phase D — Technology Architecture:** Deliberately hybrid — IBM API Connect retained for legacy core-banking exposure (a documented decision *not* to re-platform a working, regulated integration just for tooling consistency), Apigee and GCP (Vertex AI, Cloud Run, GKE) introduced as the technology standard for the new AI-facing capability specifically.

**Phase E — Opportunities & Solutions:** Gap analysis between legacy IVR/call-center-only service and an AI-augmented deflection model; the build-vs-buy and platform-boundary decision (keep IBM API Connect vs. replace it) was explicitly evaluated and the "keep and layer" option chosen for risk and cost reasons — this is a strong answer if asked about a build-vs-buy or replace-vs-integrate decision specifically.

**Phase F — Migration Planning:** Phased: read-only/advisory launch first, human-escalation for anything transactional, with any future extension toward write-capability explicitly deferred to a later phase pending risk sign-off rather than attempted in the first release — a direct application of TOGAF's risk-based sequencing principle to an AI trust problem, not just a technical rollout problem.

**Phase G — Implementation Governance:** Architecture Review Board sign-off specifically included Risk/Compliance as a mandatory gate, not just an IT architecture review — the Architecture Contract with the delivery team made "no callable transaction-execution function" a binding constraint, enforced at the tool/function level, not just documented as a policy.

**Phase H — Architecture Change Management:** Any proposal to expand the bot's capability (e.g., toward transactional actions) is explicitly required to go back through the full governance cycle rather than being treated as a minor iteration — this is the direct architectural mechanism behind the "held the line on read-only" story in your STAR prep; the two documents reinforce each other if you're asked about both in the same interview.

---

# Common TOGAF/Enterprise Architecture-specific interview questions

**Q1. "Which TOGAF artifacts did you actually produce on these engagements?"**
> Be concrete and don't over-claim: Architecture Vision documents and Statements of Architecture Work at program kickoff, Business Architecture capability/value-stream maps, Application and Data Architecture component models, an Architecture Roadmap sequencing the increments, and Architecture Contracts used at the governance-gate stage with delivery teams. If a specific artifact wasn't formally produced on a given engagement, say so plainly rather than claiming a full artifact set you didn't actually build — "we ran governance more lightweight on this one, using an Architecture Contract-equivalent checklist rather than the full formal artifact" is a credible, honest answer.

**Q2. "How do you handle the tension between Enterprise Architecture governance and the speed GenAI teams want to move at?"**
> Split the change-management cadence by risk, as described in Phase H above — lightweight, fast-cycle governance for prompt/retrieval changes with automated evaluation gates, heavier governance for anything touching guardrails, data classification, or new technology introduction. The mistake to avoid is applying one uniform governance speed to everything, which either blocks legitimate fast iteration or lets risky changes through a rubber-stamp process.

**Q3. "How do you keep the Architecture Repository/reference models current when GenAI patterns are evolving faster than traditional IT architecture cycles?"**
> Treat the reference architecture as a living set of validated patterns (retrieval pipeline, guardrail pattern, evaluation pattern) that get revisited each time a new use case surfaces a gap — not a document reviewed annually. The cargo-manifest extraction project surfacing the need for a documented cloud-exception process is a concrete example of the repository evolving in response to real project pressure rather than a scheduled review.

**Q4. "Tell me about a build-vs-buy decision you made using TOGAF's Opportunities & Solutions phase."**
> Use the AskHR vendor-chatbot-vs-custom-build decision, or the Lloyds "keep IBM API Connect vs. replace it" decision — both have a clear rationale (grounding/audit control in one case, risk/cost of re-platforming a regulated integration in the other) that shows genuine option evaluation, not a foregone conclusion.

**Q5. "How do you manage stakeholder disagreement during Phase A when business wants speed and compliance wants caution?"**
> Bring the disagreement into the Architecture Vision document itself as an explicit constraint or open risk, rather than resolving it informally in a hallway conversation — this creates a documented decision the Architecture Review Board can revisit later, and it's exactly the kind of paper trail that protected the "read-only" decision at Lloyds when there was later pressure to expand scope.

**Q6. "What's your approach to Requirements Management across the ADM cycle for an AI system, given requirements can shift as stakeholders see the system behave?"**
> Requirements Management isn't a one-time capture at Phase A — for AI systems specifically, real usage data (which queries escalate, which intents are most common) becomes a requirements-refinement input that feeds back into later phases. I treated the AskHR escalation-rate data as a live requirements signal, not just an operational metric — it informed later ingestion-pipeline and chunking changes, which is Requirements Management operating continuously rather than as a phase-gate exercise.

---

### How to use this alongside your other prep
Pull this document out specifically when the conversation shifts from "walk me through your architecture" to "walk me through your architecture *governance*" or when TOGAF is mentioned by name. Don't lead with this framing unprompted in a general technical interview — it can read as over-formal if the interviewer just wants the system design. Use it when they signal they want the Enterprise Architecture angle specifically.
