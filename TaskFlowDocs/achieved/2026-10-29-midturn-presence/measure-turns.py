import json, sys, statistics, os

def analyze(path):
    turns = []           # tool calls per user turn
    cur = 0
    seen_user = False
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            if rec.get('type') == 'user':
                msg = rec.get('message') or {}
                content = msg.get('content')
                # a real prompt, not a tool_result
                is_prompt = False
                if isinstance(content, str):
                    is_prompt = True
                elif isinstance(content, list):
                    parts = [c for c in content if isinstance(c, dict) and c.get('type') == 'text']
                    has_tr = any(isinstance(c, dict) and c.get('type') == 'tool_result' for c in content)
                    is_prompt = bool(parts) and not has_tr
                if is_prompt:
                    if seen_user:
                        turns.append(cur)
                    seen_user = True
                    cur = 0
            elif rec.get('type') == 'assistant':
                msg = rec.get('message') or {}
                content = msg.get('content')
                if isinstance(content, list):
                    cur += sum(1 for c in content if isinstance(c, dict) and c.get('type') == 'tool_use')
    if seen_user:
        turns.append(cur)
    return turns

for p in sys.argv[1:]:
    t = analyze(p)
    if not t:
        print(f"{os.path.basename(p)[:12]}  (no turns)")
        continue
    print(f"{os.path.basename(p)[:12]}  turns={len(t):<4} median={statistics.median(t):<6} mean={statistics.mean(t):<6.1f} max={max(t):<4} zero-tool-turns={sum(1 for x in t if x==0)}")
