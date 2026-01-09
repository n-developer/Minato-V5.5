from typing import Union, Iterable, Optional
from datetime import datetime

from pyrogram import raw
from pyrogram.methods.messages.forward_messages import ForwardMessages
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.utils import get_raw_peer_id


class ForwardMessagesWithButtons(ForwardMessages):
    async def forward_messages_with_buttons(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_ids: Union[int, Iterable[int]],
        disable_notification: bool = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ):
        """
        Forward messages and attach inline buttons by editing reply_markup.

        Telegram does not allow modifying forwarded content, but reply_markup
        can be edited after forwarding.
        """

        result = await self.invoke(
            raw.functions.messages.ForwardMessages(
                to_peer=await self.resolve_peer(chat_id),
                from_peer=await self.resolve_peer(from_chat_id),
                id=list(message_ids) if not isinstance(message_ids, int) else [message_ids],
                silent=disable_notification,
                schedule_date=schedule_date,
                drop_author=protect_content,
                drop_media_captions=False,
                random_id=[self.rnd_id()]
            )
        )

        messages = await self.parse_messages(result)

        if reply_markup:
            for msg in messages:
                await self.invoke(
                    raw.functions.messages.EditMessage(
                        peer=get_raw_peer_id(chat_id),
                        id=msg.id,
                        reply_markup=reply_markup.write()
                    )
                )

        return messages
