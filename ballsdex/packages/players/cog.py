@app_commands.command()
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    async def rarity(self, interaction: discord.Interaction):
        """
        show the rarity of all asiaballs!!
        """
        bot_countryballs = await Ball.filter(enabled=True).order_by("rarity")

        entries = []
        for countryball in bot_countryballs:
            emoji = self.bot.get_emoji(countryball.emoji_id)
            if emoji:
                entries.append((f"**{countryball.country}**", f"{emoji} Rarity: {countryball.rarity}"))

        if len(entries) == 0:
            await interaction.response.send_message("No sticks found.", ephemeral=True)
            return

        source = FieldPageSource(entries, per_page=5, inline=False, clear_description=False)
        source.embed.description = "Asiaballs Rarity"
        source.embed.colour = discord.Colour.blurple()
        source.embed.set_author(
            name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url
        )

        pages = Pages(source=source, interaction=interaction, compact=True)
        await pages.start()
