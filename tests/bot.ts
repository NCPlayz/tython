import { Message } from 'discord';
import { Cog, Context, Bot, command } from 'discord/ext/commands';

const token = 'TOKEN';
let client = new Bot();

async function on_ready() {
    print('test');
}

async function on_message(message: Message) {
    await message.channel.send('no');
}

client.event(on_ready);
client.event(on_message);

class CoolCog extends Cog {
    @command()
    async test(ctx: Context) {
        await ctx.send('no');
    }
}

client.add_cog(new CoolCog());
client.run(token);

