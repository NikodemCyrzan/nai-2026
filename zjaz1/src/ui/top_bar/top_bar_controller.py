from ui.top_bar.top_bar_view import TopBarView

# TODO: Implement controller
class TopBarController:
    def __init__(self, topBarView: TopBarView):
        topBarView.set_state(9, 9, True, "Your turn")