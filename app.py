import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai
from config import (
    GEMINI_API_KEY, AVAILABLE_INGREDIENTS, AVAILABLE_STYLES, FAMILY_PREFERENCES, 
    AI_MENU_PROMPT_TEMPLATE, AI_DETAIL_PROMPT_TEMPLATE,
    SMTP_SERVER, SMTP_PORT, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER
)

# --- INICIALIZACE GOOGLE GENAI KLIENTA ---
client = genai.Client(api_key=GEMINI_API_KEY)

# --- FUNKCE PRO ODESLÁNÍ E-MAILU (S PODPOROU HTML FORMÁTOVÁNÍ) ---
def odesli_recept_na_mail(nazev, text_receptu):
    """Odešle jeden konkrétní detailní recept zformátovaný do hezkého HTML."""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = f"🍳 Recept: {nazev}"
    
    # --- RYCHLÝ PŘEVOD MARKDOWNU NA HEZKÉ HTML ---
    html_recept = text_receptu
    
    # 1. Převedeme odřádkování na HTML řádky
    html_recept = html_recept.replace("\n", "<br>")
    
    # 2. Převedeme hlavní nadpisy (např. ## Postup krok za krokem)
    while "## " in html_recept:
        html_recept = html_recept.replace("## ", "<h2 style='color: #2c3e50; margin-top: 20px; border-bottom: 2px solid #ecf0f1; padding-bottom: 5px;'>", 1)
        if "<br>" in html_recept:
            html_recept = html_recept.replace("<br>", "</h2>", 1)
            
    # 3. Převedeme podnadpisy (### 1. Příprava kuřete...)
    while "### " in html_recept:
        html_recept = html_recept.replace("### ", "<h3 style='color: #16a085; margin-top: 15px;'>", 1)
        if "<br>" in html_recept:
            html_recept = html_recept.replace("<br>", "</h3>", 1)
            
    # 4. Převedeme tučné písmo (**text**) na <strong>text</strong>
    while "**" in html_recept:
        html_recept = html_recept.replace("**", "<strong>", 1)
        html_recept = html_recept.replace("**", "</strong>", 1)
        
    # 5. Převedeme odrážky na čistější formát
    html_recept = html_recept.replace("<br>* ", "<br>• ")
    html_recept = html_recept.replace("<br>- ", "<br>• ")

    # Sestavíme kompletní HTML šablonu mailu s moderním designem
    html_telo = f"""
    <html>
    <body style="font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #333333; line-height: 1.6; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid #16a085; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 16px; font-weight: bold; color: #2c3e50;">Ahoj, posílám vybraný recept z aplikace Dáša Recepty! 🍳</p>
        </div>
        
        <div style="background-color: #ffffff; padding: 10px;">
            {html_recept}
        </div>
        
        <hr style="border: 0; border-top: 1px solid #eeeeee; margin-top: 30px;">
        <p style="font-size: 12px; color: #7f8c8d; text-align: center;">Odesláno z vaší rodinné kuchyňské aplikace.</p>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(html_telo, 'html', 'utf-8'))
    
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Chyba při odesílání e-mailu: {e}")
        return False

# --- NASTAVENÍ STRÁNKY (Design pro mobil) ---
st.set_page_config(
    page_title="Dáša Recepty App",
    page_icon="🍳",
    layout="centered"
)

# --- PAMĚŤ APLIKACE (Session State) ---
if "vygenerovane_menu" not in st.session_state:
    st.session_state.vygenerovane_menu = None
if "zobrazene_detaily" not in st.session_state:
    st.session_state.zobrazene_detaily = {}

# --- GRAFICKÉ ROZHRANÍ ---
st.title("🍳 Dáša Recepty App")
st.write("Zaškrtněte akční suroviny a případně zvolte kulinářský styl. Dáša podle toho sestaví vyvážené rodinné menu.")

st.divider()

# 1. KROK: Výběr surovin podle kategorií schovaný v expanderech
st.subheader("🛒 Výběr surovin a akcí")
vsechny_vybrane_suroviny = []

for kategoria, polozky in AVAILABLE_INGREDIENTS.items():
    with st.expander(kategoria, expanded=(kategoria.startswith("🥩"))):
        vyber = st.multiselect(
            f"Vyberte z kategorie {kategoria}:",
            options=polozky,
            key=f"sec_{kategoria}",
            placeholder="Klikněte pro výběr..."
        )
        vsechny_vybrane_suroviny.extend(vyber)

# NOVINKA: Volitelný výběr kulinářského stylu
with st.expander("🌍 Kulinářský styl / Typ kuchyně (Volitelné)"):
    vybrany_styl = st.selectbox(
        "Chcete jídelníček zaměřit na konkrétní směr?",
        options=["Nespecifikováno (Dáša vybere pestrý mix)"] + AVAILABLE_STYLES,
        index=0
    )

st.divider()

# 2. KROK: Tlačítko pro vygenerování hlavního přehledu
if st.button("🪄 Vygenerovat akční jídelníček", type="primary", use_container_width=True):
    if not vsechny_vybrane_suroviny:
        st.warning("Před spuštěním prosím vyberte alespoň jednu surovinu.")
    else:
        with st.spinner("Dáša studuje suroviny a skládá 5 rodinných receptů..."):
            try:
                suroviny_pro_ai = "\n".join([f"- {s}" for s in vsechny_vybrane_suroviny])
                styl_pro_ai = vybrany_styl if vybrany_styl != "Nespecifikováno (Dáša vybere pestrý mix)" else "Pestrý rodinný mix (česká/evropská klasika)"
                
                prompt = AI_MENU_PROMPT_TEMPLATE.format(
                    pocet_osob=FAMILY_PREFERENCES["pocet_osob"],
                    styl_vareni=FAMILY_PREFERENCES["styl_vareni"],
                    omezeni_a_alergie=FAMILY_PREFERENCES["omezeni_a_alergie"],
                    vybrane_suroviny=suroviny_pro_ai,
                    preferovany_styl=styl_pro_ai
                )
                
                try:
                    odpoved = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                    )
                except Exception as model_error:
                    if "503" in str(model_error) or "UNAVAILABLE" in str(model_error):
                        st.info("Primární model je momentálně vytížený, zkouším záložní model...")
                        odpoved = client.models.generate_content(
                            model='gemini-2.5-flash-8b',
                            contents=prompt,
                        )
                    else:
                        raise model_error
                
                st.session_state.vygenerovane_menu = odpoved.text.strip()
                st.session_state.zobrazene_detaily = {}
                
            except Exception as e:
                st.error(f"Chyba při komunikaci s AI: {e}")

# --- 3. KROK: INTERAKTIVNÍ VYKRESLENÍ A TLAČÍTKA DETAILŮ ---
if st.session_state.vygenerovane_menu:
    st.subheader("💡 Návrh receptů na tento týden")
    
    suprove_rozdeleni = st.session_state.vygenerovane_menu.split("###")
    
    uvod_text = suprove_rozdeleni[0].strip()
    if uvod_text:
        st.markdown(uvod_text)
        
    for index, jidlo_blok in enumerate(suprove_rozdeleni[1:]):
        jidlo_clean = jidlo_blok.strip()
        if not jidlo_clean:
            continue
            
        if jidlo_clean.endswith("---"):
            jidlo_clean = jidlo_clean[:-3].strip()
            
        st.markdown(f"### {jidlo_clean}")
        
        nazev_jidla = jidlo_clean.split("\n")[0].strip()
        
        button_key = f"detail_{index}"
        email_key = f"email_{index}"
        
        if st.button(f"📖 Zobrazit detailní postup pro: {nazev_jidla}", key=button_key, use_container_width=True):
            if button_key not in st.session_state.zobrazene_detaily:
                with st.spinner(f"Dáša rozepisuje recept na {nazev_jidla}..."):
                    try:
                        detail_prompt = AI_DETAIL_PROMPT_TEMPLATE.format(
                            nazev_jidla=nazev_jidla,
                            pocet_osob=FAMILY_PREFERENCES["pocet_osob"],
                            styl_vareni=FAMILY_PREFERENCES["styl_vareni"],
                            omezeni_a_alergie=FAMILY_PREFERENCES["omezeni_a_alergie"]
                        )
                        
                        try:
                            detail_odpoved = client.models.generate_content(
                                model='gemini-2.5-flash',
                                contents=detail_prompt,
                            )
                        except Exception as detail_model_error:
                            if "503" in str(detail_model_error) or "UNAVAILABLE" in str(detail_model_error):
                                detail_odpoved = client.models.generate_content(
                                    model='gemini-2.5-flash-8b',
                                    contents=detail_prompt,
                                )
                            else:
                                raise detail_model_error
                                
                        st.session_state.zobrazene_detaily[button_key] = detail_odpoved.text.strip()
                    except Exception as e:
                        st.error(f"Nepodařilo se vygenerovat detail receptu: {e}")
        
        if button_key in st.session_state.zobrazene_detaily:
            st.info(st.session_state.zobrazene_detaily[button_key])
            
            if st.button(f"📧 Poslat tento recept na e-mail", key=email_key, use_container_width=True):
                with st.spinner("Odesílám e-mail..."):
                    uspech = odesli_recept_na_mail(nazev_jidla, st.session_state.zobrazene_detaily[button_key])
                    if uspech:
                        st.success(f"Recept na '{nazev_jidla}' byl úspěšně odeslán!")
            
        st.divider()