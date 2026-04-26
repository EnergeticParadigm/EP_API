from pathlib import Path
p = Path("app/services/epra.py")
text = p.read_text()

anchor = '''
    if "ride-hailing dispatch" in system:
        fill("asymmetry", "high-demand or surge-priced riders get faster matching while drivers in low-demand areas absorb idle time and earnings instability")
        fill("pressure_point", "dispatch queue in high-demand zones and driver-supply bottlenecks")
        fill("tradeoff", "faster matching and surge allocation improve throughput but worsen fairness and income consistency for drivers and remote riders")
        fill("actors", ["riders", "drivers", "dispatch algorithm", "platform operators"])
        fill("cost_bearer", "drivers in low-demand areas and riders outside priority zones")
        fill("fracture_condition", "driver shortages or demand spikes create long waits and failed matching")
'''

addon = anchor + '''

    if "university admissions" in system:
        fill("asymmetry", "high-scoring or legacy applicants gain easier access while marginal applicants absorb rejection and uncertainty")
        fill("pressure_point", "application review queue and limited seat capacity")
        fill("tradeoff", "selectivity and prestige improve ranking but worsen access and applicant stress")
        fill("actors", ["applicants","admissions office","reviewers","university"])
        fill("cost_bearer", "rejected and waitlisted applicants")
        fill("fracture_condition", "application surges overwhelm reviewers or yield targets miss")

    if "hospital triage" in system:
        fill("asymmetry", "critical patients receive immediate resources while lower-priority patients absorb waiting time")
        fill("pressure_point", "ER intake queue and bed availability")
        fill("tradeoff", "prioritizing urgent cases improves survival but worsens delays for noncritical patients")
        fill("actors", ["patients","nurses","doctors","hospital"])
        fill("cost_bearer", "noncritical waiting patients and overstretched staff")
        fill("fracture_condition", "patient surge exceeds beds or staff capacity")

    if "insurance claims" in system:
        fill("asymmetry", "low-risk or well-documented claims clear faster while disputed claimants absorb delay and denial risk")
        fill("pressure_point", "claims backlog and manual review queue")
        fill("tradeoff", "fraud control lowers payouts but worsens delay and customer burden")
        fill("actors", ["claimants","adjusters","insurer"])
        fill("cost_bearer", "claimants awaiting payment")
        fill("fracture_condition", "disaster surges or staffing shortages create backlog")

    if "bank loan approval" in system:
        fill("asymmetry", "high-credit applicants receive cheaper and faster approval while weaker applicants face rejection or high rates")
        fill("pressure_point", "underwriting queue and risk threshold cutoff")
        fill("tradeoff", "risk control reduces defaults but worsens exclusion and slower approvals")
        fill("actors", ["borrowers","loan officers","bank"])
        fill("cost_bearer", "marginal borrowers and rejected applicants")
        fill("fracture_condition", "rate shocks or recession increase defaults and tighten approvals")
'''

if anchor not in text:
    raise SystemExit("anchor block not found")

text = text.replace(anchor, addon)
p.write_text(text)
print("patched", p)
