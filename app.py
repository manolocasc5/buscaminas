import streamlit as st
from game import Game

DIFFICULTIES = {
    "😺 Pequeño (5x5, 5 minas)": (5, 5, 5),
    "😼 Mediano (10x10, 10 minas)": (10, 10, 10),
    "🐯 Grande (15x15, 20 minas)": (15, 15, 20),
}

def init_game():
    width, height, mines = DIFFICULTIES[st.session_state.difficulty]
    st.session_state.game = Game(width, height, mines)
    st.session_state.flag_mode = False

def reset_game():
    init_game()
    st.rerun()

def get_face():
    if not st.session_state.game.game_over:
        return "😊"
    elif st.session_state.game.board.is_won():
        return "😎"
    else:
        return "😵"

def count_flags():
    return sum(cell.is_flagged for row in st.session_state.game.board.grid for cell in row)

def reveal_all_mines():
    for row in st.session_state.game.board.grid:
        for cell in row:
            if cell.is_mine:
                cell.reveal()

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "😼 Mediano (10x10, 10 minas)"
if "game" not in st.session_state:
    init_game()

game = st.session_state.game
board = game.board

st.set_page_config(page_title="Buscaminas", layout="centered")
st.title("💣 Buscaminas")

# Botón de reinicio debajo del título
with st.form("restart_form"):
    st.form_submit_button("🔄 Reiniciar juego", on_click=reset_game)

# Cambiar dificultad
if not game.game_over:
    with st.expander("⚙️ Cambiar dificultad"):
        difficulty_selected = st.selectbox(
            "Dificultad", list(DIFFICULTIES.keys()),
            index=list(DIFFICULTIES.keys()).index(st.session_state.difficulty)
        )
        if difficulty_selected != st.session_state.difficulty:
            st.session_state.difficulty = difficulty_selected
            reset_game()

# Top bar
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.metric("🚩 Banderas", f"{count_flags()} / {board.num_mines}")
with col2:
    st.markdown(f"<div style='font-size: 32px; text-align: center;'>{get_face()}</div>", unsafe_allow_html=True)
with col3:
    st.checkbox("🚩 Modo bandera", key="flag_mode")

# CSS GLOBAL
st.markdown("""
    <style>
    .stButton > button {
        width: 40px;
        height: 40px;
        font-size: 20px;
        font-weight: bold;
        background-color: #4CAF50; /* Verde */
        padding: 0 !important;
        margin: 0 !important;
        text-align: center;
        border: 1px solid black;
        border-radius: 4px;
    }
    .cell-unrevealed button {
        background-color: #f0f0f0 !important;
    }
    .cell-revealed button {
        background-color: #dddddd !important;
    }
    .cell-mine button {
        background-color: #ffcccc !important;
    }
    .cell-flagged button {
        background-color: #fff7cc !important;
    }
    .color-1 { color: #0000FF !important; }
    .color-2 { color: #008000 !important; }
    .color-3 { color: #FF0000 !important; }
    .color-4 { color: #000080 !important; }
    .color-5 { color: #800000 !important; }
    .color-6 { color: #00CED1 !important; }
    .color-7 { color: #000000 !important; }
    .color-8 { color: #808080 !important; }
    </style>
""", unsafe_allow_html=True)

# Mostrar tablero
for x in range(board.height):
    cols = st.columns(board.width)
    for y in range(board.width):
        cell = board.grid[x][y]
        key = f"{x}_{y}"
        disabled = game.game_over or cell.is_revealed
        label = ""
        color_class = ""
        style_class = "cell-unrevealed"

        if game.game_over and cell.is_mine:
            label = "💣"
            style_class = "cell-mine"
        elif cell.is_revealed:
            style_class = "cell-revealed"
            if cell.is_mine:
                label = "💣"
                style_class = "cell-mine"
            elif cell.adjacent_mines > 0:
                label = str(cell.adjacent_mines)
                color_class = f"color-{cell.adjacent_mines}"
        elif cell.is_flagged:
            label = "🚩"
            style_class = "cell-flagged"

        with cols[y]:
            container = st.container()
            with container:
                st.markdown(f'<div class="{style_class}">', unsafe_allow_html=True)
                if st.button(label, key=key, disabled=disabled):
                    if st.session_state.flag_mode:
                        game.make_move(x, y, flag=True)
                    else:
                        if not cell.is_flagged:
                            exploded = game.make_move(x, y)
                            if exploded:
                                reveal_all_mines()
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

# Fin del juego
if game.game_over:
    if board.is_won():
        st.success("🎉 ¡Felicidades! Has ganado.")
        st.balloons()
    else:
        st.error("💥 Has perdido. Tocaste una mina.")