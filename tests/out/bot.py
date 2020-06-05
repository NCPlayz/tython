from discord import Client, Message
token = 'TOKEN'
client = Client()


async def on_ready():
    print('test')


async def on_message(message: Message):
    await message.channel.send('no')


client.event(on_ready)
client.event(on_message)
client.run(token)

