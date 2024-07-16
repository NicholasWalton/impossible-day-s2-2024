# See readme.md for instructions on running this code.

from typing import Any, Dict

from zulip_bots.lib import BotHandler


class HelloRcHandler:
    def usage(self) -> str:
        return """
        This is a boilerplate bot that responds to a user query with
        "beep boop", which is robot for "Hello World".

        This bot can be used as a template for other, more
        sophisticated, bots.
        """

    def handle_message(self, message: Dict[str, Any], bot_handler: BotHandler) -> None:
        content = "hello rc"
        bot_handler.send_reply(message, content)

        emoji_name = "octopus"
        bot_handler.react(message, emoji_name)


handler_class = HelloRcHandler
