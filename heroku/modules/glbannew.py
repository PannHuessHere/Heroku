import re
import time
import typing

from asyncio import sleep as asleep

from telethon.tl import functions
from telethon.tl.types import (
    Channel,
    Chat,
    Message,
    User,
)

from .. import loader, utils

BANNED_RIGHTS = {
    "view_messages": False,
    "send_messages": False,
    "send_media": False,
    "send_stickers": False,
    "send_gifs": False,
    "send_games": False,
    "send_inline": False,
    "send_polls": False,
    "change_info": False,
    "invite_users": False,
}

def get_full_name(user: typing.Union[User, Channel]) -> str:
    return utils.escape_html(
        user.title
        if isinstance(user, Channel)
        else (
            f"{user.first_name} "
            + (user.last_name if getattr(user, "last_name", False) else "")
        )
    ).strip()

@loader.tds
class GlobalRestrict(loader.Module):

    strings = {
        "name": "GlobalRestrict",
        "no_reason": "Not Specified",
        "args": "<b>Invalid arguments</b>",
        "args_id": "<b>Invalid arguments</b>",
        "invalid_id": "<b>User ID must be a number</b>",
        "user_not_found": "<b>User <code>{}</code> not found</b>",
        "glban": '<b><a href="{}">{}</a></b>\n<b></b><i>{}</i>\n\n{}',
        "glbanning": ' <b>🖕 Globally banning <a href="{}">{}</a>...</b>',
        "in_n_chats": "<b>Requests successfully {} <tg-emoji emoji-id=5287497430235899641>❄️</tg-emoji></b>",
    }

    strings_ru = {
        "no_reason": "Not Specified",
        "args": "<b>Invalid arguments</b>",
        "args_id": "<b>Invalid arguments</b>",
        "invalid_id": "<b>User ID must be a number</b>",
        "user_not_found": "<b>User <code>{}</code> not found</b>",
        "glban": '<b><a href="{}">{}</a></b>\n<b></b><i>{}</i>\n\n{}',
        "glbanning": ' <b>🖕 Globally banning <a href="{}">{}</a>...</b>',
        "in_n_chats": "<b>Requests successfully {} <tg-emoji emoji-id=5287497430235899641>❄️</tg-emoji></b>",
    }

    def __init__(self):
        self._gban_cache = {}
        self._gmute_cache = {}
        self._whitelist = []

    async def watcher(self, message):
        if (not message.is_private or 
            message.sender_id == (await message.client.get_me()).id or
            message.sender_id in self._whitelist or
            not message.text):
            return
        
        if message.text.startswith('.g '):
            args = message.text[3:].strip()
            await self.process_g_command(message, args)
        elif message.text.startswith('.g2 '):
            args = message.text[4:].strip()
            await self.process_g2_command(message, args)

    async def process_g_command(self, message, args):
        if not args:
            await message.reply(self.strings("args"))
            return
        
        try:
            user = await self._client.get_entity(args.split()[0])
        except Exception:
            await message.reply(self.strings("args"))
            return
        
        processing_msg = await message.reply(
            self.strings("glbanning").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
            ),
        )

        if not self._gban_cache or self._gban_cache.get("exp", 0) < time.time():
            self._gban_cache = {
                "exp": int(time.time()) + 10 * 60,
                "chats": [
                    chat.entity.id
                    async for chat in self._client.iter_dialogs()
                    if (
                        (isinstance(chat.entity, Chat) or isinstance(chat.entity, Channel))
                        and getattr(chat.entity, "admin_rights", None)
                        and getattr(getattr(chat.entity, "admin_rights", None), "ban_users", False) is True
                        and getattr(chat.entity, "participants_count", 6) > 5
                    )
                ],
            }

        counter = 0

        for chat_id in self._gban_cache["chats"]:
            try:
                await asleep(0.02)
                await self.ban(chat_id, user, 0, self.strings("no_reason"), silent=True)
                counter += 1
            except Exception as e:
                await processing_msg.edit(f"Error in chat {chat_id}: {e}")
                continue

        first_name = user.first_name or user.username or "User"
        await processing_msg.edit(
            f"<b>{first_name} has been globally banned.</b>\n"
            f"<b>Reason:</b> {self.strings('no_reason')}\n\n"
            f"👎 <b>Banned in {counter} chat(s)</b>"
        )

    async def process_g2_command(self, message, args):
        if not args:
            await message.reply(self.strings("args_id"))
            return

        parts = args.split()
        raw_target = parts[0]
        rest = " ".join(parts[1:])

        silent = False
        if " -s" in " " + rest:
            silent = True
            rest = rest.replace(" -s", "").strip()

        t_token = ([arg for arg in rest.split() if self.convert_time(arg)] or ["0"])[0]
        period = self.convert_time(t_token)

        if t_token != "0":
            rest = rest.replace(t_token, "").replace("  ", " ").strip()

        if time.time() + period >= 2208978000:
            period = 0

        reason = utils.escape_html(rest or self.strings("no_reason")).strip()

        user = await self._resolve_user_by_arg(raw_target)
        if not user:
            await message.reply(
                self.strings("user_not_found").format(utils.escape_html(raw_target)),
            )
            return

        user_id = int(getattr(user, "id", 0)) or None
        if not user_id:
            await message.reply(
                self.strings("user_not_found").format(utils.escape_html(raw_target)),
            )
            return

        try:
            await self._client.get_messages(user, limit=1)
        except Exception:
            pass

        try:
            first_name = getattr(user, "first_name", "") or getattr(
                user, "title", "User"
            )
            last_name = getattr(user, "last_name", "") or ""

            await self._client(
                functions.contacts.AddContactRequest(
                    id=user,
                    first_name=first_name,
                    last_name=last_name,
                    phone="",
                    add_phone_privacy_exception=False,
                )
            )
        except Exception:
            pass

        processing_msg = await message.reply(
            self.strings("glbanning").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
            ),
        )

        if not self._gban_cache or self._gban_cache.get("exp", 0) < time.time():
            self._gban_cache = {
                "exp": int(time.time()) + 10 * 60,
                "chats": [
                    chat.entity.id
                    async for chat in self._client.iter_dialogs()
                    if (
                        (isinstance(chat.entity, Chat) or isinstance(chat.entity, Channel))
                        and getattr(chat.entity, "admin_rights", None)
                        and getattr(getattr(chat.entity, "admin_rights", None), "ban_users", False) is True
                        and getattr(chat.entity, "participants_count", 6) > 5
                    )
                ],
            }

        counter = 0
        for chat_id in self._gban_cache["chats"]:
            try:
                await asleep(0.02)
                await self.ban(chat_id, user_id, period, reason, silent=True)
                counter += 1
            except Exception as e:
                await processing_msg.edit(f"Error in chat {chat_id}: {e}")
                continue

        if silent:
            try:
                await processing_msg.delete()
            except Exception:
                pass
            return

        first_name = user.first_name or user.username or "User"
        await processing_msg.edit(
            f"<b>{first_name} has been globally banned.</b>\n"
            f"<b>Reason:</b> {reason}\n\n"
            f"👎 <b>Banned in {counter} chat(s)</b>"
        )

    async def _resolve_user_by_arg(self, raw: str) -> typing.Optional[User]:
        raw = raw.strip()
        if raw.lstrip("-").isdigit():
            try:
                return await self._client.get_entity(int(raw))
            except Exception:
                return None

        username = raw
        if "t.me/" in username:
            username = username.split("t.me/", maxsplit=1)[1]
        username = username.split("/", maxsplit=1)[0]
        if username.startswith("@"):
            username = username[1:]
        if not username:
            return None

        try:
            return await self._client.get_entity(username)
        except Exception:
            pass

        try:
            result = await self._client(
                functions.contacts.SearchRequest(q=username, limit=10)
            )
        except Exception:
            return None

        if not getattr(result, "users", None):
            return None

        for user in result.users:
            if getattr(user, "username", None) and user.username.lower() == username.lower():
                return user

        return result.users[0] if result.users else None

    @staticmethod
    def convert_time(t: str) -> int:
        try:
            if not t:
                return 0
            if t.endswith('d'):
                return int(t[:-1]) * 86400
            if t.endswith('h'):
                return int(t[:-1]) * 3600
            if t.endswith('m'):
                return int(t[:-1]) * 60
            if t.endswith('s'):
                return int(t[:-1])
            return int(t)
        except ValueError:
            return 0

    async def args_parser(
        self,
        message: Message,
        include_force: bool = False,
        include_silent: bool = False,
    ) -> tuple:
        args = " " + utils.get_args_raw(message)
        if include_force and " -f" in args:
            force = True
            args = args.replace(" -f", "")
        else:
            force = False

        if include_silent and " -s" in args:
            silent = True
            args = args.replace(" -s", "")
        else:
            silent = False

        args = args.strip()
        reply = await message.get_reply_message()

        if reply and not args:
            return (
                (await self._client.get_entity(reply.sender_id)),
                0,
                utils.escape_html(self.strings("no_reason")).strip(),
                *((force,) if include_force else ()),
                *((silent,) if include_silent else ()),
            )

        try:
            a = args.split()[0]
            if str(a).isdigit():
                a = int(a)
            user = await self._client.get_entity(a)
        except Exception:
            try:
                user = await self._client.get_entity(reply.sender_id)
            except Exception:
                return False

        t = ([arg for arg in args.split() if self.convert_time(arg)] or ["0"])[0]
        args = args.replace(t, "").replace("  ", " ")
        t = self.convert_time(t)

        if not reply:
            try:
                args = " ".join(args.split()[1:])
            except Exception:
                pass

        if time.time() + t >= 2208978000:
            t = 0

        return (
            user,
            t,
            utils.escape_html(args or self.strings("no_reason")).strip(),
            *((force,) if include_force else ()),
            *((silent,) if include_silent else ()),
        )

    async def ban(
        self,
        chat: typing.Union[Chat, int],
        user: typing.Union[User, Channel, int],
        period: int = 0,
        reason: str = None,
        message: typing.Optional[Message] = None,
        silent: bool = False,
    ):
        if str(user).isdigit():
            user = int(user)

        if reason is None:
            reason = self.strings("no_reason")

        await self._client.edit_permissions(
            chat,
            user,
            until_date=(time.time() + period) if period else 0,
            **BANNED_RIGHTS,
        )

        if silent:
            return

    @loader.command(
        ru_doc="<user | id> [-s] - Global ban by username or ID",
        en_doc="<user | id> [-s] - Global ban by username or ID",
    )
    async def glban(self, message):
        raw_args = utils.get_args_raw(message)

        if not raw_args:
            await utils.answer(message, self.strings("args_id"))
            return

        parts = raw_args.split()
        raw_target = parts[0]
        silent = False
        if len(parts) > 1 and parts[1] == "-s":
            silent = True

        reason = self.strings("no_reason")
        period = 0

        user = await self._resolve_user_by_arg(raw_target)
        if not user:
            await utils.answer(
                message,
                self.strings("user_not_found").format(utils.escape_html(raw_target)),
            )
            return

        user_id = int(getattr(user, "id", 0)) or None
        if not user_id:
            await utils.answer(
                message,
                self.strings("user_not_found").format(utils.escape_html(raw_target)),
            )
            return

        try:
            await self._client.get_messages(user, limit=1)
        except Exception:
            pass

        try:
            first_name = getattr(user, "first_name", "") or getattr(
                user, "title", "User"
            )
            last_name = getattr(user, "last_name", "") or ""

            await self._client(
                functions.contacts.AddContactRequest(
                    id=user,
                    first_name=first_name,
                    last_name=last_name,
                    phone="",
                    add_phone_privacy_exception=False,
                )
            )
        except Exception:
            pass

        msg = await utils.answer(
            message,
            self.strings("glbanning").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
            ),
        )

        if not self._gban_cache or self._gban_cache.get("exp", 0) < time.time():
            self._gban_cache = {
                "exp": int(time.time()) + 10 * 60,
                "chats": [
                    chat.entity.id
                    async for chat in self._client.iter_dialogs()
                    if (
                        (isinstance(chat.entity, Chat) or isinstance(chat.entity, Channel))
                        and getattr(chat.entity, "admin_rights", None)
                        and getattr(getattr(chat.entity, "admin_rights", None), "ban_users", False) is True
                        and getattr(chat.entity, "participants_count", 6) > 5
                    )
                ],
            }

        counter = 0
        for chat_id in self._gban_cache["chats"]:
            try:
                await asleep(0.02)
                await self.ban(chat_id, user_id, period, reason, silent=True)
                counter += 1
            except Exception as e:
                await utils.answer(msg, f"Error in chat {chat_id}: {e}")
                continue

        if silent:
            try:
                await msg.delete()
            except Exception:
                pass
            return

        first_name = user.first_name or user.username or "User"
        await utils.answer(
            msg,
            f"<b>{first_name} has been globally banned.</b>\n"
            f"<b>Reason:</b> {reason}\n\n"
            f"👎 <b>Banned in {counter} chat(s)</b>"
        )

    @loader.command(
        ru_doc="<user | id> [-s] - Global ban by username or ID",
        en_doc="<user | id> [-s] - Global ban by username or ID",
    )
    async def glban2(self, message):
        """Alias for .glban"""
        await self.glban(message)
