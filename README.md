# Spring Real Estate — website concept

Visueel concept voor de nieuwe website van **Spring Real Estate**, gebouwd als
statische HTML/CSS/JS-site op basis van het **Katana**-Webflow-template en de
**Spring brand bible**. Bedoeld als visuele referentie/prototype dat per pagina
verder uitgewerkt en uiteindelijk in Webflow nagebouwd kan worden.

> **Powered by People. Backed by Tech.**

## Uitgangspunten
- **Doelgroepgestuurd**: bezoekers worden begeleid vanuit hun vraag —
  Gebruiker · Eigenaar · Investeerder · Ontwikkelaar.
- **23 business units** komen terug op de site (sectie + footer).
- **Grote, prominente zoekbalk** op de homepage (Katana-stijl), bedoeld om ook
  op andere pagina's terug te komen.
- **3 talen**: NL · EN · ES (taalschakelaar rechtsboven; concept-implementatie).
- Visuele stijl: licht & luchtig met donkere fotografische hero/secties,
  Spring-groen accent, afgeronde hoeken, Raleway.

## Huisstijl (uit het brandbook)
| Token | Hex | Gebruik |
|-------|-----|---------|
| Hoofdgroen | `#7CA73F` | Primaire kleur, buttons, accenten |
| Lijnengroen | `#89B647` | Lijnen / hover-accenten |
| Stipgroen | `#C3D88A` | Secundaire button, logo-punt |
| Hoofdgrijs | `#2B2B29` | Bodytekst / donkere secties |
| Lichtgrijs | `#AFAEB2` | Subtiele tekst / kaders |
| Wit / Zwart | `#FFFFFF` / `#000000` | Basis |

Lettertype: **Raleway** (Google Fonts). Buttons altijd met afgeronde hoeken.

## Structuur
```
spring-site-concept/
├── index.html          # Homepage (af)
├── css/styles.css      # Design system + alle secties
├── js/main.js          # Nav, mobiel menu, zoek-tabs, taalschakelaar
├── images/             # Logo + foto's
└── _assets/            # Bronmateriaal (brandbook, PDF's) — niet in git
```

## Lokaal bekijken
```bash
# vanuit de projectmap
python -m http.server 4321
# open http://localhost:4321
```

## Status / volgende pagina's
- [x] **Homepage** — hero + zoekbalk, doelgroepen, USP's, locatiekaart
      (Utrecht/Amsterdam/Valencia), team, reviews, 23 units, resources, footer
- [ ] **Listing-detailpagina** (volgens gedeeld voorbeeld: licht, groen, specs,
      adviseur, contactformulier)
- [ ] **Listings / Aanbod** (overzicht met filters — CBRE-stijl)
- [ ] **Diensten** (4 doelgroepen, CTA boven de vouw)
- [ ] **About Us · Agents/Team · Resources/Blog · Contact · Locaties**
- [ ] Vertalingen NL/EN/ES koppelen aan de taalschakelaar

## Bron-input
- `Aanpassingen Katana Template.pdf` — aanpassingen per pagina
- `Concuerrentenanalyse Spring.xlsx` — concurrentie / mee te nemen elementen
- `Brandbook Spring Real Estate DEF` — huisstijl
- Referentie-template: https://katana-real-estate.webflow.io
- Oude site: https://www.springrealestate.com/en/
