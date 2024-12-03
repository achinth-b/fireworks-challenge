import re

class DataValidator:
    def validate(self, data: dict) -> bool:
        # Validate name: non-empty and alphabetic
        if not data.get('name') or not data['name'].replace(' ', '').isalpha():
            return False

        # Validate date of birth (YYYY-MM-DD)
        dob_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(dob_pattern, data.get('dob', '')):
            return False

        # Validate document number (alphanumeric, 6-12 characters)
        doc_num_pattern = r'^[A-Z0-9]{6,12}$'
        if not re.match(doc_num_pattern, data.get('document_number', '')):
            return False

        return True