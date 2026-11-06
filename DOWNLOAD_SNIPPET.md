# Saving the bot-blocked pages as .txt (DevTools)

13 HTML pages still need a manual save. Ctrl+P to PDF works, but it is the wrong
output: the manifest lists these as `html2txt` with `.txt` targets, and `import_saved.py`
reads text. A PDF would have to be re-extracted for no gain.

The console snippet below is better for three reasons:

1. **It saves the right format,** with the right filename, chosen automatically from the URL.
2. **It defeats the JavaScript problem.** `FR-R2` returns an empty shell to a fetcher because
   its body is drawn by JavaScript. By the time you are looking at the page the text has
   rendered, so `innerText` sees what no fetch can. Scroll to the bottom first so anything
   lazy-loaded has arrived.
3. **It verifies as it saves.** Every page has an `expect` phrase that must appear in the
   genuine document. The snippet refuses to download on a miss. That guard is what would have
   caught `FR-R2`'s first apparently-successful save - 12,493 characters of pure site
   navigation that sailed through a naive length check.

## How to use

1. Open the page in a normal browser tab and let it load. **Scroll to the bottom.**
2. `F12` -> Console. First time, Chrome may ask you to type `allow pasting`.
3. Paste the snippet, Enter.
4. Green line = saved. Red line = it refused; read why and re-run.
5. Drop everything into `sources/originals/incoming/` and run
   `python3 pipeline/import_saved.py`.

The importer identifies each file by its **content, not its filename**, so a wrong filename
is harmless. It also re-checks the `expect` string, so the guard applies twice.

## The snippet

```javascript
// ---- Ofcom / Arcom page -> .txt saver -------------------------------------
// Paste once per page in the DevTools Console (F12), on the page itself.
// It picks the filename, strips the furniture, CHECKS the text is real, downloads.
(() => {
  const T = {
  "https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-standards/section-one-protecting-under-eighteens": {
    "id": "UK-S1",
    "file": "UK-S1_ofcom_code_section_1.txt",
    "expect": "prizes aimed at children"
  },
  "https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-standards/section-two-harm-offence": {
    "id": "UK-S2",
    "file": "UK-S2_ofcom_code_section_2.txt",
    "expect": "generally accepted standards must be applied"
  },
  "https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-standards/section-three-crime-disorder-hatred-abuse": {
    "id": "UK-S3",
    "file": "UK-S3_ofcom_code_section_3.txt",
    "expect": "abusive or derogatory treatment of individuals"
  },
  "https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-standards/section-four-religion": {
    "id": "UK-S4",
    "file": "UK-S4_ofcom_code_section_4.txt",
    "expect": "special powers or abilities"
  },
  "https://www.ofcom.org.uk/tv-radio-and-on-demand/broadcast-standards/mandatory-daytime-protection": {
    "id": "UK-M1",
    "file": "UK-M1_ofcom_mdp_statement.txt",
    "expect": "mandatory daytime protection"
  },
  "https://www.legislation.gov.uk/ukpga/2003/21/section/319": {
    "id": "UK-L1",
    "file": "UK-L1_communications_act_2003_s319.txt",
    "expect": "persons under the age of eighteen are protected"
  },
  "https://www.legislation.gov.uk/uksi/2020/1062/note/made": {
    "id": "UK-L2",
    "file": "UK-L2_avms_regulations_2020_note.txt",
    "expect": "audiovisual media services"
  },
  "https://www.arcom.fr/en/find-out-more/legal-area/legal-resources/december-15-2004-notice-television-service-editors-and-distributors-showing-category-v-programs-mainland-france-and-overseas-france": {
    "id": "FR-R2",
    "file": "FR-R2_reco_2004-7_category_V.txt",
    "expect": "minuit"
  },
  "https://as-pc-www.csa.fr/Proteger/Protection-de-la-jeunesse-et-des-mineurs/La-signaletique-jeunesse": {
    "id": "FR-S1c",
    "file": "FR-S1c_signaletique_jeunesse_fr.txt",
    "expect": "horaires de diffusion"
  },
  "https://solidarites.gouv.fr/classification-et-signaletique-de-la-television": {
    "id": "FR-S2",
    "file": "FR-S2_solidarites_classification.txt",
    "expect": "signaletique jeunesse"
  },
  "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000512205": {
    "id": "FR-L1",
    "file": "FR-L1_loi_86-1067.txt",
    "expect": "protection de l'enfance"
  },
  "https://www.legislation.gov.uk/eudr/2010/13/article/6a": {
    "id": "EU-D1",
    "file": "EU-D1_avmsd_article_6a.txt",
    "expect": "will not normally hear or see"
  },
  "https://eur-lex.europa.eu/legal-content/EN/TXT": {
    "id": "EU-D1b",
    "file": "EU-D1b_directive_2018_1808.txt",
    "expect": "1808"
  }
};
  const key = location.origin + location.pathname.replace(/\/$/, '');
  const t = T[key];
  if (!t) { console.warn('Not a manifest page. Saving as page.txt anyway.'); }

  // Prefer the real content element; fall back to body. Strip nav/aside/footer first.
  const root = (document.querySelector('main, article, [role=main], .page-content')
                || document.body).cloneNode(true);
  root.querySelectorAll('nav, aside, footer, header, script, style, noscript, svg,'
    + ' form, .cookie, [class*=cookie], [class*=banner], [class*=breadcrumb],'
    + ' [aria-hidden=true]').forEach(n => n.remove());

  let text = root.innerText.replace(/\n{3,}/g, '\n\n').trim();

  console.log('%c' + (t ? t.id : 'unknown') + '  ' + text.length.toLocaleString()
    + ' chars', 'font-weight:bold');

  if (t && !text.toLowerCase().includes(t.expect)) {
    console.error('STOP - expected phrase not found: "' + t.expect + '"');
    console.error('This is probably navigation only, not the document. '
      + 'Scroll the page fully, let it finish rendering, then re-run. '
      + 'Not downloading.');
    return;
  }
  if (text.length < 2000) {
    console.error('STOP - only ' + text.length + ' chars. Too short to be the document.');
    return;
  }

  const name = t ? t.file : 'page.txt';
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([text], {type: 'text/plain;charset=utf-8'}));
  a.download = name;
  a.click();
  console.log('%cSaved ' + name + ' - expected phrase present.', 'color:green');
})();
```

## Pages it covers

| doc_id | saves as | must contain |
|---|---|---|
| `EU-D1` | `EU-D1_avmsd_article_6a.txt` | `will not normally hear or see` |
| `EU-D1b` | `EU-D1b_directive_2018_1808.txt` | `1808` |
| `FR-L1` | `FR-L1_loi_86-1067.txt` | `protection de l'enfance` |
| `FR-R2` | `FR-R2_reco_2004-7_category_V.txt` | `minuit` |
| `FR-S1c` | `FR-S1c_signaletique_jeunesse_fr.txt` | `horaires de diffusion` |
| `FR-S2` | `FR-S2_solidarites_classification.txt` | `signaletique jeunesse` |
| `UK-L1` | `UK-L1_communications_act_2003_s319.txt` | `persons under the age of eighteen are protected` |
| `UK-L2` | `UK-L2_avms_regulations_2020_note.txt` | `audiovisual media services` |
| `UK-M1` | `UK-M1_ofcom_mdp_statement.txt` | `mandatory daytime protection` |
| `UK-S1` | `UK-S1_ofcom_code_section_1.txt` | `prizes aimed at children` |
| `UK-S2` | `UK-S2_ofcom_code_section_2.txt` | `generally accepted standards must be applied` |
| `UK-S3` | `UK-S3_ofcom_code_section_3.txt` | `abusive or derogatory treatment of individuals` |
| `UK-S4` | `UK-S4_ofcom_code_section_4.txt` | `special powers or abilities` |

## The PDFs

The remaining documents are PDFs, where the browser's own download is correct - no snippet
needed. Save each under the `target_filename` the manifest gives and drop it in the same
`incoming/` folder.

## If a page 404s

Three links carry a `?v=` version token that changes whenever the publisher revises the file.
If one 404s, do not hunt for a new token: open the `landing_page` in the manifest and follow
the current link from there, then tell me the new URL so the manifest gets fixed.
