import streamlit as st
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai
from google.genai import errors

# Importujeme konfiguraci z config.py
import config

st.set_page_config(page_title="Dáša Recepty App", page_icon="🍳", layout="centered")

# --- POMOCNÁ FUNKCE PRO ROTACI API KLÍČŮ ---
def získej_gemini_client():
    """
    Projede seznam klíčů v st.secrets a vrátí funkčního klienta.
    Pokud klíč selže na limit 429, zkusí další.
    """
    if "GEMINI_KEYS" not in st.secrets:
        st.error("V Secrets chybí proměnná GEMINI_KEYS!")
        return None

    seznam_klicu = st.secrets["GEMINI_KEYS"]
    
    for i, klic in enumerate(seznam_klicu):
        try:
            # Zkusíme vytvořit klienta a poslat cvičný mini-dotaz pro ověření kvóty
            klient = genai.Client(api_key=klic)
            # Použijeme nejmenší model jen na rychlé ověření, zda klíč žije
            klient.models.generate_content(
                model='gemini-2.5-flash-8b',
                contents='ping',
            )
            # Pokud ping prošel, klíč je v pořádku a vracíme klienta
            return klient
        except errors.APIError as e:
            if e.code == 429:
                # Klíč je vyčerpaný, vypíšeme varování a smyčka zkusí další klíč
                st.warning(f"⚠️ API klíč č. {i+1} je vyčerpaný (Limit 429). Přepínám na záložní...")
                continue
            else:
                st.error(f"Chyba u API klíče č. {i+1}: {e}")
                continue
                
    st.error("❌ Všechny dostupné API klíče byly pro dnešek vyčerpány!")
    return None

# --- AI LOGIKA PRO GENEROVÁNÍ ---
def generuj_z_ai(prompt, pouzij_8b=False):
    """
    Zabezpečí vygenerování textu z AI s využitím rotace klíčů a fallbacku modelu.
    """
    klient = získej_gemini_client()
    if not klient:
        return None
        
    # Volba modelu (pokud chceme explicitně 8b, nebo jako fallback)
    hlavni_model = 'gemini-2.5-flash-8b' if pouzij_8b else 'gemini-2.5-flash'
    zalozni_model = 'gemini-2.5-flash-8b'
    
    try:
        response = klient.models.generate_content(
            model=hlavni_model,
            contents=prompt,
        )
        return response.text
    except errors.APIError as e:
        # Fallback na menší model v rámci funkčního klíče (např. při chybě 503 přetížení)
        if e.code == 503 and hlavni_model != zalozni_model:
            st.info("Hlavní model je přetížený, zkouším úspornější model...")
            try:
                response = klient.models.generate_content(
                    model=zalozni_model,
                    contents=prompt,
                )
                return response.text
            except Exception as e_sub:
                st.error(f"Selhal i záložní model: {e_sub}")
        else:
            st.error(f"Chyba při generování obsahu: {e}")
    return None

# --- LOGIKA PRO ODESÍLÁNÍ E-MAILU ---
def odesli_email(predmet, html_obsah):
    odesilatel = config.EMAIL_SENDER
    heslo = st.secrets.get("EMAIL_PASSWORD", config.EMAIL_PASSWORD)
    prijemce = config.EMAIL_RECEIVER

    msg = MIMEMultipart('alternative')
    msg['Subject'] = predmet
    msg['From'] = odesilatel
    msg['To'] = prijemce

    # Převedeme čistý text na pěkné HTML pro e-mailové klienty
    html_telo = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333333; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #dddddd; border-radius: 8px;">
            {html_obsah.replace('### ', '<h3 style="color: #2e7d32; border-bottom: 1px solid #eeeeee; padding-bottom: 5px; margin-top: 20px;">').replace('###', '').replace('\n', '<br>')}
        </div>
      </body>
    </html>
    """
    
    msg.attach(MIMEText(html_telo, 'html', 'utf-8'))

    try:
        with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.login(odesilatel, heslo)
            server.sendmail(odesilatel, prijemce, msg.as_string())
        return True
    except Exception as e:
        st.error(f"E-mail se nepodařilo odeslat: {e}")
        return False

# --- UŽIVATELSKÉ ROZHRANÍ (STREAMLIT) ---
st.title("🍳 Rodinné recepty pro Dášu")
st.write("Vyber akční suroviny a styl, vygeneruj menu a pošli recepty přímo na e-mail.")

# 1. Výběr surovin podle kategorií
st.subheader("1. Co máme v akci / v lednici?")

vybrane_suroviny = []
for kategorie, polozky in config.SUROVINY_KATALOG.items():
    with st.expander(kategorie):
        for polozka in polozky:
            if st.checkbox(polozka, key=f"surovina_{polozka}"):
                vybrane_suroviny.append(polozka)

# 2. Výběr kulinářského stylu (předěláno na checkboxy)
st.subheader("2. Na jakou kuchyni máte chuť?")
vybrane_styly = []

for styl in config.KULINARSKE_STYLY:
    if st.checkbox(styl, key=f"styl_{styl}"):
        vybrane_styly.append(styl)

# 3. Tlačítko pro generování jídelníčku
if st.button("🚀 Vygenerovat návrhy jídel", type="primary"):
    if not vybrane_suroviny:
        st.warning("Vyber prosím alespoň jednu surovinu!")
    else:
        with st.spinner("AI šéfkuchař vymýšlí menu..."):
            # Sestavení promptu pro menu
            suroviny_str = ", ".join(vybrane_suroviny)
            
            # Pokud nevybere žádný styl, AI udělá pestrý mix
            if vybrane_styly:
                styl_str = ", ".join(vybrane_styly)
            else:
                styl_str = "libovolný pestrý mix (zkombinuj styly podle chuti)"
            
            prompt_menu = config.PROMPT_MENU_SABLONA.format(
                suroviny=suroviny_str,
                styl=styl_str
            )
            
            vysledek_menu = generuj_z_ai(prompt_menu)
            
            if vysledek_menu:
                st.session_state["navrhnute_menu"] = vysledek_menu
                # Vymažeme staré recepty, aby se nenačítaly z minula
                if "vygenerovany_recept" in st.session_state:
                    del st.session_state["vygenerovany_recept"]

# Zobrazení návrhů jídel, pokud existují
if "navrhnute_menu" in st.session_state:
    st.success("✨ Návrh jídelníčku je připraven!")
    st.markdown(st.session_state["navrhnute_menu"])
    
    st.write("---")
    st.subheader("3. Chceš vygenerovat a poslat kompletní recepty?")
    st.write("Pokud se ti menu líbí, kliknutím níže AI připraví detailní postupy a odešle je na e-mail.")
    
    if st.button("✉️ Vygenerovat recepty a odeslat na e-mail"):
        with st.spinner("Generuji detailní postupy and posílám e-mail..."):
            prompt_recepty = config.PROMPT_DETAIL_SABLONA.format(
                menu=st.session_state["navrhnute_menu"]
            )
            
            vysledek_recepty = generuj_z_ai(prompt_recepty)
            
            if vysledek_recepty:
                st.session_state["vygenerovany_recept"] = vysledek_recepty
                
                # Odeslání na e-mail
                uspech = odesli_email("🍳 Nové recepty na tento týden!", vysledek_recepty)
                if uspech:
                    st.balloons()
                    st.success("🎉 Recepty byly úspěšně vygenerovány a odeslány na rodinný e-mail!")
                    
# Zobrazení detailů receptů na stránce pro kontrolu
if "vygenerovany_recept" in st.session_state:
    with st.expander("👀 Zobrazit detail odeslaných receptů přímo zde"):
        st.markdown(st.session_state["vygenerovany_recept"])