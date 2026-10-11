import random
import streamlit as st

st.set_page_config(
    page_title="Pokemon Battle Arena", page_icon="⚡", layout="centered"
)

st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        height: 45px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

POKEMONS = {
    "Pikachu": {
        "hp": 100,
        "max_hp": 100,
        "moves": {
            "Dien Giat (Normal)": 15,
            "Sam Set (Strong)": 25,
            "Hoi Mau (Heal)": -20,
        },
        "icon": "⚡",
    },
    "Charmander": {
        "hp": 110,
        "max_hp": 110,
        "moves": {
            "Cao Lua (Normal)": 14,
            "Ngon Lua Dia Nguc (Strong)": 28,
            "Hoi Mau (Heal)": -18,
        },
        "icon": "🔥",
    },
    "Bulbasaur": {
        "hp": 120,
        "max_hp": 120,
        "moves": {
            "Roi May (Normal)": 12,
            "Bao La (Strong)": 22,
            "Hoi Mau (Heal)": -25,
        },
        "icon": "🍃",
    },
}

BOSSES = [
    {"name": "Wild Charizard", "hp": 130, "max_hp": 130, "icon": "🐉", "atk": 20},
    {"name": "Team Rocket Mewtwo", "hp": 160, "max_hp": 160, "icon": "😈", "atk": 25},
]

if "game_state" not in st.session_state:
  st.session_state.game_state = "SELECT"
if "player" not in st.session_state:
  st.session_state.player = None
if "boss" not in st.session_state:
  st.session_state.boss = None
if "battle_log" not in st.session_state:
  st.session_state.battle_log = "Tran chien bat dau! Hay chon chieu thuc."

if st.session_state.game_state == "SELECT":
  st.title("Pokemon Battle Arena")
  st.write("Chon Pokemon dong hanh cung ban:")

  col1, col2, col3 = st.columns(3)

  with col1:
    if st.button("Pikachu"):
      st.session_state.player = POKEMONS["Pikachu"].copy()
      st.session_state.game_state = "BATTLE"
      st.session_state.boss = random.choice(BOSSES).copy()
      st.rerun()

  with col2:
    if st.button("Charmander"):
      st.session_state.player = POKEMONS["Charmander"].copy()
      st.session_state.game_state = "BATTLE"
      st.session_state.boss = random.choice(BOSSES).copy()
      st.rerun()

  with col3:
    if st.button("Bulbasaur"):
      st.session_state.player = POKEMONS["Bulbasaur"].copy()
      st.session_state.game_state = "BATTLE"
      st.session_state.boss = random.choice(BOSSES).copy()
      st.rerun()

elif st.session_state.game_state == "BATTLE":
  player = st.session_state.player
  boss = st.session_state.boss

  st.title("Tran Chien Pokemon")
  st.divider()

  c1, c2 = st.columns(2)

  with c1:
    st.subheader(f"{player['icon']} Ban")
    st.write(f"Mau (HP): {player['hp']} / {player['max_hp']}")
    st.progress(max(0, player["hp"] / player["max_hp"]))

  with c2:
    st.subheader(f"{boss['icon']} Doi Thu: {boss['name']}")
    st.write(f"Mau (HP): {boss['hp']} / {boss['max_hp']}")
    st.progress(max(0, boss["hp"] / boss["max_hp"]))

  st.divider()

  st.info(f"Nhat ky: {st.session_state.battle_log}")

  st.markdown("### Chon hanh dong:")
  move_cols = st.columns(3)
  move_list = list(player["moves"].keys())

  with move_cols[0]:
    if st.button(move_list[0]):
      dmg = player["moves"][move_list[0]]
      boss["hp"] -= dmg
      st.session_state.battle_log = f"Ban gay ra {dmg} sat thuong!"
      if boss["hp"] <= 0:
        st.session_state.game_state = "OVER"
        st.session_state.win = True
      else:
        b_dmg = random.randint(10, boss["atk"])
        player["hp"] -= b_dmg
        st.session_state.battle_log += f" Doi thu phan cong gay {b_dmg} HP!"
        if player["hp"] <= 0:
          st.session_state.game_state = "OVER"
          st.session_state.win = False
      st.rerun()

  with move_cols[1]:
    if st.button(move_list[1]):
      dmg = player["moves"][move_list[1]]
      boss["hp"] -= dmg
      st.session_state.battle_log = f"Ban dung chieu manh gay {dmg} sat thuong!"
      if boss["hp"] <= 0:
        st.session_state.game_state = "OVER"
        st.session_state.win = True
      else:
        b_dmg = random.randint(10, boss["atk"])
        player["hp"] -= b_dmg
        st.session_state.battle_log += f" Doi thu phan cong gay {b_dmg} HP!"
        if player["hp"] <= 0:
          st.session_state.game_state = "OVER"
          st.session_state.win = False
      st.rerun()

  with move_cols[2]:
    if st.button(move_list[2]):
      heal = abs(player["moves"][move_list[2]])
      player["hp"] = min(player["max_hp"], player["hp"] + heal)
      st.session_state.battle_log = f"Ban hoi phuc duoc {heal} HP!"
      b_dmg = random.randint(10, boss["atk"])
      player["hp"] -= b_dmg
      st.session_state.battle_log += f" Doi thu tranh thu danh boi {b_dmg} HP!"
      if player["hp"] <= 0:
        st.session_state.game_state = "OVER"
        st.session_state.win = False
      st.rerun()

elif st.session_state.game_state == "OVER":
  st.title("Ket Qua Tran Dau")

  if st.session_state.win:
    st.success("Chuc mung! Ban da chien thang!")
  else:
    st.error("That bai! Pokemon cua ban da kiet suc.")

  if st.button("Choi Lai Tu Dau"):
    st.session_state.game_state = "SELECT"
    st.session_state.player = None
    st.session_state.boss = None
    st.session_state.battle_log = "Tran chien bat dau!"
    st.rerun()

] -= b_dmg
      st.session_state.battle_log += (
          f" Tranh thủ lúc hồi máu, đối thủ đánh bồi {b_dmg} sát thương!"
      )
      if player["hp"] <= 0:
        st.session_state.game_state = "OVER"
        st.session_state.win = False
      st.rerun()


# --- GIAO DIỆN 3: KẾT THÚC TRẬN ĐẤU ---
elif st.session_state.game_state == "OVER":
  st.title("🏆
