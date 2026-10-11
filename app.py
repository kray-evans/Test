import random
import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Pokémon Battle Arena", page_icon="⚡", layout="centered"
)

# Giao diện CSS tùy chỉnh
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

# Danh sách Pokémon để người chơi lựa chọn
POKEMONS = {
    "Pikachu": {
        "hp": 100,
        "max_hp": 100,
        "moves": {
            "⚡ Điện Giật (Normal)": 15,
            "💥 Tia Chớp Sấm Sét (Strong)": 25,
            "💖 Hồi Máu (Heal)": -20,
        },
        "icon": "⚡",
    },
    "Charmander": {
        "hp": 110,
        "max_hp": 110,
        "moves": {
            "🔥 Cào Lửa (Normal)": 14,
            "🌋 Ngọn Lửa Địa Ngục (Strong)": 28,
            "💖 Hồi Máu (Heal)": -18,
        },
        "icon": "🔥",
    },
    "Bulbasaur": {
        "hp": 120,
        "max_hp": 120,
        "moves": {
            "🍃 Roi Mây (Normal)": 12,
            "🌿 Bão Lá (Strong)": 22,
            "💖 Hồi Máu (Heal)": -25,
        },
        "icon": "🍃",
    },
}

BOSSES = [
    {"name": "Wild Charizard", "hp": 130, "max_hp": 130, "icon": "🐉", "atk": 20},
    {"name": "Team Rocket Mewtwo", "hp": 160, "max_hp": 160, "icon": "😈", "atk": 25},
]

# Khởi tạo trạng thái game
if "game_state" not in st.session_state:
  st.session_state.game_state = "SELECT"  # Các trạng thái: SELECT, BATTLE, OVER
if "player" not in st.session_state:
  st.session_state.player = None
if "boss" not in st.session_state:
  st.session_state.boss = None
if "battle_log" not in st.session_state:
  st.session_state.battle_log = "Trận chiến bắt đầu! Hãy tung chiêu hợp lý."


# --- GIAO DIỆN 1: CHỌN POKÉMON ---
if st.session_state.game_state == "SELECT":
  st.title("⚡ Pokémon Battle Arena")
  st.write("Chọn Pokémon đồng hành cùng bạn để bước vào trận chiến:")

  col1, col2, col3 = st.columns(3)

  with col1:
    if st.button("⚡ Pikachu"):
      st.session_state.player = POKEMONS["Pikachu"].copy()
      st.session_state.game_state = "BATTLE"
      st.session_state.boss = random.choice(BOSSES).copy()
      st.rerun()

  with col2:
    if st.button("🔥 Charmander"):
      st.session_state.player = POKEMONS["Charmander"].copy()
      st.session_state.game_state = "BATTLE"
      st.session_state.boss = random.choice(BOSSES).copy()
      st.rerun()

  with col3:
    if st.button("🍃 Bulbasaur"):
      st.session_state.player = POKEMONS["Bulbasaur"].copy()
      st.session_state.game_state = "BATTLE"
      st.session_state.boss = random.choice(BOSSES).copy()
      st.rerun()


# --- GIAO DIỆN 2: TRẬN CHIẾN ---
elif st.session_state.game_state == "BATTLE":
  player = st.session_state.player
  boss = st.session_state.boss

  st.title("⚔️ Trận Chiến Pokémon")
  st.divider()

  # Hiển thị thông số 2 bên
  c1, c2 = st.columns(2)

  with c1:
    st.subheader(f"{player['icon']} Bạn ({list(POKEMONS.keys())[0] if 'Pikachu' else ''})")
    st.write(f"❤️ Máu (HP): {player['hp']} / {player['max_hp']}")
    st.progress(max(0, player["hp"] / player["max_hp"]))

  with c2:
    st.subheader(f"{boss['icon']} Đối Thủ: {boss['name']}")
    st.write(f"❤️ Máu (HP): {boss['hp']} / {boss['max_hp']}")
    st.progress(max(0, boss["hp"] / boss["max_hp"]))

  st.divider()

  # Nhật ký trận đấu
  st.info(f"📢 **Nhật ký:** {st.session_state.battle_log}")

  # Lựa chọn chiêu thức
  st.markdown("### 🎯 Chọn hành động của bạn:")
  move_cols = st.columns(3)

  move_list = list(player["moves"].keys())

  # Nút chiêu 1
  with move_cols[0]:
    if st.button(move_list[0]):
      dmg = player["moves"][move_list[0]]
      boss["hp"] -= dmg
      st.session_state.battle_log = (
          f"Bạn dùng chiêu tấn công và gây ra {dmg sát thương!"
      )
      # Kiểm tra boss chết chưa
      if boss["hp"] <= 0:
        st.session_state.game_state = "OVER"
        st.session_state.win = True
      else:
        # Boss phản công
        b_dmg = random.randint(10, boss["atk"])
        player["hp"] -= b_dmg
        st.session_state.battle_log += (
            f" Đối thủ phản công gây {b_dmg} sát thương!"
        )
        if player["hp"] <= 0:
          st.session_state.game_state = "OVER"
          st.session_state.win = False
      st.rerun()

  # Nút chiêu 2 (Mạnh)
  with move_cols[1]:
    if st.button(move_list[1]):
      dmg = player["moves"][move_list[1]]
      boss["hp"] -= dmg
      st.session_state.battle_log = (
          f"Bạn tung chiêu cực mạnh gây ra {dmg} sát thương!"
      )
      if boss["hp"] <= 0:
        st.session_state.game_state = "OVER"
        st.session_state.win = True
      else:
        b_dmg = random.randint(10, boss["atk"])
        player["hp"] -= b_dmg
        st.session_state.battle_log += (
            f" Đối thủ phản công gây {b_dmg} sát thương!"
        )
        if player["hp"] <= 0:
          st.session_state.game_state = "OVER"
          st.session_state.win = False
      st.rerun()

  # Nút hồi máu
  with move_cols[2]:
    if st.button(move_list[2]):
      heal = abs(player["moves"][move_list[2]])
      player["hp"] = min(player["max_hp"], player["hp"] + heal)
      st.session_state.battle_log = f"Bạn hồi phục được {heal} HP!"
      # Boss vẫn đánh khi bạn hồi máu
      b_dmg = random.randint(10, boss["atk"])
      player["hp"] -= b_dmg
      st.session_state.battle_log += (
          f" Tranh thủ lúc hồi máu, đối thủ đánh bồi {b_dmg} sát thương!"
      )
      if player["hp"] <= 0:
        st.session_state.game_state = "OVER"
        st.session_state.win = False
      st.rerun()


# --- GIAO DIỆN 3: KẾT THÚC TRẬN ĐẤU ---
elif st.session_state.game_state == "OVER":
  st.title("🏆 Kết Quả Trận Đấu")

  if st.session_state.win:
    st.success("🎉 **CHÚC MỪNG! Bạn đã đánh bại Pokémon đối thủ và giành chiến thắng!**")
  else:
    st.error(
        "💀 **THẤT BY! Pokémon của bạn đã kiệt sức. Hãy luyện tập thêm nhé!**"
    )

  if st.button("🔄 Chơi Lại Từ Đầu"):
    st.session_state.game_state = "SELECT"
    st.session_state.player = None
    st.session_state.boss = None
    st.session_state.battle_log = "Trận chiến bắt đầu!"
    st.rerun()


