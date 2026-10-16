from controller.game_controller import GameController
from controller.actions import (
    GameStartAction,
    PlayerPlacePawnAction,
    PlayerMovePawnAction,
    PlayerRemovePawnAction,
)


def place(controller: GameController, index: int) -> None:
    controller.perform(PlayerPlacePawnAction(at_index=index))


def move(controller: GameController, source: int, target: int) -> None:
    controller.perform(
        PlayerMovePawnAction(from_index=source, to_index=target)
    )


def remove(controller: GameController, index: int) -> None:
    controller.perform(PlayerRemovePawnAction(at_index=index))


def game_scenario_1(wc: GameController, bc: GameController) -> None:

    # ==========================================================
    # 1. START VALIDATION
    # ==========================================================

    place(wc, 0)                # REJECT: Game not started

    wc.perform(GameStartAction())
    wc.perform(GameStartAction())  # REJECT: Already started

    place(bc, 3)                # REJECT: Not Black's turn

    # ==========================================================
    # 2. PLACING PHASE (8 PAWNS EACH)
    # ==========================================================

    place(wc, 0)
    place(bc, 0)                # REJECT: Occupied
    place(bc, 3)

    move(wc, 0, 1)              # REJECT: Still placing

    placements = [
        (2, 5),
        (4, 7),
        (11, 15),
        (14, 10),
        (18, 12),
        (19, 16),
        (21, 20),
    ]

    for white_index, black_index in placements:
        place(wc, white_index)
        place(bc, black_index)

    # ==========================================================
    # 3. WHITE MILL DURING PLACING
    # ==========================================================

    place(wc, 1)  # White mill: (0, 1, 2)

    remove(wc, 0)   # REJECT: Own pawn
    remove(wc, 23)  # REJECT: Empty

    remove(wc, 3)   # ACCEPT: Black loses first pawn

    # ==========================================================
    # 4. BLACK MILL DURING PLACING
    # ==========================================================

    place(bc, 23)  # Black mill: (7, 15, 23)

    # White's (0, 1, 2) mill is protected.
    remove(bc, 0)   # REJECT: Protected pawn

    remove(bc, 19)  # ACCEPT: Unprotected White pawn

    # Both players have placed all 9 pawns.

    # ==========================================================
    # 5. INVALID MOVEMENTS
    # ==========================================================

    remove(wc, 5)    # REJECT: Not removing
    place(wc, 22)    # REJECT: Not placing

    move(wc, 1, 1)   # REJECT: Same position
    move(wc, 1, 0)   # REJECT: Target occupied
    move(wc, 5, 9)   # REJECT: Not own pawn
    move(wc, 1, 17)  # REJECT: Not adjacent

    # ==========================================================
    # 6. OPEN FIRST MILL
    # ==========================================================

    move(wc, 1, 9)

    # Black has not reached Flying yet.
    move(bc, 23, 17)  # REJECT: Not adjacent

    move(bc, 5, 6)

    # White closes (0, 1, 2).
    move(wc, 9, 1)

    # Black has a protected mill (7, 15, 23)
    # but also unprotected pawns.
    remove(wc, 7)    # REJECT: Protected

    remove(wc, 10)   # ACCEPT

    # ==========================================================
    # 7. REPEATED MILL FORMATION
    # ==========================================================

    # White repeatedly opens and closes (0, 1, 2).
    # Black alternates between positions 5 and 6.

    for victim in (12, 16, 20):
        move(bc, 6, 5)
        move(wc, 1, 9)

        move(bc, 5, 6)
        move(wc, 9, 1)

        remove(wc, victim)

    # Black has 4 pawns remaining:
    # 6, 7, 15, 23

    # ==========================================================
    # 8. BLACK ENTERS FLYING
    # ==========================================================

    move(bc, 6, 5)
    move(wc, 1, 9)

    move(bc, 5, 6)
    move(wc, 9, 1)

    remove(wc, 6)

    # Black now has 3 pawns: 7, 15, 23.
    # Expected phase: PlayerPhase.Flying

    # ==========================================================
    # 9. FLYING AND ANOTHER BLACK MILL
    # ==========================================================

    # Not adjacent, but legal during Flying.
    move(bc, 23, 17)

    # White opens its mill.
    move(wc, 1, 9)

    # Black flies back and recreates (7, 15, 23).
    move(bc, 17, 23)

    # Black gets a capture.
    remove(bc, 14)

    # ==========================================================
    # 10. REMOVE A PROTECTED PAWN
    # ==========================================================

    move(wc, 9, 1)  # White mill: (0, 1, 2)

    # Every remaining Black pawn belongs to (7, 15, 23).
    # Therefore, removing a protected pawn is now legal.
    remove(wc, 7)

    # ==========================================================
    # 11. WHITE WINS
    # ==========================================================

    # Black: 15, 23 -> only 2 pawns remaining.
    # EXPECTED: GameEndedEvent(winner=Player.White)

    move(bc, 23, 17)  # REJECT: Game ended
    place(wc, 9)       # REJECT: Game ended
    wc.perform(GameStartAction())  # REJECT: Already started

def game_scenario_2_blocking(
    wc: GameController,
    bc: GameController,
) -> None:

    wc.perform(GameStartAction())

    # ==========================================================
    # 1. PLACING
    # ==========================================================

    placements = [
        (0, 1),
        (4, 2),
        (6, 3),
        (9, 5),
        (12, 7),
        (13, 8),
        (15, 10),
        (17, 18),
        (20, 19),
    ]

    for white_index, black_index in placements:
        place(wc, white_index)
        place(bc, black_index)

    # ==========================================================
    # 2. BLOCK BLACK
    # ==========================================================

    # Position 11 is the last available
    # neighbouring empty position for Black.
    # White moves from 12 to 11.

    move(wc, 12, 11)

    # Black now has 9 pawns but no legal movement.
    # EXPECTED: GameEndedEvent(winner=Player.White)

    move(bc, 1, 0)  # REJECT: Game ended

from game import Game
from model.player import Player, PlayerHasMillEvent
from logic.game_logic import GameEndedEvent, GameExceptionEvent


def verify_scenario(scenario, expect_mills: bool) -> None:
    game = Game()

    winners: list[Player] = []
    errors: list[str] = []
    mills: list[tuple[Player, tuple[int, int, int]]] = []

    game.bus.subscribe(
        GameEndedEvent,
        lambda event: winners.append(event.winner),
    )

    game.bus.subscribe(
        GameExceptionEvent,
        lambda event: errors.append(event.message),
    )

    game.bus.subscribe(
        PlayerHasMillEvent,
        lambda event: mills.append((event.player, event.mill)),
    )

    scenario(game.white_controller, game.black_controller)

    assert winners == [Player.White], winners

    if expect_mills:
        assert mills.count((Player.White, (0, 1, 2))) == 7
        assert (Player.Black, (7, 15, 23)) in mills
        assert "Nie można usunąć chronionego pionka!" in errors
    else:
        assert not mills, mills

    print(f"{scenario.__name__}: PASSED")
    print(f"  Mills: {len(mills)}")
    print(f"  Expected rejections: {len(errors)}")
    print(f"  Winner: {winners[0]}")
