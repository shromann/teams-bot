# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount

from conn import init_sessions, delete_sessions, prompt

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    id: str

    async def on_message_activity(self, turn_context: TurnContext):
        responses = prompt(self.id, turn_context.activity.text)
        await turn_context.send_activity(responses)

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                self.id = member_added.id
                init_sessions(self.id)
                await turn_context.send_activity(f"Hello {member_added.name} and welcome!")


    async def on_end_of_conversation_activity(  # pylint: disable=unused-argument
        self, turn_context: TurnContext
    ):
        await turn_context.send_activity("Goodbye!")
        delete_sessions(self.id)