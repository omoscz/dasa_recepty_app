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


MODELY = ["gemini-2.5-flash-lite", "gemini-2.5-flash"]


def generuj_z_ai(prompt):
    if "GEMINI_KEY" not in st.secrets:
        st.error("V Secrets chybí proměnná GEMINI_KEY!")
        return None

    klient = genai.Client(api_key=st.secrets["GEMINI_KEY"])
    for model in MODELY:
        try:
            response = klient.models.generate_content(model=model, contents=prompt)
            return response.text
        except errors.APIError as e:
            if e.code == 403:
                st.error("⚠️ API klíč je neplatný. Zkontroluj nastavení Secrets.")
                return None
            else:
                st.warning(f"⚠️ Přepínám na záložní model... [{e.code}]")

    st.error("❌ Všechny modely selhaly. Zkus to prosím za chvíli.")
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


def _bold(text):
    return re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)


def markdown_na_html(text):
    html = []
    in_ul = False
    in_ol = False

    def zavri_listy():
        nonlocal in_ul, in_ol
        if in_ul:
            html.append("</ul>")
            in_ul = False
        if in_ol:
            html.append("</ol>")
            in_ol = False

    for line in text.split("\n"):
        s = line.strip()

        if not s:
            zavri_listy()
            continue

        if s.startswith("### "):
            zavri_listy()
            html.append(
                f'<h3 style="color:#2e7d32;margin:20px 0 6px;border-bottom:1px solid #eee;padding-bottom:4px">'
                f"{_bold(s[4:])}</h3>"
            )
        elif s.startswith("## "):
            zavri_listy()
            html.append(
                f'<h2 style="color:#1a5276;margin:24px 0 8px">{_bold(s[3:])}</h2>'
            )
        elif re.match(r"^\d+\.\s", s):
            if in_ul:
                html.append("</ul>")
                in_ul = False
            if not in_ol:
                html.append('<ol style="padding-left:22px;margin:6px 0">')
                in_ol = True
            content = re.sub(r"^\d+\.\s", "", s)
            html.append(f'<li style="margin:4px 0">{_bold(content)}</li>')
        elif s.startswith("* ") or s.startswith("- "):
            if in_ol:
                html.append("</ol>")
                in_ol = False
            if not in_ul:
                html.append('<ul style="padding-left:20px;margin:6px 0">')
                in_ul = True
            html.append(f'<li style="margin:4px 0">{_bold(s[2:])}</li>')
        else:
            zavri_listy()
            html.append(f'<p style="margin:6px 0">{_bold(s)}</p>')

    zavri_listy()
    return "\n".join(html)


def odesli_email(predmet, obsah_md):
    odesilatel = config.EMAIL_SENDER
    heslo = st.secrets.get("EMAIL_PASSWORD", config.EMAIL_PASSWORD)
    prijemce = config.EMAIL_RECEIVER

    html_telo = f"""
    <html>
      <body style="font-family:Arial,sans-serif;color:#333333;line-height:1.65;background:#f9f9f9">
        <div style="max-width:600px;margin:0 auto;padding:28px 24px;
                    background:#ffffff;border:1px solid #dddddd;border-radius:10px">
          {markdown_na_html(obsah_md)}
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
            if st.checkbox(polozka, key=f"surovina_{kategorie}_{polozka}"):
                vybrane_suroviny.append(polozka)

# 2. Výběr stylu
st.subheader("2. Na jakou kuchyni máte chuť?")
vybrane_styly = []
with st.expander("🌍 Vybrat kulinářský styl / styl vaření"):
    for styl in config.KULINARSKE_STYLY:
        if st.checkbox(styl, key=f"styl_{styl}"):
            vybrane_styly.append(styl)

# 3. Počet porcí
st.subheader("3. Pro kolik porcí vařit?")
pocet_porci = st.slider("Počet porcí", min_value=1, max_value=12, value=6)

# 4. Generování přehledu 5 receptů
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
                porce=pocet_porci,
            )
            vysledek = generuj_z_ai(prompt)

            if vysledek:
                recepty = parsuj_recepty_json(vysledek)
                if recepty:
                    st.session_state["prehled_receptu"] = recepty
                    st.session_state["vybrane_suroviny"] = suroviny_str
                    st.session_state["vybrane_styly"] = styl_str
                    st.session_state["pocet_porci"] = pocet_porci
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

        nutri = recept.get("nutricni_hodnoty", {})
        if nutri:
            st.markdown(
                f"🔥 **{nutri.get('kcal', '?')} kcal** &nbsp;|&nbsp; "
                f"💪 **{nutri.get('bílkoviny', '?')} bílkovin** &nbsp;|&nbsp; "
                f"🌾 **{nutri.get('sacharidy', '?')} sacharidů** &nbsp;|&nbsp; "
                f"🫒 **{nutri.get('tuky', '?')} tuků**",
                unsafe_allow_html=True
            )

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
                            porce=st.session_state.get("pocet_porci", 6),
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
