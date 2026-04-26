from pathlib import Path

p = Path("app/services/epra.py")
text = p.read_text()

marker = '''    if missing("pressure_point") and "queue" in full:
'''
insert = '''    if "university admissions" in system:
        fill("asymmetry", "high-scoring, legacy, or otherwise preferred applicants gain easier access while marginal applicants absorb rejection and uncertainty")
        fill("pressure_point", "application review queue and limited seat capacity")
        fill("tradeoff", "selectivity and prestige improve institutional ranking but worsen access and applicant stress")
        fill("actors", ["applicants", "admissions officers", "reviewers", "university administrators"])
        fill("cost_bearer", "rejected and waitlisted applicants")
        fill("fracture_condition", "application surges overwhelm review capacity or seat constraints force harsher cutoffs")

    if "hospital triage" in system:
        fill("asymmetry", "critical patients receive immediate resources while lower-priority patients absorb waiting time and risk deterioration")
        fill("pressure_point", "ER intake queue and bed availability bottleneck")
        fill("tradeoff", "prioritizing urgent cases improves survival for the most severe cases but worsens delays for noncritical patients")
        fill("actors", ["patients", "triage nurses", "doctors", "hospital staff"])
        fill("cost_bearer", "noncritical patients and overstretched staff")
        fill("fracture_condition", "patient surge exceeds bed, staffing, or treatment capacity")

    if "insurance claims" in system:
        fill("asymmetry", "well-documented or low-risk claims clear faster while disputed or complex claimants absorb delay and denial risk")
        fill("pressure_point", "claims backlog and manual review queue")
        fill("tradeoff", "fraud control and payout discipline reduce insurer exposure but worsen delay and burden for claimants")
        fill("actors", ["claimants", "claims adjusters", "fraud investigators", "insurer staff"])
        fill("cost_bearer", "claimants awaiting payment or appeal")
        fill("fracture_condition", "disaster surges or staffing shortages create backlog and delayed settlement")

    if "food delivery platform" in system:
        fill("asymmetry", "high-volume restaurants and dense-zone customers get faster service while small restaurants and distant customers absorb delay and lower priority")
        fill("pressure_point", "dispatch queue and driver supply bottleneck")
        fill("tradeoff", "faster matching and platform efficiency improve throughput but worsen fairness and earnings stability for drivers and small merchants")
        fill("actors", ["customers", "drivers", "restaurants", "platform operators"])
        fill("cost_bearer", "drivers, small restaurants, and customers outside dense zones")
        fill("fracture_condition", "driver shortages, demand spikes, or outage events destabilize fulfillment")

    if "public housing allocation" in system:
        fill("asymmetry", "high-priority or better-documented applicants move forward while lower-priority households absorb longer waits and exclusion risk")
        fill("pressure_point", "waitlist backlog and unit availability bottleneck")
        fill("tradeoff", "stricter prioritization improves administrative targeting but worsens delay and exclusion for many applicants")
        fill("actors", ["applicants", "housing officers", "case managers", "housing authority staff"])
        fill("cost_bearer", "waitlisted households and applicants missing documents")
        fill("fracture_condition", "unit scarcity, funding cuts, or intake surges cause waitlist stagnation")

    if "visa application" in system:
        fill("asymmetry", "low-risk or well-documented applicants clear faster while flagged or ambiguous applicants absorb delay, denial risk, and repeated review")
        fill("pressure_point", "consular interview queue and administrative processing backlog")
        fill("tradeoff", "security and fraud screening improve state control but worsen uncertainty, delay, and exclusion for applicants")
        fill("actors", ["applicants", "consular officers", "review clerks", "security reviewers"])
        fill("cost_bearer", "applicants facing delay, refusal, or repeated processing")
        fill("fracture_condition", "policy shifts, security alerts, or interview backlogs overwhelm processing capacity")

    if "prison intake" in system:
        fill("asymmetry", "higher-risk or medically flagged detainees receive intensive classification while ordinary arrivals absorb queue delay and uncertainty")
        fill("pressure_point", "intake backlog and classification bottleneck")
        fill("tradeoff", "stricter intake control improves custody security but worsens waiting, congestion, and intake burden")
        fill("actors", ["detainees", "intake officers", "medical staff", "classification staff"])
        fill("cost_bearer", "new arrivals awaiting classification and overburdened staff")
        fill("fracture_condition", "surge arrests, staffing shortages, or processing delays destabilize intake flow")

    if "supply chain warehouse" in system:
        fill("asymmetry", "priority shipments and high-value customers move faster while low-priority orders and workers absorb backlog strain")
        fill("pressure_point", "picking queue, dock congestion, and inventory bottlenecks")
        fill("tradeoff", "throughput optimization improves fulfillment speed but worsens worker strain and low-priority order delay")
        fill("actors", ["pickers", "packers", "warehouse supervisors", "customers", "retailers"])
        fill("cost_bearer", "warehouse workers and low-priority orders")
        fill("fracture_condition", "demand spikes, labor shortages, or system outages create warehouse congestion")

    if "hiring recruitment" in system:
        fill("asymmetry", "high-signal or preferred candidates move faster while marginal candidates absorb ghosting, delay, and rejection")
        fill("pressure_point", "resume screening queue and interview scheduling bottleneck")
        fill("tradeoff", "stricter filtering improves recruiter efficiency but worsens candidate exclusion and pipeline drop-off")
        fill("actors", ["candidates", "recruiters", "hiring managers", "interviewers"])
        fill("cost_bearer", "candidates left waiting and recruiting staff under load")
        fill("fracture_condition", "application surges or interview bottlenecks cause hiring slowdown and candidate loss")

    if "school disciplinary" in system:
        fill("asymmetry", "compliant students preserve access while flagged students absorb sanction, removal, and bias exposure")
        fill("pressure_point", "disciplinary referral queue and hearing bottleneck")
        fill("tradeoff", "order enforcement improves institutional control but worsens exclusion and uneven burden for targeted students")
        fill("actors", ["students", "teachers", "principals", "counselors", "disciplinary staff"])
        fill("cost_bearer", "flagged students and families with weaker advocacy")
        fill("fracture_condition", "incident surges, inconsistent enforcement, or staffing gaps destabilize disciplinary processing")

    if "bank loan approval" in system:
        fill("asymmetry", "high-credit borrowers receive faster, cheaper approval while weaker applicants face rejection, delay, or worse terms")
        fill("pressure_point", "underwriting queue and risk threshold cutoff")
        fill("tradeoff", "risk control reduces default exposure but worsens exclusion and delay for marginal borrowers")
        fill("actors", ["borrowers", "loan officers", "underwriters", "bank staff"])
        fill("cost_bearer", "marginal borrowers and rejected applicants")
        fill("fracture_condition", "rate shocks, recession pressure, or underwriting backlog tighten approvals and slow flow")

''' + marker

if marker not in text:
    raise SystemExit("generic fallback marker not found")

if 'if "university admissions" in system:' in text:
    raise SystemExit("expanded domain rules already present")

text = text.replace(marker, insert, 1)
p.write_text(text)
print("patched", p)
