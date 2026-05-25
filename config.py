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
EMAIL_SENDER = "tvoj-email@seznam.cz"  # Sem doplň svůj odesílací e-mail, pokud tam ještě není
EMAIL_RECEIVER = "cilovy-email@seznam.cz"  # Sem doplň cílový e-mail pro Dášu

# Šablony promptů upravené pro robustnější parsování
PROMPT_MENU_SABLONA = """Jsi šéfkuchař. Navrhni týdenní menu pro 4člennou rodinu (2 dospělí + 2 děti) z těchto akčních surovin: {suroviny}. 
Styl kuchyně: {styl}.
Uprav gramáže tak, aby zbyly 2-3 porce na obědy do práce.
Napiš jen seznam jídel, u každého jídla použij nadpis s třemi křížky (např. ### 1. Jídlo)."""

PROMPT_DETAIL_SABLONA = """K tomuto menu vytvoř detailní recepty s ingrediencemi a postupem:
{menu}
U každého receptu zachovej nadpis s třemi křížky (###), aby to aplikace uměla přečíst."""