# "If Asked, I'd Say..." — Rehearsed Project Answers
Umapathy Boopathy | Use these as speaking scripts, not reading scripts — say them out loud a few times until they sound like you, not like a document.

---

## 1. AskHR Chatbot (Qatar Airways)

**Context.** "At Qatar Airways, employees were raising a high volume of HR tickets for things that were really just lookups — leave policy, payroll cycle questions, benefits eligibility. That was consuming HR team bandwidth on repetitive queries."

**Requirements/NFRs.** "The two constraints that shaped the design were: one, the policy content changes fairly often — leave rules, payroll cycles — so whatever we built couldn't go stale. Two, this is comp-sensitive information, so wrong answers are worse than no answer; we needed grounded, traceable responses, not the model's general knowledge."

**Architecture.** "I architected an agentic RAG assistant using Claude and LangChain over the HR, payroll, and benefits knowledge bases. Documents are chunked and embedded into a vector store, retrieval pulls the relevant policy sections, and Claude generates the answer grounded strictly in that retrieved content, with the source policy cited back to the user. There's a confidence threshold — if retrieval doesn't return a strong match, it doesn't guess, it routes to a human HR ticket instead of answering."

**Hard part/trade-off.** "The trade-off I made deliberately was RAG over fine-tuning. Fine-tuning on the HR corpus would've given faster, more fluent answers, but every policy update would mean retraining. With RAG, we just re-index the knowledge base when a policy changes — the model itself doesn't need to know anything new. I also had to be strict about the 'no answer without a grounded source' rule, because in an HR context, a confident wrong answer does more damage than an escalation."

**Outcome.** "That combination — grounded retrieval plus a hard fallback to a human ticket — is what let us cut HR ticket volume meaningfully while keeping the risk of bad advice low."

---

## 2. Loyalty (Privilege Club) Chatbot (Qatar Airways)

**Context.** "This was for premium customers navigating tier benefits, mileage redemptions, and upgrade eligibility — and unlike AskHR, this isn't static knowledge, it needs live lookups into membership and mileage systems."

**Requirements/NFRs.** "The requirement that drove the architecture was real-time accuracy — a customer's mileage balance or upgrade eligibility can change between one interaction and the next, so we couldn't rely on cached or static data. It also needed to stay predictable and auditable, since it's touching loyalty-program transactions, even if only reads."

**Architecture.** "I built this as a multi-agent system with LangGraph handling the orchestration — a supervisor agent routes the customer's intent to specialized worker agents: one for tier/benefits, one for redemption, one for upgrade eligibility. Each of those agents calls out to the actual membership or mileage system through MCP-based tool calling, so the data is always live, not cached. I used AutoGen for the more exploratory conversational patterns — cases where the request is ambiguous and agents effectively need to negotiate or clarify before acting."

**Hard part/trade-off.** "The trade-off was LangGraph for the deterministic control flow versus AutoGen for the flexible conversational layer — I didn't want one framework doing both jobs. A single large agent with every tool attached would've been harder to reason about and test. Splitting it into a supervisor plus scoped worker agents, each with MCP access to only the systems it needs, also gave us a security boundary — an agent handling tier benefits doesn't have blanket access to the mileage ledger."

**Outcome.** "The result was customers getting accurate, real-time answers on redemptions and upgrades instead of stale or generic responses, without us having to build one monolithic, hard-to-maintain agent."

---

## 3. WebCheck-In Fastpass Automation (Qatar Airways)

**Context.** "Fastpass self-service check-in had manual verification steps slowing passengers down — identity checks, document validation, seat and bag rule checks before boarding pass issuance."

**Requirements/NFRs.** "This needed to be fast and deterministic for the vast majority of passengers, but still handle the judgment-call cases — like an edge-case document photo — without falling over."

**Architecture.** "I deliberately did not build this as a conversational agent. It's an explicit state machine — identity verify, document check, seat/bag validation, boarding pass issue — each a deterministic step. The only place an LLM is involved is the document validation step, where there's genuine unstructured judgment needed, like interpreting a passport photo that doesn't match a clean template."

**Hard part/trade-off.** "The trade-off here was resisting the temptation to make the whole thing 'agentic' just because GenAI was available elsewhere in the program. Most of Fastpass is business rules — deterministic, testable, and honestly better served by a plain state machine than an LLM. I only introduced the model where a rules engine genuinely couldn't handle the ambiguity."

**Outcome.** "That restraint is actually what made it reliable — we reduced manual verification steps and sped up check-in without introducing a hard-to-debug agent into a high-volume operational flow."

---

## 4. GenAI Scientific Literature & Regulatory-Intelligence Assistant (AstraZeneca)

**Context.** "Research teams at AstraZeneca needed faster literature review and regulatory submission prep, pulling from internal clinical and research corpora."

**Requirements/NFRs.** "This is a GxP environment — every answer needs an audit trail back to a specific source document and version. That's a much stricter grounding bar than a typical RAG chatbot; the model absolutely cannot answer from its own training knowledge, only from the retrieved corpus."

**Architecture.** "I architected a RAG pipeline over the internal clinical and research corpora — domain-aware chunking that preserves table and section structure, since a lot of the critical data in these documents lives in tables, not prose. Retrieval feeds into the generation step, and every generated answer is required to carry a citation back to the specific retrieved chunk. If there's no matching chunk, there's no answer."

**Hard part/trade-off.** "The hard part was enforcing 'citation-only' as a hard constraint rather than a nice-to-have — building the validation that rejects or flags any generated claim that doesn't trace back to a retrieved passage, which is what GxP audit requirements actually demand. That's a meaningfully higher bar than the HR chatbot, where an ungrounded answer is a nuisance rather than a compliance problem."

**Outcome.** "This accelerated literature review and regulatory submission prep for the research teams, while keeping every answer defensible under GxP audit — which was non-negotiable given the regulatory environment."

---

## 5. AI-Powered Banking Chatbot Integrated with IVR + Core Banking (Lloyds)

**Context.** "Lloyds needed to deflect a large volume of toll-free customer service calls — balance inquiries, general queries, disputes — without compromising the audit and compliance posture core banking requires."

**Requirements/NFRs.** "The defining constraint was risk, not capability. In a regulated banking environment, the question isn't 'can the bot do this,' it's 'what's the blast radius if it's wrong.' So the requirement was: retrieve and explain, never execute."

**Architecture.** "The bot integrates with the IVR and core banking systems for read-only lookups — balance and transaction history — plus a RAG layer over FAQ and policy content for general queries. Anything that would touch the account — a transfer, a dispute action — is explicitly excluded from the model's capability and routed to a human agent instead."

**Hard part/trade-off.** "The trade-off I made was deliberately limiting the bot's capability rather than maximizing it. It would've been technically possible to let the bot initiate certain transactions, but the risk model in banking doesn't reward that — one bad automated transaction erodes trust far more than a slower manual escalation path. So I drew a hard line: read and explain is in scope, write and execute is not."

**Outcome.** "That constraint is actually what made adoption possible — compliance and risk teams could sign off on it because the blast radius of a mistake was bounded. It cut telephony support costs by an estimated 30% by deflecting the queries that didn't need a human, while keeping every transactional action with a person."

---

## 6. Terraform + CI/CD on AKS/EKS (Qatar Airways / AstraZeneca)

**Context.** "Across both Qatar Airways and AstraZeneca, I led cloud migrations at scale — 200+ applications to Azure and 50+ to private cloud at Qatar Airways, and Terraform/GitHub Actions CI/CD on EKS at AstraZeneca."

**Requirements/NFRs.** "At that scale, the constraint isn't 'can we provision infrastructure,' it's 'can 200+ teams provision infrastructure consistently without stepping on each other's state, and can security scanning be a gate, not an afterthought.'"

**Architecture.** "I standardized on Terraform modules per application/service pattern with remote state per module to avoid state-file conflicts across teams, and embedded DevSecOps directly into the CI/CD pipeline — automated secrets scanning and policy enforcement run before a deploy is allowed to proceed, not after. On AKS specifically, this cut deployment time by 25%; the equivalent pattern on EKS at AstraZeneca shortened deployment lead time by the same margin."

**Hard part/trade-off.** "The hard part at this scale was balancing standardization with team autonomy — if the Terraform modules are too rigid, teams route around them; if they're too loose, you lose the consistency and security posture you're trying to enforce. I landed on opinionated modules for the security-critical pieces — networking, identity, secrets — with more flexibility left for application-specific configuration."

**Outcome.** "That's ultimately what got us to a 40% infrastructure cost reduction at Qatar Airways — not just migration itself, but the rightsizing and consistency that came from a standardized, security-gated pipeline applied across 200+ applications."

---

### How to use this
Read each one aloud twice. The second time, stop reading and just talk through the five beats from memory — Context, Requirements, Architecture, Trade-off, Outcome — in your own words. If you stumble on the "hard part" beat, that's the one to rehearse most; it's the part interviewers actually remember.
