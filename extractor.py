import re
from typing import List
from logger import logger
import fitz  # PyMuPDF
from itertools import chain
from course import Course


class CourseExtractor:
	def __init__(self):
		self.logger = logger.getChild('CourseExtractor')
		self.courses_result: List[Course] = []
		self.pattern = re.compile(
			r"""
            ^(?P<course_code>
                (\w{3}\s*\d{2}\s\d{4})        # Course code format: XXX 99 9999
                |                             # OR
                (\d{6,})                      # Course code format: 999999
                |                             # OR
                (\w{3}\d{2}\s+\d{4})          # Course code format: XXX99 9999
            )
            (?P<course_name>.*?\d+|.*?)      # Course name (non-greedy)
            (\s+(?P<credits>\d.*?))?          # Credit information (including optional version number) and end of line
            $
            """,
			re.VERBOSE,
		)
		self.course_code_pattern = (
			r'(\w{3}\s*\d{2}\s\d{4})|(\d{6,})|(\w{3}\d{2}\s+\d{4})'
		)
		self.credit_pattern = (
			r'\w\s*\(\s*\d+\s*-\s*\d+\s*-\s*\d+\s*\)|\d+\s*(หน่วยกิต|[Cc]redits)'
		)
		self.prerequisite_pattern = r'(วิชาบังคับก่อน|วิชาที่บังคับก่อน|วิาบังคับก่อน|Pre-requisite|Prerequisite)\s*:\s+(?P<course_pre_req>.*)'

	def remove_thai_chars(self, text):
		match_course_code = re.findall(self.course_code_pattern, text)

		if match_course_code:
			# Flatten the nested list and remove duplicates
			flattened_list = list(set(chain.from_iterable(match_course_code)))

			# remove empty string elements
			return sorted([item for item in flattened_list if item.strip()])

		return None

	def extract_course_detail(self, lines) -> List[Course]:
		courses = []
		course: Course = {}
		pass_prerequisite = False
		start_line_description = end_line_description = 0

		for idx, line in enumerate(lines):
			line = line.strip()
			# check empty string
			if not line:
				continue

			if course and bool(course['code']) and not bool(course['name']):
				course['name'] = line

			prereq_match = re.search(self.prerequisite_pattern, line, re.IGNORECASE)
			if prereq_match and not pass_prerequisite:
				pass_prerequisite = True

				# plus 1 to skip the line 'prerequisite'
				start_line_description = idx + 1
				continue

			# TODO -> should refactor this
			# * get index of course learning outcomes for find course_description
			if (
				line == 'ผลลัพธ์การเรียนรู้ที่คาดหวังระดับรายวิชา'
				or line.lower() == 'course learning outcomes (clos)'
				or line.lower() == 'course learning outcomes (clos):'
				or line.lower()
				== 'ผลลัพธ์การเรียนรู้ที่คาดหวังระดับรายวิชา (course learning outcomes: clos):'
			):
				end_line_description = idx

			match = self.pattern.match(line)
			if match:
				if pass_prerequisite:
					continue

				# TODO: refactor this
				course_id = match.group('course_code').strip()
				existing_course: Course = next(
					(c for c in courses if c.get('id') == course_id), None
				)

				if existing_course:
					# course = {
					# 	'id': existing_course.get('id'),
					# 	'code': existing_course.get('code'),
					# 	'name': match.group('course_name').strip()
					# 	if match.group('course_name')
					# 	else None,
					# 	'credit': existing_course.get('credit'),
					# 	'description': None,
					# 	'prerequisites': None,
					# 	'prerequisites_list': existing_course.get('prerequisites_list'),
					# }
					# course = existing_course
					continue
				else:
					existing_course = next(
						(c for c in self.courses_result if c.get('id') == course_id),
						None,
					)
					if existing_course:
						continue
					course = {
						'id': course_id,
						'code': course_id,
						'name': match.group('course_name').strip()
						if match.group('course_name')
						else None,
						'credit': match.group('credits').strip()
						if match.group('credits')
						else None,
						'description': None,
						'prerequisites': None,
						'prerequisites_list': None,
					}

				courses.append(course)

			credit_match = re.match(self.credit_pattern, line)
			if course and course['code'] and credit_match:
				course['credit'] = credit_match.string.strip()

			if course and not course['description']:
				if start_line_description < end_line_description:
					# * loop from last line of description towards the start line of prerequisite
					# * until an empty line is found (empty line is separates prerequisite and description; I wish it could fine any PDF lol😂)
					for i in range(
						end_line_description - 1, start_line_description - 1, -1
					):
						if i == start_line_description and not course['description']:
							course['description'] = (
								''.join(lines[i:end_line_description])
								.replace('  ', ' ')
								.strip()
							)
							prereq = (
								''.join(lines[start_line_description - 1 : i])
								.replace('  ', ' ')
								.strip()
							)

							course['prerequisites_list'] = self.remove_thai_chars(
								prereq
							)
							course['prerequisites'] = prereq.split(':')[1].strip()

						if not lines[i].strip() and i != end_line_description - 1:
							course['description'] = (
								''.join(lines[i + 1 : end_line_description])
								.replace('  ', ' ')
								.strip()
							)

							prereq = (
								''.join(lines[start_line_description - 1 : i])
								.replace('  ', ' ')
								.strip()
							)

							course['prerequisites_list'] = self.remove_thai_chars(
								prereq
							)
							course['prerequisites'] = prereq.split(':')[1].strip()

							break
					start_line_description = end_line_description = 0

			pass_prerequisite = False
		return courses

	def extract_text_from_page(self, doc, page_number):
		page = doc.load_page(page_number)
		text = page.get_text('text', sort=True)

		return text.splitlines()

	def extract_courses_from_pdf(self, pdf_path) -> List[Course]:
		self.logger.info(f'Extracting courses from {pdf_path}')

		doc = fitz.open(pdf_path)

		for page_number in range(doc.page_count):
			lines = self.extract_text_from_page(doc, page_number)
			self.courses_result += self.extract_course_detail(lines)

		unique_courses = {course['id']: course for course in self.courses_result}

		return list(unique_courses.values())
