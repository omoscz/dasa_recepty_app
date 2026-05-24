import os

# --- 1. NASTAVENÍ E-MAILU (Pro Seznam.cz přes SSL port 465) ---
SMTP_SERVER = "smtp.seznam.cz"
SMTP_PORT = 465
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "dasajidelnicek@seznam.cz")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "zYvHmfPF8Byea4m")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "omos@email.cz")

# --- 2. GOOGLE GEMINI API KLÍČ ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDAjmKtgXI7_bNcctgpm7niYL5Y-6oB5_Q")

# --- 3. DOSTUPNÉ SUROVINY PODLE KATEGORIÍ ---
AVAILABLE_INGREDIENTS = {
    "🥩 Maso a uzeniny": [
        "Kuřecí prsa", "Kuřecí stehna", "Kuřecí křídla", "Celé kuře", "Kuřecí játra",
        "Vepřová krkovice", "Vepřová plec", "Vepřová kýta", "Vepřový bůček", "Vepřová panenka",
        "Mleté maso (mix / hovězí / vepřové)", "Hovězí zadní", "Hovězí přední / na guláš", "Uzená krkovice / plec"
    ],
    "🥛 Mléčné výrobky a sýry": [
        "Smetana na vaření / ke šlehání", "Zakysaná smetana", "Tvaroh", "Edam / Gouda (cihla)", 
        "Niva / Modrý sýr", "Mozzarella", "Hermelín / Camembert", "Máslo", "Mascarpone / Ricotta"
    ],
    "🥔 Zelenina, přílohy a houby": [
        "Brambory", "Cuketa", "Lilek", "Brokolice / Květák", "Špenát (čerstvý / mražený)", 
        "Rajčata v plechovce / Pasírovaná", "Žampiony / Lesní houby", "Papriky / Rajčata čerstvá",
        "Dýně (Hokaido)", "Kořenová zelenina (mrkev, celer, petržel)"
    ],
    "🥫 Ostatní zásoby a speciality": [
        "Listové těsto", "Tortilly", "Rýže (Basmati / Jasmínová)", "Těstoviny", 
        "Fazole / Cizrna v plechovce", "Kokosové mléko", "Vejce"
    ]
}

# --- 4. VOLITELNÉ KULINÁŘSKÉ STYLY (TYPY KUCHYNÍ) ---
AVAILABLE_STYLES = [
    "Tradiční česká (omáčky, pečená masa, hutnější jídla)",
    "Středomořská a italská (těstoviny, rajčata, bylinky, lehčí jídla)",
    "Asijská (rychlé pánve, rýže, kokosové mléko, jemný orient)",
    "Mexická a tex-mex (tortilly, fazole, mleté maso, kukuřice)",
    "Moderní rychlovky (zapékané věci, jídla z jednoho pekáče, rychlé směsi)",
    "Svěží a odlehčená (více zeleniny, méně těžkých příloh)"
]

# --- 5. PREFERENCE PRO RODINNÝ JÍDELNÍČEK ---
FAMILY_PREFERENCES = {
    "pocet_osob": 4,  
    "styl_vareni": "vaření s předstihem (batch cooking), jídla ideální na ohřev a rozležení do krabiček, omáčky skvělé i druhý den, efektivní využití zbytkového tepla",
    "omezeni_a_alergie": "žádná omezení, děti 6 a 10 let (přizpůsobit pálivost), jídlo musí perfektně chutnat i po ohřátí další dny"
}

# --- 6. PROMPT 1: ŠABLONA PRO NAVRŽENÍ MENU (S PODPOROU KUCHYNÍ) ---
AI_MENU_PROMPT_TEMPLATE = """
Jsi špičkový šéfkuchař, expert na rodinnou gastronomii a efektivní plánování jídel. 
Tvým úkolem je navrhnout stručný a inspirativní přehled přesně 5 NÁPADŮ NA JÍDLA na základě vybraných parametrů.

Zde jsou rodinné preference:
- Základní složení rodiny: {pocet_osob} osoby (dva dospělí a dvě děti)
- Styl vaření: {styl_vareni}
- Omezení a alergie: {omezeni_a_alergie}

Suroviny, které jsou momentálně k dispozici:
{vybrane_suroviny}

Preferovaný kulinářský styl / typ kuchyně:
{preferovany_styl}

CRITICAL RULES PRO GENEROVÁNÍ:
1. KULINÁŘSKÝ STYL: Pokud je specifikován konkrétní kulinářský styl, VŠECH 5 jídel musí striktně odpovídat tomuto zaměření. Pokud je styl "Nespecifikováno", vytvoř pestrý mix převážně české a evropské rodinné klasiky.
2. VELKORYSÉ PORCE (KRABIČKOVÁNÍ): Jídla navrhuj primárně pro {pocet_osob} osoby u stolu, ale koncipuj je tak, aby se vařila ve větším hrnci/pekáči a automaticky zbylo několik porcí (2-3) do krabiček na příští dny na oběd pro rodiče. Jídla musí dobře snášet ohřev.
3. ROZMANITOST A SUROVINY: Postav recepty primárně kolem vybraného masa a zakomponuj do nich co nejefektivněji i další vybrané suroviny. Jídla přizpůsob dětským chutím (nepřehánět s pálivostí).
4. BUĎ STRUČNÝ: Nepiš žádné postupy, žádné gramáže. Pouze krátký přehled.
5. FORMÁT: Odpověz v čistém Markdownu. Nepoužívej žádné HTML tagy.

Pro KAŽDÉ z 5 jídel vygeneruj PŘESNĚ tuto strukturu (každé jídlo odděl čarou `---`):

### [EMOJI] [NÁZEV JÍDLA]
* **O co jde:** [1-2 věty, stručný popis chuti a stylu, a proč se zrovna tohle jídlo skvěle ohřívá a rozkládá do krabiček pro rodiče]
* **Co bude navíc potřeba dokoupit:** [Stručný seznam hlavních surovin, které v seznamu dostupných surovin chybí a je nutné je dokoupit]

Na začátek textu vlož jen krátký, přátelský šéfkuchařský úvod (1-2 věty) a pak hned přejdi na seznam receptů.
"""

# --- 7. PROMPT 2: ŠABLONA PRO DETAILEK RECEPTU ---
AI_DETAIL_PROMPT_TEMPLATE = """
Jsi špičkový šéfkuchař. Uživatel si vybral jedno z tvých navržených jídel a chce na něj kompletní, podrobný recept.

Název vybraného jídla: {nazev_jidla}

Zde jsou rodinné preference pro kontext:
- Základní složení rodiny: {pocet_osob} osoby (2 dospělí + 2 děti)
- Styl vaření: {styl_vareni}
- Omezení a alergie: {omezeni_a_alergie}

Vygeneruj detailní kuchařský recept v přehledném Markdownu. Recept musí obsahovat:
1. **Suroviny a gramáže:** Rozpočítej množství surovin tak, aby se s přehledem najedla celá {pocet_osob}členná rodina k hlavnímu jídlu a VŽDY zbyly minimálně 2 plnohodnotné porce navíc do krabiček na obědy pro rodiče v pracovním týdnu.
2. **Postup krok za krokem** napsaný jasně a srozumitelně.
3. **Šéfkuchařské triky pro toto jídlo:** (např. jak zajistit, aby maso při ohřívání v mikrovlnce nevyschlo, jak správně využít zbytkové teplo při dovírání pod pokličkou nebo v troubě, případně jak zajistit, aby omáčka do druhého dne nezhoustla moc).

Odpověz přímo receptem, bez zbytečných uvítacích frází okolo.
"""