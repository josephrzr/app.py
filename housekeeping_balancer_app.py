import streamlit as st
import pandas as pd

def balance_checkouts(data, target):
    balanced = data.copy()
    moves = [0] * len(data)
    directions = ["-"] * len(data)

    changed = True
    while changed:
        changed = False
        for i in range(len(balanced)):
            if balanced[i] > target:
                if i > 0 and balanced[i - 1] < target:
                    move = min(balanced[i] - target, target - balanced[i - 1])
                    balanced[i] -= move
                    balanced[i - 1] += move
                    moves[i] += move
                    directions[i] = "→"
                    changed = True
                elif i < len(balanced) - 1 and balanced[i + 1] < target:
                    move = min(balanced[i] - target, target - balanced[i + 1])
                    balanced[i] -= move
                    balanced[i + 1] += move
                    moves[i] += move
                    directions[i] = "→"
                    changed = True

    return balanced, moves, directions

# Streamlit App
st.title("Hotel Housekeeping Checkout Balancer")
st.markdown("""
Enter the number of checkouts per board and a target checkout number. The tool will balance the checkouts using only left/right board adjustments.
""")

num_boards = st.number_input("Number of Boards", min_value=1, value=10)
target_checkout = st.number_input("Target Checkout per Board", min_value=1, value=8)

checkouts = []
for i in range(num_boards):
    val = st.number_input(f"Board {i+1} Checkouts", min_value=0, key=f"checkout_{i}")
    checkouts.append(val)

if st.button("Balance Now"):
    balanced, moves, directions = balance_checkouts(checkouts, target_checkout)

    df = pd.DataFrame({
        "Board": [f"Board {i+1}" for i in range(num_boards)],
        "Original Checkouts": checkouts,
        "Balanced Checkouts": balanced,
        "Rooms Moved": moves,
        "Direction": directions
    })

    st.subheader("Balanced Output")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Result as CSV", data=csv, file_name="balanced_checkouts.csv", mime="text/csv")
