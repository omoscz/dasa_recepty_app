# 🍳 Dáša Recepty App

Chytrá rodinná kuchařská aplikace postavená na frameworku **Streamlit** a poháněná nejnovějším modelem **Google Gemini (2.5-flash)** přes oficiální knihovnu `google-genai`. 

Aplikace slouží k efektivnímu plánování týdenního jídelníčku na základě akčních surovin (masa, mléčných výrobků, zeleniny atd.) s možností zaměřit menu na konkrétní kulinářský styl. Vybrané detailní recepty umí odeslat v dárkovém HTML formátu přímo na rodinný e-mail.

## 🚀 Hlavní funkce

- **Strukturovaný výběr akčních surovin:** Suroviny jsou v mobilním rozhraní přehledně rozdělené do kategorií (Masa, Mléčné výrobky, Zelenina/Přílohy, Ostatní) pomocí rozbalovacích prvků (`st.expander`).
- **Volitelný kulinářský styl (Typ kuchyně):** Možnost zúžit výběr receptů na konkrétní směr (např. *Tradiční česká*, *Asijská*, *Středomořská*, *Mexická* atd.). Pokud není vybrán, AI zvolí pestrý mix.
- **Inteligentní porcování (Batch Cooking & Krabičky):** Recepty jsou dimenzovány pro 4člennou rodinu (2 dospělí + 2 děti), avšak s šéfkuchařským pokynem navýšit základy a gramáže tak, aby **vždy zbyly 2–3 plnohodnotné porce na obědy do práce pro rodiče**.
- **Robustní AI integrace:** Využívá nejnovější SDK `google-genai`. Obsahuje automatický fallback (záložní mechanismus) – pokud je primární model `gemini-2.5-flash` přetížený (chyba 503), aplikace automaticky přepne na `gemini-2.5-flash-8b`, aby uživatel nic nepoznal.
- **Elegantní HTML e-maily:** Vygenerovaný kód čistí surový Markdown z AI a převádí ho na atraktivní HTML dopis s barevnými nadpisy a jasnou strukturou, který se správně a čistě zobrazuje v e-mailových klientech (např. Seznam.cz).

## 🛠️ Struktura projektu

```text
.
├── app.py             # Hlavní kód aplikace (Streamlit UI, parsovací a odesílací logika)
├── config.py          # Konfigurační soubor (proměnné, seznamy surovin, prompt šablony)
└── README.md          # Dokumentace k projektu
