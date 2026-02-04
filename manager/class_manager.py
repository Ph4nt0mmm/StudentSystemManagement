from typing import List, Dict, Any, Optional
from ..modules.class_section import ClassSection
import os


class ClassManager:


    def __init__(self):
        self.classes_file = "File/classes_list.text"
        os.makedirs("File", exist_ok=True)

    def create_class(self, class_data: Dict[str, Any]) -> Dict[str, Any]:
        result = {
            'success': False,
            'message': '',
            'class_id': None
        }

        try:
            class_section = ClassSection(**class_data)

            # Save to file
            with open(self.classes_file, 'a') as f:
                f.write(f"{class_section.to_dict()}\n")

            result['success'] = True
            result['message'] = 'Class created successfully'
            result['class_id'] = class_section.class_id

        except Exception as e:
            result['message'] = f'Failed to create class: {str(e)}'

        return result

    def get_all_classes(self) -> List[ClassSection]:
        classes = []

        if not os.path.exists(self.classes_file):
            return classes

        try:
            with open(self.classes_file, 'r') as f:
                for line in f:
                    try:
                        data = eval(line.strip())
                        classes.append(ClassSection(**data))
                    except:
                        continue
        except:
            pass

        return classes

    def get_class_by_id(self, class_id: str) -> Optional[ClassSection]:

        classes = self.get_all_classes()
        for class_ in classes:
            if class_.class_id == class_id:
                return class_
        return None

    def add_student_to_class(self, class_id: str, student_id: str) -> Dict[str, Any]:

        result = {
            'success': False,
            'message': ''
        }

        class_ = self.get_class_by_id(class_id)
        if not class_:
            result['message'] = f'Class {class_id} not found'
            return result

        if student_id in class_.students:
            result['message'] = f'Student {student_id} already in class'
            return result

        class_.students.append(student_id)
        return self._update_class(class_)

    def _update_class(self, class_section: ClassSection) -> Dict[str, Any]:

        result = {
            'success': False,
            'message': ''
        }

        try:
            classes = self.get_all_classes()

            # Find and update the class
            for i, class_ in enumerate(classes):
                if class_.class_id == class_section.class_id:
                    classes[i] = class_section
                    break

            # Save all classes
            with open(self.classes_file, 'w') as f:
                for class_ in classes:
                    f.write(f"{class_.to_dict()}\n")

            result['success'] = True
            result['message'] = 'Class updated successfully'

        except Exception as e:
            result['message'] = f'Failed to update class: {str(e)}'

        return result