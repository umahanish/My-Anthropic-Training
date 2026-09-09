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

I've now added an **"☁ Infra Stack"** line to every project below — this is usually the *first* follow-up after any architecture answer ("okay, but what did you actually deploy this on?"), so treat it as part of the core answer, not a footnote.

---

## Infrastructure stack reference (know this cold before any interview)

| Client | Primary stack | Where it applies |
|---|---|---|
| **Qatar Airways** | Azure API Management, Azure AI Foundry, AKS clusters, Azure DevOps (CI/CD) | AskHR, Loyalty bot, Fastpass, core cloud migration |
| **Qatar Airways** (secondary/cross-cloud) | Azure API Management, GCP Vertex AI (Custom Models), Cloud Run, GKE, Azure DevOps | Domain-specific LLM customization (cargo manifest & HR document extraction) |
| **AstraZeneca** | AWS API Gateway, Amazon Bedrock, SageMaker, EKS, GitHub + GitHub Actions | Literature/regulatory RAG assistant, clinical/genomics ML pipelines, EKS platform |
| **Lloyds Banking Group** | IBM API Connect & Apigee, GCP Vertex AI, Cloud Run, GKE, GitHub + GitHub Actions | Banking chatbot, API Management platform, Kubernetes platform |

**Pattern worth naming explicitly if asked "why so many different clouds/gateways across your career":** the stack follows the client's existing enterprise footprint, not a personal preference — Qatar Airways was Azure-first with GCP for specific ML customization needs, AstraZeneca was AWS-native (SageMaker/Bedrock is an AWS-centric pairing), and Lloyds ran IBM API Connect for legacy core-banking integration alongside Apigee/GCP for the newer AI-facing services. That's a *good* answer — it shows you architect to the client's existing landscape rather than forcing one cloud everywhere.

---

# 1. QATAR AIRWAYS (Virtusa, 2024–Present)

## 1.1 AskHR Chatbot — Agentic RAG Virtual Assistant

**Context:** Employees needed self-service answers on HR policy, payroll, and benefits without raising tickets.

**Architecture:**

**A. Ingestion pipeline (offline/batch — runs whenever HR publishes or updates a policy):**
```
Source docs (HR policy PDFs, payroll handbooks, benefits guides
   — pulled from SharePoint / HR document system)
        │
        ▼
   Document loader — extracts text, preserves headings/section structure
        │
        ▼
   Chunking — recursive/semantic chunking (~500–800 tokens, with overlap
   so a policy clause isn't split mid-sentence across chunks)
        │
        ▼
   Metadata tagging — department, policy version, effective date, region
   (this is what lets retrieval later filter to "current version only")
        │
        ▼
   Embedding model — converts each chunk to a vector
        │
        ▼
   Vector store upsert — new chunks added; superseded-version chunks are
   flagged inactive (not deleted, for audit trail) rather than overwritten
```

**B. Runtime query flow (what happens when an employee actually asks something):**
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
        ├── Query embedded with the same embedding model used at ingestion
        ├── Similarity search against the vector store (top-k chunks)
        ├── Metadata filter applied (department, current policy version, region)
        ├── (optional) re-ranking step to push the most relevant chunks to the top
        │
        ▼
   Claude (generation) — grounded answer, built only from the retrieved
   chunks, with citation back to the specific source policy doc/section
        │
        ▼
   Guardrails: Azure AI Content Safety filter on input/output
        │
        ▼
   Response + confidence score → escalate to HR ticket if low confidence
```

**Why the ingestion/runtime split matters in interview:** most candidates only describe the runtime flow (B) — being able to walk through how the knowledge base actually gets built and kept current (A) is what separates "I called an API" from "I architected the data pipeline."

**Key components to be ready to name:**
- Document ingestion pipeline (policy PDFs/HTML → chunked → embedded)
- Vector DB (be ready to say which — Pinecone/PGVector/Chroma; pick one and know it cold)
- LangChain retrieval chain + Claude for generation
- Fallback-to-human-ticket logic when confidence is low
- Observability: Ragas (faithfulness, answer relevancy) + LangSmith (trace/replay)

**☁ Infra Stack:** Azure API Management fronts the chatbot endpoint (auth, rate limiting, request routing to internal HR/payroll systems for grounding data). Azure AI Foundry hosts and manages the agent/model layer (prompt/version management, deployment). The whole service runs containerized on AKS. CI/CD through Azure DevOps pipelines, with the DevSecOps gates (secrets scanning, policy checks) from §1.5 applied here too. *If asked "why APIM specifically":* it's the natural choice given Qatar Airways' existing Azure investment — no separate gateway product to operate, and it plugs directly into Azure AD for employee auth.

**🛡 Guardrails & Prompt Evaluation:**
- **Guardrails:** Azure AI Content Safety filters both the incoming query and the generated answer (blocks harassment/hate/self-harm categories and off-topic jailbreak attempts to extract other employees' data); a hard system-prompt constraint refuses any answer not grounded in retrieved context (no "confident guess" mode); PII (employee ID, salary figures) is masked in logs and traces before they hit LangSmith.
- **Prompt evaluation:** a golden set of ~50–100 real HR questions (with HR-team-verified correct answers) is run against every prompt/retrieval change before deploy; Ragas scores faithfulness, answer relevancy, and context precision against that set, with a minimum threshold gating the release; regression testing catches cases where a prompt tweak improves one intent but silently breaks another.

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

**A. Ingestion pipeline (for the static side — tier/benefits rules, redemption policy docs):**
```
Source docs (tier benefit tables, redemption policy, upgrade eligibility
   rules — these change far less often than a mileage balance does)
        │
        ▼
   Chunking + embedding (same pattern as AskHR) → vector store
        │
        ▼
   Used only for "what are the rules" questions — never for balances,
   since balances must come from a live system call, not stored text
```
*This is the key distinction to make in interview: not everything here is RAG. Static policy text is ingested and retrieved like AskHR; account-specific data (balance, eligibility) is never ingested — it's fetched live, every time, via MCP tool calls, because ingesting and caching it would risk giving a customer stale or wrong numbers.*

**B. Runtime query flow:**
```
Customer query
     │
     ▼
Supervisor agent (LangGraph state machine)
     │
     ├──► Tier/Benefits agent ──► [static rules: retrieve from vector store]
     │                             [live status: MCP tool call ──► Membership system API]
     ├──► Redemption agent    ──► MCP tool call ──► Mileage/Loyalty ledger API
     ├──► Upgrade eligibility agent ──► MCP tool call ──► Booking/Inventory system
     │
     ▼
Aggregator node — merges sub-agent outputs (retrieved policy text +
live account data) into one coherent, grounded answer
     │
     ▼
Response to customer (with real-time balance/eligibility, not stale data)
```

**Why LangGraph + AutoGen together:** LangGraph for the deterministic state machine/control flow (you need predictable routing for a customer-facing financial-adjacent flow), AutoGen for the more exploratory multi-agent conversation patterns in edge cases (e.g., ambiguous redemption requests needing negotiation between agents).

**Why MCP specifically:** standardizes how each agent calls out to membership/mileage systems — one protocol instead of bespoke API wrappers per agent, easier to add a new backend system later without rewriting agent logic.

**☁ Infra Stack:** Same Azure-first pattern as AskHR — Azure API Management sits in front of the membership and mileage ledger APIs (this is also your security boundary: APIM policies scope which agent/service principal can call which downstream API), Azure AI Foundry runs the agent orchestration layer, deployed on AKS, shipped via Azure DevOps CI/CD. *If asked why not GCP here too:* the membership/mileage systems are Azure-native, so keeping the agent layer on the same cloud avoids cross-cloud latency and simplifies the auth chain (Azure AD end to end).

**🛡 Guardrails & Prompt Evaluation:**
- **Guardrails:** each worker agent's MCP tool access is scoped per-customer-session (an agent handling this conversation can only call the membership/mileage APIs for the authenticated customer's own account — not a blanket credential); Azure AI Content Safety screens both directions; a hard rule blocks any agent from initiating a redemption or booking action — the agents can only retrieve/explain eligibility, never execute a redemption themselves (mirrors the "no write" pattern you also used at Lloyds, worth drawing that parallel if asked).
- **Prompt evaluation:** because this is multi-agent, evaluation isn't just prompt-level — it's agent-handoff-level. A test suite of scripted conversation scenarios (ambiguous redemption request, conflicting tier data, a downstream API timeout) is run against the LangGraph flow before any change ships, checking both the final answer quality (Ragas-style scoring) and that the supervisor routed to the correct worker agent(s).

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

**Architecture:** Agentic process orchestration using explicit state machines (not a conversational agent — a workflow automation problem). Note this project has no batch document ingestion pipeline like AskHR — the only "ingestion" is real-time capture of the passenger's own document at the moment of check-in:

```
Passenger presents document (passport/boarding doc scan or photo)
        │
        ▼
   Real-time capture — image captured via kiosk/app camera, no storage
   into a knowledge base (this is a one-time validation input, not
   reusable knowledge, so it's discarded/archived per data-retention
   policy after the check-in flow completes — not indexed anywhere)
        │
        ▼
State: Identity Verify → State: Document Check (LLM judgment step reads
   the captured image here) → State: Seat/Bag Rules Validation
   → State: Boarding Pass Issue
(each state = a deterministic step, with an LLM step only where
 unstructured judgment is needed, e.g., document image validation)
```

**Worth stating explicitly if asked "where's the RAG/knowledge base here":** there isn't one — this is intentionally the project in your portfolio that is *not* RAG, precisely because the input is a one-time document capture, not a corpus to retrieve from. Interviewers sometimes ask this specifically to check you're not pattern-matching "GenAI project = RAG project" reflexively.

**Key point to make in interview:** this is where you draw the line between "use an LLM agent" and "use a plain state machine" — most of Fastpass is deterministic business rules; the LLM/agent is only in the narrow slice needing judgment (e.g., interpreting a passport photo edge case). Interviewers like architects who *don't* over-apply GenAI everywhere.

**☁ Infra Stack:** Azure API Management fronts the check-in workflow endpoints, the document-judgment step calls Azure AI Foundry-hosted model, the whole orchestration runs on AKS with Azure DevOps CI/CD — consistent with the rest of the Qatar Airways Azure-first footprint.

**🛡 Guardrails & Prompt Evaluation:**
- **Guardrails:** the LLM judgment step (document image validation) never makes a final "reject passenger" decision alone — below a confidence threshold, it routes to manual staff review rather than auto-rejecting, so the model can only approve within its confidence zone, not deny unilaterally. Azure AI Content Safety isn't really the relevant guardrail here since there's no open-ended user conversation — the real guardrail is this confidence-gated escalation.
- **Prompt evaluation:** the document-judgment prompt is evaluated against a labeled set of past check-in document images (including known edge cases — smudged passports, non-standard formats) with precision/recall tracked specifically for false-approvals (the costly error type in this context) versus false-escalations (just a minor inconvenience) — the threshold is tuned to bias toward escalation over auto-approval.

**Likely interview questions:**
- Where exactly does the LLM add value here vs. plain rules engine?
- How did you reduce "manual verification steps" — what was manual before, automated after?
- How do you handle a state machine failure mid-flow (passenger stuck between states)?

**Hands-on lab:**
- Build a small LangGraph state machine (not agent-conversation style) modeling a 4–5 step approval workflow with one step calling an LLM for unstructured judgment and the rest deterministic.
- Use: `langchain-ai/langgraph-101` state machine examples.

---

## 1.4 Agent Evaluation, Guardrails & Domain LLM Customization (cross-cutting)

*This section is the detailed version of the "🛡 Guardrails & Prompt Evaluation" note in 1.1–1.3 above — use it when an interviewer wants the full observability/safety story rather than the per-project summary.*

**Architecture (applies across AskHR + Loyalty):**
- **Observability:** LangSmith traces every agent step/tool call; Ragas scores RAG outputs (faithfulness, answer relevancy, context recall) on a held-out eval set, run in CI before deploying prompt/retrieval changes.
- **Safety:** Azure AI Content Safety on the Azure-hosted flows, Vertex AI Safety Filters where GCP components are used — layered, not single point of failure.
- **Domain customization:** Azure AI Foundry / Vertex AI custom models fine-tuned or prompt-tuned specifically for cargo manifest and HR document extraction accuracy (structured extraction is a different problem than conversational RAG — worth distinguishing in interview).

**Ingestion & extraction flow for cargo manifests (this is extraction, not RAG — no vector store involved):**
```
Cargo manifest documents (scanned/PDF, semi-structured — varying
   layouts per airline partner/route)
        │
        ▼
   Document pre-processing — OCR where needed, layout detection
   (tables, line items, consignor/consignee fields)
        │
        ▼
   Vertex AI Custom Model (tuned specifically on cargo manifest formats)
   — extracts structured fields (weight, contents, routing, HS codes)
        │
        ▼
   Validation layer — extracted fields checked against expected schema/
   business rules (e.g., weight within plausible range) before being
   written to downstream cargo systems
        │
        ▼
   Low-confidence extractions flagged for manual review, not auto-accepted
```
*Why this isn't RAG:* there's nothing to "retrieve" — each manifest is processed independently for its own structured data, not matched against a knowledge base. This is a good distinction to draw if an interviewer conflates "GenAI project" with "RAG project."

**☁ Infra Stack (this is the "secondary" Qatar Airways stack):** the cargo manifest/HR document extraction service is the one piece that runs on GCP rather than Azure — Azure API Management still fronts the overall request (single entry point for consumers), but the extraction workload itself calls GCP Vertex AI Custom Models, packaged and deployed as containerized services on **Cloud Run** (for the lighter, on-demand extraction calls) and **GKE** (for the more persistent/batch processing pieces), still shipped through Azure DevOps pipelines. *If asked why GCP just for this piece:* Vertex AI's custom model tuning for document/structured extraction was the stronger fit for cargo manifest formats specifically — this is a genuine "best tool for the job" call, not an accident of two teams doing their own thing, and it's worth saying so plainly.

**Likely interview questions:**
- What specific Ragas/LangSmith metrics did you track, and what was your threshold to block a deploy?
- How do you measure hallucination rate quantitatively, not just "we noticed fewer errors"?
- Why two different safety layers (Azure + Vertex) instead of one — was that a technical need or a legacy-of-two-clouds situation?
- Why does the cargo manifest extraction service live on GCP (Cloud Run/GKE) when the rest of your Qatar Airways footprint is Azure — how do the two clouds talk to each other, and where's the auth boundary?

**Hands-on lab:**
- Take the RAG pipeline from 1.1 and wire in a Ragas eval + a simple LangSmith trace (or open-source equivalent) so you can screen-share a real eval dashboard if asked "show me."

---

## 1.5 Cloud Migration, DevSecOps, Terraform/AKS (infra side)

**Architecture:** 200+ apps migrated to Azure + 50+ to private cloud; Terraform IaC + GitHub Actions/Azure DevOps CI/CD on AKS; DevSecOps gates (secrets scanning, policy enforcement) embedded in the pipeline, not bolted on after.

**🛡 Guardrails & Prompt Evaluation:** not directly applicable here — this is infrastructure migration, not an LLM-facing system. If an interviewer tries to pull this into a "guardrails" question anyway, the honest answer is that the equivalent control here is the DevSecOps gate itself (secrets scanning, policy enforcement) rather than a model-level guardrail.

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

**A. Ingestion pipeline (offline — clinical/research corpus is processed as it's added or updated):**
```
Internal corpora (clinical trial docs, regulatory filings, scientific
   literature — often complex PDFs with tables, figures, footnotes)
        │
        ▼
   Domain-aware document parsing — preserves table structure and
   section hierarchy (a plain text-splitter would break tables apart
   and lose the exact data GxP answers depend on)
        │
        ▼
   Chunking — section/table-aware chunks, each tagged with source
   document ID, version, and page/section reference
        │
        ▼
   Embedding → vector store (e.g., OpenSearch or Bedrock Knowledge
   Bases), each chunk retrievable back to its exact source location
        │
        ▼
   Version control — when a regulatory filing is amended, the old
   version's chunks are retained (not deleted) with a superseded flag,
   since GxP audit may need to reference what was known at a past date
```

**B. Runtime query flow:**
```
Researcher query
        │
        ▼
   Retrieval — query embedded, top-k chunks retrieved from the vector
   store, filtered to current/active document versions by default
   (with an option to search prior versions for audit purposes)
        │
        ▼
   Claude/Bedrock model generation — answer built only from retrieved
   chunks
        │
        ▼
   Citation-grounding check — every claim in the generated answer is
   verified against a matching retrieved chunk; unmatched claims are
   stripped or the answer is flagged for human review (see guardrails)
        │
        ▼
   Response returned with inline citations back to source doc + section,
   satisfying the GxP audit-trail requirement
```

**Key distinguishing point vs. AskHR:** GxP compliance means every answer needs an audit trail back to the source document and version — this is a much stricter grounding requirement than an HR chatbot. Be ready to explain how you enforced "no ungrounded claims."

**☁ Infra Stack:** AWS API Gateway is the entry point for the assistant (auth, throttling, request validation before it ever reaches the model layer). Amazon Bedrock hosts the foundation model and Knowledge Bases (retrieval) side of the RAG pipeline. The surrounding services — ingestion jobs, audit-log storage, orchestration — run on EKS. CI/CD is GitHub + GitHub Actions (source control and pipelines both native to GitHub, unlike the Azure DevOps pattern at Qatar Airways). *If asked why AWS API Gateway specifically over, say, an ALB:* API Gateway gives you built-in request/response validation and throttling per API key, which matters when research teams across different groups are hitting the same assistant with different quota needs.

**🛡 Guardrails & Prompt Evaluation:**
- **Guardrails:** the hard "citation-or-nothing" rule from the architecture above is itself the primary guardrail — every generated claim is checked for a matching retrieved chunk before the answer is returned, and unmatched claims are stripped or the answer is flagged for human review rather than shown as-is. This is stricter than a content-safety filter; it's a factual-grounding guardrail specific to a regulated research context.
- **Prompt evaluation:** evaluation here needed domain expert sign-off, not just automated metrics — a benchmark set of literature/regulatory questions with answers validated by the research/regulatory affairs team, scored for faithfulness and citation accuracy (does the citation actually say what the answer claims it says, not just "a citation exists"), re-run whenever the retrieval or prompt logic changes, with results retained as part of the GxP validation record.

**Likely interview questions:**
- How do you guarantee the model doesn't answer from its own training data instead of the retrieved corpus (a common regulatory concern)?
- How did you handle tables/figures in scientific PDFs during chunking?
- What audit trail exists for a generated answer — can you trace it back six months later?
- How is this different from a general-purpose RAG chatbot given GxP requirements?
- Why API Gateway + Bedrock + EKS rather than a simpler Lambda-only serverless setup — what made EKS necessary here?

**Hands-on lab:**
- Rebuild a scientific-PDF RAG pipeline that forces citation-only answers (reject/flag any answer without a matching retrieved chunk).
- Use: `anthropics/claude-cookbooks` (RAG + citations sections) + `aws-samples/amazon-bedrock-workshop` (Knowledge Bases + RAG lab).

## 2.2 ML Pipelines (SageMaker + Bedrock) for Clinical Data / Genomics

**Architecture:** SageMaker for training/experimentation pipelines on genomics data, Bedrock for foundation-model-based processing of clinical text — two different workloads (traditional ML training vs. LLM inference) integrated into one MLOps flow.

**☁ Infra Stack:** AWS API Gateway exposes the pipeline's trigger/status endpoints, SageMaker runs the training jobs and experiment tracking for the genomics models, Bedrock handles the clinical-text inference workloads, and the orchestration/serving layer around both sits on EKS. GitHub Actions runs the CI/CD — including the model validation gates required for GxP promotion (dev → staging → prod isn't just an environment change, it's a governance gate with sign-off recorded in the pipeline).

**🛡 Guardrails & Prompt Evaluation:** this side is more "model evaluation" than "prompt evaluation" since SageMaker is training classical/genomics models rather than prompting an LLM — accuracy, precision/recall, and drift metrics are tracked per model version, with a validation gate that blocks promotion if performance drops below the previous production baseline. For the Bedrock clinical-text inference piece specifically, the same faithfulness/citation-style evaluation from §2.1 applies, since it's the same GxP audit-trail requirement — worth explicitly distinguishing "model eval" (SageMaker/genomics) from "prompt/grounding eval" (Bedrock/clinical text) if asked, since conflating them is a common architect mistake interviewers probe for.

**Likely interview questions:**
- Why SageMaker for genomics but Bedrock for clinical text — what's the technical boundary between the two?
- How did you cut training/iteration time by 40% — pipeline parallelization, spot instances, data pipeline optimization?
- What does your GxP-aligned MLOps governance actually enforce (model versioning, validation gates, audit trails) — walk through a model promotion from dev to prod.

**Hands-on lab:**
- Use `aws-samples/amazon-bedrock-workshop` labs 01–03 (text generation, RAG, model customization) to get concrete Bedrock API reps.
- If you want SageMaker reps too, a basic SageMaker training-job notebook (any AWS official SageMaker example) alongside it, so you can speak to both halves of this pipeline.

## 2.3 Terraform + GitHub Actions CI/CD on EKS

**☁ Infra Stack:** the full CI/CD chain here is GitHub for source control and GitHub Actions for the pipeline itself — no separate CI product, which is a deliberate contrast to the Azure DevOps pattern at Qatar Airways (be ready to explain that difference is client-driven, not a personal preference switch). Terraform provisions the EKS cluster and networking; GitHub Actions runs the security scan, test, and deploy stages.

Same prep as the AKS lab above (§1.5), but be ready to name the EKS-specific differences if asked (IAM roles for service accounts vs. Azure AD workload identity, EKS networking/VPC CNI vs. AKS CNI, and GitHub Actions vs. Azure DevOps pipeline YAML differences).

---

# 3. LLOYDS BANKING GROUP (May 2022 – Jul 2023)

## 3.1 AI-Powered Banking Chatbot Integrated with IVR + Core Banking

**Context:** Deflect toll-free customer service call volume; must integrate with legacy IVR and core banking systems — heavily regulated, high-availability, audit-sensitive environment.

**Architecture:**

**A. Ingestion pipeline (for the FAQ/policy knowledge base side):**
```
Source content (banking FAQ articles, product policy docs, terms &
   conditions — content team-maintained, updated on a regular cadence)
        │
        ▼
   Chunking + embedding (same core pattern as AskHR) → vector store
        │
        ▼
   Content review gate — given the regulated context, any new/updated
   FAQ content goes through a compliance review before being ingested,
   not just a content-team publish
```

**B. Runtime query flow:**
```
Customer channel (IVR / web / app)
        │
        ▼
   NLU/Intent layer ──► routes: balance inquiry / dispute / general query
        │
        ├──► Core banking system integration (read-only balance/
        │    transaction lookups — live call, never cached/ingested,
        │    same principle as the Loyalty bot's live-data rule)
        ├──► Knowledge base (FAQ/policy RAG — retrieval as above)
        │
        ▼
   Response generation (with strict guardrails — no financial advice
   generation, no unauthorized account actions from the bot)
        │
        ▼
   Escalation to human agent if confidence low or transaction-type request
```

**Key trade-off:** in banking, the LLM is deliberately kept away from any *write* action on the account — it can retrieve/explain but not execute transactions. This is a design decision interviewers in fintech love to probe.

**☁ Infra Stack:** this is the one project in your history with two different API layers doing two different jobs — **IBM API Connect** fronts the legacy core banking system integration (this is almost always how core banking is exposed in a bank that's run IBM infrastructure for years — you're not replacing that, you're integrating with it), while **Apigee** manages the newer customer-facing/chatbot-side APIs. The NLU/response generation layer runs on **GCP Vertex AI**, deployed as containerized services on **Cloud Run** (lightweight, request-driven chatbot inference) and **GKE** (for the always-on orchestration/session components). CI/CD is GitHub + GitHub Actions. *If asked why two API gateways instead of one:* IBM API Connect was already the governance layer for core banking long before this project — introducing Apigee for the new AI-facing surface avoided re-platforming a regulated legacy integration just to standardize tooling, which would have added risk without clear benefit.

**🛡 Guardrails & Prompt Evaluation:**
- **Guardrails:** the hard "read-only, no transaction execution" rule is the primary guardrail, enforced at the tool/function level, not just prompt instruction — the bot literally has no callable function capable of moving money, so even a successful prompt-injection attempt can't produce a real transaction. A second layer screens for attempts to extract financial advice the bot isn't licensed to give (regulatory requirement in banking) and redirects those to a human advisor. PII/account data is redacted before anything is logged or traced.
- **Prompt evaluation:** adversarial testing is the standout here — a red-team-style test set specifically tries to jailbreak the bot into giving financial advice, revealing another customer's data, or attempting a blocked action, run before every release. Alongside that, a standard golden-question set (balance inquiries, FAQ-style queries) is scored for accuracy and groundedness, same pattern as AskHR, since accuracy on routine queries is what actually drove the call-deflection numbers.

**Likely interview questions:**
- Why is the bot read-only against core banking — what's the risk model behind that decision?
- How does it integrate with legacy IVR (protocol/API specifics)?
- How did you validate the 30% telephony cost reduction — call volume data, deflection rate methodology?
- What compliance/audit requirements shaped this differently from a generic chatbot?
- Why IBM API Connect for core banking but Apigee for the AI-facing layer — walk me through that boundary.
- Why Vertex AI here rather than a bank-native option — was that a technical or vendor-relationship decision?

**Hands-on lab:**
- Build a small RAG+guardrail chatbot with a hard rule layer: certain intents (e.g., "transfer money") are explicitly blocked from LLM execution and routed to a stub "human escalation" function instead.
- Use: `anthropics/claude-cookbooks` (tool use section — build a tool the model is *not* allowed to call for certain intents, and demonstrate the guardrail).

## 3.2 Enterprise API Management Platform (millions of transactions/day)

**☁ Infra Stack:** IBM API Connect for the core-banking-facing side (retail/corporate banking channel integration), Apigee for the modern API surface — this is the platform referenced in §3.1's infra stack, just described here at the platform-migration level rather than the single-chatbot level.

**🛡 Guardrails & Prompt Evaluation:** not LLM-facing, so no prompt evaluation here — the equivalent controls at this layer are rate limiting, request validation, and audit logging at the gateway level (IBM API Connect and Apigee policies), which is worth naming explicitly if an interviewer asks "what are your guardrails" about this specific piece, so you don't awkwardly force a prompt-eval answer onto infrastructure that doesn't have one.

**Likely interview questions:**
- What API Management platform (IBM API Connect / Apigee) and why two rather than one?
- How did you ensure high availability and audit-readiness at that transaction volume — rate limiting, caching, circuit breakers?
- What did the migration cutover look like — how did you avoid downtime?
- Given millions of daily transactions, how did IBM API Connect and Apigee avoid becoming two separate points of failure or two separate monitoring stories?

**Hands-on lab:** less GenAI-specific — if time-constrained, deprioritize vs. the RAG/agent labs above, but be ready to talk through API gateway patterns (rate limiting, auth, versioning) conceptually since this is a "describe, don't necessarily rebuild" area.

## 3.3 Hybrid Cloud (AWS + Azure + on-prem) & Kubernetes/GitHub Enterprise Migration

**☁ Infra Stack:** the Kubernetes platform delivery in this era used **GKE**, matching the GCP/Vertex AI direction the AI-facing chatbot work was already heading toward, with **GitHub Enterprise** as the source-control migration target and **GitHub Actions** for the resulting pipelines — replacing whatever legacy CI/SCM tooling existed before.

**Likely interview questions:**
- What made this hybrid rather than single-cloud — regulatory data residency, latency, legacy dependency?
- How did you achieve "100% delivery success" on the Kubernetes/GitHub Enterprise migration — what was your rollback plan?
- Why GKE specifically for this platform rather than a managed Kubernetes offering on AWS or Azure, given the hybrid environment?

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
