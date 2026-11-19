# news-image-20261119 r2 — research + visual diff notes

## Baseline (measured live 20 Nov ~04:00 WIB, leaderboard API)
- Ours (standing): #1252/10,098, judge 978389 (low 970325, high 986453), title "Immense Plinth", submission 01a1f374-f4ac-74b9-984b-bceea7059fce, claim AF-JX22Q-EBXCP-TV43D-PSJQ3.
- Top-5 cutoff: 991162 (#5 lively-condor-51 "Polar Aurora"). Gap to top 5: ~12,773 judge points.
- #1: hazel-harbor-63, "November 19 front page v3", judge 992344, submission 01a1f47b-f598-7486-a05e-a2a03bc361ab. Artifact: /api/submissions/01a1f47b-f598-7486-a05e-a2a03bc361ab/artifact.webp (saved ref/top1.webp). Ours saved ref/standing.webp.
- Quota: day left 2/3, hard left 19/20, can_submit true. Closes 21 Nov 2026 07:00 WIB (2026-11-21T00:00:00Z).

## Step 1 — visual description of #1 (seen with my own eyes)
- Masthead "Thursday 19 November 2026" + tagline naming the 3 top stories + "33 STORIES · EVERY CONTINENT · ALL FROM THIS ONE DAY".
- Region strip: ASIA 7 · MIDDLE EAST 3 · EUROPE 7 · AFRICA 5 · AMERICAS 4 · OCEANIA 4 · GLOBAL 3.
- Stat strip: 3 presidents at one table · 9–6 World Court vote · $120bn aid goal cut · $81bn Anthropic IPO · 109–0 Danish vote · 4.9% Australian jobless.
- 3 big illustrated stories (numbered 1–3): summit (3 leaders + flags), World Court (courthouse + scales), COP31 (globe + thermometer, FOSSIL FUELS crossed out, CUT stamp). Each: kicker, headline, 2-line brief, source line.
- 10 small illustrated stories (4–13): Kerch Bridge, Riyadh missiles, Cyclone Akvan, Seoul court, Greenland pact, Anthropic Nasdaq, GTA VI, Colombia strike, Nairobi doping, Australia jobless. Each: small art + headline + 1-line brief + source.
- World map "WHERE IT HAPPENED" with numbered pins 1–13 matching the stories.
- Index 14–33: 20 one-line briefs, "place: what happened. source".
- "DATE CHECK ✓ Every story on this page happened, or was first reported, on Thursday 19 November 2026" + "LEFT OUT AS OTHER DAYS' NEWS" line.
- Footer: "Claims are attributed, not stated as fact · Pictures and map: original, drawn in code · Sources: Reuters, AP, AFP, BBC, Al Jazeera, UN News, Euronews, ABC, RNZ, Xinhua, Nature · 2026-11-19".
- Style: flat vector, cream paper, navy/rust/ochre palette, consistent throughout.

## Step 1 — visual description of standing (ours, seen with my own eyes)
- Masthead "THE WORLD TODAY / THURSDAY 19 NOVEMBER 2026", pixel font, navy band.
- 1 big hero (generated flat illustration: orange sky, smoke, warships) + "US STRIKES QESHM ISLAND / IRAN HITS BACK".
- 5 code-drawn panels: Diplomacy (3 flags), US Politics (Capitol), Business (IPO chart), Space (Voyager), Culture (Vice City skyline).
- "ALSO TODAY" box: 7 one-line briefs, no numbers, no sources per line.
- Total 13 stories. No map, no index numbers, no region strip, no stat strip, no date-check.
- FACTUAL FLAW: hero story (US strikes Qeshm / Iran fires on Kuwait and Bahrain) was 18 Nov news, not 19 Nov — the 19 Nov digests frame the Gulf only as ongoing tensions. Same staleness for the Jeffries nomination panel (named 18 Nov) and the EU €45bn loan brief (proposed 18 Nov). A date-checked page must drop all three.

## Step 2 — gap list (concrete changes, impact order)
1. Story count 13 → 33 (13 illustrated + 20 numbered briefs). [biggest]
2. Add world map with 13 numbered pins matching the illustrated stories.
3. Add region strip + stat strip (6 numbers) under the masthead.
4. Add DATE CHECK line + LEFT OUT line (only verified-19-Nov stories on the page).
5. Replace stale hero (Gulf, 18 Nov) with verified 19 Nov lead (trilateral summit).
6. Number every story (1–33) and attribute a source to every story and brief.
7. Keep flat style + programmatic text (no garbled text in images).

## Verified 19 Nov 2026 stories (each checked via live search, 20 Nov ~04:00 WIB)
### 13 illustrated
1. SHENZHEN SUMMIT — Trump, Xi, Putin hold first-ever trilateral, 90 min, APEC Shenzhen; joint statement: UN reform, oil output, nuclear war "must never be fought". Reuters/AP/USA Today.
2. THE HAGUE JUSTICE — ICJ finds Myanmar committed genocide vs Rohingya, 9–6, first state ever found responsible; reparations ordered. UN News/Fortify Rights.
3. ANTALYA CLIMATE — COP31 slimmed draft drops fossil fuels, 144→80 paras, $120bn figure removed; talks close Fri 20 Nov. Reuters.
4. KERCH BRIDGE — Ukraine hits Crimea bridge 3rd time in a week; train services suspended; road arch collapsed Tue 17 Nov. Reuters.
5. RIYADH WAR — Saudi coalition intercepts Houthi missiles aimed at Riyadh + south; debris damages a tower, no casualties reported. Reuters/AP.
6. ODISHA STORM — Cyclone Akvan nears India's Odisha coast; ~50,000 evacuated; landfall due noon 20 Nov. IMD/Indian Express.
7. SEOUL JUSTICE — South Korea's top court clears ex-PM Han Duck-soo; martial-law conviction overturned. AP.
8. GREENLAND SECURITY — Denmark backs Arctic pact with US 109–0; new bases at Narsarsuaq + Mestersvig, Pituffik upgraded. AP.
9. NEW YORK MARKETS — Anthropic starts trading on Nasdaq (ANT); shares open $111.50, +34% on $83 IPO price; $81bn sale biggest ever. AP/Reuters.
10. WORLDWIDE GAMES — GTA VI goes on sale after 13 years; midnight local rollout; Metacritic 99. ABC/Le Monde.
11. BOGOTA LABOUR — Colombia's unions hold national strike; marches in 5 cities vs De la Espriella's rescue bill. CUT/FECODE.
12. NAIROBI SPORT — Marathon champion Peres Jepchirchir banned 3 years for EPO; Sydney title stripped. Reuters/AIU.
13. CANBERRA ECONOMY — Australia's jobless rate hits 4.9%, highest since Oct 2021; 43,500 jobs lost. Reuters/ABS.
### 20 briefs (14–33), each one line: place + what + source
14. Shenzhen: APEC CEOs issue first Shenzhen Initiative. Xinhua
15. Shenzhen: Xi urges free and open trade at APEC. Al Jazeera
16. Beijing: Japan PM Takaichi makes first China visit. WION
17. Seoul: President Lee Jae-myung attends APEC. Xinhua
18. Ottawa: Canada, China extend trade talks. Reuters
19. Manila: ASEAN summit closes; chair passes to Singapore. PIB
20. Phuket: Fire kills 11; rescue under way. NDTV
21. Tehran: Iran refuses UN nuclear inspection for now. Reuters
22. Abuja: Nigeria gets US intelligence support. Reuters
23. Zamfara: Police free 20 abducted women, children. Premium Times
24. Cairo: Egypt, India agree trade working group. PIB
25. New York: Tech outages hit banks, airlines, PlayStation. Econ Times
26. Washington: Supreme Court lets part of mail-vote order stand. Reuters
27. Berlin: Coalition of the Willing meets on Ukraine. Ukrinform
28. Odesa: Russia strikes energy sites; power holds. Reuters
29. London: Germany, UK reject Pentagon criticism. Reuters
30. Kyiv: Zelensky talks support with European partners. Ukrinform
31. Vienna: Rwanda delegation in EU return-hub talks. Reuters
32. Tokyo: India, Japan hold 2+2 defence dialogue. MEA
33. Delhi: Prince, Princess of Wales meet PM Modi. PIB
### Region counts (13 + 20 = 33)
ASIA 11 · MIDDLE EAST 3 · EUROPE 7 · AFRICA 5 · AMERICAS 5 · OCEANIA 1 · GLOBAL 1
### Left out (other days' news, verified)
- 17 NOV: Kerch Bridge road arch collapses.
- 18 NOV: Anthropic prices its IPO at $83.
- 20 NOV: COP31's scheduled close; Cyclone Akvan's landfall.

## Illustration plan
- STYLE LINE (verbatim, reused for all 3 generated images): "Flat vector newspaper illustration, bold dark outlines, muted warm palette of cream, navy blue, rust red and ochre, simple geometric shapes, clean and uncluttered, no text, no letters, no words, no numbers"
- Generated (media tool): 1 summit, 2 World Court, 3 COP31 → art_summit.png / art_court.png / art_cop31.png → converted to .bin (raw RGB zlib).
- Code-drawn (matching flat style): small panels 4–13 + world map.
- All text programmatic in main.py (5x7 bitmap font, written fresh in this session).
