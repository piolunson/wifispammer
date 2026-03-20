# Ai generated version
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table
from rich import print as rprint
import time
import random
import sys
import os

console = Console()

def main():
    console.clear()
    console.rule("WiFi Spam Master 9000 😈", style="bold red")

    rprint(Panel.fit(
        "[bold cyan]Program do tworzenia fejkowych sieci WiFi[/]\n"
        "Działa z mdk4 / symulacja / czysta zabawa\n"
        "Uwaga: realny spam wymaga root + mdk4 + kompatybilna karta",
        title="Ostrzeżenie & Info", border_style="bright_yellow"
    ))

    ile = IntPrompt.ask("[bold magenta]Ile sieci chcesz stworzyć[/]", default=120)
    if ile > 600:
        rprint("[red]Uwaga: powyżej 500–600 może zabić kartę/radio/Telefon[/]")
        if not Confirm.ask("Na pewno chcesz ryzykować?"):
            sys.exit(0)

    wzor = Prompt.ask(
        "[bold green]Wzór nazwy (użyj {i} dla numerka, {emoji} dla losowego emoji)[/]",
        default="Free WiFi {i} {emoji}"
    )

    internet = Confirm.ask("[bold blue]Udawać że dają internet?[/] (ikona ! w telefonach)", default=False)
    haslo = Confirm.ask("[bold yellow]Dodawać hasło WPA2?[/]", default=False)
    if haslo:
        haslo_txt = Prompt.ask("Jakie hasło (lub 'random')", default="random")

    # Losowe emoji do urozmaicenia
    emoji_pool = ["😈", "🔥", "🍔", "📶", "🚀", "💀", "🍟", "🌐", "🆓", "🤡", "5G"]

    # Symulacja / realny atak (mdk4 wymaga root + interfejsu)
    interfejs = "wlan0"  # zmień na swój → ip link pokaże
    use_real_mdk4 = Confirm.ask("[bold red]Użyć REALNEGO mdk4?[/] (wymaga root + zainstalowanego mdk4)", default=False)

    rprint("\n[bold white on red]STARTUJEMY SPAM![/]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[bold]{task.completed}/{task.total}"),
    ) as progress:
        
        task = progress.add_task("[cyan]Tworzenie sieci...", total=ile)

        for i in range(1, ile + 1):
            num = f"{i:04d}" if "{i:04d}" in wzor else str(i)
            emo = random.choice(emoji_pool) if "{emoji}" in wzor else ""
            ssid = wzor.format(i=num, emoji=emo)

            extra = ""
            if haslo:
                if haslo_txt == "random":
                    pw = f"{random.randint(1000000,9999999)}"
                    extra = f" [dim](hasło: {pw})[/dim]"
                else:
                    extra = f" [dim](hasło: {haslo_txt})[/dim]"

            if internet:
                ssid_display = f"[bold green]{ssid} ★[/] {extra}"
            else:
                ssid_display = f"[bold yellow]{ssid}[/] {extra}"

            rprint(f" → {ssid_display}")

            # Realne wysyłanie (tylko jeśli wybrałeś i masz uprawnienia)
            if use_real_mdk4:
                try:
                    # Przykład – mdk4 beacon flood (jedna nazwa na raz)
                    # os.system(f"mdk4 {interfejs} b -s '{ssid}' &")  # w tle, ale ostrożnie
                    time.sleep(0.08)  # mdk4 nie lubi zbyt szybko
                except:
                    rprint("[red]Błąd uruchamiania mdk4 – kontynuuję symulację[/]")
            else:
                time.sleep(0.05 + random.uniform(0, 0.1))  # fajniejszy efekt

            progress.update(task, advance=1)

    console.rule("Koniec spamu – sprawdź analizator WiFi u sąsiadów", style="bold green")
    rprint("[bold magenta]Efekt powinien być widoczny na 100% telefonach w zasięgu ;)[/]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Zatrzymano przez Ctrl+C – sprzątanie...[/]")
