import streamlit as st
import smtplib
import json
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai
from google.genai import errors

import config

st.set_page_config(page_title="Dáša Recepty App", page_icon="🍳", layout="centered")


# --- ROTACE API KLÍČŮ ---
def získej_gemini_client():
    if "GEMINI_KEYS" not in st.secrets:
        st.error("V Secrets chybí proměnná GEMINI_KEYS!")
        return None

    for i, klic in enumerate(st.secrets["GEMINI_KEYS"]):
        try:
            klient = genai.Client(api_key=klic)
            klient.models.generate_content(model="gemini-2.5-flash", contents="ping")
            return klient
        except errors.APIError as e:
            if e.code == 429:
                st.warning(f"⚠️ API klíč č. {i + 1} je vyčerpaný (Limit 429). Přepínám na záložní...")
            else:
                st.error(f"Chyba u API klíče č. {i + 1}: {e}")

    st.error("❌ Všechny dostupné API klíče byly pro dnešek vyčerpány!")
    return None


def generuj_z_ai(prompt):
    klient = získej_gemini_client()
    if not klient:
        return None
    try:
        response = klient.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return response.text
    except errors.APIError as e:
        st.error(f"Chyba při generování obsahu: {e}")
    return None


def parsuj_recepty_json(text):
    # Odstraníme markdown code fences pokud jsou přítomny
    text = re.sub(r"```(?:json)?\s*", "", text).strip()
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    return None


def odesli_email(predmet, obsah_md):
    odesilatel = config.EMAIL_SENDER
    heslo = st.secrets.get("EMAIL_PASSWORD", config.EMAIL_PASSWORD)
    prijemce = config.EMAIL_RECEIVER

    # Převod markdownu na čitelné HTML
    html_obsah = obsah_md.replace("\n", "<br>")

    html_telo = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333333; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;
                    border: 1px solid #dddddd; border-radius: 8px;">
          {html_obsah}
        </div>
      </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = predmet
    msg["From"] = odesilatel
    msg["To"] = prijemce
    msg.attach(MIMEText(html_telo, "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.login(odesilatel, heslo)
            server.sendmail(odesilatel, prijemce, msg.as_string())
        return True
    except Exception as e:
        st.error(f"E-mail se nepodařilo odeslat: {e}")
        return False


# --- UI ---
st.title("🍳 Rodinné recepty pro Dášu")
st.write("Vyber akční suroviny a styl, vygeneruj návrhy jídel a pošli oblíbený recept na e-mail.")

# 1. Výběr surovin
st.subheader("1. Co máme v akci / v lednici?")
vybrane_suroviny = []
for kategorie, polozky in config.SUROVINY_KATALOG.items():
    with st.expander(kategorie):
        for polozka in polozky:
            if st.checkbox(polozka, key=f"surovina_{polozka}"):
                vybrane_suroviny.append(polozka)

# 2. Výběr stylu
st.subheader("2. Na jakou kuchyni máte chuť?")
vybrane_styly = []
with st.expander("🌍 Vybrat kulinářský styl / styl vaření"):
    for styl in config.KULINARSKE_STYLY:
        if st.checkbox(styl, key=f"styl_{styl}"):
            vybrane_styly.append(styl)

# 3. Generování přehledu 5 receptů
if st.button("🚀 Vygenerovat návrhy jídel", type="primary"):
    if not vybrane_suroviny:
        st.warning("Vyber prosím alespoň jednu surovinu!")
    else:
        with st.spinner("AI šéfkuchař vymýšlí menu..."):
            suroviny_str = ", ".join(vybrane_suroviny)
            styl_str = ", ".join(vybrane_styly) if vybrane_styly else "libovolný pestrý mix"

            prompt = config.PROMPT_PREHLED_SABLONA.format(
                suroviny=suroviny_str,
                styl=styl_str,
            )
            vysledek = generuj_z_ai(prompt)

            if vysledek:
                recepty = parsuj_recepty_json(vysledek)
                if recepty:
                    st.session_state["prehled_receptu"] = recepty
                    st.session_state["vybrane_suroviny"] = suroviny_str
                    st.session_state["vybrane_styly"] = styl_str
                    # Reset detailů a zobrazených karet při novém generování
                    st.session_state.pop("detail_receptu", None)
                    st.session_state["zobrazene_detaily"] = []
                else:
                    st.error("Nepodařilo se zpracovat odpověď AI. Zkus to prosím znovu.")

# 4. Zobrazení přehledu 5 receptů
if "prehled_receptu" in st.session_state:
    st.success("✨ Tady je 5 návrhů jídel — klikni na recept pro zobrazení detailu:")
    st.write("---")

    if "detail_receptu" not in st.session_state:
        st.session_state["detail_receptu"] = {}
    if "zobrazene_detaily" not in st.session_state:
        st.session_state["zobrazene_detaily"] = []

    for i, recept in enumerate(st.session_state["prehled_receptu"]):
        nazev = recept.get("nazev", f"Recept {i + 1}")
        popis = recept.get("popis", "")
        dalsi = recept.get("dalsi_ingredience", [])

        st.markdown(f"### {i + 1}. {nazev}")
        st.write(popis)

        if dalsi:
            st.caption(f"🛒 Další potřebné ingredience: {', '.join(dalsi)}")
        else:
            st.caption("✅ Vystačíš si s vybranými surovinami!")

        # Tlačítko pro zobrazení detailu
        if i not in st.session_state["zobrazene_detaily"]:
            if st.button(f"📖 Zobrazit celý recept", key=f"detail_btn_{i}"):
                st.session_state["zobrazene_detaily"].append(i)
                if i not in st.session_state["detail_receptu"]:
                    with st.spinner(f"Generuji detailní recept pro '{nazev}'..."):
                        prompt_detail = config.PROMPT_DETAIL_SABLONA.format(
                            nazev_jidla=nazev,
                            suroviny=st.session_state.get("vybrane_suroviny", ""),
                            styl=st.session_state.get("vybrane_styly", ""),
                        )
                        detail = generuj_z_ai(prompt_detail)
                        if detail:
                            st.session_state["detail_receptu"][i] = detail

        # Zobrazení detailu receptu
        if i in st.session_state["zobrazene_detaily"] and i in st.session_state["detail_receptu"]:
            with st.expander(f"📋 {nazev} — celý recept", expanded=True):
                st.markdown(st.session_state["detail_receptu"][i])

                st.write("---")
                if st.button(f"✉️ Odeslat tento recept na e-mail", key=f"email_btn_{i}"):
                    with st.spinner("Odesílám e-mail..."):
                        uspech = odesli_email(
                            f"🍳 Recept: {nazev}",
                            st.session_state["detail_receptu"][i],
                        )
                        if uspech:
                            st.balloons()
                            st.success("🎉 Recept byl úspěšně odeslán na e-mail!")

        st.write("---")
