import re
import fitz  # PyMuPDF
import logging
import json
from typing import TypedDict, List
import csv
import os

logging.basicConfig(
	level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)


class Course(TypedDict):
	id: str
	code: str
	name: str
	credit: str
	prerequisites: str
	description: str


pattern = r"""
    ^(?P<course_code>
        (\w{3}\s*\d{2}\s\d{4})        # Course code format: XXX 99 9999
        |                             # OR
        (\d{6,})                      # Course code format: 999999
        |                             # OR
        (\w{3}\d{2}\s+\d{4})          # Course code format: XXX99 9999
    )
    # \s+                               # One or more whitespace characters
    (?P<course_name>.*?\d+|.*?)      # Course name (non-greedy)
    (\s+(?P<credits>\d.*?))?          # Credit information (including optional version number) and end of line
$
"""
compiled_pattern = re.compile(pattern, re.VERBOSE)

course_code_pattern = r'(\w{3}\s*\d{2}\s\d{4})|(\d{6,})|(\w{3}\d{2}\s+\d{4})'
course_name_pattern = r'.*?\d+|.*?'
# credit_pattern = r'\d\((\d)-(\d)-(\d)\)'
# credit_pattern = r'\d\s*\(\s*(\d)\s*-\s*(\d)\s*-\s*(\d)\s*\)'
# credit_pattern = r'\d\s*\(\s*\d\s*-\s*\d\s*-\s*\d\s*\)|\d\s*หน่วยกิต'
credit_pattern = r'\w\s*\(\s*\d+\s*-\s*\d+\s*-\s*\d+\s*\)|\d+\s*(หน่วยกิต|[Cc]redits)'
# prerequisite_pattern = (
# 	r'(วิชาบังคับก่อน|วิชาที่บังคับก่อน|วิาบังคับก่อน|Pre-requisite|Prerequisite)\s*:\s+'
# )
prerequisite_pattern = r'(วิชาบังคับก่อน|วิชาที่บังคับก่อน|วิาบังคับก่อน|Pre-requisite|Prerequisite)\s*:\s+(?P<course_pre_req>.*)'

c = 'IST30 1101'
t = 'ภาษาอังกฤษเพื่อการสื่อสาร 1'
credit = '  4(3-3-9)     '

# prove the pattern works
tee = 'IST30 1101  ภาษาอังกฤษเพื่อการสื่อสาร 1   8 หน่วยกิต     '
m = compiled_pattern.match(tee)
cc = m.group('course_code')
cn = m.group('course_name')
cr = m.group('credits')
# print(re.match(credit_pattern, credit))
# print(cc, cn, cr)


def remove_thai_chars(text):
	# Character class that matches Thai characters
	thai_chars = r'[\u0E00-\u0E7F]+\s+(\d+.*?)'

	match = re.search(thai_chars, text)

	if match:
		print(match)
		return text[: match.start()].replace('  ', '')

	return text


def extract_course_detail(lines) -> List[Course]:
	courses = []

	course: Course = {}
	pass_prerequisite = False

	start_line_description = 0
	end_line_description = 0

	for idx, line_raw in enumerate(lines):
		line = line_raw.strip()

		# check empty string
		if not line:
			continue

		if course and bool(course['code']) and not bool(course['name']):
			course['name'] = line.strip()

		prereq_match = re.search(prerequisite_pattern, line)
		if prereq_match and not pass_prerequisite:
			# course['prerequisites'] = line.split(':')[1].strip()
			course['prerequisites'] = remove_thai_chars(
				prereq_match.group('course_pre_req')
			)

			pass_prerequisite = True
			start_line_description = idx + 1  # plus 1 to skip the line 'prerequisite'
			continue

		# * get index of course learning outcomes for find course_description
		if (
			line == 'ผลลัพธ์การเรียนรู้ที่คาดหวังระดับรายวิชา'
			or line.lower() == 'Course learning outcomes (CLOs)'.lower()
		):
			end_line_description = idx

		match = compiled_pattern.match(line)
		if match:
			# check if match is prerequisite
			if pass_prerequisite:
				continue

			course_code = match.group('course_code')
			course_name = match.group('course_name')
			credits = match.group('credits')

			course = {
				'id': course_code.strip() if course_code else None,
				'code': course_code.strip() if course_code else None,
				'name': course_name.strip() if course_name else None,
				'credit': credits.strip() if credits else None,
				'description': None,
				'prerequisites': None,
			}

			courses.append(course)

		credit_match = re.match(credit_pattern, line)
		if course and course['code'] and credit_match:
			course['credit'] = credit_match.string.strip()

		# TODO -> make this to support multi-line prerequisite
		if course and not course['description']:
			if start_line_description < end_line_description:
				course['description'] = (
					''.join(lines[start_line_description:end_line_description])
					.replace('  ', ' ')
					.strip()
				)

				# reset index for other course
				start_line_description = 0
				end_line_description = 0

		pass_prerequisite = False
	return courses


def extract_text_one_page(doc, page_number):
	page = doc.load_page(page_number)
	text = page.get_text('text', sort=True, flags=fitz.TEXT_INHIBIT_SPACES)
	lines = text.splitlines()

	return extract_course_detail(lines)


def extract_text_all_page(doc) -> List[Course]:
	courses: List[Course] = []

	for page_number in range(doc.page_count):
		page = doc.load_page(page_number)
		text = page.get_text(sort=True)
		# print(text.replace('\n', ''))
		lines = text.splitlines()

		print('page:', page_number + 1)
		courses += extract_course_detail(lines)

	return courses


def extract_courses_from_pdf(pdf_path):
	doc = fitz.open(pdf_path)

	# first page start at `0`
	courses = extract_text_one_page(doc=doc, page_number=16)
	# courses = extract_text_all_page(doc=doc)

	return courses


def save_courses_to_csv(courses, csv_path):
	fieldnames = ['id', 'code', 'name', 'credit', 'prerequisites', 'description']
	with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		writer.writeheader()
		for course in courses:
			writer.writerow(course)


def save_courses_to_json(courses, json_path):
	with open(json_path, mode='w', encoding='utf-8') as jsonfile:
		json.dump(courses, jsonfile, ensure_ascii=False, indent=4)


pdf_path = './courses/engineering/cpe/index.pdf'
# pdf_path = './courses/science/com_sci/index.pdf'

courses = extract_courses_from_pdf(pdf_path)
# print('course:', courses)
count_dont_have_credit = 0
count_dont_have_name = 0
count_dont_have_description = 0
count_dont_have_prerequisites = 0

for idx, course in enumerate(courses):
	if not course['name']:
		count_dont_have_name += 1
		# print(f'{idx}: {course}')

	if not course['credit']:
		count_dont_have_credit += 1

	if not course['description']:
		count_dont_have_description += 1
		# print(f'{idx}: {course}')

	if not course['prerequisites']:
		count_dont_have_prerequisites += 1
		# print(f'{idx}: {course}')

	logging.info(
		f'Course {idx+1}:\n{json.dumps(course, indent=4, sort_keys=True, ensure_ascii=False)}\n'
	)
	# logging.info(course)

print()
logging.info(f'count dont have credit: {count_dont_have_credit}')
logging.info(f'count dont have name: {count_dont_have_name}')
logging.info(f'count dont have description: {count_dont_have_description}')
logging.info(f'count dont have prerequisites: {count_dont_have_prerequisites}')

# Specify the CSV and JSON paths in the same directory as the PDF
base_path = os.path.dirname(pdf_path)
csv_path = os.path.join(base_path, 'courses.csv')
json_path = os.path.join(base_path, 'courses.json')

save_courses_to_csv(courses, csv_path)
save_courses_to_json(courses, json_path)

logging.info(f'Courses saved to {csv_path}')
logging.info(f'Courses saved to {json_path}')
# [
# 	{
# 		'code': 'SCI05 1191',
# 		'name': 'ปฏิบัติการฟิสิกส์ 1',
# 		'credit': '1(0-3-0)',
# 		'prereqs': 'SCI05 1001 ฟิสิกส์ 1 หรือเรียนควบคู่กับฟิสิกส์ 1 หรือโดยความเห็นชอบของสาขาวิชา',
# 	},
# 	{
# 		'code': 'SCI05 1192',
# 		'name': 'ปฏิบัติการฟิสิกส์ 2',
# 		'credit': '1(0-3-0)',
# 		'prereqs': 'SCI05 1191 ปฏิบัติการฟิสิกส์ 1 และ SCI05 1002 ฟิสิกส์ 2 หรือผ่านการเรียน SCI05 1191 ปฏิบัติการฟิสิกส์ 1 มาแล้ว และกำลังเรียน SCI05 1002 ฟิสิกส์ 2 อยู่ หรือโดยความเห็นชอบของสาขาวิชา',
# 	},
# ]
