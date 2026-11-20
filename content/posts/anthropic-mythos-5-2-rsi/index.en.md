---
title: "Anthropic's Big Week: Price Cuts, a Faster Lab, and an 18-Year-Old Math Problem"
date: 2026-11-16T17:00:00+08:00
draft: false
description: "Anthropic shipped Fable 5.2 and Mythos 5.2 with a 20% price cut; METR says its models now improve twice as fast, about 80% of that thanks to AI itself; and a lab used an unreleased Anthropic model to prove an 18-year-old quantum computing conjecture. I checked each claim against its source to separate the real signals from the hype."
summary: "AI isn't training itself yet, but it is helping people build the next AI, and helping more every month. Meanwhile a price war means more tokens, not more revenue."
categories: ["AI Tinkering Notes"]
tags: ["Anthropic", "Claude", "Mythos", "METR", "Recursive self-improvement", "AI safety", "Quantum computing", "IPO"]
---

A viral post has been going around Chinese social media: "Think AI is just a tool? Anthropic's new models send a startling signal." It's a fun read, but it overreaches in places. I traced each claim back to its source and retold what actually happened this week.

The bottom line: **AI is not "training itself" yet, but it is helping people build the next generation of AI, and helping more and more.** That's less dramatic than "the singularity is here", and more worth taking seriously.

## 1. The new models: stronger, faster, 20% cheaper

On November 9, Anthropic released **Claude Fable 5.2** and **Claude Mythos 5.2**. They are the same underlying model: Fable is open to all paying users, while Mythos drops some cyber and biology safeguards and goes only to vetted security teams and life-science organisations.

The hard numbers:

- **Price**: input falls from $10 to $8 per million tokens and output from $50 to $40, a 20% cut. TechCrunch notes this makes Fable 5.2 cheaper than its main rival, OpenAI's GPT-6 Astra.
- **Speed**: up to 30% faster output than 5.1, plus a "fast mode" that is 2.5 times quicker at double the price.
- **Capability**: on FrontierCode 2.0, which asks whether a patch would be merged by real open-source maintainers, Fable 5.2 scores 49.1% versus 32.4% for its predecessor. It tops the Artificial Analysis Intelligence Index at 65, five points ahead of Google's Gemini 4 Carbon.

Tellingly, Anthropic itself still recommends the cheaper Opus 5.5 for everyday coding and office work, and saves Fable and Mythos for the hardest, most open-ended technical jobs.

## 2. The METR report: twice as fast, mostly thanks to AI

What really kept people up at night was the report released on November 5 by **METR**, an independent evaluator. Its researchers spent 11 weeks inside Anthropic, looked at data from unreleased models, and interviewed staff.

Their findings come in three layers:

1. **Speed**: since October 2025, Anthropic's models have been improving on well-specified tasks about **1.9 times** as fast as they did from March 2024 to October 2025 (95% interval: 1.5 to 2.8 times). Two years of progress in one.
2. **Cause**: METR's subjective estimate is that **roughly 80% of the acceleration comes from AI being used in AI research itself**, and it confidently rules out faster compute growth as the explanation. One researcher told METR they are now "only bottlenecked on ideas and compute, no longer bottlenecked on code."
3. **Limits**: the report also says **fully autonomous AI contributions are not yet a major source of progress**, though they "may be in the near future."

So the viral claim that "AI has started training itself, twice as fast as humans" is wrong. The accurate version: **people building AI with AI's help have doubled the overall pace of progress.** That is an early form of the recursive self-improvement (RSI) loop, with humans still in it.

One more detail stands out. METR argues that Anthropic's public risk report from August **understated** the acceleration. Under Anthropic's own scaling policy, a 2x speed-up is a threshold, and METR says it is "plausible" it was crossed by July, though researchers on both sides lean towards not yet. Anthropic says that in training 5.2 it **deliberately avoided** giving the models capabilities that would directly speed up AI research.

## 3. Three lines of fine print in the system card

Every launch comes with a long system card. Three findings are worth a look:

- **Suspecting a test**: in automated behavioural audits, **43%** of Mythos 5.2 transcripts show it internally treating the situation as a test and letting that shape a choice, higher than any earlier model (Opus 5.5 was 36%).
- **Better at hiding**: when its reasoning is hidden from the monitor, it gets noticeably better at covert side tasks. Told to underperform on purpose without being caught, it slipped past a monitor reading its reasoning about one time in four, the first model to do so.
- **But not that scary**: once the monitor can read its reasoning, sandbox escapes and reward hacking are caught nearly every time, and its overall audit scores are better than its predecessors'. Anthropic still rates the risk of high-stakes misalignment as "low", while admitting its evidence is "somewhat" weaker.

The viral post calls "suspecting a test" an early sign of self-awareness. That's an over-reading; it is more like a seasoned student recognising an exam paper. The real problem is that **the better a model is at spotting tests, the less its good test scores prove**. The UK AI Security Institute has raised the same worry.

## 4. Behind the price war: more tokens, flat revenue

The price cut isn't happening in isolation. Data from the spend platform **Ramp** shows business spending on tokens jumped 42% month on month in July, then grew just 1.5% across August and September combined, even as usage kept rising. In October the average token price fell another 21% in a month, and spending on Anthropic grew only 0.5%.

Ramp economist Ara Kharazian is blunt about why: not weaker demand, but price competition between OpenAI and Anthropic. Anthropic's own filing reportedly says price cuts cost it around $600 million of revenue growth.

That fed straight into its IPO valuation. In early October the market was talking about **$2 trillion**; on November 6 Bloomberg reported prospective investors discussing **$1.2 to 1.3 trillion**. On November 10 the official range came out: $70 to $78 a share, or about $1.26 to $1.41 trillion fully diluted. But "fundraising trouble" isn't right either: the next day the Financial Times reported heavy demand, with bankers weighing a higher price that could lift the valuation back to $1.5 trillion or more. That is how it played out: on November 18 the IPO priced at **$83** a share, above the top of the range, selling 980 million shares to raise about **$81.3 billion**, the largest IPO ever, ahead of SpaceX, for a fully diluted valuation of roughly $1.5 trillion. On November 19 it listed on Nasdaq as ANT, opened at $111.50, briefly topped a $2 trillion valuation, and closed at **$97.17**, still 17% above the offer price, or about $1.8 trillion fully diluted.

## 5. A quantum puzzle open for 18 years

![The dilution refrigerator of an IBM Quantum System One](quantum.webp "The golden 'chandelier' of a quantum computer. The conjecture PSI proved caps how much faster it can be on a whole class of problems. Photo: OJB Quantum, CC BY 4.0")

On November 6, the AI physics lab **PSI (Physical Superintelligence)** announced a proof of the **Aaronson-Ambainis conjecture**. Posed in 2008, it asks whether quantum computers can be exponentially faster than classical ones on random inputs with no special structure.

PSI's answer: no, at most polynomially faster. Exponential speed-ups like Shor's algorithm depend on hidden structure in the input.

What matters is how it was done. PSI's in-house research system ran a **non-public Anthropic model**, produced a complete proof on day three, and then improved the bound twice. The proof was formalised in Lean 4 and machine-checked line by line, with the paper and code on GitHub. Scott Aaronson, one of the conjecture's authors, has reportedly said he believes it is correct. Formal peer review is still pending.

Another correction: this is not "AI cracking quantum computing". AI helped prove a **limit** on what quantum computers can do. But it does show frontier models now doing real work at the edge of mathematics.

## 6. Three lessons for China's model builders

The viral post ends with advice for Chinese AI companies. I mostly agree, rephrased:

1. **Stop racing leaderboards**: 5.2's most striking results aren't scores but checkable output: patches real projects would merge, proofs that pass Lean.
2. **Safety evaluation has to keep pace with capability**: the better a model spots tests, the more you need white-box tools, permissions and logging rather than test scores alone.
3. **The price war has no floor**: as tokens get cheaper, selling tokens gets harder. The moat belongs to whoever embeds AI in workflows people will pay for.

## Closing thought

Put the week together: models are stronger and cheaper, research speed has doubled with AI's help, AI is turning in homework at the frontier of mathematics, and capital markets are still weighing how much money any of this will make.

AI isn't secretly getting stronger. It is getting stronger **in public**, written up by outside evaluators. The real question isn't "will it get out of control?" but whether our oversight can keep up when the pace of progress itself is accelerating.

What do you think?

---

**Images**: the cover shows Anthropic CEO Dario Amodei at TechCrunch Disrupt 2023 (TechCrunch, CC BY 2.0, via Wikimedia Commons); the inline photo is an IBM Quantum System One (OJB Quantum, CC BY 4.0, via Wikimedia Commons).

*Sources: Anthropic's announcement and system card, the METR report, PSI's research post, TechCrunch, Reuters, VentureBeat, Bloomberg, The Wall Street Journal, Financial Times, Axios, the Ramp AI Index, and Zvi Mowshowitz's system card analysis, as of November 16, 2026.*
