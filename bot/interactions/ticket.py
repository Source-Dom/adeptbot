import discord
from discord import ui, ButtonStyle

import configs
from bot import util
from bot.tickets import TicketType


class TicketOpeningInteraction(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label='Plainte', style=ButtonStyle.blurple, custom_id=configs.TICKET_COMPLAINT_ID)
    async def plainte(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("Êtes-vous sûre de vouloir ouvrir un ticket de plainte?",
                                                view=TicketConfirmationInteraction(TicketType.COMPLAINT),
                                                ephemeral=True)

    @ui.button(label='Appel de moron', style=ButtonStyle.blurple, custom_id=configs.TICKET_MORON_ID)
    async def moron(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("Êtes-vous sûre de vouloir ouvrir un ticket d'appel de moron?",
                                                view=TicketConfirmationInteraction(TicketType.MORON),
                                                ephemeral=True)


class TicketConfirmationInteraction(ui.View):
    def __init__(self, ticket_type: TicketType):
        super().__init__(timeout=30)
        self.ticket_type = ticket_type

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)

        return await super().interaction_check(interaction)

    @ui.button(label='Oui', style=ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: ui.Button):
        await util.create_ticket(interaction.user, self.ticket_type)

    @ui.button(label='Non', style=ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.edit_original_response(content='Vous avez annulé la création du ticket.')


class TicketCloseInteraction(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)

        return await super().interaction_check(interaction)

    @ui.button(label='Fermer', style=ButtonStyle.red, custom_id=configs.TICKET_CLOSE_ID)
    async def close(self, interaction: discord.Interaction, button: ui.Button):
        await util.archive_ticket(interaction.user, interaction.channel)
