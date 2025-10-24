from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class NestedConfigManager:
    """
    Utils for nested config management
    """

    def __init__(self):
        pass

    def get_nested_value(
        self, data: Dict[str, Any], keys: List[str], default: Any = None
    ) -> Any:
        """Get a value from nested dictionary using a list of keys.

        Args:
            data: The dictionary to search
            keys: List of keys representing the path (e.g., ['todoist', 'api_key'])
            default: Default value if key path not found

        Returns:
            The value at the key path or default if not found
        """
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current

    def set_nested_value(self, data: Dict[str, Any], keys: List[str], value: Any) -> None:
        """Set a value in nested dictionary using a list of keys.

        Args:
            data: The dictionary to modify
            keys: List of keys representing the path (e.g., ['todoist', 'api_key'])
            value: The value to set
        """
        current = data
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            elif not isinstance(current[key], dict):
                # If intermediate key exists but is not a dict, replace it
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value

    def delete_nested_key(self, data: Dict[str, Any], keys: List[str]) -> bool:
        """Delete a value from nested dictionary using a list of keys.

        Args:
            data: The dictionary to modify
            keys: List of keys representing the path

        Returns:
            True if key was found and deleted, False otherwise
        """
        if not keys:
            return False

        current = data
        # Navigate to parent of the key to delete
        for key in keys[:-1]:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return False

        # Delete the final key
        if isinstance(current, dict) and keys[-1] in current:
            del current[keys[-1]]
            return True
        return False

    def get_flattened_values(
        self, data: Dict[str, Any], parent_key: str = "", sep: str = "."
    ) -> Dict[str, Any]:
        """Flatten a nested dictionary using dot notation.

        Args:
            data: The dictionary to flatten
            parent_key: The parent key prefix
            sep: Separator to use (default: '.')

        Returns:
            Flattened dictionary with dot notation keys
        """
        items = []
        logger.debug(f"Traversing config dict: ({data})")
        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, dict):
                items.extend(self.get_flattened_values(value, new_key, sep=sep).items())
            else:
                logger.debug(f"Adding flattened key: ({new_key},{value})")
                items.append((new_key, value))
        return dict(items)