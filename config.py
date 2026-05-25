# config.py

SUROVINY_KATALOG = {
    "🥩 Masa a ryby": ["Kuřecí prsa", "Vepřová krkovice", "Mleté maso", "Hovězí zadní", "Losos", "Uzené maso"],
    "🥛 Mléčné výrobky a vejce": ["Cihla eidam", "Mozzarella", "Tvaroh", "Smetana ke šlehání", "Vejce", "Máslo"],
    "🥦 Zelenina a přílohy": ["Brambory", "Rýže", "Těstoviny", "Brokolice", "Mrkev", "Cibule", "Rajčata", "Paprika"],
    "🥫 Ostatní zásoby": ["Rajčatové pyré", "Tuna v konzervě", "Fazole", "Kokosové mléko", "Olivový olej"]
}

KULINARSKE_STYLY = [
    "Pestrý mix (nechat na AI)",
    "Tradiční česká",
    "Italská / Středomořská",
    "Asijská (rychlá pánvička)",
    "Mexická",
    "Rychlovky do 30 minut"
]

SMTP_SERVER = "smtp.seznam.cz"
SMTP_PORT = 465
EMAIL_SENDER = "tvoj-email@seznam.cz"  # Sem dej svůj odesílací e-mail
EMAIL_RECEIVER = "cilovy-email@seznam.cz"  # Sem dej e-mail, kam to má chodit

# Tady máš schované ty šablony pro AI
PROMPT_MENU_SABLONA = """Jsi šéfkuchař. Navrhni týdenní menu pro 4člennou rodinu (2 dospělí + 2 děti) z těchto akčních surovin: {suroviny}. 
Styl kuchyně: {styl}.
Uprav gramáže tak, aby zbyly 2-3 porce na obědy do práce.
Napiš jen seznam jídel, u každého jídla použij nadpis s třemi křížky (např. ### 1. Jídlo)."""

PROMPT_DETAIL_SABLONA = """K tomuto menu vytvoř detailní recepty s ingrediencemi a postupem:
{menu}
U každého receptu zachovej nadpis s třemi křížky (###), aby to aplikace uměla přečíst."""