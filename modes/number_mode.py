import pygame


class NumberMode:

    def __init__(self, screen):
        self.screen = screen

        self.title_font = pygame.font.Font(None, 70)
        self.text_font = pygame.font.Font(None, 40)

        self.background = (245, 235, 210)
        self.text_color = (50, 40, 30)

        self.back_button = pygame.Rect(
            350, 500, 300, 70
        )

    def handle_events(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.back_button.collidepoint(event.pos):
                return "back"

        return None

    def draw(self):

        self.screen.fill(self.background)

        title = self.title_font.render(
            "NUMBER MODE",
            True,
            self.text_color
        )

        self.screen.blit(
            title,
            title.get_rect(
                center=(500, 150)
            )
        )

        text = self.text_font.render(
            "Number game will be here...",
            True,
            self.text_color
        )

        self.screen.blit(
            text,
            text.get_rect(
                center=(500, 300)
            )
        )

        pygame.draw.rect(
            self.screen,
            (120, 170, 100),
            self.back_button,
            border_radius=15
        )

        back_text = self.text_font.render(
            "BACK",
            True,
            self.text_color
        )

        self.screen.blit(
            back_text,
            back_text.get_rect(
                center=self.back_button.center
            )
        )