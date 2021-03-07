from discord import Embed


# creates our survey question as a snazzy embed
def create_question(title, description, avatar):
    embed = Embed(title=title, description=description, color=0x8932b8)
    embed.set_author(name="DiscMatch")
    embed.set_footer(text="Please select a number 1-5, one being the least and 5 being the most")
    embed.set_image(avatar)

    return embed
