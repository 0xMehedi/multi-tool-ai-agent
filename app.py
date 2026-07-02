import sys
import time
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.style import Style
from rich.text import Text

from agent.create_agent import create_agent, prepare_initial_message
from agent.router import AgentState
from config.logging_config import setup_logging
from config.settings import (
    CSV_FILES,
    CLEANED_CSV_FILES,
    DATABASES,
    LOGS_DIR,
)
from scripts.download_datasets import download_all_datasets
from scripts.clean_dataset import clean_all_datasets
from scripts.csv_to_sqlite import convert_all
from scripts.inspect_dataset import inspect_all
from tools.institution_tool import InstitutionsDBTool
from tools.hospital_tool import HospitalsDBTool
from tools.restaurant_tool import RestaurantsDBTool
from tools.web_search_tool import WebSearchTool

console = Console()
logger = setup_logging(__name__)

BANNER = """
╔══════════════════════════════════════════════╗
║     Multi-Tool AI Agent for Bangladesh       ║
║   Ask anything about institutions, hospitals, ║
║   restaurants, or general knowledge           ║
╚══════════════════════════════════════════════╝
"""


def check_databases() -> bool:
    for name, path in DATABASES.items():
        if not path.exists():
            logger.warning("Database not found: %s", path)
            return False
    return True


def check_csv_files() -> bool:
    for name, path in CSV_FILES.items():
        if not path.exists():
            logger.warning("CSV file not found: %s", path)
            return False
    return True


def setup_environment() -> bool:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    if check_databases():
        logger.info("All databases found.")
        return True

    logger.info("Databases not found. Starting setup...")

    if not check_csv_files():
        logger.info("Downloading datasets...")
        success = download_all_datasets()
        if not success:
            logger.warning(
                "Some datasets could not be downloaded automatically."
            )

    raw_exists = any(p.exists() for p in CSV_FILES.values())
    if not raw_exists:
        console.print(
            "[red]No CSV files found. Please place CSV files manually in[/red]"
        )
        console.print(f"[yellow]{CSV_DIR}[/yellow]")
        console.print(
            "See README.md for instructions on manual dataset setup."
        )
        return False

    console.print("[blue]Inspecting datasets...[/blue]")
    inspect_all()

    console.print("[blue]Cleaning datasets...[/blue]")
    clean_all_datasets()

    console.print("[blue]Converting CSV to SQLite databases...[/blue]")
    convert_all()

    if check_databases():
        console.print("[green]All databases created successfully![/green]")
        return True

    console.print("[red]Failed to create databases.[/red]")
    return False


def process_message(graph: StateGraph, user_input: str) -> str:
    messages = prepare_initial_message(user_input)

    start_time = time.time()
    try:
        events = graph.stream(
            {"messages": messages},
            {"recursion_limit": 25},
        )

        final_answer = ""
        for event in events:
            if isinstance(event, dict):
                for node_name, output in event.items():
                    if isinstance(output, dict):
                        msg_list = output.get("messages", [])
                        for msg in msg_list:
                            if hasattr(msg, "content") and msg.content:
                                final_answer = msg.content

        elapsed = time.time() - start_time
        logger.info(
            "Processed query in %.2f seconds: %s", elapsed, user_input
        )
        return final_answer

    except Exception as exc:
        elapsed = time.time() - start_time
        logger.error("Error processing query after %.2fs: %s", elapsed, exc)
        return f"I encountered an error while processing your question: {exc}"


def interactive_chat(graph: StateGraph) -> None:
    console.print(BANNER, style="bold cyan")
    console.print(
        "[yellow]Type your question or 'quit' to exit, 'help' for examples.[/yellow]\n"
    )

    while True:
        try:
            user_input = Prompt.ask("[bold green]You[/bold green]")
        except (EOFError, KeyboardInterrupt):
            console.print("\n[yellow]Goodbye![/yellow]")
            break

        if user_input.lower() in ("quit", "exit", "q"):
            console.print("[yellow]Goodbye![/yellow]")
            break

        if user_input.lower() == "help":
            show_help()
            continue

        if not user_input.strip():
            continue

        console.print()
        with console.status("[bold blue]Thinking...[/bold blue]"):
            answer = process_message(graph, user_input)

        console.print(Panel(
            Markdown(str(answer) if answer else "Sorry, I couldn't find an answer."),
            title="[bold magenta]Agent[/bold magenta]",
            border_style="magenta",
        ))
        console.print()


def show_help() -> None:
    examples = [
        ("Institutions", "How many government institutions are in Rajshahi?"),
        ("Institutions", "List universities in Dhaka."),
        ("Institutions", "What institutions offer medical education?"),
        ("Hospitals", "List hospitals in Dhaka."),
        ("Hospitals", "How many hospitals have ICU facilities?"),
        ("Hospitals", "Top hospitals in Chattogram."),
        ("Restaurants", "Top restaurants in Sylhet."),
        ("Restaurants", "Restaurants serving biryani in Dhaka."),
        ("Web Search", "What is the healthcare policy of Bangladesh?"),
        ("Web Search", "Who regulates hospitals in Bangladesh?"),
        ("Web Search", "Difference between public and private hospitals."),
    ]

    console.print("[bold]Example Questions:[/bold]\n")
    for category, question in examples:
        console.print(f"  [cyan]{category}:[/cyan] {question}")

    console.print()
    console.print("[bold]Commands:[/bold]")
    console.print("  [green]quit/exit/q[/green] - Exit the application")
    console.print("  [green]help[/green] - Show this help message")
    console.print()


def main() -> None:
    try:
        console.print("[blue]Initializing Multi-Tool AI Agent...[/blue]")

        ready = setup_environment()
        if not ready:
            logger.error("Environment setup failed.")
            sys.exit(1)

        tools = [
            InstitutionsDBTool(),
            HospitalsDBTool(),
            RestaurantsDBTool(),
            WebSearchTool(),
        ]

        graph = create_agent(tools)

        interactive_chat(graph)

    except ValueError as exc:
        console.print(f"[red]Configuration Error:[/red] {exc}")
        logger.error("Configuration error: %s", exc)
        sys.exit(1)
    except Exception as exc:
        console.print(f"[red]Unexpected Error:[/red] {exc}")
        logger.error("Unexpected error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
