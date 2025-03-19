"""Repository for major-related database operations."""

from typing import List, Dict, Any, Optional
from supabase import Client

from .base import BaseRepository
from models.major import Major


class MajorRepository(BaseRepository[Major]):
    """Repository for major-related database operations."""
    
    def __init__(self, supabase_client: Client):
        """Initialize with Supabase client."""
        super().__init__(supabase_client, 'majors')
    
    def get_active_version(self, major_id: int, catalog_year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Get the active version of a major, optionally filtering by catalog year.
        
        Args:
            major_id: The major's ID
            catalog_year: Optional catalog year to filter by
            
        Returns:
            Dictionary representing the major version, or None if not found
        """
        query = self.supabase.table('majorversions').select('*').eq('major_id', major_id)
        
        if catalog_year:
            query = query.eq('catalog_year', catalog_year)
        else:
            query = query.eq('is_active', True)
        
        response = query.order('catalog_year', desc=True).limit(1).execute()
        
        if response.data:
            return response.data[0]
        return None
    
    def get_requirements(self, major_version_id: int, requirement_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all requirements for a major version.
        
        Args:
            major_version_id: The major version's ID
            requirement_type: Optional requirement type to filter by
            
        Returns:
            List of dictionaries representing the major requirements
        """
        query = self.supabase.table('majorrequirements')\
            .select('*')\
            .eq('major_version_id', major_version_id)
            
        if requirement_type:
            query = query.eq('requirement_type', requirement_type)
            
        response = query.execute()
        return response.data if response.data else []
    
    def get_requirement_groups(self, requirement_id: int) -> List[Dict[str, Any]]:
        """
        Get all requirement groups for a requirement.
        
        Args:
            requirement_id: The requirement's ID
            
        Returns:
            List of dictionaries representing the requirement groups
        """
        response = self.supabase.table('requirementgroups')\
            .select('*')\
            .eq('requirement_id', requirement_id)\
            .execute()
            
        return response.data if response.data else []
    
    def get_requirement_rules(self, major_version_id: int) -> List[Dict[str, Any]]:
        """
        Get all requirement rules for a major version.
        
        Args:
            major_version_id: The major version's ID
            
        Returns:
            List of dictionaries representing the requirement rules
        """
        response = self.supabase.table('requirementrules')\
            .select('*')\
            .eq('major_version_id', major_version_id)\
            .execute()
            
        return response.data if response.data else []
    
    def get_rule_courses(self, rule: Dict[str, Any]) -> List[int]:
        """
        Get all course IDs related to a requirement rule.
        
        Args:
            rule: The requirement rule dictionary
            
        Returns:
            List of course IDs related to the rule
        """
        courses_to_check = []
        
        if rule.get('requirement_id'):
            # Get requirement groups for this requirement
            groups_query = self.supabase.table('requirementgroups')\
                .select('requirement_group_id')\
                .eq('requirement_id', rule['requirement_id'])\
                .execute()
            
            if groups_query.data:
                group_ids = [g['requirement_group_id'] for g in groups_query.data]
                
                # Get courses for these requirement groups
                courses_query = self.supabase.table('requirementgroupcourses')\
                    .select('course_id')\
                    .in_('requirement_group_id', group_ids)\
                    .execute()
                
                if courses_query.data:
                    courses_to_check = [c['course_id'] for c in courses_query.data]
        
        elif rule.get('requirement_group_id'):
            # Get courses for this requirement group
            courses_query = self.supabase.table('requirementgroupcourses')\
                .select('course_id')\
                .eq('requirement_group_id', rule['requirement_group_id'])\
                .execute()
            
            if courses_query.data:
                courses_to_check = [c['course_id'] for c in courses_query.data]
        
        return courses_to_check
