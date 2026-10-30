import json, sys, os, statistics

def analyze(path):
    edits = 0            # Edit/Write tool_use on repo files
    progress = 0         # hooks/task progress calls
    other_task = 0       # any other hooks/task call
    turns_with_edits = 0
    cur_edits = 0
    seen = False
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try: rec = json.loads(line)
            except Exception: continue
            t = rec.get('type')
            if t == 'user':
                c = (rec.get('message') or {}).get('content')
                is_prompt = False
                if isinstance(c, str): is_prompt = True
                elif isinstance(c, list):
                    has_tr = any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in c)
                    has_tx = any(isinstance(x, dict) and x.get('type') == 'text' for x in c)
                    is_prompt = has_tx and not has_tr
                if is_prompt:
                    if seen and cur_edits: turns_with_edits += 1
                    seen = True; cur_edits = 0
            elif t == 'assistant':
                c = (rec.get('message') or {}).get('content')
                if not isinstance(c, list): continue
                for blk in c:
                    if not isinstance(blk, dict) or blk.get('type') != 'tool_use': continue
                    name = blk.get('name') or ''
                    inp = blk.get('input') or {}
                    if name in ('Edit','Write','NotebookEdit'):
                        fp = str(inp.get('file_path',''))
                        if '/TaskFlowDocs/' in fp or fp.endswith('/plan.md'):
                            continue  # doc edits aren't implementation
                        edits += 1; cur_edits += 1
                    elif name == 'Bash':
                        cmd = str(inp.get('command',''))
                        if 'hooks/task progress' in cmd: progress += 1
                        elif 'hooks/task ' in cmd: other_task += 1
    if seen and cur_edits: turns_with_edits += 1
    return edits, progress, other_task, turns_with_edits

print(f"{'session':<12} {'code-edits':>10} {'progress':>9} {'task-other':>10} {'turns-w-edits':>13}")
for p in sys.argv[1:]:
    e, pr, ot, tw = analyze(p)
    print(f"{os.path.basename(p)[:12]:<12} {e:>10} {pr:>9} {ot:>10} {tw:>13}")
