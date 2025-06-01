import streamlit as st
import google.generativeai as genai

# Configure your API key here
genai.configure(api_key="AIzaSyB5r5f2dwAMLZS_6tCo-_RJCQZnRxJk2uU")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Set page config
st.set_page_config(
    page_title="🌱 Renewable Energy Chatbot",
    page_icon="🌞",
    layout="wide",
)

st.title("🌱 Renewable Energy Chatbot")

st.sidebar.title("About this bot")
st.sidebar.info("""
Hello user 😊. This is Pehvi an Renewable energy chatbot. I'm here to helps you learn about renewable energy topics like solar, wind, hydro, and saving energy at home.
Ask any question, and the bot will answer using AI.
""")

# Start or continue chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

RENEWABLE_KEYWORDS = [
    "solar", "solar energy", "solar power", "solar panel", "solar cells", "photovoltaic",
    "pv system", "solar thermal", "solar water heater", "solar inverter", "solar battery",
    "solar ","wind energy", "wind power", "wind turbine", "wind farm", "windmill", "offshore wind",
    "onshore wind", "wind generator", "wind blade", "wind speed",
    "hydro",  "farm", "solar plant", "solar radiation", "solar irradiance",
    "wind","hydropower", "hydroelectric", "hydroelectric power", "hydro turbine", "dam",
    "run-of-river", "pumped storage", "water energy",
    "geothermal", "geothermal energy", "geothermal power", "geothermal plant", "geothermal heat pump",
    "biomass", "biomass energy", "bioenergy", "biogas", "biomass fuel", "biofuel", "bioethanol",
    "biodiesel", "biomass combustion", "waste to energy", "organic waste",
    "tidal energy", "tidal power", "tidal turbine", "tidal stream", "tidal barrage",
    "wave energy", "wave power", "wave turbine",
    "renewable", "renewable energy", "renewable power", "clean energy", "green energy",
    "alternative energy", "sustainable energy", "sustainability", "sustainable power",
    "energy storage", "battery storage", "energy efficiency", "energy saving", "energy conservation",
    "smart grid", "microgrid", "net metering", "grid integration", "energy management system",
    "carbon footprint", "carbon neutral", "carbon offset", "carbon emissions", "carbon dioxide",
    "greenhouse gases", "climate change", "global warming", "climate action", "environmental impact",
    "pollution", "air quality", "eco-friendly", "low carbon", "zero emissions",
    "electric vehicle", "ev charging", "charging station", "electric grid", "energy policy",
    "government incentives", "renewable subsidies", "feed-in tariff", "power purchase agreement",
    "energy transition", "decarbonization", "energy audit", "energy rating", "building insulation",
    "LED lighting", "efficient appliances", "heat pump", "solar water pump", "off-grid solar",
    "on-grid solar", "battery inverter", "hybrid systems", "energy analytics", "energy forecasting",
    "hydrogen energy", "green hydrogen", "blue hydrogen", "hydrogen fuel cell",
    "renewable heating", "solar cooling", "passive solar design", "net zero energy",
    "clean tech", "climate finance", "environmental sustainability", "renewable investments",
    "renewable energy certificates", "power grid", "energy infrastructure",
    "energy economics", "energy market", "energy demand", "energy supply",
    "renewable energy storage", "thermal energy storage", "compressed air energy storage",
    "flywheel energy storage", "pumped hydro storage",
    "solar desalination", "renewable desalination",
    "carbon capture", "carbon sequestration",
    "energy independence", "energy security",
    "biochar", "algae biofuel", "municipal solid waste", "landfill gas",
    "solar tracking system", "solar concentrator", "solar furnace",
    "floating solar", "agrivoltaics", "solar irrigation",
    "wave buoy", "ocean energy", "blue economy",
    "energy poverty", "energy access", "energy equity",
    "energy literacy", "energy education",
    "green building", "LEED certification", "BREEAM",
    "energy retrofitting", "demand response",
    "smart meters", "virtual power plant",
    "clean energy jobs", "green jobs",
    "renewable energy targets", "Paris Agreement", "COP26",
    "energy innovation", "energy technology",
    "energy resilience", "climate resilience",
    "energy policy framework", "sustainable development goals",
    "corporate sustainability", "renewable energy startups",
    "energy storage systems", "flow batteries", "lithium-ion battery",
    "solid-state battery", "battery recycling",
    "power electronics", "inverter technology",
    "energy harvesting", "kinetic energy harvesting",
    "solar fuel", "artificial photosynthesis",
    "renewable natural gas", "biomethane",
    "district heating", "district cooling",
    "energy retrofitting",
    "energy-efficient building design",
    "passive house",
    "cool roofs", "green roofs",
    "solar roads", "solar windows",
    "energy poverty alleviation",
    "energy access solutions",
    "smart city", "urban sustainability",
    "carbon trading", "emissions trading system",
    "clean energy finance",
    "electrification of transport",
    "power-to-x",
    "renewable energy storage technologies",
    "thermal solar",
    "solar photovoltaic module",
    "solar cell efficiency",
    "renewable energy potential",
    "renewable energy resources",
    "energy transition roadmap",
    "energy sector reform",
    "energy conservation measures",
    "energy-efficient appliances",
    "carbon neutrality goals",
    "climate mitigation",
    "solar lanterns",
    "off-grid electrification",
    "micro-hydropower",
    "energy balance",
    "power generation",
    "distributed generation",
    "energy market liberalization",
    "capacity building",
    "energy forecasting",
    "electricity market",
    "energy storage capacity",
    "solar module degradation",
    "energy consumption",
    "energy efficiency standards",
    "power system stability",
    "energy yield",
    "energy infrastructure development",
    "clean energy technologies",
    "energy performance",
    "wind power potential",
    "renewable energy integration",
    "solar irradiance measurement",
    "energy scenario analysis",
    "energy policy analysis",
    "clean energy innovation",
    "energy system modeling",
    "energy transition scenarios",
    "solar radiation forecasting",
    "wind resource assessment",
    "energy sector decarbonization",
    "energy grid modernization",
    "energy system optimization",
    "renewable energy economics",
    "renewable energy deployment",
    "energy regulatory framework",
    "renewable energy barriers",
    "solar power plants",
    "wind power plants",
    "energy efficiency improvement",
    "energy access challenges",
    "renewable energy adoption",
    "renewable energy projects",
    "green hydrogen production",
    "renewable energy policy",
    "energy poverty reduction",
    "renewable energy financing",
    "renewable energy education",
    "clean energy development",
    "energy technology innovation",
    "renewable energy resources assessment",
    "energy poverty index",
    "renewable energy job creation",
    "renewable energy awareness",
    "energy infrastructure investment",
    "renewable energy research",
    "energy storage solutions",
    "energy transition policy",
    "energy efficiency policy",
    "solar power generation",
    "wind power generation",
    "hydropower generation",
    "energy management",
    "energy conservation programs","energy efficiency programs","renewable energy integration challenges",
    "renewable energy environmental impact","renewable energy social impact","energy consumption reduction","solar energy systems",
    "wind energy systems","hydropower systems","biomass energy systems","tidal energy systems","wave energy systems",
    "renewable energy education programs","clean energy solutions","energy transition challenges","energy efficiency technologies",
    "renewable energy grid integration","energy policy development","renewable energy project financing","energy access initiatives",
    "renewable energy standards","clean energy standards","solar energy market","wind energy market","hydropower market",
    "renewable energy market analysis","energy efficiency market","energy consumption patterns","renewable energy impact assessment",
    "energy sector challenges","renewable energy sustainability","clean energy investment","energy efficiency investment",
    "renewable energy awareness campaigns","energy conservation awareness","renewable energy workforce","clean energy workforce",
    "energy sector jobs","renewable energy technology transfer","energy efficiency improvement measures","renewable energy innovation",
    "clean energy innovation","energy sector modernization","renewable energy development","energy storage technologies",
    "renewable energy infrastructure","clean energy infrastructure","energy access for all","renewable energy solutions",
    "energy system transformation","renewable energy transformation","energy transition strategies","renewable energy policies",
    "clean energy policies","energy sector policies","renewable energy funding","energy efficiency funding","renewable energy future",
    "clean energy future","sustainable energy future","renewable energy challenges","clean energy challenges","energy efficiency challenges",
    "renewable energy benefits","clean energy benefits","energy efficiency benefits","renewable energy technologies","clean energy technologies",
    "energy efficiency technologies","renewable energy systems","hello", "hi", "hey", "help", "question", "query", "ask", "information",
    "knowledge", "learn", "understand", "explain", "clarify", "details", "facts", "data","power",
    "electricity", "energy", "renewable", "sustainable", "environment", "climate", "green","clean",
    "solar", "wind", "hydro", "geothermal", "biomass", "tidal", "wave", "carbon", "footprint","emissions",
    "pollution", "conservation", "efficiency", "savings", "technology", "innovation", "future","sustainability",
    "policy", "regulation", "incentives", "subsidies", "investment", "economics", "market","industry"
]


def is_renewable_related(text):
    return any(word in text.lower() for word in RENEWABLE_KEYWORDS)

def get_response(user_input):
    if is_renewable_related(user_input):
        response = st.session_state.chat_session.send_message(user_input)
        return response.text
    else:
        return "I'm sorry, I can only answer questions related to renewable energy."

# Function to display chat messages
def display_chat_message(message, is_user=True):
    if is_user:
        st.markdown(f"""
        <div style='background-color:#DCF8C6;
                    padding:10px;
                    border-radius:10px;
                    width:60%;
                    margin-left:auto;
                    margin-bottom:5px;
                    color: black;'>
            <b>You:</b> {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background-color:#F1F0F0;
                    padding:10px;
                    border-radius:10px;
                    width:60%;
                    margin-right:auto;
                    margin-bottom:5px;
                    color: black;'>
            <b>Pehvi :</b> {message}
        </div>
        """, unsafe_allow_html=True)

# Display chat history
for user_msg, bot_msg in st.session_state.chat_history:
    display_chat_message(user_msg, is_user=True)
    display_chat_message(bot_msg, is_user=False)

# Input and send button placed at the bottom
user_input = st.text_input("Ask me about renewable energy:", key="user_input")
send_button = st.button("Send", key="send_button")

if send_button and user_input:
    response = get_response(user_input)
    st.session_state.chat_history.append((user_input, response))
    st.rerun()