#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# Some functions took from Hikarichat by Hikariatama

# ---------------------------------------------------------------------------------

# Proprietary License Agreement

# Copyright (c) 2024-29 CodWiz

# Permission is hereby granted to any person obtaining a copy of this software and associated documentation files (the "Software"), to use the Software for personal and non-commercial purposes, subject to the following conditions:

# 1. The Software may not be modified, altered, or otherwise changed in any way without the explicit written permission of the author.

# 2. Redistribution of the Software, in original or modified form, is strictly prohibited without the explicit written permission of the author.

# 3. The Software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the author or copyright holder be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the Software or the use or other dealings in the Software.

# 4. Any use of the Software must include the above copyright notice and this permission notice in all copies or substantial portions of the Software.

# 5. By using the Software, you agree to be bound by the terms and conditions of this license.

# For any inquiries or requests for permissions, please contact codwiz@yandex.ru.

# ---------------------------------------------------------------------------------
# Name: Snoser
# Description: Global snos whore bots
# Author: @clickDeak
# ---------------------------------------------------------------------------------
# meta developer: @clickDeak
# ---------------------------------------------------------------------------------

import re
import time
import typing

from telethon.tl.types import (
    Channel,
    Chat,
    Message,
    User,
    ChannelForbidden,
    ChatForbidden,
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

MUTES_RIGHTS = {
    "view_messages": True,
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

EXCEPTIONS = [
    1026050835,
    1605486033,
    8343611888,
]
    
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
class Yayz(loader.Module):
    """Global Snos whore bots"""

    strings = {
        "name": "Yayz",
        "no_reason": "Not specified",
        "args": (
            "<emoji document_id=5300759756669984376>🚫</emoji> <b>Incorrect arguments</b>"
        ),
        "glban": (
            '<emoji document_id=5301059317753979286>🖕</emoji> <b><a href="{}">{}</a>'
            " has been globally banned.</b>\n<b>Reason: </b><i>{}</i>\n\n{}"
        ),
        "glbanning": (
            "<emoji document_id=5301059317753979286>🖕</emoji> <b>Globally banning <a"
            ' href="{}">{}</a>...</b>'
        ),
        "gunban": (
            '<emoji document_id=6334872157947955302>🤗</emoji> <b><a href="{}">{}</a>'
            " has been globally unbanned.</b>\n\n{}"
        ),
        "gunbanning": (
            "<emoji document_id=6334872157947955302>🤗</emoji> <b>Global unbanning <a"
            ' href="{}">{}</a>...</b>'
        ),
        "in_n_chats": (
            "<emoji document_id=5379568936218009290>👎</emoji> <b>Banned in {}"
            " chat(s)</b>"
        ),
        "unbanned_in_n_chats": (
            "<emoji document_id=5461129450341014019>✋️</emoji> <b>Unbanned in {}"
            " chat(s)</b>"
        ),
        "glmute": (
            '<emoji document_id=5301059317753979286>🖕</emoji> <b><a href="{}">{}</a>'
            " has been globally muted.</b>\n<b>Reason: </b><i>{}</i>\n\n{}"
        ),
        "glmutes": (
            "<emoji document_id=5301059317753979286>🖕</emoji> <b>Global mute <a"
            ' href="{}">{}</a>...</b>'
        ),
        "gunmute": (
            '<emoji document_id=6334872157947955302>🤗</emoji> <b><a href="{}">{}</a>'
            " has been globally unmuted.</b>\n\n{}"
        ),
        "gunmutes": (
            "<emoji document_id=6334872157947955302>🤗</emoji> <b>Global unmute <a"
            ' href="{}">{}</a>...</b>'
        ),
        "in_m_chats": (
            "<emoji document_id=5379568936218009290>👎</emoji> <b>Muted in {}"
            " chat(s)</b>"
        ),
        "unmute_in_n_chats": (
            "<emoji document_id=5461129450341014019>✋️</emoji> <b>Unmuted in {}"
            " chat(s)</b>"
        ),
    }

    strings_ru = {
        "no_reason": "Не указана",
        "args": (
            "<emoji document_id=5300759756669984376>🚫</emoji> <b>Неверные"
            " аргументы</b>"
        ),
        "glban": (
            '<emoji document_id=5301059317753979286>🖕</emoji> <b><a href="{}">{}</a>'
            " был гзабанен.</b>\n<b>Причина: </b><i>{}</i>\n\n{}"
        ),
        "glbanning": (
            "<emoji document_id=5301059317753979286>🖕</emoji> <b>Гбан <a"
            ' href="{}">{}</a>...</b>'
        ),
        "gunban": (
            '<emoji document_id=6334872157947955302>🤗</emoji> <b><a href="{}">{}</a>'
            " был гразбанен.</b>\n\n{}"
        ),
        "gunbanning": (
            "<emoji document_id=6334872157947955302>🤗</emoji> <b>Гразбан <a"
            ' href="{}">{}</a>...</b>'
        ),
        "in_n_chats": (
            "<emoji document_id=5379568936218009290>👎</emoji> <b>Забанил в {}"
            " чат(-ах)</b>"
        ),
        "unbanned_in_n_chats": (
            "<emoji document_id=5461129450341014019>✋️</emoji> <b>Разбанил in {}"
            " чат(-ах)</b>"
        ),
        "glmute": (
            '<emoji document_id=5301059317753979286>🖕</emoji> <b><a href="{}">{}</a>'
            " был замучен.</b>\n<b>Причина: </b><i>{}</i>\n\n{}"
        ),
        "glmutes": (
            "<emoji document_id=5301059317753979286>🖕</emoji> <b>Гмут <a"
            ' href="{}">{}</a>...</b>'
        ),
        "gunmute": (
            '<emoji document_id=6334872157947955302>🤗</emoji> <b><a href="{}">{}</a>'
            " был размучен.</b>\n\n{}"
        ),
        "gunmutes": (
            "<emoji document_id=6334872157947955302>🤗</emoji> <b>Гразмут <a"
            ' href="{}">{}</a>...</b>'
        ),
        "in_m_chats": (
            "<emoji document_id=5379568936218009290>👎</emoji> <b>Мут в {} чат(-ах)</b>"
        ),
        "unmute_in_n_chats": (
            "<emoji document_id=5461129450341014019>✋️</emoji> <b>Размут in {}"
            " чат(-ах)</b>"
        ),
    }

    def __init__(self):
        self._gban_cache = {}
        self._gmute_cache = {}
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
            "except_ids",
            doc="айди чатов, что над исключить из глобана",
            default=EXCEPTIONS, 
            validator=loader.validators.Series(loader.validators.Integer())
            )
        )

    @staticmethod
    def convert_time(t: str) -> int:
        """
        Tries to export time from text
        """
        try:
            if not str(t)[:-1].isdigit():
                return 0

            if "d" in str(t):
                t = int(t[:-1]) * 60 * 60 * 24

            if "h" in str(t):
                t = int(t[:-1]) * 60 * 60

            if "m" in str(t):
                t = int(t[:-1]) * 60

            if "s" in str(t):
                t = int(t[:-1])

            t = int(re.sub(r"[^0-9]", "", str(t)))
        except ValueError:
            return 0

        return t

    async def args_parser(
            self,
            message: Message,
            include_force: bool = False,
            include_silent: bool = False,
        ) -> tuple:
            """Get args from message (supports ID, username, and replies)"""
            args = " " + utils.get_args_raw(message)
            
            # Обработка флагов
            force = False
            if include_force and " -f" in args:
                force = True
                args = args.replace(" -f", "")

            silent = False
            if include_silent and " -s" in args:
                silent = True
                args = args.replace(" -s", "")

            args = args.strip()
            reply = await message.get_reply_message()

            user = None
            t = 0
            reason = self.strings("no_reason")

            # 1. Сначала пробуем достать ID или юзернейм из текста
            if args:
                parts = args.split()
                potential_id = parts[0]
                
                try:
                    # Если это число (ID), конвертируем в int
                    if potential_id.replace("-", "").isdigit():
                        entity_id = int(potential_id)
                    else:
                        entity_id = potential_id # Юзернейм
                    
                    user = await self._client.get_entity(entity_id)
                    
                    # Если получилось найти пользователя, убираем его из строки причины
                    args = " ".join(parts[1:]) 
                except Exception:
                    user = None

            # 2. Если в тексте ничего нет, пробуем реплай
            if not user and reply:
                user = await self._client.get_entity(reply.sender_id)

            # Если пользователя найти не удалось
            if not user:
                return False

            # Поиск времени в оставшихся аргументах
            t_arg = ([arg for arg in args.split() if self.convert_time(arg)] or ["0"])[0]
            if t_arg != "0":
                t = self.convert_time(t_arg)
                args = args.replace(t_arg, "").replace("  ", " ").strip()

            if time.time() + t >= 2208978000:  # Лимит до 2040 года
                t = 0

            final_reason = utils.escape_html(args or self.strings("no_reason")).strip()

            return (
                user,
                t,
                final_reason,
                *((force,) if include_force else []),
                *((silent,) if include_silent else []),
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
        """Ban user in chat"""
        if str(user).isdigit():
            user = int(user)

        if reason is None:
            reason = self.strings("no_reason")

        try:
            await self.inline.bot.kick_chat_member(
                int(f"-100{getattr(chat, 'id', chat)}"),
                int(getattr(user, "id", user)),
            )
        except Exception:
            await self._client.edit_permissions(
                chat,
                user,
                until_date=(time.time() + period) if period else 0,
                **BANNED_RIGHTS,
            )

        if silent:
            return

    async def mute(
        self,
        chat: typing.Union[Chat, int],
        user: typing.Union[User, Channel, int],
        period: int = 0,
        reason: str = None,
        message: typing.Optional[Message] = None,
        silent: bool = False,
    ):
        """Mute user in chat"""
        if str(user).isdigit():
            user = int(user)

        if reason is None:
            reason = self.strings("no_reason")

        try:
            await self.inline.bot.restrict_chat_member(
                int(f"-100{getattr(chat, 'id', chat)}"),
                int(getattr(user, "id", user)),
            )
        except Exception:
            await self._client.edit_permissions(
                chat,
                user,
                until_date=(time.time() + period) if period else 0,
                **MUTES_RIGHTS,
            )

        if silent:
            return

    @loader.command(
        ru_doc="<реплай | юзер> [причина] [-s] - Забанить пользователя во всех чатах где ты админ",
        en_doc="<replay | user> [reason] [-s] - Ban the user in all chats where you are the admin",
    )
    async def glban(self, message):
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        if not reply and not args:
            await utils.answer(message, self.strings("args"))
            return

        a = await self.args_parser(message, include_silent=True)

        if not a:
            await utils.answer(message, self.strings("args"))
            return

        user, t, reason, silent = a

        message = await utils.answer(
            message,
            self.strings("glbanning").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
            ),
        )

        if not self._gban_cache or self._gban_cache["exp"] < time.time():
            self._gban_cache = {
                "exp": int(time.time()) + 10 * 60,
                "chats": [
                    chat.entity.id
                    async for chat in self._client.iter_dialogs()
                    if (
                        (
                            isinstance(chat.entity, Chat)
                            or (
                                isinstance(chat.entity, Channel)
                                and getattr(chat.entity, "megagroup", False) or getattr(chat.entity, "broadcast", False)
                            )
                        )
                        and not isinstance(chat.entity, ChannelForbidden)
                        and not isinstance(chat.entity, ChatForbidden)
                        and chat.entity.id not in self.config["except_ids"]
                        and chat.entity.admin_rights
                        and chat.entity.participants_count > 2
                        and chat.entity.admin_rights.ban_users
                    )
                ],
            }

        chats = ""
        counter = 0

        for chat in self._gban_cache["chats"]:
            try:
                await self.ban(chat, user, 0, reason, silent=True)
            except Exception:
                pass
            else:
                chats += '▫️ <b><a href="{}">{}</a></b>\n'.format(
                    utils.get_entity_url(await self._client.get_entity(chat, exp=0)),
                    utils.escape_html(
                        get_full_name(await self._client.get_entity(chat, exp=0))
                    ),
                )
                counter += 1

        await utils.answer(
            message,
            self.strings("glban").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
                reason,
                self.strings("in_n_chats").format(counter) if silent else chats,
            ),
        )

    @loader.command(
        ru_doc="<реплай | юзер> [причина] [-s] - Разбанить пользователя во всех где ты админ",
        en_doc="<replay | user> [reason] [-s] - To unban the user in all where you are the admin",
    )
    async def glunban(self, message: Message):
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        if not reply and not args:
            await utils.answer(message, self.strings("args"))
            return

        a = await self.args_parser(message, include_silent=True)

        if not a:
            await utils.answer(message, self.strings("args"))
            return

        user, t, reason, silent = a

        message = await utils.answer(
            message,
            self.strings("gunbanning").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
            ),
        )

        if not self._gban_cache or self._gban_cache["exp"] < time.time():
            self._gban_cache = {
                "exp": int(time.time()) + 10 * 60,
                "chats": [
                    chat.entity.id
                    async for chat in self._client.iter_dialogs()
                    if (
                        (
                            isinstance(chat.entity, Chat)
                            or (
                                isinstance(chat.entity, Channel)
                                and chat.entity.id != 2685666919
                                and getattr(chat.entity, "megagroup", False) or getattr(chat.entity, "broadcast", False)
                            )
                        )
                        and not isinstance(chat.entity, ChannelForbidden)
                        and not isinstance(chat.entity, ChatForbidden)
                        and chat.entity.admin_rights
                        and chat.entity.participants_count > 2
                        and chat.entity.admin_rights.ban_users
                    )
                ],
            }

        chats = ""
        counter = 0

        for chat in self._gban_cache["chats"]:
            try:
                await self._client.edit_permissions(
                    chat,
                    user,
                    until_date=0,
                    **{right: True for right in BANNED_RIGHTS.keys()},
                )
            except Exception:
                pass
            else:
                chats += '▫️ <b><a href="{}">{}</a></b>\n'.format(
                    utils.get_entity_url(await self._client.get_entity(chat, exp=0)),
                    utils.escape_html(
                        get_full_name(await self._client.get_entity(chat, exp=0))
                    ),
                )
                counter += 1

        await utils.answer(
            message,
            self.strings("gunban").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
                (
                    self.strings("unbanned_in_n_chats").format(counter)
                    if silent
                    else chats
                ),
            ),
        )

    @loader.command(
        ru_doc="<реплай | юзер> [причина] [-s] - Замутить пользователя во всех чатах где ты админ",
        en_doc="<replay | user> [reason] [-s] - To hook up the user in all chats where you are the admin",
    )
    async def glmute(self, message):
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        if not reply and not args:
            await utils.answer(message, self.strings("args"))
            return

        a = await self.args_parser(message, include_silent=True)

        if not a:
            await utils.answer(message, self.strings("args"))
            return

        user, t, reason, silent = a

        message = await utils.answer(
            message,
            self.strings("glmutes").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
            ),
        )

        if not self._gmute_cache or self._gmute_cache["exp"] < time.time():
            self._gmute_cache = {
                "exp": int(time.time()) + 10 * 60,
                "chats": [
                    chat.entity.id
                    async for chat in self._client.iter_dialogs()
                    if (
                        (
                            isinstance(chat.entity, Chat)
                            or (
                                isinstance(chat.entity, Channel)
                                and chat.entity.id != 2685666919
                                and getattr(chat.entity, "megagroup", False) or getattr(chat.entity, "broadcast", False)
                            )
                        )
                        and not isinstance(chat.entity, ChannelForbidden)
                        and not isinstance(chat.entity, ChatForbidden)
                        and chat.entity.admin_rights
                        and chat.entity.participants_count > 2
                        and chat.entity.admin_rights.ban_users
                    )
                ],
            }

        chats = ""
        counter = 0

        for chat in self._gmute_cache["chats"]:
            try:
                await self.mute(chat, user, 0, reason, silent=True)
            except Exception:
                pass
            else:
                chats += '▫️ <b><a href="{}">{}</a></b>\n'.format(
                    utils.get_entity_url(await self._client.get_entity(chat, exp=0)),
                    utils.escape_html(
                        get_full_name(await self._client.get_entity(chat, exp=0))
                    ),
                )
                counter += 1

        await utils.answer(
            message,
            self.strings("glmute").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
                reason,
                self.strings("in_m_chats").format(counter) if silent else chats,
            ),
        )

    @loader.command(
        ru_doc="<реплай | юзер> [причина] [-s] - Размутит пользователя во всех где ты админ",
        en_doc="<replay | user> [reason] [-s] - Will confuse the user in all where you are the admin",
    )
    async def glunmute(self, message: Message):
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        if not reply and not args:
            await utils.answer(message, self.strings("args"))
            return

        a = await self.args_parser(message, include_silent=True)

        if not a:
            await utils.answer(message, self.strings("args"))
            return

        user, t, reason, silent = a

        message = await utils.answer(
            message,
            self.strings("gunmutes").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
            ),
        )

        if not self._gmute_cache or self._gmute_cache["exp"] < time.time():
            self._gmute_cache = {
                "exp": int(time.time()) + 10 * 60,
                "chats": [
                    chat.entity.id
                    async for chat in self._client.iter_dialogs()
                    if (
                        (
                            isinstance(chat.entity, Chat)
                            or (
                                isinstance(chat.entity, Channel)
                                and chat.entity.id != 2685666919
                                and getattr(chat.entity, "megagroup", False) or getattr(chat.entity, "broadcast", False)
                            )
                        )
                        and not isinstance(chat.entity, ChannelForbidden)
                        and not isinstance(chat.entity, ChatForbidden)
                        and chat.entity.admin_rights
                        and chat.entity.participants_count > 2
                        and chat.entity.admin_rights.ban_users
                    )
                ],
            }

        chats = ""
        counter = 0

        for chat in self._gmute_cache["chats"]:
            try:
                await self._client.edit_permissions(
                    chat,
                    user,
                    until_date=0,
                    **{right: True for right in MUTES_RIGHTS.keys()},
                )
            except Exception:
                pass
            else:
                chats += '▫️ <b><a href="{}">{}</a></b>\n'.format(
                    utils.get_entity_url(await self._client.get_entity(chat, exp=0)),
                    utils.escape_html(
                        get_full_name(await self._client.get_entity(chat, exp=0))
                    ),
                )
                counter += 1

        await utils.answer(
            message,
            self.strings("gunmute").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
                (
                    self.strings("unmutes_in_n_chats").format(counter)
                    if silent
                    else chats
                ),
            ),
        )