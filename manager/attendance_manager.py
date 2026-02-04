
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from ..modules.attendance import AttendanceRecord, AttendanceSummary


class AttendanceManager:


    def __init__(self):
        self.attendance_file = "File/attendance_records.text"
        self.attendance_summary_file = "File/attendance_summary.text"
        os.makedirs("File", exist_ok=True)

    def create_attendance_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:

        result = {
            'success': False,
            'message': '',
            'attendance_id': None
        }

        try:
            # Validate required fields
            required = ['attendance_id', 'course_id', 'session_date',
                        'start_time', 'end_time', 'lecturer_id']
            for field in required:
                if field not in session_data:
                    result['message'] = f'Missing required field: {field}'
                    return result

            # Create attendance record
            attendance = AttendanceRecord(**session_data)

            # Save to file
            with open(self.attendance_file, 'a') as f:
                f.write(f"{attendance.to_dict()}\n")

            result['success'] = True
            result['message'] = 'Attendance session created'
            result['attendance_id'] = attendance.attendance_id

        except Exception as e:
            result['message'] = f'Failed to create session: {str(e)}'

        return result

    def take_attendance(self, attendance_id: str, student_statuses: Dict[str, str]) -> Dict[str, Any]:

        result = {
            'success': False,
            'message': ''
        }

        try:
            # Load attendance record
            attendance = self._get_attendance_by_id(attendance_id)
            if not attendance:
                result['message'] = f'Attendance session {attendance_id} not found'
                return result

            # Mark attendance for each student
            for student_id, status in student_statuses.items():
                attendance.mark_attendance(student_id, status)

            # Update the record
            update_result = self._update_attendance_record(attendance)
            if update_result['success']:
                result['success'] = True
                result['message'] = 'Attendance recorded successfully'

                # Update attendance summary
                self._update_attendance_summary(attendance)
            else:
                result['message'] = update_result['message']

        except Exception as e:
            result['message'] = f'Failed to take attendance: {str(e)}'

        return result

    def get_attendance_by_course(self, course_id: str) -> List[AttendanceRecord]:

        records = self._get_all_attendance_records()
        return [r for r in records if r.course_id == course_id]

    def get_student_attendance(self, student_id: str, course_id: str = None) -> List[Dict]:

        records = self._get_all_attendance_records()
        student_records = []

        for record in records:
            if student_id in record.students:
                if course_id is None or record.course_id == course_id:
                    student_records.append({
                        'attendance_id': record.attendance_id,
                        'course_id': record.course_id,
                        'session_date': record.session_date,
                        'start_time': record.start_time,
                        'status': record.students[student_id],
                        'notes': record.notes
                    })

        return student_records

    def get_attendance_summary(self, student_id: str, course_id: str) -> Optional[AttendanceSummary]:

        summaries = self._get_all_attendance_summaries()

        for summary in summaries:
            if summary.student_id == student_id and summary.course_id == course_id:
                return summary

        return None

    def generate_attendance_report(self, course_id: str, start_date: str, end_date: str) -> Dict[str, Any]:

        result = {
            'success': False,
            'message': '',
            'report_data': None
        }

        try:
            records = self.get_attendance_by_course(course_id)

            # Filter by date range
            filtered_records = []
            for record in records:
                record_date = datetime.strptime(record.session_date, "%Y-%m-%d")
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")

                if start <= record_date <= end:
                    filtered_records.append(record)

            if not filtered_records:
                result['message'] = 'No attendance records found in the date range'
                return result

            # Compile report data
            report_data = {
                'course_id': course_id,
                'date_range': f"{start_date} to {end_date}",
                'total_sessions': len(filtered_records),
                'sessions': [],
                'student_stats': {}
            }

            # Collect student statistics
            for record in filtered_records:
                session_info = {
                    'date': record.session_date,
                    'time': f"{record.start_time}-{record.end_time}",
                    'total_students': len(record.students),
                    'stats': record.get_attendance_stats()
                }
                report_data['sessions'].append(session_info)

                # Update per-student stats
                for student_id, status in record.students.items():
                    if student_id not in report_data['student_stats']:
                        report_data['student_stats'][student_id] = {
                            'present': 0,
                            'absent': 0,
                            'late': 0,
                            'excused': 0,
                            'total': 0
                        }

                    report_data['student_stats'][student_id][status] += 1
                    report_data['student_stats'][student_id]['total'] += 1

            result['success'] = True
            result['message'] = 'Report generated successfully'
            result['report_data'] = report_data

        except Exception as e:
            result['message'] = f'Failed to generate report: {str(e)}'

        return result

    # === HELPER METHODS ===

    def _get_all_attendance_records(self) -> List[AttendanceRecord]:
        """Get all attendance records"""
        records = []

        if not os.path.exists(self.attendance_file):
            return records

        try:
            with open(self.attendance_file, 'r') as f:
                for line in f:
                    try:
                        data = eval(line.strip())
                        records.append(AttendanceRecord(**data))
                    except:
                        continue
        except:
            pass

        return records

    def _get_attendance_by_id(self, attendance_id: str) -> Optional[AttendanceRecord]:

        records = self._get_all_attendance_records()
        for record in records:
            if record.attendance_id == attendance_id:
                return record
        return None

    def _get_all_attendance_summaries(self) -> List[AttendanceSummary]:

        summaries = []

        if not os.path.exists(self.attendance_summary_file):
            return summaries

        try:
            with open(self.attendance_summary_file, 'r') as f:
                for line in f:
                    try:
                        data = eval(line.strip())
                        summaries.append(AttendanceSummary(**data))
                    except:
                        continue
        except:
            pass

        return summaries

    def _update_attendance_record(self, attendance: AttendanceRecord) -> Dict[str, Any]:
        """Update attendance record in file"""
        result = {
            'success': False,
            'message': ''
        }

        try:
            records = self._get_all_attendance_records()

            # Find and update the record
            for i, record in enumerate(records):
                if record.attendance_id == attendance.attendance_id:
                    records[i] = attendance
                    break

            # Save all records
            with open(self.attendance_file, 'w') as f:
                for record in records:
                    f.write(f"{record.to_dict()}\n")

            result['success'] = True
            result['message'] = 'Attendance record updated'

        except Exception as e:
            result['message'] = f'Failed to update record: {str(e)}'

        return result

    def _update_attendance_summary(self, attendance: AttendanceRecord):
        """Update attendance summary after taking attendance"""
        summaries = self._get_all_attendance_summaries()

        for student_id, status in attendance.students.items():
            # Find existing summary
            summary_found = False
            for summary in summaries:
                if (summary.student_id == student_id and
                        summary.course_id == attendance.course_id):

                    summary.total_sessions += 1
                    if status == "present":
                        summary.present_count += 1
                    elif status == "absent":
                        summary.absent_count += 1
                    elif status == "late":
                        summary.late_count += 1
                    elif status == "excused":
                        summary.excused_count += 1

                    summary.calculate_rate()
                    summary_found = True
                    break

            # Create new summary if not found
            if not summary_found:
                # Need to get semester/year from course - simplified
                new_summary = AttendanceSummary(
                    student_id=student_id,
                    course_id=attendance.course_id,
                    semester="Spring",  # Should get from course
                    year=2024,  # Should get from course
                    total_sessions=1
                )

                if status == "present":
                    new_summary.present_count = 1
                elif status == "absent":
                    new_summary.absent_count = 1
                elif status == "late":
                    new_summary.late_count = 1
                elif status == "excused":
                    new_summary.excused_count = 1

                new_summary.calculate_rate()
                summaries.append(new_summary)

        # Save updated summaries
        with open(self.attendance_summary_file, 'w') as f:
            for summary in summaries:
                f.write(f"{summary.to_dict()}\n")