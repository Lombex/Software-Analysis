from enum import Enum

class Role(Enum):
    SUPER_ADMIN = 1
    ADMIN = 2
    CONSULTANT = 3
    USER = 4

    @staticmethod
    def from_string(role_string):
        """Convert string to Role enum."""
        role_mapping = {
            'super_admin': Role.SUPER_ADMIN,
            'admin': Role.ADMIN,
            'consultant': Role.CONSULTANT,
            'user': Role.USER
        }
        return role_mapping.get(role_string.lower(), None)
