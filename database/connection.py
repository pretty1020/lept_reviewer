"""
LEPT AI Reviewer - Snowflake Database Connection
OPTIMIZED: Single cached connection, reused across all queries
"""

import streamlit as st
import snowflake.connector
from typing import Optional, List, Any, Tuple
import time


def _increment_query_count():
    """Safely increment the query counter."""
    try:
        if "db_query_count" not in st.session_state:
            st.session_state.db_query_count = 0
        st.session_state.db_query_count += 1
    except Exception:
        # Session state not available (e.g., in cached function context)
        pass


@st.cache_resource
def get_snowflake_connection():
    """
    Create and cache a single Snowflake connection.
    This connection is reused across ALL reruns and users.
    """
    try:
        conn = snowflake.connector.connect(
            account=st.secrets["snowflake"]["account"],
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            role=st.secrets["snowflake"].get("role", "ACCOUNTADMIN"),
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            client_session_keep_alive=True,  # Keep connection alive
            network_timeout=30,
        )
        return conn
    except Exception as e:
        st.error(f"Failed to connect to Snowflake: {str(e)}")
        return None


def get_cursor():
    """Get a cursor from the cached connection."""
    conn = get_snowflake_connection()
    if conn:
        try:
            # Test if connection is still valid
            if not conn.is_closed():
                return conn.cursor()
            else:
                # Connection closed, clear cache and reconnect
                st.cache_resource.clear()
                conn = get_snowflake_connection()
                if conn:
                    return conn.cursor()
        except Exception:
            # Connection error, clear cache and reconnect
            st.cache_resource.clear()
            conn = get_snowflake_connection()
            if conn:
                return conn.cursor()
    return None


def execute_query(query: str, params: tuple = None, fetch: bool = True) -> Optional[List]:
    """
    Execute a query using the cached connection.
    
    Args:
        query: SQL query string
        params: Query parameters (optional)
        fetch: Whether to fetch results (default True)
    
    Returns:
        List of results if fetch=True, True if successful write, None on error
    """
    # Safely increment debug counter
    _increment_query_count()
    
    cursor = None
    try:
        cursor = get_cursor()
        if cursor is None:
            return None
        
        start_time = time.time()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
        else:
            # Commit for write operations
            get_snowflake_connection().commit()
            result = True
        
        # Debug timing (remove in production)
        elapsed = (time.time() - start_time) * 1000
        if elapsed > 500:  # Log slow queries
            print(f"SLOW QUERY ({elapsed:.0f}ms): {query[:100]}...")
        
        return result
        
    except snowflake.connector.errors.ProgrammingError as e:
        if "Authentication token has expired" in str(e) or "session" in str(e).lower():
            # Session expired, clear cache and retry once
            st.cache_resource.clear()
            try:
                cursor = get_cursor()
                if cursor:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    if fetch:
                        return cursor.fetchall()
                    else:
                        get_snowflake_connection().commit()
                        return True
            except Exception:
                pass
        return None
    except Exception as e:
        # Don't show error in UI for every query failure
        print(f"Query error: {str(e)}")
        return None
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception:
                pass


def execute_write(query: str, params: tuple = None) -> bool:
    """Execute a write query (INSERT, UPDATE, DELETE)."""
    result = execute_query(query, params, fetch=False)
    return result is True


def test_connection() -> Tuple[bool, str]:
    """Test the Snowflake connection."""
    try:
        result = execute_query("SELECT CURRENT_VERSION()")
        if result and len(result) > 0:
            return True, result[0][0]
        return False, "Connection test failed"
    except Exception as e:
        return False, str(e)


def get_query_count() -> int:
    """Get the number of queries executed in this session (for debugging)."""
    try:
        return st.session_state.get("db_query_count", 0)
    except Exception:
        return 0


def reset_query_count():
    """Reset the query counter (for debugging)."""
    try:
        st.session_state.db_query_count = 0
    except Exception:
        pass
