import { Client, Message } from 'discord';

const token = 'TOKEN';
let client = new Client();

async function on_ready() {
    print('test');
}

async function on_message(message: Message) {
    await message.channel.send('no');
}

client.event(on_ready);
client.event(on_message);

client.run(token);

