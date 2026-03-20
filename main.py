from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input, Select, Label, Static
from textual.containers import Vertical, Horizontal
from textual import on
import subprocess
import random
import os
import asyncio

class WifiSpammer(App):
    CSS = """
    Screen {
        background: $panel;
    }
    Label {
        margin: 1;
    }
    Input, Select {
        margin: 1 2;
        width: 50%;
    }
    Button {
        margin: 1 2;
    }
    #status {
        height: 8;
        overflow-y: auto;
        background: $surface;
        border: tall $primary;
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header("WiFi Spam Generator 😈", "bold")
        with Vertical():
            yield Label("Ile sieci chcesz stworzyć?")
            yield Input(placeholder="Liczba (max 500 zalecane)", id="count", value="100")

            yield Label("Wzór nazwy (użyj {i} dla numerka)")
            yield Input(placeholder="np. Free WiFi {i} 🍟", id="pattern", value="Free WiFi {i} 😈")

            yield Label("Dostęp do internetu?")
            yield Select(
                [("Tak (wymaga root + tethering)", "yes"), ("Nie – czysty fake", "no")],
                id="internet",
                value="no"
            )

            yield Label("Z hasłem?")
            yield Select(
                [("Open (bez hasła)", "open"), ("WPA2 losowe hasło", "wpa_random"), ("Własne hasło", "wpa_custom")],
                id="auth",
                value="open"
            )

            yield Input(placeholder="Hasło jeśli wybrałeś własne", id="password", disabled=True)

            with Horizontal():
                yield Button("START SPAM!", id="start", variant="success")
                yield Button("STOP", id="stop", variant="error", disabled=True)

            yield Static(id="status", markup=True)

        yield Footer()

    @on(Select.Changed, "#auth")
    def toggle_password(self, event: Select.Changed) -> None:
        pw_input = self.query_one("#password", Input)
        pw_input.disabled = event.value != "wpa_custom"
        if not pw_input.disabled:
            pw_input.focus()

    @on(Button.Pressed, "#start")
    async def start_spam(self) -> None:
        count = self.query_one("#count", Input).value.strip()
        pattern = self.query_one("#pattern", Input).value.strip()
        internet = self.query_one("#internet", Select).value
        auth = self.query_one("#auth", Select).value
        password = self.query_one("#password", Input).value.strip()

        try:
            count_int = int(count)
            if count_int < 1 or count_int > 999:
                raise ValueError
        except:
            self.query_one("#status").update("[red]Podaj sensowną liczbę (1–999)[/]")
            return

        status = self.query_one("#status")
        status.update("[yellow]Przygotowanie...[/]")

        self.query_one("#start").disabled = True
        self.query_one("#stop").disabled = False

        cmd_base = ["mdk4", "wlan0", "b"]  # beacon flood – zmień wlan0 na swój interfejs!

        for i in range(1, count_int + 1):
            ssid = pattern.format(i=i)
            extra = ""
            if auth == "wpa_random":
                extra = f" (hasło: {random.randint(10000000,99999999)})"
            elif auth == "wpa_custom" and password:
                extra = f" (hasło: {password})"

            status.update(status.renderable + f"\n→ {ssid}{extra}")
            # Tutaj realne wysyłanie beaconów – mdk4 nie lubi zbyt szybkich zmian, więc sleep
            # subprocess.run(cmd_base + ["-s", ssid])  # odkomentuj gdy masz mdk4 i uprawnienia
            await asyncio.sleep(0.15)  # symulacja – realnie usuń sleep i odkomentuj subprocess

        status.update(status.renderable + "\n[yellow]Koniec spamu – sprawdź w okolicy![/]")
        self.query_one("#start").disabled = False
        self.query_one("#stop").disabled = True

    @on(Button.Pressed, "#stop")
    def stop_spam(self):
        # Tutaj kill mdk4 jeśli działa w tle – na razie tylko UI
        self.query_one("#status").update("[green]Zatrzymano.[/]")
        self.query_one("#start").disabled = False
        self.query_one("#stop").disabled = True

if __name__ == "__main__":
    app = WifiSpammer()
    app.run()
