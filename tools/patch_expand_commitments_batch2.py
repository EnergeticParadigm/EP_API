from pathlib import Path

p = Path("app/services/epra.py")
text = p.read_text()

marker = '''    if missing("pressure_point") and "queue" in full:
'''
block = '''    if "trucking load assignment" in system:
        fill("asymmetry", "high-value or time-sensitive loads get assigned first while low-priority drivers and loads absorb idle time and delay")
        fill("pressure_point", "dispatch queue and driver-capacity bottleneck")
        fill("tradeoff", "throughput and on-time delivery improve for priority loads but worsen fairness and utilization stability for lower-priority assignments")
        fill("actors", ["drivers", "dispatchers", "carriers", "shippers"])
        fill("cost_bearer", "drivers waiting on assignments and lower-priority loads")
        fill("fracture_condition", "demand spikes, driver shortages, or route disruptions create cascading dispatch backlog")

    if "airline overbooking" in system:
        fill("asymmetry", "high-value, protected, or early-confirmed passengers preserve seats while bumped passengers absorb delay and compensation risk")
        fill("pressure_point", "seat allocation cutoff and rebooking queue at departure time")
        fill("tradeoff", "higher seat utilization improves airline revenue but worsens disruption and recovery burden for displaced passengers")
        fill("actors", ["passengers", "gate agents", "airline operations", "revenue management"])
        fill("cost_bearer", "bumped passengers and frontline airline staff")
        fill("fracture_condition", "oversell plus flight disruption forces mass rebooking and gate congestion")

    if "mortgage underwriting" in system:
        fill("asymmetry", "strong-credit and well-documented borrowers clear faster while marginal borrowers absorb delay, rejection, or worse terms")
        fill("pressure_point", "underwriting queue and documentation verification bottleneck")
        fill("tradeoff", "risk control reduces lender exposure but worsens exclusion and delay for weaker applicants")
        fill("actors", ["borrowers", "underwriters", "loan officers", "lender staff"])
        fill("cost_bearer", "marginal borrowers and applicants missing documentation")
        fill("fracture_condition", "rate shocks, housing stress, or backlog tighten standards and slow approvals")

    if "credit card fraud detection" in system:
        fill("asymmetry", "high-risk or anomalous transactions face holds while routine spenders pass quickly and flagged users absorb friction")
        fill("pressure_point", "real-time alert queue and manual fraud review backlog")
        fill("tradeoff", "stronger fraud interception reduces issuer loss but worsens false positives and customer friction")
        fill("actors", ["cardholders", "fraud analysts", "issuer systems", "merchants"])
        fill("cost_bearer", "flagged cardholders and merchants blocked by fraud controls")
        fill("fracture_condition", "alert surges or model drift overwhelm review capacity and increase false positives")

    if "collections enforcement" in system:
        fill("asymmetry", "high-recovery or easily reachable debtors receive faster enforcement attention while vulnerable debtors absorb fees, stress, and repeated contact")
        fill("pressure_point", "collections queue and account-escalation backlog")
        fill("tradeoff", "recovery pressure improves creditor cash flow but worsens debtor burden and enforcement intensity")
        fill("actors", ["debtors", "collections agents", "creditors", "enforcement staff"])
        fill("cost_bearer", "debtors facing repeated contact, fees, and escalating enforcement")
        fill("fracture_condition", "economic stress or account surges overwhelm collections capacity and intensify backlog")

    if "performance review system" in system:
        fill("asymmetry", "favored, visible, or manager-aligned employees receive better evaluations while marginal employees absorb slower advancement and greater scrutiny")
        fill("pressure_point", "manager review queue and calibration meeting bottleneck")
        fill("tradeoff", "standardized evaluation improves managerial control but worsens morale, bias exposure, and advancement inequality")
        fill("actors", ["employees", "managers", "review committees", "HR"])
        fill("cost_bearer", "lower-rated employees and managers handling overloaded review cycles")
        fill("fracture_condition", "review compression, stack ranking, or managerial inconsistency destabilizes trust and retention")

    if "search ranking system" in system:
        fill("asymmetry", "high-authority or platform-favored results gain visibility while lower-ranked sources absorb obscurity and traffic loss")
        fill("pressure_point", "ranking threshold and top-result visibility bottleneck")
        fill("tradeoff", "relevance optimization improves user efficiency but worsens concentration of attention and exposure inequality")
        fill("actors", ["users", "publishers", "ranking system", "platform operators"])
        fill("cost_bearer", "lower-ranked publishers and users pushed toward narrow result visibility")
        fill("fracture_condition", "spam surges, ranking shifts, or policy changes destabilize visibility and trust")

    if "recommender system for short-video platforms" in system:
        fill("asymmetry", "high-engagement creators gain amplified reach while ordinary creators absorb invisibility and unstable exposure")
        fill("pressure_point", "engagement threshold and recommendation queue")
        fill("tradeoff", "engagement maximization improves watch time but worsens concentration, volatility, and opaque exclusion")
        fill("actors", ["creators", "users", "moderators", "platform operators"])
        fill("cost_bearer", "ordinary creators, users exposed to narrow content loops, and moderators")
        fill("fracture_condition", "content surges, model shifts, or abuse patterns destabilize recommendation quality and reach")

    if "ad auction system" in system:
        fill("asymmetry", "high-bidding or high-quality advertisers win premium placement while weaker bidders absorb low visibility and rising acquisition costs")
        fill("pressure_point", "auction threshold and premium-inventory scarcity")
        fill("tradeoff", "revenue optimization improves monetization but worsens cost pressure and exclusion for smaller advertisers")
        fill("actors", ["advertisers", "platform operators", "users", "auction system"])
        fill("cost_bearer", "smaller advertisers and users exposed to denser ad allocation")
        fill("fracture_condition", "bid inflation, inventory scarcity, or policy shifts destabilize auction efficiency and advertiser viability")

    if "app store review system" in system:
        fill("asymmetry", "trusted, large, or well-resourced developers clear faster while smaller or flagged developers absorb delay, rejection, and uncertainty")
        fill("pressure_point", "review queue and escalation backlog")
        fill("tradeoff", "stricter review improves platform control and safety but worsens developer delay and inconsistent approval risk")
        fill("actors", ["developers", "reviewers", "platform operators", "appeals staff"])
        fill("cost_bearer", "smaller developers and apps held for repeated review")
        fill("fracture_condition", "submission surges, policy ambiguity, or reviewer shortage create approval backlog and inconsistent enforcement")

''' + marker

if marker not in text:
    raise SystemExit("fallback marker not found")

if 'if "trucking load assignment" in system:' in text:
    raise SystemExit("batch2 rules already present")

text = text.replace(marker, block, 1)
p.write_text(text)
print("patched", p)
