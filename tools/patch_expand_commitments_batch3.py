from pathlib import Path

p = Path("app/services/epra.py")
text = p.read_text()

marker = '''    if missing("pressure_point") and "queue" in full:
'''
block = '''    if "layoffs selection process" in system:
        fill("asymmetry", "protected, high-value, or manager-favored employees are more likely to be retained while lower-ranked workers absorb job loss and instability")
        fill("pressure_point", "selection review queue and headcount reduction cutoff")
        fill("tradeoff", "rapid cost reduction improves organizational cash preservation but worsens workforce insecurity and morale collapse")
        fill("actors", ["employees", "managers", "HR", "executives"])
        fill("cost_bearer", "terminated employees and surviving teams absorbing workload shocks")
        fill("fracture_condition", "revenue shock or rushed ranking decisions create legal risk, morale breakdown, and operational disruption")

    if "workplace access badge system" in system:
        fill("asymmetry", "approved staff with correct permissions move freely while contractors, visitors, and flagged employees absorb denial and delay")
        fill("pressure_point", "badge approval queue and entry checkpoint bottleneck")
        fill("tradeoff", "stricter access control improves security but worsens convenience and movement speed for lower-trust users")
        fill("actors", ["employees", "security staff", "IT access admins", "visitors"])
        fill("cost_bearer", "flagged users, visitors, and staff delayed at controlled entry points")
        fill("fracture_condition", "badge outage, sync failure, or shift-change surge creates entry backlog and access failures")

    if "content copyright strike" in system:
        fill("asymmetry", "large rights holders and trusted claimants gain faster enforcement while creators and disputed users absorb takedown risk and appeal burden")
        fill("pressure_point", "claim review queue and appeals backlog")
        fill("tradeoff", "aggressive copyright enforcement improves rights-holder protection but worsens false takedowns and creator uncertainty")
        fill("actors", ["creators", "rights holders", "platform reviewers", "appeals teams"])
        fill("cost_bearer", "flagged creators and users navigating appeals or lost reach")
        fill("fracture_condition", "claim surges, automated overmatching, or appeal overload create inconsistent enforcement and creator disruption")

    if "cloud incident escalation" in system:
        fill("asymmetry", "highest-severity incidents and major customers receive immediate attention while lower-severity teams absorb delay and degraded service")
        fill("pressure_point", "incident queue and on-call escalation bottleneck")
        fill("tradeoff", "severity-based escalation improves containment of critical outages but worsens response time for lower-priority incidents")
        fill("actors", ["on-call engineers", "incident commanders", "service teams", "customers"])
        fill("cost_bearer", "teams handling lower-priority incidents and customers waiting on slower remediation")
        fill("fracture_condition", "multi-service outage or on-call overload overwhelms escalation capacity and delays containment")

    if "enterprise access approval" in system:
        fill("asymmetry", "high-priority or manager-backed requests clear faster while ordinary employees and contractors absorb waiting time and access denial risk")
        fill("pressure_point", "approval queue and reviewer bottleneck")
        fill("tradeoff", "tight access control reduces security exposure but worsens work delay and administrative friction")
        fill("actors", ["employees", "managers", "security reviewers", "IT admins"])
        fill("cost_bearer", "requesters blocked from tools and teams waiting on access restoration")
        fill("fracture_condition", "approval surges, reviewer shortage, or policy changes create access backlog and work stoppage")

    if "grant application review" in system:
        fill("asymmetry", "well-networked, established, or high-signal applicants advance faster while marginal applicants absorb rejection and uncertainty")
        fill("pressure_point", "review queue and funding-capacity bottleneck")
        fill("tradeoff", "selective funding improves portfolio confidence but worsens exclusion and volatility for less established applicants")
        fill("actors", ["applicants", "reviewers", "program officers", "funding committees"])
        fill("cost_bearer", "unfunded applicants and reviewers facing overloaded cycles")
        fill("fracture_condition", "application surges or budget contraction intensify backlog and selection harshness")

    if "scientific peer review" in system:
        fill("asymmetry", "prestigious institutions, established authors, or norm-conforming work clear more easily while marginal authors absorb delay, rejection, and invisibility")
        fill("pressure_point", "reviewer assignment queue and revision backlog")
        fill("tradeoff", "quality control improves publication filtering but worsens delay, conservatism, and exclusion of uncertain or novel work")
        fill("actors", ["authors", "reviewers", "editors", "journals"])
        fill("cost_bearer", "authors awaiting decisions and reviewers carrying unpaid review load")
        fill("fracture_condition", "reviewer scarcity, submission surges, or revision pileups stall publication flow")

    if "nonprofit donor screening" in system:
        fill("asymmetry", "high-capacity or reputationally safe donors receive more attention while smaller or flagged donors absorb reduced access and scrutiny")
        fill("pressure_point", "donor review queue and gift-acceptance approval bottleneck")
        fill("tradeoff", "reputational screening improves institutional safety but worsens fundraising flexibility and donor inclusion")
        fill("actors", ["donors", "screening staff", "development officers", "leadership"])
        fill("cost_bearer", "smaller donors, flagged donors, and fundraising teams slowed by extra checks")
        fill("fracture_condition", "reputational scares or due-diligence surges create approval backlog and fundraising slowdown")

    if "public procurement bidding" in system:
        fill("asymmetry", "well-connected or highly compliant bidders navigate requirements more easily while smaller vendors absorb delay, compliance cost, and disqualification risk")
        fill("pressure_point", "bid review queue and award-decision bottleneck")
        fill("tradeoff", "procedural rigor improves formal fairness and auditability but worsens speed and access for smaller suppliers")
        fill("actors", ["vendors", "procurement officers", "review committees", "public agencies"])
        fill("cost_bearer", "smaller bidders and staff handling complex compliance review")
        fill("fracture_condition", "bid surges, protest actions, or documentation complexity stall award decisions")

    if "zoning approval process" in system:
        fill("asymmetry", "politically connected, well-resourced, or code-compliant applicants move faster while smaller or contested applicants absorb delay and denial risk")
        fill("pressure_point", "hearing queue and permit-review bottleneck")
        fill("tradeoff", "procedural scrutiny improves planning control but worsens development delay and exclusion for weaker applicants")
        fill("actors", ["applicants", "planners", "zoning boards", "community opponents"])
        fill("cost_bearer", "smaller applicants and projects delayed by hearings or appeals")

        fill("fracture_condition", "hearing backlog, political conflict, or documentation disputes stall approvals and project timelines")

    if "environmental permitting" in system:
        fill("asymmetry", "well-resourced projects with strong compliance capacity move faster while smaller or environmentally contentious applicants absorb long review and denial risk")
        fill("pressure_point", "permit review queue and interagency clearance bottleneck")
        fill("tradeoff", "stronger environmental scrutiny improves risk control but worsens development delay and compliance burden")
        fill("actors", ["applicants", "permit reviewers", "regulators", "consultants"])
        fill("cost_bearer", "applicants waiting on approvals and communities affected by delayed decisions")
        fill("fracture_condition", "document complexity, interagency delay, or contested findings create long permitting backlog")

    if "hospital staffing scheduler" in system:
        fill("asymmetry", "critical units and senior staff receive priority coverage while less protected staff absorb unstable shifts, overtime, and understaffing")
        fill("pressure_point", "shift-allocation queue and staffing shortage bottleneck")
        fill("tradeoff", "coverage preservation for critical services improves continuity but worsens burnout and schedule volatility for staff")
        fill("actors", ["nurses", "doctors", "schedulers", "hospital administrators"])
        fill("cost_bearer", "frontline staff facing overtime, shift volatility, and burnout")
        fill("fracture_condition", "absence spikes, census surges, or scheduler shortage create unsafe staffing gaps")

    if "child care subsidy allocation" in system:
        fill("asymmetry", "higher-priority or fully documented households receive subsidies faster while marginal families absorb waiting and exclusion risk")
        fill("pressure_point", "application queue and subsidy-slot bottleneck")
        fill("tradeoff", "targeted allocation improves budget control but worsens delay and instability for families needing immediate support")
        fill("actors", ["families", "caseworkers", "subsidy administrators", "child care providers"])
        fill("cost_bearer", "families waiting for aid and providers holding unpaid or unstable placements")
        fill("fracture_condition", "funding caps, application surges, or verification backlog delay subsidy access")

    if "homelessness shelter intake" in system:
        fill("asymmetry", "high-visibility, acute-risk, or priority cases receive faster placement while ordinary unhoused people absorb waiting, exposure, and repeated intake")
        fill("pressure_point", "intake queue and bed-availability bottleneck")
        fill("tradeoff", "risk-based prioritization improves emergency placement for severe cases but worsens exclusion and outdoor exposure for others")
        fill("actors", ["unhoused people", "intake workers", "case managers", "shelter operators"])
        fill("cost_bearer", "people left waiting for beds and staff managing chronic scarcity")
        fill("fracture_condition", "weather shocks, intake surges, or bed shortages create overflow and repeated denial")

    if "disaster relief distribution" in system:
        fill("asymmetry", "high-visibility or better-documented claimants receive aid faster while remote, lower-capacity, or poorly documented households absorb delay and exclusion")
        fill("pressure_point", "relief intake queue and distribution bottleneck")
        fill("tradeoff", "centralized control improves accountability and fraud resistance but worsens delay and unequal access during crisis")
        fill("actors", ["affected households", "aid workers", "logistics teams", "government agencies"])
        fill("cost_bearer", "remote or weakly documented households and overloaded relief workers")
        fill("fracture_condition", "surge demand, damaged infrastructure, or coordination failure stall relief delivery")

    if "ai content safety review" in system:
        fill("asymmetry", "high-risk or controversial outputs receive tighter review while ordinary users absorb latency or false blocks from safety thresholds")
        fill("pressure_point", "review queue and escalation threshold bottleneck")
        fill("tradeoff", "stronger safety control reduces harmful outputs but worsens latency, false positives, and user frustration")
        fill("actors", ["users", "reviewers", "safety teams", "model operators"])
        fill("cost_bearer", "users whose requests are delayed or blocked and reviewers handling escalations")
        fill("fracture_condition", "query surges, policy shifts, or adversarial attacks overwhelm review and escalation capacity")

''' + marker

if marker not in text:
    raise SystemExit("fallback marker not found")

if 'if "layoffs selection process" in system:' in text:
    raise SystemExit("batch3 rules already present")

text = text.replace(marker, block, 1)
p.write_text(text)
print("patched", p)
