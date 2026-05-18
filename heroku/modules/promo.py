import asyncio
import typing
from .. import loader, utils


@loader.tds
class PromoModule(loader.Module):
    """Modul promosi otomatis — reply pesan dengan .promo <waktu>"""

    strings = {
        "name": "Promo",
        "started": "<b>✅ Promosi dimulai setiap {}</b>",
        "stopped": "<b>🛑 Semua promosi dihentikan</b>",
        "no_reply": "<b>❌ Reply pesan yang ingin dipromosikan</b>",
        "no_args": "<b>❌ Contoh: .promo 30s / .promo 5m / .promo 1h</b>",
        "list_empty": "<b>📭 Tidak ada promosi aktif</b>",
        "list": "<b>📋 Promosi aktif:</b>\n{}",
        "stopped_one": "<b>🛑 Promosi di chat ini dihentikan</b>",
        "not_found": "<b>❌ Tidak ada promosi aktif di chat ini</b>",
    }

    def __init__(self):
        self._tasks: typing.Dict[int, asyncio.Task] = {}

    def convert_time(self, t: str) -> int:
        """Convert waktu ke detik"""
        try:
            if not t:
                return 0
            if t.endswith('h'):
                return int(t[:-1]) * 3600
            if t.endswith('m'):
                return int(t[:-1]) * 60
            if t.endswith('s'):
                return int(t[:-1])
            return int(t)
        except ValueError:
            return 0

    def format_time(self, seconds: int) -> str:
        """Format detik ke string yang mudah dibaca"""
        if seconds >= 3600:
            return f"{seconds // 3600}h"
        if seconds >= 60:
            return f"{seconds // 60}m"
        return f"{seconds}s"

    async def _promo_loop(self, chat_id: int, message_id: int, delay: int):
        """Loop kirim pesan promosi"""
        try:
            while True:
                await asyncio.sleep(delay)
                try:
                    # Ambil pesan asli
                    msg = await self._client.get_messages(chat_id, ids=message_id)
                    if msg:
                        # Forward/kirim ulang pesan
                        await self._client.send_message(
                            chat_id,
                            msg.text or msg.message,
                            file=msg.media if msg.media else None,
                            parse_mode="html",
                        )
                except Exception:
                    pass
        except asyncio.CancelledError:
            pass

    @loader.command(
        en_doc="<waktu> — Reply pesan untuk dipromosikan. Contoh: .promo 30s / .promo 5m / .promo 1h",
    )
    async def promo(self, message):
        """Reply pesan yang ingin dipromosikan dengan .promo <waktu>"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings("no_reply"))
            return

        args = utils.get_args_raw(message).strip()
        if not args:
            await utils.answer(message, self.strings("no_args"))
            return

        delay = self.convert_time(args)
        if delay <= 0:
            await utils.answer(message, self.strings("no_args"))
            return

        chat_id = message.chat_id

        # Stop task lama kalau ada
        if chat_id in self._tasks:
            self._tasks[chat_id].cancel()

        # Buat task baru
        task = asyncio.ensure_future(
            self._promo_loop(chat_id, reply.id, delay)
        )
        self._tasks[chat_id] = task

        await utils.answer(
            message,
            self.strings("started").format(self.format_time(delay)),
        )

    @loader.command(
        en_doc="Stop promosi di chat ini",
    )
    async def promooff(self, message):
        """Stop promosi di chat ini"""
        chat_id = message.chat_id

        if chat_id not in self._tasks:
            await utils.answer(message, self.strings("not_found"))
            return

        self._tasks[chat_id].cancel()
        del self._tasks[chat_id]
        await utils.answer(message, self.strings("stopped_one"))

    @loader.command(
        en_doc="Stop semua promosi aktif",
    )
    async def promooffall(self, message):
        """Stop semua promosi aktif"""
        if not self._tasks:
            await utils.answer(message, self.strings("list_empty"))
            return

        for task in self._tasks.values():
            task.cancel()
        self._tasks.clear()
        await utils.answer(message, self.strings("stopped"))

    @loader.command(
        en_doc="Lihat daftar promosi aktif",
    )
    async def promolist(self, message):
        """Lihat daftar promosi aktif"""
        if not self._tasks:
            await utils.answer(message, self.strings("list_empty"))
            return

        lines = []
        for i, chat_id in enumerate(self._tasks.keys(), 1):
            try:
                entity = await self._client.get_entity(chat_id)
                name = getattr(entity, "title", str(chat_id))
            except Exception:
                name = str(chat_id)
            lines.append(f"{i}. <b>{name}</b> — <code>{chat_id}</code>")

        await utils.answer(
            message,
            self.strings("list").format("\n".join(lines)),
        )
