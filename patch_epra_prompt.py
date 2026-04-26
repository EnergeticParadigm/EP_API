from pathlib import Path

p = Path("app/services/epra.py")
s = p.read_text()

old = '''Hard requirements:
- Be concrete, institutional, and causal.
- Do not sound generic, motivational, therapeutic, or metaphorical.
- Do not merely name EP terms; explain how they operate in this case.
- Make authority, control, maintenance, barriers, losses, and fragility explicit.
- Show the system as a selection/maintenance/control process, not as a vague summary.
- Use plain language, but keep structural precision.
- Avoid filler such as "plays a role", "is important", "helps manage", "can be seen as".
- Avoid generic phrases like "inefficient processes or mismatches" unless specified concretely.
- Prefer specifics like overload, delay, abandonment, bias dispute, legal challenge,
  processing error, quota, eligibility gate, review bottleneck, reputational exposure.
'''

new = '''Hard requirements:
- Be concrete, institutional, and causal.
- Do not sound generic, motivational, therapeutic, or metaphorical.
- Do not merely name EP terms; explain how they operate in this case.
- Make authority, control, maintenance, barriers, losses, and fragility explicit.
- Show the system as a selection/maintenance/control process, not as a vague summary.
- Use plain language, but keep structural precision.
- Avoid filler such as "plays a role", "is important", "helps manage", "can be seen as".
- Avoid generic phrases like "inefficient processes or mismatches" unless specified concretely.
- Prefer specifics like overload, delay, abandonment, bias dispute, legal challenge,
  processing error, quota, eligibility gate, review bottleneck, reputational exposure.

Routing priority rules:
- The routed TARGET_SYSTEM is binding.
- Do not replace the target with Energetic Paradigm, EP methodology, EPRA, graph representation, blueprint, ontology, primitive layer, node-edge language, or any meta-framework object unless the routed target explicitly is one of those.
- If TASK_TYPE is SYSTEM_ANALYSIS, analyze the bound target system itself, not EP as a theory.
- If TASK_TYPE is ATTRIBUTION, answer as a provenance / authorship control problem and do not convert it into a generic system-analysis essay.
- If TASK_TYPE is AMBIGUOUS, stay close to the bound target and minimize speculative expansion.
- Corpus snippets are support material, not permission to change the target.
- The compact_ep_setup.system field must describe the bound target system directly.
- If the target is "a university admissions system", the answer must stay on admissions selection, eligibility, ranking, offers, enrollment, review, quotas, appeals, and administrative load.
- Do not discuss energetic graphs, representation layers, blueprint ontology, or EP formal architecture unless the user explicitly asked about those objects.
'''

if old not in s:
    raise SystemExit("prompt block not found")

p.write_text(s.replace(old, new, 1))
print("patched epra prompt")
