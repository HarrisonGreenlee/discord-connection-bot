from discord import Embed


# creates our survey question as a snazzy embed
def create_question(author, title, description):
    embed = Embed(title=title, description=description, color=0x8932b8)
    embed.set_author(name=author)
    embed.set_footer(text="Please answer the question by selecting a number from 1-5 below.")

    return embed
