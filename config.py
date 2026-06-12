# config.py

SUROVINY_KATALOG = {
    "🥩 Maso, drůbež a ryby": [
        # Kuřecí / Krůtí
        "Kuřecí prsa", "Kuřecí stehna (horní/dolní)", "Kuřecí křídla", "Celé kuře", "Mleté kuřecí/krůtí", "Krůtí prsa",
        # Vepřové
        "Vepřová krkovice", "Vepřová plec", "Vepřová panenka", "Vepřová pečeně / kotlet", "Vepřový bůček", "Mleté vepřové maso",
        # Hovězí
        "Hovězí zadní", "Hovězí přední / na guláš", "Hovězí mleté maso", "Hovězí roštěná / steak",
        # Ryby a ostatní
        "Losos (filet)", "Pstruh", "Treska / filé", "Uzené maso", "Slanina / špek", "Klobásy / párky"
    ],
    "🥛 Mléčné výrobky a vejce": [
        "Bílý jogurt / Skyr", "Cihla Eidam / Gouda", "Feta / Balkánský sýr", "Hermelín / Camembert",
        "Máslo", "Mozzarella", "Niva / modrý sýr", "Parmazán / Grana Padano",
        "Smetana ke šlehání (31%+)", "Smetana na vaření (12%)", "Tavený sýr", "Tvaroh (měkký/tvrdý)",
        "Vejce", "Zakysaná smetana", "Zakysané podmáslí / kefír"
    ],
    "🥦 Zelenina, houby a luštěniny": [
        "Brambory", "Brokolice", "Cibule (žlutá/červená)", "Cizrna", "Cuketa",
        "Česnek", "Čočka (červená/hnědá)", "Fazole (v konzervě/suché)", "Jarní cibulka",
        "Květák", "Lilek", "Mražená zeleninová směs", "Mrkev", "Okurka",
        "Paprika", "Petržel / Celer", "Pórek", "Rajčata",
        "Špenát (čerstvý/mražený)", "Žampiony / lesní houby"
    ],
    "🍚 Přílohy": [
        "Vařené brambory", "Bramborová kaše", "Těstoviny (špagety/vřetena...)", "Rýže (jasmínová/basmati)",
        "Houskový knedlík", "Bramborový knedlík", "Hranolky", "Krokety",
        "Kuskus", "Bulgur", "Tarhoňa", "Tortilly", "Pečivo (chléb/housky)"
    ],
    "🥫 Ostatní": [
        "Rajčatové pyré / pasírovaná rajčata", "Rajčata v konzervě (krájená)", "Tuňák v konzervě",
        "Kokosové mléko", "Hořčice (plnotučná/dijonská)", "Kečup", "Sójová omáčka", "Solamyl / škrob",
        "Hladká mouka", "Polohrubá mouka", "Strouhanka", "Med", "Citrónová šťáva", "Olivový olej", "Slunečnicový olej"
    ]
}

KULINARSKE_STYLY = [
    "Tradiční česká",
    "Italská / Středomořská",
    "Asijská (rychlá pánvička)",
    "Mexická",
    "Rychlovky do 30 minut",
    "Pečení z jednoho pekáče",
    "Lehká / Dietnější jídla"
]

PECENI_TYPY_DEZERTY = [
    "Bábovka",
    "Brownies",
    "Bublanina",
    "Buchty",
    "Cheesecake",
    "Cookies / Sušenky",
    "Crumble",
    "Dort",
    "Knedlíky (ovocné / tvarohové)",
    "Koblihy / Šišky",
    "Koláč (křehký)",
    "Koláč (kynutý)",
    "Lívance",
    "Muffiny / Cupcaky",
    "Ovocný koláč",
    "Palačinkový dort / Roláda",
    "Palačinky",
    "Perník",
    "Rolka / Biskupský chlebíček",
    "Štrúdl / Závin",
    "Tiramisu",
    "Tvarohový koláč",
    "Vánoční cukroví",
    "Vdolky",
]

PECENI_OVOCE = [
    "Angrešt",
    "Banány",
    "Borůvky",
    "Broskve / Nektarinky",
    "Brusinkový džem",
    "Citron / Limetka",
    "Datle / Sušené ovoce",
    "Hrušky",
    "Jahody",
    "Jablka",
    "Kiwi",
    "Maliny",
    "Mango",
    "Meruňky",
    "Pomeranč",
    "Rozinky",
    "Rybíz (červený / černý)",
    "Švestky",
    "Třešně / Višně",
]

PECENI_OSTATNI = [
    "Celozrnná mouka",
    "Čokoláda (hořká)",
    "Čokoláda (mléčná)",
    "Čokoládové chips",
    "Droždí",
    "Hladká mouka",
    "Jedlá soda",
    "Jogurt",
    "Kakao",
    "Kešu / Para ořechy",
    "Kokos (strouhaný)",
    "Listové těsto",
    "Lískové ořechy",
    "Mandle (celé / mleté)",
    "Máslo",
    "Med",
    "Mléko",
    "Moučkový cukr",
    "Olej (slunečnicový)",
    "Piškoty",
    "Polohrubá mouka",
    "Prášek do pečiva",
    "Rum / Rumová aroma",
    "Skořice",
    "Smetana ke šlehání",
    "Škrob / Solamyl",
    "Třtinový cukr",
    "Tvaroh (měkký)",
    "Tvaroh (tvrdý)",
    "Vanilkový cukr / extrakt",
    "Vejce",
    "Vlašské ořechy",
    "Zakysaná smetana",
    "Želatina",
]

SMTP_SERVER = "smtp.seznam.cz"
SMTP_PORT = 465
EMAIL_SENDER = "dasajidelnicek@seznam.cz"
EMAIL_RECEIVER = "dady.89@seznam.cz"
EMAIL_PASSWORD = ""

PROMPT_PREHLED_SABLONA = """Jsi šéfkuchař. Navrhni přesně 10 různorodých receptů.
Dostupné ingredience: {suroviny}.
Styl kuchyně: {styl}.
Každý recept připrav na {porce} porcí.
Dbej na variabilitu — různé způsoby přípravy, různé chutě, různé kombinace surovin.

Odpověz POUZE validním JSON polem bez jakéhokoliv dalšího textu nebo markdown formátování.
Každý objekt v poli musí mít přesně tyto klíče:
- "nazev": název jídla (string)
- "popis": krátký popis o co se jedná, cca 3 věty — co to je, z čeho se to dělá a proč to stojí za to uvařit (string)
- "dalsi_ingredience": seznam dalších ingrediencí potřebných nad rámec dostupných (pole stringů, může být prázdné)
- "nutricni_hodnoty": objekt s odhadovanými hodnotami na 1 porci: "kcal" (číslo), "bílkoviny" (string "Xg"), "sacharidy" (string "Xg"), "tuky" (string "Xg")

Formát: [{{"nazev": "...", "popis": "...", "dalsi_ingredience": ["...", "..."], "nutricni_hodnoty": {{"kcal": 450, "bílkoviny": "32g", "sacharidy": "48g", "tuky": "12g"}}}}, ...]"""

PROMPT_DETAIL_SABLONA = """Vytvoř detailní recept pro jídlo: {nazev_jidla}

Dostupné ingredience uživatele: {suroviny}
Styl kuchyně: {styl}
Porce: {porce}

Struktura receptu:
### {nazev_jidla}

**Ingredience** (s přesnými gramážemi):
- ...

**Postup krok za krokem:**
1. ...

**Tipy a triky:**
- ...

**Doba přípravy:** ... min | **Doba vaření/pečení:** ... min

**Výživové hodnoty (na 1 porci):** 🔥 ~XXX kcal | 💪 XXg bílkovin | 🌾 XXg sacharidů | 🫒 XXg tuků"""

PROMPT_PREHLED_PECENI_SABLONA = """Jsi zkušený cukrář. Navrhni přesně 10 různorodých receptů na sladké pečení.
Typ dezertu / pečiva: {typ_dezertu}.
Dostupné ovoce: {ovoce}.
Ostatní dostupné suroviny: {ostatni}.
Dbej na variabilitu — různé postupy, textury, chutě a kombinace surovin.

Odpověz POUZE validním JSON polem bez jakéhokoliv dalšího textu nebo markdown formátování.
Každý objekt v poli musí mít přesně tyto klíče:
- "nazev": název dezertu (string)
- "popis": krátký popis o co se jedná, cca 3 věty — co to je, z čeho se to dělá a proč to stojí za to upéct (string)
- "dalsi_ingredience": seznam dalších ingrediencí potřebných nad rámec dostupných (pole stringů, může být prázdné)
- "nutricni_hodnoty": objekt s odhadovanými hodnotami na 1 kus / porci: "kcal" (číslo), "bílkoviny" (string "Xg"), "sacharidy" (string "Xg"), "tuky" (string "Xg")

Formát: [{{"nazev": "...", "popis": "...", "dalsi_ingredience": ["...", "..."], "nutricni_hodnoty": {{"kcal": 250, "bílkoviny": "5g", "sacharidy": "35g", "tuky": "10g"}}}}, ...]"""

PROMPT_DETAIL_PECENI_SABLONA = """Vytvoř detailní recept na dezert: {nazev_jidla}

Typ pečení: {typ_dezertu}
Dostupné ovoce: {ovoce}
Ostatní dostupné suroviny: {ostatni}

Struktura receptu:
### {nazev_jidla}

**Ingredience** (s přesnými gramážemi):
- ...

**Postup krok za krokem:**
1. ...

**Tipy a triky:**
- ...

**Doba přípravy:** ... min | **Doba pečení:** ... min

**Výživové hodnoty (na 1 kus / porci):** 🔥 ~XXX kcal | 💪 XXg bílkovin | 🌾 XXg sacharidů | 🫒 XXg tuků"""
