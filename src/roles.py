from enum import Enum

class Role(Enum):
    SUPER_ADMIN = 'super_admin'
    ADMIN = 'admin'
    CONSULTANT = 'consultant'
    USER = 'user'

    @classmethod
    def from_string(cls, role_str):
        """Convert a string to a Role enum."""
        try:
            return cls[role_str.upper()]
        except KeyError:
            raise ValueError(f"{role_str} is not a valid Role")
