"""Base repository class with common database operations."""

from typing import Dict, List, Any, Optional, TypeVar, Generic, Type
from supabase import Client

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """Base repository class with common database operations."""
    
    def __init__(self, supabase_client: Client, table_name: str):
        """
        Initialize the repository with a Supabase client and table name.
        
        Args:
            supabase_client: The Supabase client
            table_name: The name of the database table
        """
        self.supabase = supabase_client
        self.table_name = table_name
    
    def get_all(self) -> List[Dict[str, Any]]:
        """
        Get all records from the table.
        
        Returns:
            List of dictionaries representing all records
        """
        response = self.supabase.table(self.table_name).select('*').execute()
        return response.data if response.data else []
    
    def get_by_id(self, id_value: int, id_column: str = None) -> Optional[Dict[str, Any]]:
        """
        Get a record by its ID.
        
        Args:
            id_value: The ID value to look up
            id_column: The name of the ID column (defaults to table_name + '_id')
            
        Returns:
            Dictionary representing the record, or None if not found
        """
        if id_column is None:
            id_column = f"{self.table_name.rstrip('s')}_id"
            
        response = self.supabase.table(self.table_name).select('*').eq(id_column, id_value).execute()
        
        if response.data:
            return response.data[0]
        return None
    
    def filter_by(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Filter records by the given criteria.
        
        Args:
            **kwargs: Column-value pairs to filter by
            
        Returns:
            List of dictionaries representing the filtered records
        """
        query = self.supabase.table(self.table_name).select('*')
        
        for column, value in kwargs.items():
            query = query.eq(column, value)
            
        response = query.execute()
        return response.data if response.data else []
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new record.
        
        Args:
            data: Dictionary of column-value pairs
            
        Returns:
            Dictionary representing the created record
        """
        response = self.supabase.table(self.table_name).insert(data).execute()
        
        if response.data:
            return response.data[0]
        return {}
    
    def update(self, id_value: int, data: Dict[str, Any], id_column: str = None) -> Optional[Dict[str, Any]]:
        """
        Update a record by its ID.
        
        Args:
            id_value: The ID value to update
            data: Dictionary of column-value pairs to update
            id_column: The name of the ID column (defaults to table_name + '_id')
            
        Returns:
            Dictionary representing the updated record, or None if not found
        """
        if id_column is None:
            id_column = f"{self.table_name.rstrip('s')}_id"
            
        response = self.supabase.table(self.table_name).update(data).eq(id_column, id_value).execute()
        
        if response.data:
            return response.data[0]
        return None
    
    def delete(self, id_value: int, id_column: str = None) -> bool:
        """
        Delete a record by its ID.
        
        Args:
            id_value: The ID value to delete
            id_column: The name of the ID column (defaults to table_name + '_id')
            
        Returns:
            Boolean indicating success or failure
        """
        if id_column is None:
            id_column = f"{self.table_name.rstrip('s')}_id"
            
        response = self.supabase.table(self.table_name).delete().eq(id_column, id_value).execute()
        
        return bool(response.data)
