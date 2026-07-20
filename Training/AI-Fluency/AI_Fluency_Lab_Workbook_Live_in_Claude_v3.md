# AI Fluency Lab Workbook
### Hands-On in Claude — For Students

This workbook is your copy. Every lab below is something you **run live in Claude**, not something you read about. Each step has an exact prompt to paste in, and a short note on *what to watch for* — this is where you actually see Delegation, Description, Discernment, and Diligence happen, instead of just hearing them defined.

**Before you start:**
- Open Claude in a fresh conversation for each lab unless a step tells you otherwise.
- Every prompt below is ready to copy-paste exactly as written — no fields to fill in. If you'd rather use your own real code, stack, or past conversation instead of the example, that works just as well; the examples exist so nobody is blocked waiting to find "real" material.
- Nothing here requires special access — plain Claude.ai or the Claude app is enough.

---

## Lab 1 — Audit Your Last AI Interaction
**Module 1 · 10 minutes · Individual, Claude-assisted, then pair-share**

**Objective:** Use Claude itself to hold up a mirror to how you already work with AI.

**Step 1.** Find your most recent real AI conversation — code help, an email draft, anything. Have the prompt you sent and the response you got ready to paste in below. (No recent example handy? Use the placeholder scenario built into the prompt below instead.)

**Step 2.** In a new Claude conversation, paste:

```
I want to audit a past AI interaction using the AI Fluency 4D Framework
(Delegation, Description, Discernment, Diligence). Here's what happened:

I asked an AI "Why is my API slow?" It suggested adding Redis caching and
gave me code for it. I copied the code into my service and deployed it
that same afternoon without testing it locally first.

For each of the 4 Ds, tell me:
1. What I did well
2. What I likely missed
3. One specific thing I could have done differently

Be direct and specific. Don't just validate me — I can handle honest feedback.
```

*(If you have your own recent interaction, swap the middle paragraph for your real prompt-and-response — the audit is more useful on your own material once you've seen how it works.)*

**What to watch for:** Claude will usually surface a gap in Discernment ("did you actually verify this before using it?") or Diligence ("did anyone else see this output — did they know AI was involved?") that you hadn't consciously registered. That's the exercise working, not Claude being harsh.

If the audit comes back feeling too agreeable or generic, that itself is a live Discernment lesson: push back —

```
Be more critical. Assume I'm a professional who wants the honest gaps, not reassurance.
```

Notice how the answer changes. That shift is exactly what "confident tone ≠ correctness" means in reverse: default helpfulness can also be shallow, and it's on you to ask for the sharper version.

**Debrief:** Pair up. Share the one D that Claude's audit flagged as your weakest. Hold onto it — Lab 5 comes back to it.

---

## Lab 2 — Spot the Hallucination
**Module 2 · 20 minutes · Pairs, live in Claude**

**Objective:** Build the reflex of verifying a specific technical claim before trusting it — regardless of how confidently it's stated.

**Step 1.** Ask Claude something specific and detail-heavy about a library or tool. Use either example below, or swap in a library your pair doesn't use daily:

**Option A — everyday library, specific detail:**
```
Show me how to configure connection pooling in SQLAlchemy 2.0, including
the exact parameter names and their default values.
```

**Option B — more obscure corner, higher chance of a shaky answer:**
```
What are all the configuration options in the behavior.scaleDown section
of a Kubernetes HorizontalPodAutoscaler (autoscaling/v2)? List every field
with its default value.
```

**Step 2.** Do not take the answer at face value. Open the real source: the official docs, the GitHub source, or `--help` output for that exact library and version. Check every specific claim — parameter names, defaults, behavior.

**Step 3.** Log one sentence, either way:
- *"Claude claimed ___; the real docs say ___."* — if you found a discrepancy, or
- *"Verified: no discrepancy found, verification took ~X minutes."* — if it checked out.

**What to watch for:** Claude will often hedge on genuinely obscure details ("I'm not fully certain of the exact default — verify this") — notice that hedge when it shows up, it's useful signal. Also notice the cases where the phrasing is fully confident but still wrong, or where a version-specific detail is stated as if universal. Both patterns are worth naming out loud with your partner.

**Debrief:** How long did verification take, compared to how long a wrong config value would take to surface as a bug in production?

---

## Lab 3 — Prompt Rewrite Sprint
**Module 3 · 40 minutes · Individual, then groups of 3, live in Claude**

**Objective:** Feel the output-quality gap between a vague prompt and a structured one, from the same tool, back to back.

**Step 1.** In a fresh conversation, send your real, natural, first-draft prompt for something on your actual backlog. No backlog item handy? Use this ready-made example:

```
Fix this code.

public class UserService
{
    public string GetDisplayName(User user)
    {
        return user.Profile.NickName.ToUpper();
    }
}
```

**Step 2.** Open a **second, brand-new conversation** — this matters, don't let Claude carry context from the first one. Send the same task rewritten with Goal / Context / Constraints / Format:

```
Goal: This throws a NullReferenceException on line 3 when user.Profile is
null. Fix it so it returns "Guest" instead of throwing.

Context:
public class UserService
{
    public string GetDisplayName(User user)
    {
        return user.Profile.NickName.ToUpper();
    }
}

Constraints: Keep the method signature unchanged. Don't introduce new
dependencies.

Format: Return a diff, not the full file re-pasted.
```

**Step 3.** Put both responses side by side. Write down specifically what changed — not just "better," but *what kind* of better: fewer follow-up questions, matched your code's existing style, caught an edge case the vague version didn't.

**What to watch for:** the vague prompt usually makes Claude either ask a clarifying question or silently guess at scope — that guess is Claude filling in gaps *you* left, and it's filling them with a generic assumption, not your actual intent. The structured prompt should need little or no back-and-forth to be usable.

**Step 4 (groups of 3).** Compare your three "weak" prompts. Pick the weakest one as a group and rewrite it together on one screen, narrating out loud why each addition (Context vs. Constraints vs. Format) changes the output.

**Debrief:** Which single addition moved the output furthest for you personally?

---

## Lab 4 — The Flawed PR Review (Claude-Generated, Live)
**Module 4 · 30 minutes · Pairs, live in Claude**

**Objective:** Practice checklist-driven Discernment — using Claude to generate a fresh flawed sample on the spot, so every pair gets a different one.

**Step 1.** One person in the pair runs this prompt (swap the stack/language if your team doesn't work in Node):

```
For a code-review training exercise, write a 30-40 line Node.js Express
route handler for "GET /orders/:id" that looks correct at first glance but
contains exactly three planted problems: one functional bug, one security
issue, and one comment referencing a configuration option or library
behavior that does not actually exist.

Do not tell me what the problems are or where they are. Just give me the code.
```

**Step 2.** Share that code with your partner. Using the 7-point Discernment checklist (Correctness, Verifiability, Security, Fit with Constraints, Maintainability, Completeness, Reasoning Quality), find all three planted issues in 15 minutes. For the suspicious library/config claim specifically, verify it against real documentation before deciding it's fabricated — don't just guess.

**Step 3.** Once you've made your calls, go back to the same Claude conversation and send:

```
Reveal the three planted issues and exactly where they are in the code.
```

Score yourselves against the reveal.

**What to watch for:** this mirrors real review pressure — you have limited time and have to choose where to look closely. Notice which issue you found first and which you missed entirely; that gap usually maps directly to the checklist dimension you personally skip when you're moving fast.

**Debrief:** Which of the three was hardest to catch, and why?

---

## Lab 5 — Capstone: The Full 4D Loop
**Module 5 · 35 minutes · Individual or pairs, one continuous Claude conversation**

**Objective:** Run one real task through the Description-Discernment loop, closing it however many passes it takes — then pass through Diligence once, as a separate gate, before anything ships.

**Important distinction before you start:** Description, Discernment, and Refine are not three one-time steps — they're one loop that repeats until Discernment stops finding anything new. It might take one pass, it might take three. Diligence is *not* part of that loop. It only happens once, after the loop closes, right before you'd actually ship something.

**Step 1 — Delegation.** Before opening Claude, write down (on paper or in a notes doc, not in the chat): for a `POST /users/{id}/reset-password` endpoint, what will you delegate to AI vs. design/review yourself, and why. One sentence is enough.

**Step 2 — Description.** In Claude, send:

```
Goal: Add a POST /users/:id/reset-password endpoint. It must validate the
requester's permissions, rate-limit repeated attempts, and return a generic
success message regardless of whether the user exists, to prevent user
enumeration.

Context: Node.js + Express + PostgreSQL. Here's an existing route in our
style:

router.post('/users/:id/verify-email', requireAuth, async (req, res) => {
  const { id } = req.params;
  try {
    await userService.verifyEmail(id);
    res.status(200).json({ status: 'ok' });
  } catch (err) {
    logger.error('verify-email failed', err);
    res.status(500).json({ status: 'error' });
  }
});

Constraints: Follow the error-handling pattern shown above. Flag any new
dependency before adding it.

Format: Return the full route handler, plus a one-paragraph explanation of
the rate-limiting approach.
```

*(Using a different stack? Swap the Context block for a real route of your own — the exercise works the same way, Claude will just match your conventions instead.)*

**Step 3 — Discernment.** In the same conversation, stress-test the claims instead of trusting them at face value:

```
Walk through what happens if the same IP hits this endpoint 50 times in a
row, and what happens if the user ID doesn't exist. Does this implementation
actually prevent enumeration and actually rate-limit, or does it just
describe doing so?
```

Read the answer critically. Check the actual code against what it claims — this is the same "verify, don't just accept" habit from Lab 2, now applied to your own real task.

**Step 4 — Refine the loop.** Based on the specific gap you find, send **one targeted correction** — not a full re-ask:

```
The rate limiter resets on server restart and isn't shared across
instances. Fix that specifically — leave everything else as is.
```

Notice how much faster this is than starting over, and how it only works because Step 3 gave you something precise to point at.

**Now close the loop — don't skip this part.** Go back to Step 3: run the same stress-test question against your *refined* output. Did that fix the gap without breaking anything else? Did it surface something new? If Discernment finds anything at all, do Step 4 again with a new targeted correction, then check again. Keep going around Describe → Generate → Discern → Refine until one full Discernment pass turns up nothing left to flag. That might happen after this one refinement. It might take two more. Either is normal — the number of passes isn't the point, closing the loop is.

**This is a great moment to notice, out loud with a partner or the room:** how many times did you actually go around? Compare with someone near you — it's very likely you didn't land on the same number, and that's exactly the point: the loop doesn't have a fixed length.

---

**Once — and only once — a Discernment pass finds nothing left, you exit the loop and move to Diligence.** This is not "step 5 of the loop." It's a separate, one-time gate you pass through exactly once, after the loop is satisfied, right before anything would actually ship.

**Diligence (outside Claude, in your own notes).** Write one line each:
- **Creation:** was this task and this data appropriate to run through this tool, given your org's data policy?
- **Transparency:** how would you disclose AI involvement in the real PR description?
- **Deployment:** what will *you* personally test before this merges, beyond what Claude showed you?

---

**Step 6 — Close the loop with Claude.** Once your notes are done, go back to the same Claude conversation and ask it to reflect the whole thing back to you. Try the natural version first — most people phrase it exactly like this:

```
How did the 4D loop work in this conversation?
```

**Watch what happens — this usually fails.** Claude will likely say it has no information about a "4D loop." That's not Claude forgetting anything; nobody in this conversation ever told it what that term means. Claude only knows what's actually inside the thread, and "4D loop" was never defined there. This is the exact same failure as a weak Description prompt from Module 3 — assuming shared context that was never actually given.

Now fix it the same way you'd fix any vague prompt: give it the missing context.

```
This training uses the "AI Fluency 4D Framework": Delegation (deciding what
to hand off), Description (giving clear goal, context, constraints, and
format), Discernment (verifying output before trusting it), and Diligence
(owning what ships — verified and disclosed).

Looking back at this entire conversation — my original prompt, the endpoint
you generated, my stress-test question, and the fix I asked for — walk me
through where each of the 4 Ds actually showed up. Specifically: how many
times did Description and Discernment go back and forth before the loop
closed, and what specifically closed it?
```

**What to notice:** the second prompt works for the same reason every prompt in this workbook has worked since Lab 3 — it gives Goal, Context, Constraints, and Format. You just pointed it at yourself instead of at a piece of code.

**Debrief (full group):** Ask for a show of hands: who went around the loop once? Twice? Three or more times? There should be a real spread — that spread *is* the lesson, not a grading criterion. Then: what happened when you asked Claude about "the 4D loop" before giving it the definition — and what changed once you did? Then: did this capstone touch the weak D you identified back in Lab 1? What's the one thing you'll do differently on your very next real AI-assisted task?

**Facilitator tip:** Two things are worth modeling live, in front of the room, before students try this lab themselves.

First, the loop itself: run the capstone yourself, deliberately let your first Discernment pass find something small, refine, then discern again — narrate out loud, *"Notice — I just went around a second time. That's the loop. I'm not doing Diligence yet, because Discernment still found something."*

Second, Step 6: run the broken "how did the 4D loop work?" prompt live and let it fail in front of everyone, then immediately run the fixed version right after. Don't explain the failure first — let the room watch Claude genuinely not know, then watch the same conversation answer fully once it has the context. That contrast teaches Description's whole point faster than any slide can.

---

## Facilitator note

Every prompt above is ready to run exactly as printed — nobody needs to hunt for "real" material to participate. Where it's noted, students with their own code, stack, or past conversation can substitute it in; that tends to land even better, since the discovery becomes personal rather than a shared demo. Either way, encourage students to let the Claude conversation run a little wild (follow-up questions, unexpected answers) rather than steering it back to script; the off-script moments are usually where a D gets learned, not where the lab goes wrong.
