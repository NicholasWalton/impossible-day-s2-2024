# See readme.md for instructions on running this code.

import logging
from collections import OrderedDict
from pprint import pformat
from typing import Any, Dict

import zulip
from zulip_bots.lib import BotHandler

logging.basicConfig(level=logging.DEBUG)


class MatcherHandler:
    def __init__(self) -> None:
        self.client = zulip.Client()
        self._ready_to_pair = OrderedDict()
        nicholas = 731920
        sender_profile = self.get_profile(nicholas)
        logging.debug("Nicholas is: " + pformat(sender_profile))
        request = {
            "type": "direct",
            "to": [nicholas],
            "content": f"good morning from {self} via {self.client}!",
        }
        logging.debug("Greeting result: " + pformat(self.client.send_message(request)))

    def get_profile(self, user_id):
        profile_response = self.client.get_user_by_id(
            user_id, include_custom_profile_fields=True
        )
        if profile_response["result"] != "success":
            logging.warn(
                f"Failed to get_user_by_id({user_id}), response was {pformat(profile_response)}"
            )
            raise ZulipApiFailed(profile_response)
        return profile_response["user"]

    def usage(self) -> str:
        return """
        This bot finds you a pairing partner!
        """

    def handle_message(self, message: Dict[str, Any], bot_handler: BotHandler) -> None:
        sender_id = message["sender_id"]
        try:
            sender_profile = self.get_profile(sender_id)

            if message["type"] == "private":
                content, emoji_name = self._handle_private_message(
                    message, sender_profile
                )
            else:
                self._usage_response(sender_profile)
        except ZulipApiFailed:
            content = "An error occurred!"
            emoji_name = "crash"
        bot_handler.send_reply(message, content)
        bot_handler.react(message, emoji_name)

    def _usage_response(self, sender_profile):
        return (
            f"Hello {sender_profile['full_name']}! To pair now, say 'pair now'",
            "question",
        )

    def _handle_private_message(self, message, sender_profile):
        if message["full_content"] == "pair now":
            logging.debug(f"Attempting to pair up {pformat(sender_profile)}")
            try:
                return self._pair_now(sender_profile), "pear"
            except ProfileNotFound:
                return (
                    "Could not find your RC Directory Profile link in your Zulip profile, please update your Zulip profile at https://recurse.zulipchat.com/#settings/profile",
                    "interrobang",
                )
        return self._usage_response(sender_profile)

    def _pair_now(self, sender_profile):
        pairing_profile = self._get_rc_directory_link(sender_profile)
        sender_id = sender_profile["user_id"]
        try:
            partner = self._ready_to_pair.popitem()
            message = f"You paired with {partner}"
        except KeyError:  # dictionary is empty
            self._ready_to_pair[sender_id] = pairing_profile
            logging.info(f"Added {sender_id} to queue")
            message = "You've been added to the queue"

        logging.debug(f"Ready to pair: {self._ready_to_pair}")
        return message

    def _get_rc_directory_link(self, sender_profile):
        try:
            return sender_profile["profile_data"]["5313"]["value"]
        except KeyError as e:
            raise ProfileNotFound(e)


class ProfileNotFound(Exception):
    pass


class ZulipApiFailed(Exception):
    pass


handler_class = MatcherHandler
