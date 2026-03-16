import streamlit as st
import anthropic

# ── CONFIG ────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Estella", page_icon="✦", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Jost:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Jost', sans-serif;
    background-color: #FAF7F2;
    color: #2C2416;
}
.estella-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.2rem;
    font-weight: 300;
    letter-spacing: 0.18em;
    color: #2C2416;
    text-align: center;
    line-height: 1;
    margin-bottom: 0;
}
.estella-tagline {
    font-size: 0.72rem;
    font-weight: 300;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #9C8A6E;
    text-align: center;
    margin-top: 8px;
    margin-bottom: 2rem;
}
.gold-divider {
    height: 1px;
    background: linear-gradient(to right, transparent, #C9A84C, transparent);
    margin: 1.5rem auto;
    width: 60%;
}
.step-label {
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #9C8A6E;
    text-align: center;
    margin-bottom: 1.5rem;
}
.question-card {
    background: #FFFDF8;
    border: 0.5px solid #E8DFC8;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
}
.question-number {
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #C9A84C;
    margin-bottom: 6px;
}
.question-text {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.25rem;
    font-weight: 400;
    color: #2C2416;
    line-height: 1.5;
    margin-bottom: 4px;
}
.question-hint {
    font-size: 0.78rem;
    font-weight: 300;
    color: #9C8A6E;
    font-style: italic;
    line-height: 1.5;
}
.reading-section {
    background: #FFFDF8;
    border: 0.5px solid #E8DFC8;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}
.reading-section-label {
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #C9A84C;
    margin-bottom: 8px;
}
.reading-body {
    font-size: 0.92rem;
    font-weight: 300;
    line-height: 1.9;
    color: #3A2E1E;
}
.profile-badge {
    display: inline-block;
    background: #F5EDD8;
    border: 0.5px solid #C9A84C;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    color: #7A5C1E;
    margin: 3px;
}
.chat-user {
    background: #F0EBE0;
    border-radius: 16px 16px 4px 16px;
    padding: 10px 16px;
    margin: 8px 0 8px auto;
    font-size: 0.88rem;
    line-height: 1.6;
    max-width: 82%;
    color: #2C2416;
}
.chat-estella {
    background: #FFFDF8;
    border: 0.5px solid #E8DFC8;
    border-radius: 16px 16px 16px 4px;
    padding: 12px 16px;
    margin: 8px auto 8px 0;
    font-size: 0.88rem;
    font-weight: 300;
    line-height: 1.9;
    max-width: 82%;
    color: #2C2416;
}
.estella-signature {
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.85rem;
    font-style: italic;
    color: #9C8A6E;
    margin-top: 6px;
}
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] > div,
div[data-testid="stTextArea"] textarea {
    background: #FFFDF8 !important;
    border: 0.5px solid #D4C5A9 !important;
    border-radius: 8px !important;
    font-family: 'Jost', sans-serif !important;
    font-weight: 300 !important;
    color: #2C2416 !important;
}
div[data-testid="stButton"] button {
    background: #2C2416 !important;
    color: #FAF7F2 !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'Jost', sans-serif !important;
    font-weight: 400 !important;
    letter-spacing: 0.14em !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
}
div[data-testid="stButton"] button:hover {
    background: #C9A84C !important;
    color: #2C2416 !important;
}
</style>
""", unsafe_allow_html=True)


# ── CONSTANTS ─────────────────────────────────────────────────────────────────

HD_TYPES = {
    "Generator":            {"strategy": "To Respond",              "work_style": "sustained energy, mastery through response"},
    "Manifesting Generator":{"strategy": "To Respond then Inform",  "work_style": "multi-passionate, fast-moving, built for variety"},
    "Projector":            {"strategy": "To Wait for Invitation",  "work_style": "guides and directs others, needs recognition"},
    "Manifestor":           {"strategy": "To Inform",               "work_style": "initiates independently, here to create impact"},
    "Reflector":            {"strategy": "To Wait a Lunar Cycle",   "work_style": "mirrors the environment, needs consistency"},
}

ASTRO_SIGNS = [
    "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
    "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces",
]

ENNEAGRAM_TYPES = [
    "Not sure yet",
    "Type 1 — The Reformer",   "Type 2 — The Helper",
    "Type 3 — The Achiever",   "Type 4 — The Individualist",
    "Type 5 — The Investigator","Type 6 — The Loyalist",
    "Type 7 — The Enthusiast", "Type 8 — The Challenger",
    "Type 9 — The Peacemaker",
]

ATTACHMENT_STYLES = [
    "Not sure yet",
    "Secure",
    "Anxious / Preoccupied",
    "Avoidant / Dismissive",
    "Fearful / Disorganized",
]

READING_SECTIONS = [
    "THE THROUGH-LINE",
    "YOUR GIFTS",
    "THE SHADOW",
    "YOUR WORK IN THE WORLD",
    "WHAT WANTS TO EMERGE",
    "A NOTE FROM ESTELLA",
]

SYSTEM_PROMPT = """You are Estella — a warm, wise, deeply perceptive guide who synthesizes astrology,
Human Design, numerology, Enneagram, attachment theory, and Ikigai into one coherent, compassionate reading.

Your voice is:
- Warm and nurturing, never clinical or cold
- Wise without being preachy or prescriptive
- Poetic but grounded — you illuminate, you don't mystify
- You treat the person as whole, capable, and already enough
- You find the through-lines across all systems — the patterns that confirm who someone truly is
- You speak to gifts first, then growth edges
- You always connect to the real lived experience of work, purpose, and relationships

Your specialty is the Gray Season — the in-between times when people have lost the plot and are
finding the real one. Career transitions, identity shifts, the question of "what now."
You hold this territory with profound respect and zero judgment.

When synthesizing a reading:
1. Find the resonant themes ACROSS all systems — not one at a time
2. Use their specific data — not generic descriptions
3. Connect their blueprint to what meaningful work could look like for them
4. Address what blocks them (shadow, conditioning, attachment patterns)
5. Point toward what's emergent — what wants to come through them now
6. Be specific, personal, and actionable — not vague and cosmic

Always sign off warmly as Estella."""


# ── HELPERS ───────────────────────────────────────────────────────────────────

def calculate_life_path(birthdate_str: str) -> str:
    """Reduce birth date digits to a life path number (master numbers 11, 22, 33 preserved)."""
    digits = [int(ch) for ch in birthdate_str if ch.isdigit()]
    total = sum(digits)
    while total > 9 and total not in (11, 22, 33):
        total = sum(int(ch) for ch in str(total))
    return str(total)


def get_sun_sign(month: int, day: int) -> str:
    """Return Western sun sign for a given month and day."""
    cusp_dates = [
        (1, 20, "Aquarius"),  (2, 19, "Pisces"),    (3, 21, "Aries"),
        (4, 20, "Taurus"),    (5, 21, "Gemini"),     (6, 21, "Cancer"),
        (7, 23, "Leo"),       (8, 23, "Virgo"),      (9, 23, "Libra"),
        (10, 23, "Scorpio"),  (11, 22, "Sagittarius"),(12, 22, "Capricorn"),
    ]
    for m, d, sign in cusp_dates:
        if month < m or (month == m and day < d):
            return sign
    return "Capricorn"


def build_context(p: dict) -> str:
    """Assemble the full profile context string to inject into the AI prompt."""
    life_path = calculate_life_path(p.get("birthdate", ""))
    hd_info   = HD_TYPES.get(p.get("hd_type", ""), {})

    return f"""FULL BLUEPRINT FOR {p.get('name', '').upper()}

BIRTH: {p.get('birthdate')} at {p.get('birth_time', 'unknown time')} in {p.get('birth_city')}

ASTROLOGY:
- Sun:    {p.get('sun_sign')}
- Moon:   {p.get('moon_sign')}
- Rising: {p.get('rising_sign')}

NUMEROLOGY:
- Life Path: {life_path}

HUMAN DESIGN:
- Type:      {p.get('hd_type')}
- Strategy:  {hd_info.get('strategy')}
- Work style:{hd_info.get('work_style')}
- Profile:   {p.get('hd_profile')}
- Authority: {p.get('hd_authority')}

ENNEAGRAM:       {p.get('enneagram', 'Not specified')}
ATTACHMENT STYLE:{p.get('attachment', 'Not specified')}

IKIGAI — PURPOSE LANDSCAPE:
- Loses track of time doing:            {p.get('ikigai_love')}
- What people consistently come to them for: {p.get('ikigai_good')}
- Problems in the world that bother them:    {p.get('ikigai_need')}
- When work has felt most meaningful:        {p.get('ikigai_paid')}

WHAT THEY'RE NAVIGATING NOW:
{p.get('current_context', 'Not specified')}"""


def generate_reading(profile: dict, api_key: str) -> str:
    """Call Claude to produce a full integrated reading."""
    client  = anthropic.Anthropic(api_key=api_key)
    context = build_context(profile)
    name    = profile.get("name", "")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"""{context}

Generate {name}'s full integrated reading using exactly these section headers on their own line:

THE THROUGH-LINE
YOUR GIFTS
THE SHADOW
YOUR WORK IN THE WORLD
WHAT WANTS TO EMERGE
A NOTE FROM ESTELLA

2–3 paragraphs per section. Be specific to their actual data — not generic.
Speak directly to {name} as "you".
Make YOUR WORK IN THE WORLD the most concrete and actionable section — this is a
Gray Season audience figuring out what's next."""}],
    )
    return response.content[0].text


def chat_response(message: str, profile: dict, history: list, api_key: str) -> str:
    """Return a contextual reply from Estella in ongoing conversation."""
    client  = anthropic.Anthropic(api_key=api_key)
    context = build_context(profile)
    name    = profile.get("name", "")

    messages = [{"role": h["role"], "content": h["content"]} for h in history]
    messages.append({"role": "user", "content": message})

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=600,
        system=f"""{SYSTEM_PROMPT}

You are in ongoing conversation with {name}. Their full blueprint:
{context}

Their reading has been delivered. Respond warmly and specifically to their question.
2–3 paragraphs max. If attachment or Enneagram patterns surface, probe gently.
Sign off as — Estella""",
        messages=messages,
    )
    return response.content[0].text


def reset_session():
    """Clear all session state and return to step 1."""
    st.session_state.step         = "birth"
    st.session_state.profile      = {}
    st.session_state.reading      = None
    st.session_state.chat_history = []


def init_session():
    if "step"         not in st.session_state: st.session_state.step         = "birth"
    if "profile"      not in st.session_state: st.session_state.profile      = {}
    if "reading"      not in st.session_state: st.session_state.reading      = None
    if "chat_history" not in st.session_state: st.session_state.chat_history = []


def question_card(number: str, text: str, hint: str) -> str:
    return (
        f'<div class="question-card">'
        f'<div class="question-number">{number}</div>'
        f'<div class="question-text">{text}</div>'
        f'<div class="question-hint">{hint}</div>'
        f'</div>'
    )


# ── INIT ──────────────────────────────────────────────────────────────────────

init_session()

try:
    api_key = st.secrets["ANTHROPIC_KEY"]
except Exception:
    api_key = st.sidebar.text_input("Anthropic API key", type="password", placeholder="sk-ant-...")

# ── HEADER ────────────────────────────────────────────────────────────────────

st.markdown('<div class="estella-title">ESTELLA</div>', unsafe_allow_html=True)
st.markdown('<div class="estella-tagline">know yourself. find your work. trust your path.</div>', unsafe_allow_html=True)
st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)


# ── STEP 1: BIRTH DATA ────────────────────────────────────────────────────────

if st.session_state.step == "birth":
    st.markdown('<div class="step-label">Step 1 of 3 — Where and when you arrived</div>', unsafe_allow_html=True)

    with st.form("birth_form"):
        name = st.text_input("Your first name", placeholder="e.g. Olivia")

        col1, col2 = st.columns(2)
        with col1:
            birthdate  = st.text_input("Birth date", placeholder="MM/DD/YYYY")
            birth_city = st.text_input("Birth city", placeholder="e.g. Fresno, CA")
        with col2:
            birth_time = st.text_input("Birth time", placeholder="e.g. 1:45 AM")
            st.caption("Birth time matters for rising sign and Human Design. Check your birth certificate if unsure.")

        st.markdown("**Your astrology** — enter what you know, skip what you don't")
        col1, col2, col3 = st.columns(3)
        with col1:
            sun_sign    = st.selectbox("Sun sign",    ["— select —"] + ASTRO_SIGNS)
        with col2:
            moon_sign   = st.selectbox("Moon sign",   ["— select —"] + ASTRO_SIGNS)
        with col3:
            rising_sign = st.selectbox("Rising sign", ["— select —"] + ASTRO_SIGNS)

        st.markdown("**Your Human Design** — find yours free at mybodygraph.com")
        col1, col2, col3 = st.columns(3)
        with col1:
            hd_type      = st.selectbox("HD Type",   ["— select —"] + list(HD_TYPES.keys()))
        with col2:
            hd_profile   = st.text_input("Profile",   placeholder="e.g. 3/5, 2/4")
        with col3:
            hd_authority = st.text_input("Authority", placeholder="e.g. Emotional, Sacral")

        st.markdown("**If you know these** — optional but adds depth")
        col1, col2 = st.columns(2)
        with col1:
            enneagram  = st.selectbox("Enneagram type",  ENNEAGRAM_TYPES)
        with col2:
            attachment = st.selectbox("Attachment style", ATTACHMENT_STYLES)

        submitted = st.form_submit_button("Continue →", use_container_width=True)

    if submitted:
        if not name:
            st.error("Please enter your name.")
        else:
            # Auto-calculate sun sign from birth date if not selected
            auto_sun = ""
            try:
                parts    = birthdate.replace("/", "-").split("-")
                auto_sun = get_sun_sign(int(parts[0]), int(parts[1]))
            except Exception:
                pass

            st.session_state.profile.update({
                "name":        name,
                "birthdate":   birthdate,
                "birth_time":  birth_time,
                "birth_city":  birth_city,
                "sun_sign":    sun_sign    if sun_sign    != "— select —"  else auto_sun,
                "moon_sign":   moon_sign   if moon_sign   != "— select —"  else "",
                "rising_sign": rising_sign if rising_sign != "— select —"  else "",
                "hd_type":     hd_type     if hd_type     != "— select —"  else "",
                "hd_profile":  hd_profile,
                "hd_authority":hd_authority,
                "enneagram":   enneagram   if enneagram   != "Not sure yet" else "",
                "attachment":  attachment  if attachment  != "Not sure yet" else "",
            })
            st.session_state.step = "ikigai"
            st.rerun()


# ── STEP 2: IKIGAI ────────────────────────────────────────────────────────────

elif st.session_state.step == "ikigai":
    name = st.session_state.profile.get("name", "")

    st.markdown('<div class="step-label">Step 2 of 3 — Your purpose landscape</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="text-align:center;font-family:\'Cormorant Garamond\',serif;'
        f'font-size:1.1rem;font-weight:300;color:#9C8A6E;margin-bottom:1.5rem;">'
        f'Four questions, {name}. Take your time with these.<br>'
        f'There are no right answers — only honest ones.</div>',
        unsafe_allow_html=True,
    )

    with st.form("ikigai_form"):
        st.markdown(question_card(
            "Question 01",
            "What do you lose track of time doing?",
            "The thing that absorbs you completely — where hours disappear and you forget to eat.",
        ), unsafe_allow_html=True)
        ikigai_love = st.text_area("", placeholder="Write freely...", key="q1",
                                   label_visibility="collapsed", height=100)

        st.markdown(question_card(
            "Question 02",
            "What do people consistently come to you for — even things you take for granted?",
            "The gifts so natural to you that you assume everyone has them. They don't.",
        ), unsafe_allow_html=True)
        ikigai_good = st.text_area("", placeholder="Write freely...", key="q2",
                                   label_visibility="collapsed", height=100)

        st.markdown(question_card(
            "Question 03",
            "What problems in the world actually bother you — the ones you wish someone would fix?",
            "The injustices, gaps, or broken systems that genuinely light a fire in you.",
        ), unsafe_allow_html=True)
        ikigai_need = st.text_area("", placeholder="Write freely...", key="q3",
                                   label_visibility="collapsed", height=100)

        st.markdown(question_card(
            "Question 04",
            "When has work felt most meaningful to you? What was happening?",
            "A specific moment or chapter — even if it was brief. What made it feel real?",
        ), unsafe_allow_html=True)
        ikigai_paid = st.text_area("", placeholder="Write freely...", key="q4",
                                   label_visibility="collapsed", height=100)

        st.markdown(question_card(
            "One more thing",
            "What are you navigating right now?",
            "Career transition, a relationship shift, a creative block, a quiet restlessness — "
            "whatever brought you here.",
        ), unsafe_allow_html=True)
        current_context = st.text_area("", placeholder="Write freely...", key="q5",
                                       label_visibility="collapsed", height=100)

        submitted = st.form_submit_button("Generate my reading →", use_container_width=True)

    if submitted:
        if not ikigai_love and not ikigai_good:
            st.error("Please answer at least the first two questions.")
        else:
            st.session_state.profile.update({
                "ikigai_love":     ikigai_love,
                "ikigai_good":     ikigai_good,
                "ikigai_need":     ikigai_need,
                "ikigai_paid":     ikigai_paid,
                "current_context": current_context,
            })
            st.session_state.step = "reading"
            st.rerun()


# ── STEP 3: READING + CHAT ────────────────────────────────────────────────────

elif st.session_state.step == "reading":
    profile = st.session_state.profile
    name    = profile.get("name", "")

    # Generate reading on first load
    if not st.session_state.reading:
        if not api_key:
            st.error("Please add your Anthropic API key to continue.")
            st.stop()
        with st.spinner("Estella is reading your blueprint..."):
            try:
                st.session_state.reading = generate_reading(profile, api_key)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.stop()

    # Reading header
    st.markdown(
        f'<div style="font-family:\'Cormorant Garamond\',serif;font-size:1.7rem;'
        f'font-weight:300;text-align:center;letter-spacing:0.06em;margin-bottom:0.75rem;">'
        f'A reading for {name}</div>',
        unsafe_allow_html=True,
    )

    # Profile badges
    life_path = calculate_life_path(profile.get("birthdate", ""))
    badges = []
    if profile.get("sun_sign"):    badges.append(f"☉ {profile['sun_sign']}")
    if profile.get("moon_sign"):   badges.append(f"☽ {profile['moon_sign']}")
    if profile.get("rising_sign"): badges.append(f"↑ {profile['rising_sign']}")
    if profile.get("hd_type"):     badges.append(f"HD {profile['hd_type']}")
    if life_path:                  badges.append(f"Life Path {life_path}")
    if profile.get("enneagram") and "Not" not in profile.get("enneagram", ""):
        badges.append(profile["enneagram"].split("—")[0].strip())

    if badges:
        badge_html = "".join(f'<span class="profile-badge">{b}</span>' for b in badges)
        st.markdown(
            f'<div style="text-align:center;margin-bottom:1.5rem;">{badge_html}</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # Render reading sections
    remaining = st.session_state.reading
    for label in READING_SECTIONS:
        if label not in remaining:
            continue

        _, remaining      = remaining.split(label, 1)
        next_pos          = len(remaining)
        for other in READING_SECTIONS:
            if other != label and other in remaining:
                pos = remaining.find(other)
                if pos < next_pos:
                    next_pos = pos

        body          = remaining[:next_pos].strip()
        remaining     = remaining[next_pos:]
        border_style  = "border-left: 2px solid #C9A84C;" if label == "A NOTE FROM ESTELLA" else ""

        st.markdown(
            f'<div class="reading-section" style="{border_style}">'
            f'<div class="reading-section-label">{label}</div>'
            f'<div class="reading-body">{body.replace(chr(10), "<br>")}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # Chat section
    st.markdown(
        '<div style="font-family:\'Cormorant Garamond\',serif;font-size:1.4rem;'
        'font-weight:300;text-align:center;letter-spacing:0.06em;margin:1.5rem 0 0.5rem;">'
        'Continue the conversation</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="text-align:center;font-size:0.8rem;font-weight:300;color:#9C8A6E;margin-bottom:1.25rem;">'
        "Ask Estella anything about your chart, your path, or what's next.</div>",
        unsafe_allow_html=True,
    )

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-user">{msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="chat-estella">{msg["content"]}'
                f'<div class="estella-signature">— Estella</div></div>',
                unsafe_allow_html=True,
            )

    user_input = st.chat_input(f"Ask Estella something, {name}...")
    if user_input:
        if not api_key:
            st.error("API key needed.")
        else:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.spinner(""):
                reply = chat_response(user_input, profile, st.session_state.chat_history, api_key)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

    # Footer actions
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start a new reading", use_container_width=True):
            reset_session()
            st.rerun()
    with col2:
        if st.button("Edit my answers", use_container_width=True):
            st.session_state.step    = "ikigai"
            st.session_state.reading = None
            st.rerun()
