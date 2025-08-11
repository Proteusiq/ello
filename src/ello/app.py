import chainlit as cl
from ello.client import chat 




@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{
                "content": "You are Ello, you always reply in Emojis. Do not use words. Just emojis to communicate your message",
                "role": "system"
        }],
    )

@cl.on_message
async def on_message(message: cl.Message):
    message_history = cl.user_session.get("message_history", [])
    message_history.append({"role": "user", "content": message.content})


    msg = cl.Message(content="")

    stream = await chat(
        messages=message_history,
        stream=True,
    )
    
    async for chunk in stream:
        if token := chunk.choices[0].delta.content or "":
            await msg.stream_token(token)
    
    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()

