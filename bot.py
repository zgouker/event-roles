import discord,time

tokenfile = open("private/token.dat","r")
token = tokenfile.read()
serverfile = open("private/server.txt","r")
server_id = int(serverfile.read())
intents = discord.Intents(messages=True, guilds=True, members=True, guild_scheduled_events=True)
client = discord.Client(intents=intents)

event_role_dict = {}

def make_role_name(inputString):
    return ''.join(c for c in inputString if c.isalnum())

def get_role_from_event(event):
    role_id = event_role_dict[event.id]
    return event.guild.get_role(role_id)

def get_member_from_user(server,user):
    user_id = user.id
    return server.get_member(user_id)

async def event_create_role(event):
    role_name = "Event-" + make_role_name(event.name)
    print(role_name)
    new_role = await event.guild.create_role(name=role_name,mentionable=True)
    print(new_role.id)
    event_role_dict[event.id] = new_role.id
    member = get_member_from_user(event.guild,user)
    await member.add_roles(role)



async def event_delete_role(event):
    role = get_role_from_event(event)
    await role.delete()
    print("deleted")


@client.event
async def on_ready():
    print('Connected as:')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print(server_id)
    server = client.get_guild(server_id)
    event_list = await server.fetch_scheduled_events()
    print(event_list)
    for ev in event_list:
        async for u in ev.users():
            print(u)

@client.event
async def on_scheduled_event_create(event):
    print("Create")
    print(event)
    await event_create_role(event)

@client.event
async def on_scheduled_event_delete(event):
    print("Delete")
    print(event)
    await event_delete_role(event)

@client.event
async def on_scheduled_event_delete(event):
    print("Update")
    print(event)

@client.event
async def on_scheduled_event_user_add(event,user):
    print("Add")
    role = get_role_from_event(event)
    member = get_member_from_user(event.guild,user)
    await member.add_roles(role)
    print(event,user)

@client.event
async def on_scheduled_event_user_remove(event,user):
    print("Remove")
    role = get_role_from_event(event)
    member = get_member_from_user(event.guild,user)
    await member.remove_roles(role)
    print(event,user)



client.run(token)