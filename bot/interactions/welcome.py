from disnake import ui
from disnake.enums import ButtonStyle
from disnake.interactions import Interaction


class BaseWelcomeInteraction(ui.View):
    def __init__(self, *, timeout: int = 60):
        super().__init__(timeout=timeout)


class WelcomeInteraction(BaseWelcomeInteraction):
    def __init__(self):
        self.is_student = None
        super().__init__()

    async def start(self):
        timed_out = await self.wait()

        if timed_out:
            return None

        return self.is_student

    @ui.button(label="Oui", style=ButtonStyle.green)
    async def yes_student(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        self.is_student = True
        self.stop()

    @ui.button(label="Non", style=ButtonStyle.red)
    async def no_student(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        self.is_student = False
        self.stop()


class StudentInteraction(BaseWelcomeInteraction):
    def __init__(self):
        self.program = None

    async def start(self):
        timed_out = await self.wait()

        if timed_out:
            return None

        return self.program

    @ui.button(label="Programmation", style=ButtonStyle.primary)
    async def prog(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        self.program = "prog"
        self.stop()

    @ui.button(label="Réseautique", style=ButtonStyle.primary)
    async def network(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        self.program = "network"
        self.stop()

    @ui.button(label="DEC-BAC", style=ButtonStyle.primary)
    async def decbac(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        self.program = "decbac"
        self.stop()


class TeacherInteraction(BaseWelcomeInteraction):
    def __init__(self):
        self.is_teacher = None
        super().__init__()

    async def start(self):
        timed_out = await self.wait()

        if timed_out:
            return None

        return self.is_teacher

    @ui.button(label="Oui", style=ButtonStyle.green)
    async def yes_teacher(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        self.is_teacher = True
        self.stop()

    @ui.button(label="Non", style=ButtonStyle.red)
    async def no_teacher(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        self.is_teacher = False
        self.stop()


class ConfirmationInteraction(BaseWelcomeInteraction):
    def __init__(self):
        self.confirmed = None
        super().__init__()

    async def start(self):
        timed_out = await self.wait()

        for button in self.children:
            button.disabled = True

        if timed_out:
            return None

        return self.confirmed

    @ui.button(label="Oui", style=ButtonStyle.green)
    async def yes(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        self.confirmed = True
        self.stop()

    @ui.button(label="Non", style=ButtonStyle.red)
    async def no(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        self.confirmed = False
        self.stop()
