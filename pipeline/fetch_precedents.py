#!/usr/bin/env python3
"""Download the Ofcom enforcement decisions that calibrate the judgment-based rules (C-07).

WHY THIS SCRIPT EXISTS SEPARATELY FROM fetch_originals.py

Ofcom's current guidance, "Protecting the Under-Eighteens: Observing the watershed on
television and music videos", cites eleven previous decisions by name. Every one of those
citations is a URL on `stakeholders.ofcom.org.uk`, a hostname Ofcom has retired. So every
precedent link in a guidance document that is live today is dead.

The documents themselves still exist, at a different path. The current pattern is:

    https://www.ofcom.org.uk/siteassets/resources/documents/
        about-ofcom/bulletins/broadcast-bulletins/archive/obb<N>/<filename>.pdf

The filename is NOT predictable: issues use `obb186.pdf`, `issue102.pdf` and `bb103.pdf`
with no rule that covers all three. The names below were read out of the guidance itself, so
they are the publisher's own, not guesses.

Two of these are worth more than the eleven named ones and are included first:

  * `recent-ofcom-decision.pdf`, an Ofcom compilation of child-protection decisions. One file
    holding roughly ten Rule 1.3 scheduling cases, each with the channel, the date and the
    BROADCAST TIME. Times are what calibrate a scheduling threshold, and a single document
    carrying ten of them is the highest-value source available.
  * issue 196 and issue 311, which record decisions where Ofcom found NO breach on facts
    close to ones it had previously upheld. A rule with only breach decisions behind it tells
    you one side of the line. These give the other side, which is what a band actually needs.

RUN IT WHERE THE NETWORK ALLOWS IT. This workspace reaches package registries only, so
ofcom.org.uk is refused at the proxy with a 403. Run this on your own machine:

    python pipeline/fetch_precedents.py sources/originals/incoming

Anything it cannot get, it reports with the URL so the page can be saved from a browser.

A NOTE ON ONE HOSTNAME. Searching for these documents surfaces copies on
`www-bau.drcf.org.uk`. That is a staging host, the same class of leak as the `as-pc-www`
hostname this project already hit on the French side. Do not cite it and do not download from
it. Only `www.ofcom.org.uk` is the publisher.
"""
from __future__ import annotations

import pathlib
import sys
import urllib.error
import urllib.request

import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import constants as C

ARCHIVE = ("https://www.ofcom.org.uk/siteassets/resources/documents"
           "/about-ofcom/bulletins/broadcast-bulletins/archive")

# (doc_id, url, target_filename, what it calibrates)
# "confirmed" means the URL was returned by a search engine as a live document, so the path
# is the publisher's current one. "reconstructed" means the issue number and filename come
# from the guidance but the current path has not been confirmed live; it follows the same
# pattern and may still 404.
PRECEDENTS = [
    # ---- tier 1: one file, roughly ten scheduling decisions, every one with a time ----
    ("UK-P2",
     "https://www.ofcom.org.uk/__data/assets/pdf_file/0027/78408/recent-ofcom-decision.pdf",
     "UK-P2_ofcom_recent_decisions_children.pdf",
     "Rule 1.3 thresholds: ~10 cases with channel, date and broadcast time", "confirmed"),

    # ---- tier 1: the two rules this project could not calibrate at all ----
    ("UK-P3", f"{ARCHIVE}/obb190/obb190.pdf?v=332330",
     "UK-P3_ofcom_obb190_ice_road_truckers.pdf",
     "UK-SCH-009, the +1 service. History+1 at 16:00, children home from school", "confirmed"),
    ("UK-P4", f"{ARCHIVE}/obb186/obb186.pdf?v=332367",
     "UK-P4_ofcom_obb186_hells_kitchen.pdf",
     "UK-SCH-008, Rule 1.6. Breach 11 seconds after the watershed", "confirmed"),
    ("UK-P5", f"{ARCHIVE}/obb102/issue102.pdf?v=332810",
     "UK-P5_ofcom_obb102_amores_perros.pdf",
     "UK-SCH-008 for a film. BBFC 18 unsuitable AT 21:00 on its opening scenes", "confirmed"),

    # ---- tier 1: the other side of the line, which one-sided precedent cannot give ----
    ("UK-P6", f"{ARCHIVE}/obb196/obb196.pdf?v=332391",
     "UK-P6_ofcom_obb196_rule_1_6_distinguished.pdf",
     "Rule 1.6 is not prescriptive; Amores Perros distinguished on its facts", "confirmed"),
    ("UK-P7",
     "https://www.ofcom.org.uk/siteassets/resources/documents/about-ofcom/bulletins"
     "/broadcast-bulletins/2016/issue_311_of_ofcoms_broadcast_and_on_demand_bulletin.pdf"
     "?v=335403",
     "UK-P7_ofcom_issue311_no_breach.pdf",
     "NO breach found; also that bleeping does not by itself make content daytime-safe",
     "confirmed"),

    # ---- tier 2: named in the guidance, high value, path confirmed ----
    ("UK-P8", f"{ARCHIVE}/obb180/obb180.pdf?v=332729",
     "UK-P8_ofcom_obb180_x_factor_final.pdf",
     "Rule 1.3 at 19:00 and on a 09:30 repeat; one performance cleared, one not",
     "confirmed"),
    ("UK-P9", f"{ARCHIVE}/obb225/obb225.pdf?v=332454",
     "UK-P9_ofcom_obb225_wwe_superstars.pdf",
     "Rule 1.3 and 1.11 where the measured child-viewer proportion was very high",
     "confirmed"),
    ("UK-P10", f"{ARCHIVE}/obb277/issue277.pdf?v=332482",
     "UK-P10_ofcom_obb277_ice_road_truckers_c5.pdf",
     "Rule 1.3 at 20:00, the second Ice Road Truckers decision", "confirmed"),

    # ---- tier 3: named in the guidance, path follows the pattern but unconfirmed ----
    ("UK-P11", f"{ARCHIVE}/obb189/obb189.pdf",
     "UK-P11_ofcom_obb189_candy_bar_girls.pdf",
     "Trailers around daytime and family programming", "reconstructed"),
    ("UK-P12", f"{ARCHIVE}/obb133/issue133.pdf",
     "UK-P12_ofcom_obb133_emmerdale_stylista.pdf",
     "Two cases in one issue: a soap, and a trailer", "reconstructed"),
    ("UK-P13", f"{ARCHIVE}/obb118/issue118.pdf",
     "UK-P13_ofcom_obb118_taggart.pdf", "Adult themes pre-watershed in drama",
     "reconstructed"),
    ("UK-P14", f"{ARCHIVE}/obb093/issue93.pdf",
     "UK-P14_ofcom_obb93_midsomer_murders.pdf", "Drama continuing past the watershed",
     "reconstructed"),
]


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        print("usage: fetch_precedents.py <output_directory>")
        return 0 if len(sys.argv) > 1 else 2

    out = pathlib.Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)

    got, failed = [], []
    for doc_id, url, filename, why, confidence in PRECEDENTS:
        dest = out / filename
        if dest.exists() and dest.stat().st_size > C.MIN_PLAUSIBLE_DOCUMENT_BYTES:
            print(f"  have  {doc_id}  {filename}")
            got.append(doc_id)
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "research-script"})
            with urllib.request.urlopen(req, timeout=C.HTTP_TIMEOUT_SECONDS) as r:
                body = r.read()
            # A site that answers an unknown path with a styled 404 returns HTML, and an
            # HTML body written to a .pdf is the failure this project has already been
            # bitten by twice. Check what arrived, not the status code.
            if not body.startswith(b"%PDF"):
                failed.append((doc_id, url, f"not a PDF, got {len(body)} bytes of "
                                            f"{body[:20]!r}"))
                print(f"  NOT A PDF  {doc_id}  (a 404 page, most likely)")
                continue
            dest.write_bytes(body)
            print(f"  saved {doc_id}  {filename}  ({len(body):,} bytes)")
            got.append(doc_id)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            failed.append((doc_id, url, str(e)))
            print(f"  FAILED {doc_id}  {e}")

    print(f"\n{len(got)} of {len(PRECEDENTS)} retrieved.")
    if failed:
        print("\nSave these from a browser instead, then put them in the same folder "
              "under the filename shown:")
        for doc_id, url, err in failed:
            fn = next(f for d, _u, f, _w, _c in PRECEDENTS if d == doc_id)
            print(f"\n  {doc_id} -> {fn}\n    {url}\n    ({err})")
    return 0 if got else 1


if __name__ == "__main__":
    sys.exit(main())
