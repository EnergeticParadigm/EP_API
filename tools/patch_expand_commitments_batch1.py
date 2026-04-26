from pathlib import Path

p = Path("app/services/epra.py")
text = p.read_text()

marker = '''    if missing("pressure_point") and "queue" in full:
'''
block = '''    if "emergency room boarding" in system:
        fill("asymmetry", "critical patients and those with immediate bed priority receive scarce treatment capacity first, while boarded and lower-priority patients absorb delay and hallway care")
        fill("pressure_point", "emergency department bed shortage and boarding queue")
        fill("tradeoff", "prioritizing acute emergencies improves survival for critical patients but worsens delay, congestion, and care quality for boarded patients")
        fill("actors", ["patients", "triage nurses", "ER physicians", "bed managers", "inpatient units"])
        fill("cost_bearer", "boarded patients, lower-priority patients, and overloaded staff")
        fill("fracture_condition", "patient surge exceeds bed or staffing capacity, causing hallway boarding and treatment delays")

    if "organ transplant waitlist" in system:
        fill("asymmetry", "patients with higher urgency, compatibility, or priority scores move faster while lower-priority patients absorb waiting time and mortality risk")
        fill("pressure_point", "waitlist backlog and organ availability bottleneck")
        fill("tradeoff", "strict prioritization improves organ allocation efficiency and survival for urgent cases but worsens waiting and exclusion for lower-ranked patients")
        fill("actors", ["patients", "transplant coordinators", "surgeons", "allocation authority"])
        fill("cost_bearer", "lower-priority patients and families waiting on scarce organs")
        fill("fracture_condition", "organ scarcity or evaluation delays cause backlog growth and higher mortality for patients still waiting")

    if "insurance prior authorization" in system:
        fill("asymmetry", "well-documented or insurer-preferred cases clear faster while patients with complex, expensive, or disputed requests absorb delay and denial risk")
        fill("pressure_point", "prior authorization queue and manual medical review backlog")
        fill("tradeoff", "utilization control reduces insurer spending and unnecessary treatment approvals but worsens care delay and administrative burden for patients and providers")
        fill("actors", ["patients", "providers", "medical reviewers", "insurer staff"])
        fill("cost_bearer", "patients awaiting treatment and providers handling repeated authorization work")
        fill("fracture_condition", "request surges, reviewer shortages, or documentation disputes create authorization backlog and delayed care")

    if "student financial aid" in system:
        fill("asymmetry", "well-documented or higher-priority students receive aid decisions faster while marginal or incomplete applicants absorb delay, uncertainty, and reduced access")
        fill("pressure_point", "application processing queue and award-disbursement bottleneck")
        fill("tradeoff", "verification rigor and budget control improve compliance but worsen uncertainty and delay for students needing aid")
        fill("actors", ["students", "financial aid officers", "review staff", "institution administrators"])
        fill("cost_bearer", "students awaiting disbursement or missing documentation")
        fill("fracture_condition", "application surges, verification backlog, or funding shortfalls delay awards and disrupt enrollment")

    if "child protective services intake" in system:
        fill("asymmetry", "high-risk or highly visible cases receive immediate attention while lower-signal families and screened-out reports absorb delay or non-intervention risk")
        fill("pressure_point", "intake hotline queue and investigator assignment backlog")
        fill("tradeoff", "stricter risk triage improves focus on severe cases but worsens missed intervention risk and delay for borderline cases")
        fill("actors", ["children", "families", "intake workers", "case investigators", "supervisors"])
        fill("cost_bearer", "families waiting for response and workers carrying overloaded caseloads")
        fill("fracture_condition", "report surges or investigator shortages create screening backlog and delayed intervention")

    if "public housing eviction" in system:
        fill("asymmetry", "housing authorities preserve rule enforcement and arrears control while tenants with weak leverage or unstable income absorb delay, insecurity, and displacement risk")
        fill("pressure_point", "eviction filing queue and court-hearing backlog")
        fill("tradeoff", "enforcement of payment and occupancy rules improves administrative control but worsens housing insecurity and displacement risk for vulnerable tenants")
        fill("actors", ["tenants", "housing authority staff", "case managers", "court officers"])
        fill("cost_bearer", "tenants facing eviction and households disrupted by prolonged proceedings")
        fill("fracture_condition", "rent arrears spikes, court backlog, or funding cuts accelerate filings and destabilize housing continuity")

    if "visa overstay enforcement" in system:
        fill("asymmetry", "high-priority or easily traceable overstayers receive focused enforcement while low-visibility migrants absorb uncertainty, surveillance pressure, and selective targeting risk")
        fill("pressure_point", "case backlog and enforcement-priority queue")
        fill("tradeoff", "tighter enforcement improves state control and deterrence but worsens fear, uncertainty, and uneven burden across migrant populations")
        fill("actors", ["visa holders", "enforcement officers", "case analysts", "immigration authorities"])
        fill("cost_bearer", "overstayers subject to monitoring, detention, or removal action")
        fill("fracture_condition", "case surges, policy shifts, or limited enforcement capacity create uneven targeting and backlog growth")

    if "asylum adjudication" in system:
        fill("asymmetry", "high-priority, well-documented, or fast-tracked claims move faster while ordinary applicants absorb prolonged waiting, detention risk, and uncertainty")
        fill("pressure_point", "asylum case backlog and hearing queue")
        fill("tradeoff", "stricter credibility and fraud control improve state screening confidence but worsen delay, uncertainty, and exclusion risk for asylum seekers")
        fill("actors", ["asylum seekers", "adjudicators", "interpreters", "legal representatives", "immigration officials"])
        fill("cost_bearer", "asylum seekers waiting on hearings, status, or release")
        fill("fracture_condition", "application surges, judge shortages, or policy tightening create massive backlog and prolonged limbo")

    if "probation compliance monitoring" in system:
        fill("asymmetry", "high-risk or frequently flagged probationers receive more intense scrutiny while others face lower monitoring intensity")
        fill("pressure_point", "case manager caseload and violation review backlog")
        fill("tradeoff", "closer monitoring improves enforcement and violation detection but worsens administrative burden and sanction risk for supervised individuals")
        fill("actors", ["probationers", "probation officers", "case managers", "courts"])
        fill("cost_bearer", "probationers under intensive monitoring and officers handling overloaded caseloads")
        fill("fracture_condition", "caseload surges, reporting failures, or technology outages create missed violations or excessive sanction delays")

    if "customs inspection" in system:
        fill("asymmetry", "trusted or low-risk travelers and shipments move faster while flagged travelers, unknown importers, and suspicious cargo absorb inspection delay and seizure risk")
        fill("pressure_point", "inspection line and secondary screening queue")
        fill("tradeoff", "tighter border screening improves interdiction and compliance but worsens throughput, delay, and disruption for travelers and importers")
        fill("actors", ["travelers", "inspectors", "importers", "cargo handlers", "customs officers"])
        fill("cost_bearer", "flagged travelers, importers, and shipments held for secondary review")
        fill("fracture_condition", "traffic surges, staffing shortages, or alert spikes create border congestion and delayed clearance")

''' + marker

if marker not in text:
    raise SystemExit("fallback marker not found")

if 'if "emergency room boarding" in system:' in text:
    raise SystemExit("batch1 rules already present")

text = text.replace(marker, block, 1)
p.write_text(text)
print("patched", p)
