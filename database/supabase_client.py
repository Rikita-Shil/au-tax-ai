import os

from dotenv import load_dotenv
from supabase import Client, create_client


load_dotenv()


def get_supabase_client() -> Client:
    """
    Create a Supabase client using the server-side key.
    """

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")

    if not supabase_url:
        raise ValueError("SUPABASE_URL is missing from .env")

    if not supabase_service_key:
        raise ValueError("SUPABASE_SERVICE_KEY is missing from .env")

    return create_client(
        supabase_url,
        supabase_service_key,
    )


if __name__ == "__main__":
    client = get_supabase_client()
    print("Supabase client created successfully.")