"""Repository for distribution requirement database operations."""

from typing import Dict, List, Any, Optional
from supabase import Client

from .base import BaseRepository


class DistributionRepository(BaseRepository):
    """Repository for distribution requirement-related database operations."""
    
    def __init__(self, supabase_client: Client):
        """Initialize with Supabase client."""
        self.supabase = supabase_client
    
    def get_distribution_types(self) -> List[Dict[str, Any]]:
        """Get all distribution types."""
        response = self.supabase.table('distributiontypes').select('*').execute()
        return response.data if response.data else []
    
    def get_academic_years(self) -> List[Dict[str, Any]]:
        """Get all academic years, ordered by display_order."""
        response = self.supabase.table('academicyears').select('*').order('display_order').execute()
        return response.data if response.data else []
    
    def get_distribution_requirements(self) -> List[Dict[str, Any]]:
        """Get all active distribution requirements with related data."""
        response = self.supabase.table('distributionrequirements')\
            .select('*, distributiontypes(*), academicyears(*)')\
            .eq('active', True)\
            .execute()
        return response.data if response.data else []
    
    def get_year_rules(self) -> List[Dict[str, Any]]:
        """Get all active year rules with related data."""
        response = self.supabase.table('yearrequirementrules')\
            .select('*, academicyears(*)')\
            .eq('active', True)\
            .execute()
        return response.data if response.data else []
    
    def get_requirements_by_year(self, year_name: str) -> List[Dict[str, Any]]:
        """Get distribution requirements for a specific academic year."""
        response = self.supabase.table('distributionrequirements')\
            .select('*, distributiontypes(*), academicyears(*)')\
            .eq('active', True)\
            .eq('academicyears.name', year_name)\
            .execute()
        return response.data if response.data else []
    
    def get_rules_by_year(self, year_name: str) -> List[Dict[str, Any]]:
        """Get special rules for a specific academic year."""
        response = self.supabase.table('yearrequirementrules')\
            .select('*')\
            .eq('active', True)\
            .eq('academicyears.name', year_name)\
            .execute()
        return response.data if response.data else []