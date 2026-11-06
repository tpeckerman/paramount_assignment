#!/usr/bin/env python3
"""Build a 24-hour timeline of when each rule bites, from the real rule table.

Reads rules/csv/Rules.csv and parses the `time_rule_machine` tokens into intervals. Nothing is
invented: a rule appears only if its token actually encodes a clock time, and rules whose
restriction is not a time at all are listed separately rather than being drawn at a made-up
hour, because drawing them would imply a precision the rule does not have.

Output: docs/timeline.html, self-contained, with a country and service-type selector.
"""
from __future__ import annotations

import csv
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs/timeline.html"


def to_min(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


# The UK watershed is explicitly two-ended: the Code's meaning says material unsuitable for
# children "should not, in general, be shown before 2100 or after 0530". So a UK not_before
# rule permits a window that CLOSES at 05:30, and drawing it as running to midnight would
# understate it. France has no equivalent general closing time, so a French not_before is
# drawn open-ended rather than having a 05:30 invented for it.
UK_WATERSHED_CLOSE = 5 * 60 + 30


def intervals(tok: str, country: str = ""):
    """Return (list of [start,end] minute pairs, kind) or (None, kind) if not a clock rule."""
    spans, kind = [], None
    for part in [p.strip() for p in tok.split(";") if p.strip()]:
        m = re.match(r"^not_before=(\d{2}:\d{2})$", part)
        if m:
            spans.append([to_min(m.group(1)), 24 * 60])
            if country == "UK":
                spans.append([0, UK_WATERSHED_CLOSE])
            kind = "permitted"
            continue
        m = re.match(r"^window=(\d{2}:\d{2})-(\d{2}:\d{2})$", part)
        if m:
            a, b = to_min(m.group(1)), to_min(m.group(2))
            spans += ([[a, b]] if a < b else [[a, 24 * 60], [0, b]])
            kind = "permitted"
            continue
        m = re.match(r"^restricted_window=(\d{2}:\d{2})-(\d{2}:\d{2})$", part)
        if m:
            a, b = to_min(m.group(1)), to_min(m.group(2))
            spans += ([[a, b]] if a < b else [[a, 24 * 60], [0, b]])
            kind = "permitted"
            continue
        m = re.match(r"^prohibited_in=(\d{2}:\d{2})-(\d{2}:\d{2})$", part)
        if m:
            a, b = to_min(m.group(1)), to_min(m.group(2))
            spans += ([[a, b]] if a < b else [[a, 24 * 60], [0, b]])
            kind = "prohibited"
            continue
        m = re.match(r"^soft_prefer_not_before=(\d{2}:\d{2})$", part)
        if m:
            spans.append([to_min(m.group(1)), 24 * 60])
            kind = "preferred"
            continue
        if part == "prohibited":
            spans.append([0, 24 * 60])
            kind = "prohibited"
        elif part == "any_time":
            spans.append([0, 24 * 60])
            kind = "permitted"
    return (spans or None), kind


def main() -> None:
    rows = [r for r in csv.DictReader(
        (ROOT / "rules/csv/Rules.csv").open(newline="", encoding="utf-8"))
        if r["status"] == "approved"]

    timed, untimed = [], []
    for r in rows:
        spans, kind = intervals(r["time_rule_machine"], r["country"])
        rec = {
            "id": r["rule_id"], "country": r["country"],
            "cat": r["content_category"], "svc": r["service_type"],
            "cls": r["classification"], "det": r["determinacy"],
            "clause": r["clause_ref"], "tok": r["time_rule_machine"],
            "text": r["threshold_description"][:260],
            "hr": r["human_review_required"] == "yes",
        }
        if spans:
            rec["spans"] = spans
            rec["kind"] = kind
            timed.append(rec)
        else:
            untimed.append(rec)

    data = json.dumps({"timed": timed, "untimed": untimed}, ensure_ascii=False)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(HTML.replace("__DATA__", data), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(timed)} rules with a clock time, "
          f"{len(untimed)} whose restriction is not a time")


HTML = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>When each rule bites, over 24 hours</title>
<style>
:root{--bg:#fbfaf8;--ink:#1a1a1a;--mut:#6b6b6b;--line:#e2e0db;--card:#fff;
--ok:#2f7d55;--okb:#d6ead e;--no:#9e2b2b;--nob:#f6dada;--soft:#8a6d1f;--softb:#f6eccf;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.5 ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial;padding:28px}
h1{font-size:21px;margin:0 0 4px}
p.sub{color:var(--mut);margin:0 0 20px;max-width:70ch}
.controls{display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end;margin-bottom:18px}
label{display:block;font-size:12px;color:var(--mut);margin-bottom:4px}
select{font:14px inherit;padding:7px 10px;border:1px solid var(--line);border-radius:7px;
background:var(--card);min-width:190px}
.wrap{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;
overflow-x:auto}
table{border-collapse:collapse;width:100%;min-width:860px}
th,td{padding:0;vertical-align:middle}
th.h{font-size:11px;color:var(--mut);font-weight:500;text-align:left;padding-bottom:6px}
td.lbl{width:300px;padding:5px 12px 5px 0;font-size:12.5px;white-space:nowrap}
td.lbl .rid{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11.5px}
td.lbl .meta{color:var(--mut);font-size:11px}
.track{position:relative;height:22px;background:repeating-linear-gradient(90deg,
#f4f2ee 0 1px,transparent 1px calc(100%/24));border:1px solid var(--line);border-radius:4px}
.bar{position:absolute;top:2px;bottom:2px;border-radius:3px}
.permitted{background:var(--okb);border:1px solid var(--ok)}
.prohibited{background:var(--nob);border:1px solid var(--no)}
.preferred{background:var(--softb);border:1px solid var(--soft);
background-image:repeating-linear-gradient(45deg,transparent 0 4px,rgba(0,0,0,.05) 4px 8px)}
.ws{position:absolute;top:-4px;bottom:-4px;width:1px;background:#444;opacity:.45}
.axis{display:flex;margin:6px 0 0 300px;font-size:10.5px;color:var(--mut)}
.axis span{flex:1;text-align:left}
.legend{display:flex;gap:18px;flex-wrap:wrap;margin:14px 0 0;font-size:12px;color:var(--mut)}
.k{display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-2px;
margin-right:5px}
.note{margin-top:22px;padding:14px 16px;background:#fff;border:1px solid var(--line);
border-radius:10px;font-size:13px;max-width:92ch}
.note h2{font-size:14px;margin:0 0 8px}
.note ul{margin:6px 0 0;padding-left:18px}
.hr{color:var(--no);font-size:10.5px;margin-left:5px}
.empty{color:var(--mut);padding:18px 0}
code{background:#f1efea;padding:1px 4px;border-radius:3px;font-size:12px}
</style></head><body>
<h1>When each rule bites, over 24 hours</h1>
<p class="sub">Built from the rule table, not drawn by hand. A rule appears here only if its
machine token encodes an actual clock time. Rules whose restriction is not a time are listed
underneath instead of being placed at an invented hour.</p>

<div class="controls">
  <div><label for="c">Country</label><select id="c"></select></div>
  <div><label for="s">Service type</label><select id="s"></select></div>
  <div><label for="g">Content category</label><select id="g"></select></div>
</div>

<div class="wrap">
  <div id="chart"></div>
  <div class="axis" id="axis"></div>
  <div class="legend">
    <span><i class="k permitted"></i>permitted in this window</span>
    <span><i class="k prohibited"></i>prohibited in this window</span>
    <span><i class="k preferred"></i>soft preference, not a prohibition</span>
    <span><i style="display:inline-block;width:1px;height:12px;background:#444;
      vertical-align:-2px;margin-right:5px"></i>21:00 and 05:30</span>
    <span class="hr">R = human review required</span>
  </div>
</div>

<div class="note" id="untimed"></div>

<script>
const D = __DATA__;
const $ = s => document.querySelector(s);
const uniq = a => [...new Set(a)].sort();

function svcList(){
  const s = new Set();
  D.timed.concat(D.untimed).forEach(r => r.svc.split(';').forEach(t => s.add(t.trim())));
  return [...s].filter(Boolean).sort();
}
function fill(sel, vals, allLabel){
  sel.innerHTML = '<option value="">' + allLabel + '</option>' +
    vals.map(v => `<option>${v}</option>`).join('');
}
fill($('#c'), uniq(D.timed.concat(D.untimed).map(r => r.country)), 'All countries');
fill($('#s'), svcList(), 'Any service');
fill($('#g'), uniq(D.timed.concat(D.untimed).map(r => r.cat)), 'All categories');

function match(r){
  const c = $('#c').value, s = $('#s').value, g = $('#g').value;
  if (c && r.country !== c) return false;
  if (g && r.cat !== g) return false;
  if (s){
    const toks = r.svc.split(';').map(t => t.trim());
    const anyScope = toks.some(t => ['all_linear_tv','all_avms'].includes(t));
    if (!anyScope && !toks.includes(s)) return false;
  }
  return true;
}

function draw(){
  const rows = D.timed.filter(match);
  const chart = $('#chart');
  if (!rows.length){ chart.innerHTML = '<p class="empty">No clock-time rule matches that '
    + 'combination. Check the list below: the restriction may not be a time at all.</p>';
    $('#axis').innerHTML=''; untimed(); return; }
  let h = '<table><tr><th class="h">rule</th><th class="h">00:00 to 24:00</th></tr>';
  for (const r of rows){
    const bars = r.spans.map(([a,b]) =>
      `<div class="bar ${r.kind}" style="left:${a/14.4}%;width:${(b-a)/14.4}%"></div>`).join('');
    h += `<tr><td class="lbl"><span class="rid">${r.id}</span>`
      + `${r.hr ? '<span class="hr">R</span>' : ''}`
      + `<br><span class="meta">${r.cat} &middot; ${r.cls}</span></td>`
      + `<td><div class="track" title="${r.tok.replace(/"/g,'')}\n${r.clause}">`
      + `<div class="ws" style="left:87.5%"></div>`
      + `<div class="ws" style="left:22.9%"></div>${bars}</div></td></tr>`;
  }
  chart.innerHTML = h + '</table>';
  $('#axis').innerHTML = Array.from({length:8}, (_,i) =>
    `<span>${String(i*3).padStart(2,'0')}:00</span>`).join('');
  untimed();
}

function untimed(){
  const rows = D.untimed.filter(match);
  let h = '<h2>Rules that restrict something other than the hour'
    + ` (${rows.length} shown)</h2>`
    + '<p>These are not drawn above because they have no clock time to draw. They are not '
    + 'lesser rules. Several of them <em>change</em> the hours above: an access control can '
    + 'disapply the watershed entirely, so a bar in this chart can be lifted by a rule in '
    + 'this list.</p><ul>';
  for (const r of rows.slice(0, 40)){
    h += `<li><code>${r.id}</code> ${r.cat}`
      + (r.tok && r.tok !== 'n/a' ? ` &mdash; <code>${r.tok.slice(0,70)}</code>` : '')
      + `${r.hr ? '<span class="hr">R</span>' : ''}</li>`;
  }
  $('#untimed').innerHTML = h + '</ul>'
    + (rows.length > 40 ? `<p>and ${rows.length-40} more.</p>` : '');
}

['#c','#s','#g'].forEach(s => $(s).addEventListener('change', draw));
draw();
</script></body></html>
"""

if __name__ == "__main__":
    main()
