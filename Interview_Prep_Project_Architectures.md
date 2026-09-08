# Interview Prep: Project Architectures & Hands-On Lab Plan
Umapathy Boopathy — Principal AI Architect

---

## How to structure any architecture answer in the interview

For every project below, use this 5-part shape when asked "tell me about a project" or "walk me through the architecture":

1. **Context** — client, business problem, scale/constraints
2. **Requirements & NFRs** — what forced the design (compliance, latency, volume, security)
3. **Architecture** — components, data flow, why each tech was chosen (be ready to defend alternatives you rejected)
4. **Hard part / trade-off** — the one decision that wasn't obvious, and why you made it
5. **Outcome** — the number (cost saved, tickets deflected, time cut)

Interviewers dig hardest into #3 and #4. That's why the hands-on labs below exist — so when someone asks "why LangGraph over AutoGen for the Loyalty bot" or "how did you handle hallucination in AskHR," you've actually felt the friction, not just described it.

---

# 1. QATAR AIRWAYS (Virtusa, 2024–Present)

## 1.1 AskHR Chatbot — Agentic RAG Virtual Assistant

**Context:** Employees needed self-service answers on HR policy, payroll, and benefits without raising tickets.

**Architecture:**
```
Employee query (Teams/Web widget)
        │
        ▼
   Orchestration layer (LangChain agent)
        │
        ├──► Intent/routing node ──► decides: policy Q&A / payroll / benefits / escalate
        │
        ▼
   Retrieval layer
        ├── Vector store (embeddings of HR policy docs, payroll handbooks)
        ├── Chunking + metadata filters (department, policy version, region)
        │
        ▼
   Claude (generation) — grounded answer + citation of source policy doc
        │
        ▼
   Guardrails: Azure AI Content Safety filter on input/output
        │
        ▼
   Response + confidence score → escalate to HR ticket if low confidence
```

**Key components to be ready to name:**
- Document ingestion pipeline (policy PDFs/HTML → chunked → embedded)
- Vector DB (be ready to say which — Pinecone/PGVector/Chroma; pick one and know it cold)
- LangChain retrieval chain + Claude for generation
- Fallback-to-human-ticket logic when confidence is low
- Observability: Ragas (faithfulness, answer relevancy) + LangSmith (trace/replay)

**Trade-off to articulate:** Why RAG instead of fine-tuning on HR docs — policies change frequently (leave rules, payroll cycles), so fine-tuning would go stale; RAG lets you swap the knowledge base without retraining.

**Likely interview questions:**
- How did you chunk the HR documents, and why that chunk size?
- How do you prevent the bot from giving wrong payroll advice (hallucination risk in a comp-sensitive domain)?
- How did you measure "ticket volume reduction" — what was the before/after methodology?
- What happens when the retrieved context doesn't contain the answer?
- How is PII (employee ID, salary) handled in the pipeline / logs?

**Hands-on lab to rebuild a mini version:**
- Build a small RAG pipeline: ingest 20–30 sample "HR policy" style docs → chunk → embed → retrieve → Claude generates answer with citation.
- Use: `anthropics/claude-cookbooks` (RAG + tool use sections) + `pinecone-io/pinecone-examples` or Chroma.
- Add: a Ragas eval script scoring faithfulness/context precision on 10 test questions.
- Goal: be able to say "I built and evaluated this exact pattern" not just "I architected it."

---

## 1.2 Loyalty (Privilege Club) Chatbot — Multi-Agent + MCP Tool Calling

**Context:** Premium customers need real-time answers on tier status, mileage redemption, and upgrade eligibility — this requires live lookups into membership/mileage systems, not just static knowledge.

**Architecture:**
```
Customer query
     │
     ▼
Supervisor agent (LangGraph state machine)
     │
     ├──► Tier/Benefits agent ──► MCP tool call ──► Membership system API
     ├──► Redemption agent    ──► MCP tool call ──► Mileage/Loyalty ledger API
     ├──► Upgrade eligibility agent ──► MCP tool call ──► Booking/Inventory system
     │
     ▼
Aggregator node — merges sub-agent outputs into one coherent answer
     │
     ▼
Response to customer (with real-time balance/eligibility, not stale data)
```

**Why LangGraph + AutoGen together:** LangGraph for the deterministic state machine/control flow (you need predictable routing for a customer-facing financial-adjacent flow), AutoGen for the more exploratory multi-agent conversation patterns in edge cases (e.g., ambiguous redemption requests needing negotiation between agents).

**Why MCP specifically:** standardizes how each agent calls out to membership/mileage systems — one protocol instead of bespoke API wrappers per agent, easier to add a new backend system later without rewriting agent logic.

**Likely interview questions:**
- Why a supervisor/multi-agent pattern instead of one large agent with many tools?
- How do you keep the mileage balance from being stale or wrong (cache vs. live call)?
- What happens if a downstream membership API times out mid-conversation?
- How do you test a stateful multi-agent graph — what's your eval strategy for agent handoffs?
- Security: how is the MCP tool call scoped so the agent can't access another customer's account?

**Hands-on lab:**
- Build a 2–3 agent LangGraph graph: a supervisor + two worker agents each calling a **mock** MCP tool (e.g., wrap a fake "membership API" as an MCP server).
- Use: `langchain-ai/langgraph-101` (multi-agent notebooks) + `modelcontextprotocol/servers` (Filesystem or Memory server as a stand-in pattern, then write your own tiny custom MCP server).
- Add: a failure-injection test (make the mock API time out) and handle it gracefully in the graph.

---

## 1.3 WebCheck-In Fastpass Automation

**Context:** Manual verification steps in self-service check-in were slowing passengers down.

**Architecture:** Agentic process orchestration using explicit state machines (not a conversational agent — a workflow automation problem):
```
Check-in request → State: Identity Verify → State: Document Check
   → State: Seat/Bag Rules Validation → State: Boarding Pass Issue
(each state = a deterministic step, with an LLM step only where
 unstructured judgment is needed, e.g., document image validation)
```

**Key point to make in interview:** this is where you draw the line between "use an LLM agent" and "use a plain state machine" — most of Fastpass is deterministic business rules; the LLM/agent is only in the narrow slice needing judgment (e.g., interpreting a passport photo edge case). Interviewers like architects who *don't* over-apply GenAI everywhere.

**Likely interview questions:**
- Where exactly does the LLM add value here vs. plain rules engine?
- How did you reduce "manual verification steps" — what was manual before, automated after?
- How do you handle a state machine failure mid-flow (passenger stuck between states)?

**Hands-on lab:**
- Build a small LangGraph state machine (not agent-conversation style) modeling a 4–5 step approval workflow with one step calling an LLM for unstructured judgment and the rest deterministic.
- Use: `langchain-ai/langgraph-101` state machine examples.

---

## 1.4 Agent Evaluation, Guardrails & Domain LLM Customization (cross-cutting)

**Architecture (applies across AskHR + Loyalty):**
- **Observability:** LangSmith traces every agent step/tool call; Ragas scores RAG outputs (faithfulness, answer relevancy, context recall) on a held-out eval set, run in CI before deploying prompt/retrieval changes.
- **Safety:** Azure AI Content Safety on the Azure-hosted flows, Vertex AI Safety Filters where GCP components are used — layered, not single point of failure.
- **Domain customization:** Azure AI Foundry / Vertex AI custom models fine-tuned or prompt-tuned specifically for cargo manifest and HR document extraction accuracy (structured extraction is a different problem than conversational RAG — worth distinguishing in interview).

**Likely interview questions:**
- What specific Ragas/LangSmith metrics did you track, and what was your threshold to block a deploy?
- How do you measure hallucination rate quantitatively, not just "we noticed fewer errors"?
- Why two different safety layers (Azure + Vertex) instead of one — was that a technical need or a legacy-of-two-clouds situation?

**Hands-on lab:**
- Take the RAG pipeline from 1.1 and wire in a Ragas eval + a simple LangSmith trace (or open-source equivalent) so you can screen-share a real eval dashboard if asked "show me."

---

## 1.5 Cloud Migration, DevSecOps, Terraform/AKS (infra side)

**Architecture:** 200+ apps migrated to Azure + 50+ to private cloud; Terraform IaC + GitHub Actions/Azure DevOps CI/CD on AKS; DevSecOps gates (secrets scanning, policy enforcement) embedded in the pipeline, not bolted on after.

**Likely interview questions:**
- Walk me through one specific application's migration — lift-and-shift or re-architected?
- Where exactly did the 40% cost reduction come from (rightsizing, reserved instances, decommissioning, containerization)?
- What did your Terraform module structure look like — how did you avoid state file conflicts across 200+ apps?
- What DevSecOps gate would block a deployment, and what happens then?

**Hands-on lab:**
- Stand up a small AKS cluster via Terraform with a CI/CD pipeline that includes a security scan gate (Trivy/Checkov) — mirrors exactly what you'd be asked to whiteboard.
- Use: `didiberman/practical-aks` (Terraform + AKS + Trivy + GitHub Actions, includes a keyless Azure OpenAI inference pattern relevant to your AI work too).

---

# 2. ASTRAZENECA (Aug 2023 – Jan 2024)

## 2.1 GenAI Scientific Literature & Regulatory-Intelligence Assistant (RAG)

**Context:** Research teams needed faster literature review and regulatory submission prep, over internal clinical/research corpora — a regulated, high-precision domain (wrong answers have real consequences).

**Architecture:**
```
Internal corpora (clinical trial docs, regulatory filings, literature)
        │
        ▼
  Ingestion + chunking (domain-aware: preserve section/table structure)
        │
        ▼
  Embeddings → Vector store (likely OpenSearch/Bedrock KB or similar, given AWS context)
        │
        ▼
  Retrieval + Claude/Bedrock model generation
        │
        ▼
  Citation-grounded output (mandatory — no answer without traceable source, for GxP audit trail)
```

**Key distinguishing point vs. AskHR:** GxP compliance means every answer needs an audit trail back to the source document and version — this is a much stricter grounding requirement than an HR chatbot. Be ready to explain how you enforced "no ungrounded claims."

**Likely interview questions:**
- How do you guarantee the model doesn't answer from its own training data instead of the retrieved corpus (a common regulatory concern)?
- How did you handle tables/figures in scientific PDFs during chunking?
- What audit trail exists for a generated answer — can you trace it back six months later?
- How is this different from a general-purpose RAG chatbot given GxP requirements?

**Hands-on lab:**
- Rebuild a scientific-PDF RAG pipeline that forces citation-only answers (reject/flag any answer without a matching retrieved chunk).
- Use: `anthropics/claude-cookbooks` (RAG + citations sections) + `aws-samples/amazon-bedrock-workshop` (Knowledge Bases + RAG lab).

## 2.2 ML Pipelines (SageMaker + Bedrock) for Clinical Data / Genomics

**Architecture:** SageMaker for training/experimentation pipelines on genomics data, Bedrock for foundation-model-based processing of clinical text — two different workloads (traditional ML training vs. LLM inference) integrated into one MLOps flow.

**Likely interview questions:**
- Why SageMaker for genomics but Bedrock for clinical text — what's the technical boundary between the two?
- How did you cut training/iteration time by 40% — pipeline parallelization, spot instances, data pipeline optimization?
- What does your GxP-aligned MLOps governance actually enforce (model versioning, validation gates, audit trails) — walk through a model promotion from dev to prod.

**Hands-on lab:**
- Use `aws-samples/amazon-bedrock-workshop` labs 01–03 (text generation, RAG, model customization) to get concrete Bedrock API reps.
- If you want SageMaker reps too, a basic SageMaker training-job notebook (any AWS official SageMaker example) alongside it, so you can speak to both halves of this pipeline.

## 2.3 Terraform + GitHub Actions CI/CD on EKS

Same prep as the AKS lab above (§1.5), but be ready to name the EKS-specific differences if asked (IAM roles for service accounts vs. Azure AD workload identity, EKS networking/VPC CNI vs. AKS CNI).

---

# 3. LLOYDS BANKING GROUP (May 2022 – Jul 2023)

## 3.1 AI-Powered Banking Chatbot Integrated with IVR + Core Banking

**Context:** Deflect toll-free customer service call volume; must integrate with legacy IVR and core banking systems — heavily regulated, high-availability, audit-sensitive environment.

**Architecture:**
```
Customer channel (IVR / web / app)
        │
        ▼
   NLU/Intent layer ──► routes: balance inquiry / dispute / general query
        │
        ├──► Core banking system integration (read-only balance/transaction lookups)
        ├──► Knowledge base (FAQ/policy RAG)
        │
        ▼
   Response generation (with strict guardrails — no financial advice generation,
   no unauthorized account actions from the bot)
        │
        ▼
   Escalation to human agent if confidence low or transaction-type request
```

**Key trade-off:** in banking, the LLM is deliberately kept away from any *write* action on the account — it can retrieve/explain but not execute transactions. This is a design decision interviewers in fintech love to probe.

**Likely interview questions:**
- Why is the bot read-only against core banking — what's the risk model behind that decision?
- How does it integrate with legacy IVR (protocol/API specifics)?
- How did you validate the 30% telephony cost reduction — call volume data, deflection rate methodology?
- What compliance/audit requirements shaped this differently from a generic chatbot?

**Hands-on lab:**
- Build a small RAG+guardrail chatbot with a hard rule layer: certain intents (e.g., "transfer money") are explicitly blocked from LLM execution and routed to a stub "human escalation" function instead.
- Use: `anthropics/claude-cookbooks` (tool use section — build a tool the model is *not* allowed to call for certain intents, and demonstrate the guardrail).

## 3.2 Enterprise API Management Platform (millions of transactions/day)

**Likely interview questions:**
- What API Management platform (Azure APIM/Kong/Apigee) and why?
- How did you ensure high availability and audit-readiness at that transaction volume — rate limiting, caching, circuit breakers?
- What did the migration cutover look like — how did you avoid downtime?

**Hands-on lab:** less GenAI-specific — if time-constrained, deprioritize vs. the RAG/agent labs above, but be ready to talk through API gateway patterns (rate limiting, auth, versioning) conceptually since this is a "describe, don't necessarily rebuild" area.

## 3.3 Hybrid Cloud (AWS + Azure + on-prem) & Kubernetes/GitHub Enterprise Migration

**Likely interview questions:**
- What made this hybrid rather than single-cloud — regulatory data residency, latency, legacy dependency?
- How did you achieve "100% delivery success" on the Kubernetes/GitHub Enterprise migration — what was your rollback plan?

---

# Suggested prep sequence (given limited time)

| Priority | Project focus | Lab | Time |
|---|---|---|---|
| 1 | AskHR (RAG) | Claude cookbooks RAG + Ragas eval | 2–3 days |
| 2 | Loyalty bot (multi-agent + MCP) | LangGraph-101 + custom MCP server | 3–4 days |
| 3 | Lloyds chatbot (guardrails) | Claude cookbooks tool-use + blocked-action pattern | 1 day |
| 4 | AstraZeneca RAG (citation-strict) | Bedrock workshop KB/RAG lab | 2 days |
| 5 | Fastpass (state machine) | LangGraph state-machine notebook | 1 day |
| 6 | Terraform/AKS infra | practical-aks repo | 1–2 days |

For each, after the lab, write yourself a **one-page "if asked, I'd say..."** answer using the 5-part structure at the top of this doc — that's what actually gets rehearsed before an interview, not the code itself.
