from zulip_bots.test_lib import BotTestCase, DefaultTests


class TestHelpBot(BotTestCase, DefaultTests):
    bot_name: str = "matcher"

    def test_bot(self) -> None:
        dialog = [
            ("", "hello rc"),
            ("help", "hello rc"),
            ("foo", "hello rc"),
        ]

        self.verify_dialog(dialog)
