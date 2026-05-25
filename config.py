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
        "Vejce", "Máslo", "Cihla Eidam / Gouda", "Hermelín / Camembert", "Niva / modrý sýr", "Mozzarella",
        "Parmazán / Grana Padano", "Tvaroh (měkký/tvrdý)", "Smetana na vaření (12%)", "Smetana ke šlehání (31%+)",
        "Zakysaná smetana", "Bílý jogurt / Skyr", "Zakysané podmáslí / kefír", "Tavený sýr", "Feta / Balkánský sýr"
    ],
    "🥦 Zelenina, houby a luštěniny": [
        "Cibule (žlutá/červená)", "Česnek", "Brambory", "Mrkev", "Petržel / Celer", "Rajčata", "Paprika",
        "Okurka", "Cuketa", "Lilek", "Brokolice", "Květák", "Špenát (čerstvý/mražený)", "Pórek", "Jarní cibulka",
        "Žampiony / lesní houby", "Mražená zeleninová směs", "Fazole (v konzervě/suché)", "Čočka (červená/hnědá)", "Cizrna"
    ],
    "🍚 Přílohy": [
        "Těstoviny (špagety/vřetena...)", "Rýže (jasmínová/basmati)", "Knoflíky / houskový knedlík",
        "Bramborový knedlík", "Kuskus", "Bulgur", "Tarhoňa", "Tortilly", "Pečivo (chléb/housky)"
    ],
    "🥫 Ostatní zásoby a špajz": [
        "Rajčatové pyré / pasírovaná rajčata", "Rajčata v konzervě (krájená)", "Tuňák v konzervě",
        "Kokosové mléko", "Hořčice (plnotučná/dijonská)", "Kečup", "Sójová omáčka", "Solamyl / škrob",
        "Hladká mouka", "Polohrubá mouka", "Strouhanka", "Med", "Citrónová šťáva", "Olivový olej", "Slunečnicový olej"
    ]
}

KULINARSKE_STYLY = [
    "Pestrý mix (nechat na AI)",
    "Tradiční česká",
    "Italská / Středomořská",
    "Asijská (rychlá pánvička)",
    "Mexická",
    "Rychlovky do 30 minut",
    "Pečení z jednoho pekáče",
    "Lehká / Dietnější jídla"
]

SMTP_SERVER = "smtp.seznam.cz"
SMTP_PORT = 465
EMAIL_SENDER = "dasajidelnicek@seznam.cz"
EMAIL_RECEIVER = "omos@email.cz"
EMAIL_PASSWORD = ""

# Prompt pro přehled 5 receptů – vrací čisté JSON pole
PROMPT_PREHLED_SABLONA = """Jsi šéfkuchař. Navrhni přesně 5 receptů pro 4člennou rodinu (2 dospělí + 2 děti).
Dostupné ingredience: {suroviny}.
Styl kuchyně: {styl}.
Porce uprav tak, aby zbyly 2-3 porce na obědy do práce (cca 6 porcí celkem).

Odpověz POUZE validním JSON polem bez jakéhokoliv dalšího textu nebo markdown formátování.
Každý objekt v poli musí mít přesně tyto klíče:
- "nazev": název jídla (string)
- "popis": krátký popis o co se jedná, cca 3 věty — co to je, z čeho se to dělá a proč to stojí za to uvařit (string)
- "dalsi_ingredience": seznam dalších ingrediencí potřebných nad rámec dostupných (pole stringů, může být prázdné)

Formát: [{{"nazev": "...", "popis": "...", "dalsi_ingredience": ["...", "..."]}}, ...]"""

# Prompt pro detailní recept jednoho konkrétního jídla
PROMPT_DETAIL_SABLONA = """Vytvoř detailní recept pro jídlo: {nazev_jidla}

Dostupné ingredience uživatele: {suroviny}
Styl kuchyně: {styl}
Porce: pro 4 osoby + 2-3 porce na obědy (celkem cca 6 porcí)

Struktura receptu:
### {nazev_jidla}

**Ingredience** (s přesnými gramážemi):
- ...

**Postup krok za krokem:**
1. ...

**Tipy a triky:**
- ...

**Doba přípravy:** ... min | **Doba vaření/pečení:** ... min"""
