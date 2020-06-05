from discord import Message
from discord.ext.commands import Cog, Context, Bot, command
token = 'TOKEN'
client = Bot() # TODO: add kwargs


async def on_ready():
    print('test')


async def on_message(message: Message):
    await message.channel.send('no')


client.event(on_ready)
client.event(on_message)


class CoolCog(Cog):

    @command()
    async def test(self, ctx: Context):
        await ctx.send('no')


client.add_cog(CoolCog())
client.run(token)

