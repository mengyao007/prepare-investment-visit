# Research method

## Source hierarchy

Use four evidence grades:

- A — primary and authoritative: regulator or government records, listed-company filings, official company documents, patents, standards, court records, procurement documents, original conference video or transcript.
- B — credible independent secondary: established media, recognized industry associations, peer-reviewed papers, reputable analyst research with disclosed methodology.
- C — interested-party claims: BP, teaser, company website, founder interview, investor announcement, customer or partner publicity.
- D — leads only: commercial database summaries, scraped profiles, reposts, unsourced rankings, anonymous social posts.

Grade the source, not the conclusion. A primary filing proves what was filed; it does not automatically prove current operations or performance.

## Research sequence

1. Resolve identity: names, legal entities, location, website, founders, products, aliases, and related companies.
2. Build a dated fact spine: incorporation, product launches, financing, key hires, customers, projects, regulatory milestones, and recent events.
3. Test the problem and product: user, pain, workflow, architecture, technical mechanism, deployment, pricing, and replacement alternative.
4. Map the industry: value chain, market drivers, market constraints, policy, technology inflections, and realistic addressable revenue pool.
5. Map competition: direct competitors, substitutes, incumbents, customers or suppliers that can integrate, and failed analogues.
6. Test commercial proof: paid status, contract type, revenue recognition, implementation stage, retention or expansion, concentration, and receivables.
7. Test team claims: exact role, dates, scope, measurable outcomes, publications, patents, public talks, and employment or IP boundaries.
8. Test capital and governance: financing rounds, investors, consideration, valuation if disclosed, registered-capital changes, related parties, control, option pool, and special rights.
9. Search for disconfirming evidence: plan changes, delayed projects, disputes, penalties, lawsuits, customer churn, safety events, layoffs, and inconsistent metrics.
10. Search recent developments separately with a date filter and record the cutoff date.

## Bounded search allocation

Allocate the selected query ceiling before searching. For `standard` mode, a useful default is:

- identity, entities, and timeline: 3 queries;
- product, technology, and customer proof: 5 queries;
- founder and team: 3 queries;
- financing, ownership, and governance: 3 queries;
- competition and market: 4 queries;
- recent events and disconfirming evidence: 2 queries.

Reallocate unused queries to decision-critical gaps only. Do not spend the market budget before resolving the target company identity and supplied-material claims.

## Query families

Combine company, legal entity, founder, product, and location with relevant terms:

- `融资 投资方 增资 股东 股权 估值`
- `客户 合同 中标 采购 交付 收入 回款`
- `产品 发布 价格 API 手册 白皮书 专利 标准`
- `创始人 演讲 采访 播客 论文 专利 履历`
- `诉讼 处罚 事故 召回 失信 裁员 延期`
- English equivalents such as `funding`, `customer`, `contract`, `patent`, `founder interview`, `lawsuit`, `regulatory`, and `recall`.

Search claimed customers and investors from their side as well. A company press release alone does not establish a paid customer or completed financing.

After two distinct searches fail to verify a narrow claim, mark it `未找到可靠公开披露` and stop. Absence of search results is not proof of absence.

## Evidence ledger fields

Maintain: source ID, grade, publisher, title, publication date, access date, URL or file/page, claim supported, and limitations. For important claims, prefer two independent sources, including at least one primary source when possible.

## Market sizing discipline

Prefer bottom-up sizing tied to the company revenue model. Show units, price, adoption, take rate, utilization, or capacity assumptions. Keep TAM, SAM, SOM, current market revenue, and company obtainable revenue distinct. Use scenarios when uncertainty dominates precision.

## Failure modes to prevent

- Mistaking announced partnerships for revenue.
- Treating cumulative financing headlines as cash on hand.
- Treating registered capital as valuation or funds raised.
- Comparing shipment, deployment, installed base, paid units, and active units as if identical.
- Comparing gross transaction value with net revenue.
- Assigning a founder's former employer achievements to the individual without scope evidence.
- Converting a company forecast into an independent market forecast.
- Hiding contradictory dates or metrics instead of reconciling them.
