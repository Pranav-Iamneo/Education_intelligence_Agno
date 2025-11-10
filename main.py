"""
Main entry point for Education & Learning Intelligence System
Supports multiple interfaces: CLI, Streamlit UI, and API
"""

import argparse
import sys
import subprocess
from pathlib import Path

from config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


def run_streamlit_ui():
    """Launch the Streamlit UI"""
    logger.info("Starting Streamlit UI...")
    try:
        streamlit_file = Path(__file__).parent / "streamlit_ui.py"
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(streamlit_file)],
            check=True
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running Streamlit UI: {e}")
        sys.exit(1)


def run_api_server():
    """Launch the API server"""
    logger.info("Starting API server...")
    logger.info(f"API running on http://{settings.API_HOST}:{settings.API_PORT}")
    try:
        # Example: uvicorn app:app --host localhost --port 8083
        subprocess.run(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "api.main:app",
                "--host",
                settings.API_HOST,
                "--port",
                str(settings.API_PORT),
            ],
            check=True
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running API server: {e}")
        sys.exit(1)
    except FileNotFoundError:
        logger.error("Uvicorn not installed. Install with: pip install uvicorn")
        sys.exit(1)


def run_cli():
    """Run command-line interface"""
    logger.info("Running CLI mode...")
    from agents.orchestrator import orchestrator

    print("\n" + "=" * 60)
    print(f"{settings.APP_NAME} - CLI Interface")
    print(f"Version: {settings.APP_VERSION}")
    print("=" * 60 + "\n")

    # Example CLI workflow
    student_id = input("Enter student ID: ").strip()
    if not student_id:
        logger.warning("No student ID provided")
        return

    print("\nAvailable operations:")
    print("1. Assess student")
    print("2. Get learning path")
    print("3. Get progress report")
    print("4. Get recommendations")

    choice = input("\nSelect operation (1-4): ").strip()

    try:
        if choice == "1":
            subject = input("Enter subject: ").strip()
            print(f"\nAssessing student {student_id} in {subject}...")
            # Add assessment logic here

        elif choice == "2":
            print(f"\nGenerating learning path for student {student_id}...")
            # Add learning path logic here

        elif choice == "3":
            print(f"\nGenerating progress report for student {student_id}...")
            # Add progress report logic here

        elif choice == "4":
            print(f"\nGenerating recommendations for student {student_id}...")
            # Add recommendations logic here

        else:
            print("Invalid choice")

    except Exception as e:
        logger.error(f"Error in CLI operation: {e}")
        print(f"Error: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description=settings.DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --streamlit          # Launch Streamlit UI
  python main.py --api                # Start API server
  python main.py --cli                # Run command-line interface
  python main.py --version            # Show version
        """
    )

    parser.add_argument(
        "--streamlit",
        action="store_true",
        help="Launch Streamlit web interface"
    )
    parser.add_argument(
        "--api",
        action="store_true",
        help="Start API server"
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run command-line interface"
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Show version and exit
    if args.version:
        print(f"{settings.APP_NAME}")
        print(f"Version: {settings.APP_VERSION}")
        sys.exit(0)

    # Set verbose logging if requested
    if args.verbose:
        logger.info("Verbose logging enabled")

    # Default to Streamlit if no option specified
    if not args.api and not args.cli:
        args.streamlit = True

    try:
        if args.streamlit:
            run_streamlit_ui()
        elif args.api:
            run_api_server()
        elif args.cli:
            run_cli()

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\nApplication terminated by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
