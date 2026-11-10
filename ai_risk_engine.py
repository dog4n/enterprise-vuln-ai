"""Enterprise Vulnerability Context Engine (EVCE).

Reads Nuclei findings (JSONL or a JSON array), asks Google Gemini for the business
context of each finding and writes a single self-contained HTML report.

Usage:
    python3 ai_risk_engine.py                         # nuclei_output.json -> risk_report.html
    python3 ai_risk_engine.py scan.jsonl -o rapor.html --lang en
    python3 ai_risk_engine.py --dry-run               # no API call, layout preview only
"""

import argparse
import html
import json
import os
import re
import sys
from datetime import datetime

DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-flash-latest")
SEVERITY_ORDER = ["critical", "high", "medium", "low", "info", "unknown"]
SEVERITY_COLORS = {
    "critical": "#b42318",
    "high": "#d9480f",
    "medium": "#b08800",
    "low": "#2f6fdf",
    "info": "#5c6670",
    "unknown": "#5c6670",
}

PROMPTS = {
    "tr": """Sen kurumsal bir firmada görev yapan kıdemli siber güvenlik analistisin.
Tarama aracımız {host} hedefinde şu bulguyu tespit etti:
- Bulgu: {name}
- Önem derecesi: {severity}
- CVE: {cve}
- Açıklama: {description}

Bu bulgu için yönetici seviyesine uygun, kısa ve net bir özet yaz. Tam olarak şu üç başlığı kullan:
1. Gerçek İş Riski: Sömürülürse kuruma maliyeti ve etkisi ne olur?
2. Saldırgan Perspektifi: Bir saldırgan bunu nasıl kullanır?
3. Acil Çözüm Önerisi: Sistem yöneticisinin yapması gereken ilk iki adım.
Her başlık en fazla üç cümle olsun.""",
    "en": """You are a senior security analyst at an enterprise company.
Our scanner found the following on {host}:
- Finding: {name}
- Severity: {severity}
- CVE: {cve}
- Description: {description}

Write a short, executive-level summary for this finding. Use exactly these three headings:
1. Real Business Risk: what would exploitation cost the company?
2. Attacker Perspective: how would an attacker use this?
3. Immediate Remediation: the first two steps the system administrator should take.
Keep each heading to three sentences at most.""",
}

LABELS = {
    "tr": {"title": "Kurumsal Zafiyet Risk Raporu", "generated": "Oluşturulma",
           "findings": "bulgu", "host": "Hedef", "dry": "(deneme modu: yapay zeka çağrılmadı)"},
    "en": {"title": "Enterprise Vulnerability Risk Report", "generated": "Generated",
           "findings": "findings", "host": "Host", "dry": "(dry run: AI was not called)"},
}


def load_findings(path):
    """Read Nuclei output. Accepts JSONL (one object per line) or a JSON array."""
    with open(path, encoding="utf-8") as f:
        text = f.read().strip()
    if not text:
        return []
    if text.startswith("["):
        raw = json.loads(text)
    else:
        raw = []
        for line_no, line in enumerate(text.splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                raw.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"[!] {path}:{line_no} skipped, invalid JSON ({e.msg})", file=sys.stderr)
    return [normalize(item) for item in raw]


def normalize(item):
    """Map a Nuclei result to the fields the report needs."""
    info = item.get("info", {}) or {}
    classification = info.get("classification", {}) or {}
    cves = classification.get("cve-id") or []
    if isinstance(cves, str):
        cves = [cves]
    severity = str(info.get("severity", "unknown")).lower()
    if severity not in SEVERITY_ORDER:
        severity = "unknown"
    return {
        "host": item.get("matched-at") or item.get("host") or "?",
        "name": info.get("name") or item.get("template-id") or "?",
        "severity": severity,
        "cve": ", ".join(c.upper() for c in cves) or "-",
        "description": (info.get("description") or "-").strip(),
    }


def dedupe_and_sort(findings):
    seen, unique = set(), []
    for f in findings:
        key = (f["host"], f["name"])
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return sorted(unique, key=lambda f: SEVERITY_ORDER.index(f["severity"]))


def make_ai_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        sys.exit("[x] GEMINI_API_KEY is not set. Export it, or use --dry-run to preview the report.")
    try:
        from google import genai
    except ImportError:
        sys.exit("[x] google-genai is not installed. Run: pip install -r requirements.txt")
    return genai.Client(api_key=api_key)


def ask_ai(client, model, finding, lang):
    prompt = PROMPTS[lang].format(**finding)
    try:
        response = client.models.generate_content(model=model, contents=prompt)
        return (response.text or "").strip() or "AI returned an empty answer."
    except Exception as e:  # network/quota errors should not stop the whole report
        return f"AI error: {e}"


def to_html_text(text):
    """Escape AI output and keep its line breaks and **bold** markers."""
    safe = html.escape(text)
    safe = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", safe)
    return safe.replace("\n", "<br>")


def render_report(findings, lang, dry_run):
    L = LABELS[lang]
    counts = {s: sum(1 for f in findings if f["severity"] == s) for s in SEVERITY_ORDER}
    badges = "".join(
        f'<span class="badge" style="background:{SEVERITY_COLORS[s]}">{s.upper()}: {n}</span>'
        for s, n in counts.items() if n
    )
    cards = []
    for f in findings:
        color = SEVERITY_COLORS[f["severity"]]
        cards.append(f"""
    <article class="card" style="border-left-color:{color}">
      <header>
        <span class="sev" style="background:{color}">{f['severity'].upper()}</span>
        <h2>{html.escape(f['name'])}</h2>
      </header>
      <p class="meta">{L['host']}: <code>{html.escape(f['host'])}</code> &nbsp;·&nbsp; CVE: {html.escape(f['cve'])}</p>
      <div class="ai">{to_html_text(f['analysis'])}</div>
    </article>""")
    note = f'<p class="dry">{L["dry"]}</p>' if dry_run else ""
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{L['title']}</title>
<style>
  body {{ font-family: -apple-system, "Segoe UI", Roboto, sans-serif; background:#f4f5f7; color:#1d2329; margin:0; }}
  main {{ max-width: 920px; margin: 0 auto; padding: 32px 20px 64px; }}
  h1 {{ margin: 0 0 4px; font-size: 26px; }}
  .sub {{ color:#5c6670; margin: 0 0 16px; }}
  .badge {{ display:inline-block; color:#fff; border-radius:4px; padding:3px 9px; margin:0 6px 6px 0; font-size:13px; font-weight:600; }}
  .dry {{ background:#fff4ce; border:1px solid #e6c84f; padding:8px 12px; border-radius:6px; }}
  .card {{ background:#fff; border-left:6px solid; border-radius:8px; padding:16px 20px; margin-top:18px; box-shadow:0 1px 3px rgba(0,0,0,.08); }}
  .card header {{ display:flex; align-items:center; gap:10px; }}
  .card h2 {{ font-size:18px; margin:0; }}
  .sev {{ color:#fff; font-size:12px; font-weight:700; border-radius:4px; padding:2px 8px; }}
  .meta {{ color:#5c6670; font-size:14px; margin:8px 0 12px; }}
  .ai {{ line-height:1.55; font-size:15px; }}
  code {{ background:#eef0f3; padding:1px 5px; border-radius:3px; }}
</style>
</head>
<body>
<main>
  <h1>{L['title']}</h1>
  <p class="sub">{L['generated']}: {datetime.now():%Y-%m-%d %H:%M} &nbsp;·&nbsp; {len(findings)} {L['findings']}</p>
  {badges}
  {note}
  {''.join(cards)}
</main>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Turn Nuclei findings into an executive HTML risk report with Gemini.")
    parser.add_argument("input", nargs="?", default="nuclei_output.json", help="Nuclei JSONL/JSON file (default: nuclei_output.json)")
    parser.add_argument("-o", "--output", default="risk_report.html", help="HTML report path (default: risk_report.html)")
    parser.add_argument("--lang", choices=["tr", "en"], default="tr", help="report language (default: tr)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Gemini model (default: {DEFAULT_MODEL})")
    parser.add_argument("--limit", type=int, default=0, help="analyse only the first N findings (0 = all)")
    parser.add_argument("--dry-run", action="store_true", help="skip the AI call and only build the report layout")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        sys.exit(f"[x] Input file not found: {args.input}")
    findings = dedupe_and_sort(load_findings(args.input))
    if args.limit:
        findings = findings[: args.limit]
    if not findings:
        sys.exit("[x] No findings to analyse.")

    client = None if args.dry_run else make_ai_client()
    print(f"[*] {len(findings)} findings, model: {'-' if args.dry_run else args.model}")
    for i, f in enumerate(findings, 1):
        print(f"[{i}/{len(findings)}] {f['severity'].upper():8} {f['name']} @ {f['host']}")
        if args.dry_run:
            f["analysis"] = f["description"]
        else:
            f["analysis"] = ask_ai(client, args.model, f, args.lang)

    with open(args.output, "w", encoding="utf-8") as out:
        out.write(render_report(findings, args.lang, args.dry_run))
    print(f"[+] Report written: {args.output}")


if __name__ == "__main__":
    main()
