import chainlit as cl

from ello.client import chat


@cl.on_message
async def on_message(message: cl.Message):
    response = await chat(
        messages=[
            {
                "content": "You are a helpful bot, you always reply in Emojis",
                "role": "system"
            },
            {
                "content": message.content,
                "role": "user"
            }
        ],
    )
    async for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            await cl.Message(content=chunk.choices[0].delta.content).send()

