from controller.game_controller import GameController
from controller.actions import (
    GameStartAction,
    PlayerPlacePawnAction,
    PlayerMovePawnAction,
    PlayerRemovePawnAction,
)

def game_scenario_1(wc: GameController, bc: GameController) -> None:

    def place(controller: GameController, index: int) -> None:
        controller.perform(PlayerPlacePawnAction(at_index=index))

    def move(
        controller: GameController,
        source: int,
        target: int,
    ) -> None:
        controller.perform(
            PlayerMovePawnAction(
                from_index=source,
                to_index=target,
            )
        )

    def remove(controller: GameController, index: int) -> None:
        controller.perform(PlayerRemovePawnAction(at_index=index))

    # =========================================================
    # 1. GAME START & PLACING
    # =========================================================

    wc.perform(GameStartAction())

    place(bc, 3)   # REJECT: Not Black's turn

    place(wc, 0)
    place(bc, 0)   # REJECT: Position occupied
    place(bc, 3)

    move(wc, 0, 1)  # REJECT: Still in Placing phase

    # Place 7 more pawns for each player.
    # No mills should be created here.
    placements = [
        (2, 5),
        (4, 7),
        (11, 8),
        (14, 10),
        (18, 12),
        (19, 16),
        (21, 20),
    ]

    for white_index, black_index in placements:
        place(wc, white_index)
        place(bc, black_index)

    # =========================================================
    # 2. MILL DURING PLACING
    # =========================================================

    # White places the 9th pawn.
    # Creates mill (0, 1, 2).
    place(wc, 1)

    remove(wc, 0)   # REJECT: Own pawn
    remove(wc, 23)  # REJECT: Empty position

    # White removes Black pawn.
    remove(wc, 3)

    # Black places the final (9th) pawn.
    place(bc, 22)

    # Both players have finished Placing.

    # =========================================================
    # 3. INVALID MOVEMENT TESTS
    # =========================================================

    place(wc, 23)   # REJECT: Not in Placing phase
    remove(wc, 5)   # REJECT: Not in Removing phase

    move(wc, 1, 1)   # REJECT: Same position
    move(wc, 1, 0)   # REJECT: Target occupied
    move(wc, 5, 9)   # REJECT: Not White's pawn
    move(wc, 1, 17)  # REJECT: Not adjacent

    # =========================================================
    # 4. FIRST MOVEMENT
    # =========================================================

    # White opens mill (0, 1, 2).
    move(wc, 1, 9)

    # =========================================================
    # 5. REPEATED MILLS
    # =========================================================

    # White repeatedly closes the mill (0, 1, 2).
    # Black moves between 5 and 6.
    #
    # Black starts with 8 remaining pawns.
    # Each iteration removes one pawn.

    for victim_index in (8, 10, 12, 16, 20):

        # Black moves pawn to position 6.
        move(bc, 5, 6)

        # White closes mill (0, 1, 2).
        move(wc, 9, 1)

        # White removes Black pawn.
        remove(wc, victim_index)

        if victim_index != 20:
            # Black moves back to position 5.
            move(bc, 6, 5)

            # White opens mill again.
            move(wc, 1, 9)

    # =========================================================
    # 6. FLYING PHASE
    # =========================================================

    # Black now has exactly 3 pawns:
    # Positions: 6, 7, 22
    #
    # Black should automatically enter Flying phase.

    # This is NOT an adjacent move.
    # It is only legal during Flying.
    move(bc, 22, 17)

    # White opens the mill.
    move(wc, 1, 9)

    # Black flies back to position 22.
    move(bc, 17, 22)

    # =========================================================
    # 7. FINAL MILL & VICTORY
    # =========================================================

    # White closes mill (0, 1, 2).
    move(wc, 9, 1)

    # Black drops from 3 to 2 pawns.
    remove(wc, 22)

    # EXPECTED:
    # GameStatus.Ended
    # GameEndedEvent(winner=Player.White)
