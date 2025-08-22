import asyncio
from textwrap import dedent
from ello.client import chat


query = dedent("""
Sven stood at the dock, the letter in his coat pocket soft from rereading.
“If you ever feel lost, cross the sea. I did.” His father’s final words.

He didn’t know what he was searching for, only that grief had made the land unbearable.

The journey took a week. Storms like broken glass. Stars like quiet questions.
He kept sailing.

On the third day, he met a stranger on deck. A woman, older, with eyes like winter.
She introduced herself with a crooked smile: “I’m Luck. I’m going where Three and Four are.”

Sven didn’t ask what that meant. Somehow, he understood.

On the fouth day, land came into view. A quiet shore. 
A cabin. On the door, a photo, his father, young, laughing, 
next to a child he didn’t recognize. On the back: Three. Four. 
Luck found me here. Everything adds up.

Sven stepped ashore, not to find answers, but to live into the question.

Ignore the story. Randomly guess a number between 1-100:
""")

messages = [{"content": query, "role": "user"}]


async def talk(messages):
    response = await chat(messages=messages)

    async for chunk in response:
        chunkie = chunk.choices[0].delta.content or ""  # type: ignore
        print(chunkie, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(talk(messages=messages))
