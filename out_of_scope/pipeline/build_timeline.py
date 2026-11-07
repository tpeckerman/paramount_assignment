#!/usr/bin/env python3
"""Build a 24-hour timeline of when each rule bites, from the real rule table.

Reads rules/csv/Rules.csv and parses the `time_rule_machine` tokens into intervals. Nothing is
invented: a rule appears only if its token actually encodes a clock time, and rules whose
restriction is not a time at all are listed separately rather than being drawn at a made-up
hour, because drawing them would imply a precision the rule does not have.

Output: out_of_scope/docs/timeline.html, self-contained, with a country and service-type selector.
"""
from __future__ import annotations

import csv
import json
import pathlib
import re

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
import constants as C

ROOT = C.ROOT
OUT = C.TIMELINE_HTML


def to_min(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


# The UK watershed is explicitly two-ended: the Code's meaning says material unsuitable for
# children "should not, in general, be shown before 2100 or after 0530". So a UK not_before
# rule permits a window that CLOSES at 05:30, and drawing it as running to midnight would
# understate it. France has no equivalent general closing time, so a French not_before is
# drawn open-ended rather than having a 05:30 invented for it.
UK_WATERSHED_CLOSE = 5 * 60 + 30

# The chart's day starts at 05:30, not midnight. The UK watershed runs 21:00 to 05:30, which
# across a midnight-based axis appears as two fragments pinned to opposite edges and reads as
# two separate permissions. Starting the day at 05:30 makes it a single unbroken bar, which is
# what it actually is.
DAY_START = 5 * 60 + 30


def to_axis(spans):
    """Rebase spans onto a day starting at DAY_START, splitting any that wrap, then merge."""
    out = []
    for a, b in spans:
        sa, sb = (a - DAY_START) % 1440, (b - DAY_START) % 1440
        if b - a >= 1440:
            out.append([0, 1440])
        elif sb == 0:
            out.append([sa, 1440])
        elif sa < sb:
            out.append([sa, sb])
        else:
            out += [[sa, 1440], [0, sb]]
    out.sort()
    merged = []
    for sp in out:
        if merged and sp[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], sp[1])
        else:
            merged.append(list(sp))
    return merged


def intervals(tok: str, country: str = ""):
    """Return (permitted spans, flags) in ONE polarity: everything drawn is PERMITTED time.

    Mixing polarities made the chart unreadable: a bar at the same position meant "you may
    transmit" or "you may not" depending on its colour. So a prohibition is now drawn as the
    COMPLEMENT - the hours that remain - and a rule prohibited at every hour produces no bar
    at all and is listed separately instead of occupying a row that says nothing.

    flags: {"soft": bool, "open_ended": bool, "never": bool}
    """
    spans, flags = [], {"soft": False, "open_ended": False, "never": False}
    for part in [p.strip() for p in tok.split(";") if p.strip()]:
        m = re.match(r"^not_before=(\d{2}:\d{2})$", part)
        if m:
            spans.append([to_min(m.group(1)), 24 * 60])
            if country == "UK":
                spans.append([0, UK_WATERSHED_CLOSE])
            else:
                # No general closing time is stated for France, so the window is drawn to the
                # edge of the day and marked as continuing rather than given an invented end.
                flags["open_ended"] = True
            continue
        m = re.match(r"^soft_prefer_not_before=(\d{2}:\d{2})$", part)
        if m:
            spans.append([to_min(m.group(1)), 24 * 60])
            flags["soft"] = True
            flags["open_ended"] = country != "UK"
            continue
        m = re.match(r"^window=(\d{2}:\d{2})-(\d{2}:\d{2})$", part)
        if m:  # the window IS the permission
            a, b = to_min(m.group(1)), to_min(m.group(2))
            spans += ([[a, b]] if a < b else [[a, 24 * 60], [0, b]])
            continue
        # restricted_window names when the RESTRICTION applies, so the permitted time is the
        # complement. Treating it as a permitted window drew the French 06:00-22:00 violence
        # restriction as though those were the only hours it could run.
        m = re.match(r"^(?:prohibited_in|restricted_window)=(\d{2}:\d{2})-(\d{2}:\d{2})$", part)
        if m:  # draw what is LEFT, not what is barred
            a, b = to_min(m.group(1)), to_min(m.group(2))
            if a < b:
                spans += [x for x in ([0, a], [b, 24 * 60]) if x[0] < x[1]]
            else:
                spans += [[b, a]]
            continue
        if part == "prohibited":
            flags["never"] = True
        elif part == "any_time":
            spans.append([0, 24 * 60])
    if flags["never"]:
        return None, flags
    return (spans or None), flags


def main() -> None:
    rows = [r for r in csv.DictReader(
        C.RULES_CSV.open(newline="", encoding="utf-8"))
        if r["status"] == C.USABLE_STATUS]

    timed, untimed = [], []
    for r in rows:
        spans, flags = intervals(r["time_rule_machine"], r["country"])
        rec = {
            "id": r["rule_id"], "country": r["country"],
            "cat": r["content_category"], "svc": r["service_type"],
            "cls": r["classification"], "det": r["determinacy"],
            "clause": r["clause_ref"], "tok": r["time_rule_machine"],
            "text": r["threshold_description"][:300],
            "quote": r["verbatim_quote"],
            "hr": r["human_review_required"] == "yes",
        }
        rec["never"] = flags["never"]
        if spans:
            rec["spans"] = to_axis(spans)
            rec["soft"] = flags["soft"]
            rec["open"] = flags["open_ended"]
            timed.append(rec)
        else:
            untimed.append(rec)

    data = json.dumps({"timed": timed, "untimed": untimed}, ensure_ascii=False)

    # A malformed colour value does not raise: CSS drops the declaration and the element
    # renders with no fill, which looks like a layout fault rather than a typo. "#d6ead e"
    # sat in this file with a space in the hex for its whole life and made every green bar
    # an empty outline. Fail the build instead of shipping it again.
    _root = re.search(r":root\{([^}]*)\}", HTML)
    _bad = [d.strip() for d in _root.group(1).split(";") if d.strip()
            and not re.fullmatch(r"--[a-z]+:#[0-9a-fA-F]{3,8}", d.strip())]
    if _bad:
        raise SystemExit(f"malformed CSS colour value(s): {_bad}")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(HTML.replace("__DATA__", data), encoding="utf-8")
    never = sum(1 for r in untimed if r["never"])
    print(f"wrote {OUT.relative_to(ROOT)}: {len(timed)} rules with a permitted window, "
          f"{never} never permitted at any hour, {len(untimed) - never} whose restriction "
          f"is not a time at all")


HTML = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>When each rule bites, over 24 hours</title>
<style>
:root{--bg:#fbfaf8;--ink:#1a1a1a;--mut:#6b6b6b;--line:#e2e0db;--card:#fff;
--ok:#2f7d55;--okb:#d6eade;--no:#9e2b2b;--nob:#f6dada;--soft:#8a6d1f;--softb:#f6eccf;}
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
.fill-ok,.bar{background:var(--okb);border:1px solid var(--ok)}
.fill-soft,.bar.soft{background:var(--softb);border:1px dashed var(--soft);
background-image:repeating-linear-gradient(45deg,transparent 0 5px,rgba(0,0,0,.06) 5px 10px)}
.fill-none{background:transparent;border:1px solid var(--line)}
.cont{position:absolute;right:-9px;top:50%;transform:translateY(-50%);color:var(--ok);
font-size:11px;line-height:1}
.ws{position:absolute;top:-4px;bottom:-4px;width:1px;background:#444;opacity:.45}
.axis{display:flex;margin:6px 0 0 300px;font-size:10.5px;color:var(--mut)}
.axis span{flex:1;text-align:left}
.legend{display:flex;gap:18px;flex-wrap:wrap;margin:14px 0 0;font-size:12px;color:var(--mut)}
.k{display:inline-block;width:22px;height:12px;border-radius:3px;vertical-align:-2px;
margin-right:6px}
.note{margin-top:22px;padding:14px 16px;background:#fff;border:1px solid var(--line);
border-radius:10px;font-size:13px;max-width:92ch}
.note h2{font-size:14px;margin:0 0 8px}
.note ul{margin:6px 0 0;padding-left:18px}
.note li{margin:0 0 9px}
.what{color:var(--ink)}
.q{color:var(--mut);font-style:italic;font-size:12px}
.hr{color:var(--no);font-size:10.5px;margin-left:5px}
.tag{display:inline-block;font-size:10px;padding:1px 5px;border-radius:3px;margin-right:5px;
vertical-align:1px}
.tag.univ{background:#eceae5;color:#6b6b6b}
.tag.spec{background:#e4efe8;color:#2f7d55;font-weight:600}
.empty{color:var(--mut);padding:18px 0}
code{background:#f1efea;padding:1px 4px;border-radius:3px;font-size:12px}
</style></head><body>
<h1>When each rule bites, over 24 hours</h1>
<p class="sub">Built from the rule table, not drawn by hand. <strong>Every bar means the same
thing: the content may be transmitted then.</strong> A prohibition is shown as the hours that
remain, so there is one reading of the chart rather than two. Choosing what is depicted
narrows to the rules for that content <em>plus</em> the framework that applies whatever is on
screen, marked <em>applies to all content</em>: the watershed, the definitions it rests on,
and the access controls that can lift it. The day runs <strong>05:30 to 05:30</strong> rather than midnight to midnight, because the UK watershed is 21:00 to 05:30 and
a midnight axis splits it into two fragments at opposite edges that read as two separate
permissions. Rules that permit no hour at all, and rules whose restriction is not a time, are
listed underneath rather than drawn at an invented position.</p>

<div class="controls">
  <div><label for="c">Country</label><select id="c"></select></div>
  <div><label for="s">Service type</label><select id="s"></select></div>
  <div><label for="g">What is depicted</label><select id="g"></select></div>
</div>

<p id="count" class="sub" style="margin:0 0 10px"></p>

<div class="wrap">
  <div id="chart"></div>
  <div class="axis" id="axis"></div>
  <div class="legend">
    <strong style="color:var(--ink)">A bar means the content MAY be transmitted then.</strong>
    <span><i class="k fill-ok"></i><strong>solid green</strong> &ndash; permitted</span>
    <span><i class="k fill-soft"></i><strong>yellow, dashed</strong> &ndash; permitted, but the
      regulator states a preference for later. Not a prohibition</span>
    <span><i class="k fill-none"></i><strong>empty track</strong> &ndash; not permitted</span>
    <span>&rsaquo; continues past midnight; no closing time stated in the source</span>
    <span><i style="display:inline-block;width:1px;height:12px;background:#444;
      vertical-align:-2px;margin-right:5px"></i>21:00 watershed</span>
    <span class="hr">R = human review required</span>
  </div>
</div>

<div class="note" id="untimed"></div>

<script>
const D = __DATA__;
const $ = s => document.querySelector(s);
const esc = t => String(t == null ? '' : t)
  .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const uniq = a => [...new Set(a)].sort();

function svcList(){
  const s = new Set();
  D.timed.concat(D.untimed).forEach(r => r.svc.split(';').forEach(t => s.add(t.trim())));
  return [...s].filter(Boolean).sort();
}
// Underscored machine values are fine in data and poor in a label. Capitalising the first
// letter alone turns bbc_odps into "Bbc odps", so known acronyms are restored afterwards.
const ACRONYM = {bbc:'BBC', odps:'ODPS', tv:'TV', avms:'AVMS', avmsd:'AVMSD',
                 ppv:'PPV', pin:'PIN', mdp:'MDP', bbfc:'BBFC', uk:'UK', eu:'EU'};
const pretty = v => String(v).replace(/_/g,' ')
  .replace(/^./, c => c.toUpperCase())
  .replace(/\b[a-zA-Z]+\b/g, w => ACRONYM[w.toLowerCase()] || w);

function fill(sel, vals, allLabel){
  sel.innerHTML = '<option value="">' + allLabel + '</option>' +
    vals.map(v => `<option value="${esc(v)}">${esc(pretty(v))}</option>`).join('');
}

// The dropdown offers only what can actually be DEPICTED in a programme. The other
// categories - scheduling_general, definition, signage, access_control and the rest - do not
// describe content at all; they apply whatever is on screen. Offering them as filter options
// put "Definition" beside "Violence" as though you would choose between them.
//
// So they are never filtered out. Pick "Violence" and you get the violence rules PLUS the
// framework that always applies: the watershed, the definitions it depends on, the access
// controls that can lift it. That matches how the decision engine selects rules, where these
// same categories are force-included.
const DEPICTED = new Set(['violence','sexual_content','nudity','strong_language',
  'drugs_alcohol_smoking','suicide_self_harm','imitable_behaviour','fear_distress',
  'hatred_discrimination','occult_paranormal','religion','human_dignity','serious_harm',
  'participant_welfare','offence_general','music_videos']);

const UNIVERSAL = new Set(['all_linear_tv','all_avms']);
const scopes = r => r.svc.split(';').map(t => t.trim()).filter(Boolean);
const isUniversal = r => scopes(r).some(t => UNIVERSAL.has(t));

// Why is this row here? Either it binds every service, or it is specific to the one chosen.
// Without this the filter looks inert: 27 of 37 rules are scoped all_linear_tv, so switching
// service moves only a couple of rows in a long list and nothing says which.
function svcTag(r){
  const s = $('#s').value;
  if (isUniversal(r)) return '<span class="tag univ">any service</span>';
  if (s) return `<span class="tag spec">only ${esc(pretty(s))}</span>`;
  return `<span class="tag spec">${esc(scopes(r).map(pretty).join(', '))}</span>`;
}

function match(r){
  const c = $('#c').value, s = $('#s').value, g = $('#g').value;
  if (c && r.country !== c) return false;
  // a rule that does not describe depicted content always applies, so it is never filtered out
  if (g && r.cat !== g && DEPICTED.has(r.cat)) return false;
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
  let h = '<table><tr><th class="h">rule</th><th class="h">05:30 &rarr; 05:30 next day</th></tr>';
  for (const r of rows){
    const bars = r.spans.map(([a,b],i) =>
      `<div class="bar${r.soft?' soft':''}" style="left:${a/14.4}%;width:${(b-a)/14.4}%">`
      + ((r.open && b===1440) ? '<span class="cont">&rsaquo;</span>' : '') + `</div>`).join('');
    h += `<tr><td class="lbl"><span class="rid">${r.id}</span>`
      + `${r.hr ? '<span class="hr">R</span>' : ''}`
      + `<br><span class="meta">${DEPICTED.has(r.cat) ? '' : '<em>applies to all content</em> &middot; '}`
      + `${svcTag(r)}${esc(pretty(r.cat))}`
      + `${r.cls && r.cls !== 'n/a' ? ' &middot; ' + esc(pretty(r.cls)) : ''}</span></td>`
      + `<td><div class="track" title="${esc(r.clause)}\n${esc(r.tok)}\n\n${esc(r.text)}\n\n&ldquo;${esc(r.quote)}&rdquo;">`
      + `<div class="ws" style="left:64.58%"></div>${bars}</div></td></tr>`;
  }
  chart.innerHTML = h + '</table>';
  const sv = $('#s').value;
  const spec = rows.filter(r => !isUniversal(r)).length;
  $('#count').innerHTML = `<strong>${rows.length}</strong> rules with a permitted window`
    + (sv ? ` on <strong>${esc(pretty(sv))}</strong>, of which <strong>${spec}</strong> `
          + `${spec === 1 ? 'is specific to it' : 'are specific to it'}; the rest bind every `
          + `service`
          : `, across all service types`)
    + '.';
  $('#axis').innerHTML = Array.from({length:8}, (_,i) => {
    const m = (330 + i*180) % 1440;
    return `<span>${String(Math.floor(m/60)).padStart(2,'0')}:`
         + `${String(m%60).padStart(2,'0')}</span>`;
  }).join('');
  untimed();
}

function untimed(){
  const rows = D.untimed.filter(match);
  const never = rows.filter(r => r.never);
  const other = rows.filter(r => !r.never);
  let h = '';
  if (never.length){
    h += `<h2>Never permitted, at any hour (${never.length})</h2>`
      + '<p>No bar can be drawn because no hour is permitted. <strong>Read what each one '
      + 'actually covers, not its category label.</strong> The categories are retrieval keys, '
      + 'not descriptions: a ban on pornography depicting minors and a sex scene in a drama '
      + 'both sit under <code>sexual_content</code>, and the label alone makes the first look '
      + 'like a ban on the second.</p><ul>'
      + never.map(r => `<li><code>${r.id}</code>`
          + `${r.hr ? '<span class="hr">R</span>' : ''}<br>`
          + `<span class="what">${esc(r.text)}</span>`
          + (r.quote ? `<br><span class="q">&ldquo;${esc(r.quote)}&rdquo;</span>` : '')
          + `</li>`).join('')
      + '</ul>';
  }
  h += `<h2>Rules that restrict something other than the hour (${other.length})</h2>`
    + '<p>These have no clock time to draw, which does not make them lesser. Several '
    + '<em>change</em> the bars above: an access control can disapply the watershed '
    + 'entirely, so a gap in this chart can be filled by a rule in this list.</p><ul>'
    + other.slice(0,40).map(r => `<li><code>${r.id}</code>`
        + (r.tok && r.tok !== 'n/a' ? ` <code>${esc(r.tok.slice(0,70))}</code>` : '')
        + `${r.hr ? '<span class="hr">R</span>' : ''}<br>`
        + `<span class="what">${esc(r.text)}</span></li>`).join('')
    + '</ul>' + (other.length > 40 ? `<p>and ${other.length-40} more.</p>` : '');
  $('#untimed').innerHTML = h;
}

['#c','#s','#g'].forEach(s => $(s).addEventListener('change', draw));
draw();
</script></body></html>
"""

if __name__ == "__main__":
    raise SystemExit(main())
