import re
from pypdf import PdfReader


def remove_thai_chars(text):
	# Character class that matches Thai characters
	thai_chars = r'[\u0E00-\u0E7F]+\s+(\d+.*?)'

	match = re.search(thai_chars, text)

	if match:
		print(match)
		return text[: match.start()].replace('  ', '')

	return text


# creating a pdf reader object
reader = PdfReader('./courses/engineering/cpe/index.pdf')

page = reader.pages[16]

# extracting text from page
# text = page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False)
text = page.extract_text(extraction_mode='layout', layout_mode_space_vertically=False)

lines = text.splitlines()

courses = []

pattern = r"""
    ^(?P<course_code>
        (\w{3}\s*\d{2}\s\d{4})        # Course code format: XXX 99 9999
        |                             # OR
        (\d{6,})                      # Course code format: 999999
        |                             # OR
        (\w{3}\d{2}\s+\d{4})          # Course code format: XXX99 9999
    )
    \s+                               # One or more whitespace characters
    (?P<course_name>.*?\d+|.*?)      # Course name (non-greedy)
    (\s+(?P<credits>\d.*?))?          # Credit information (including optional version number) and end of line
$
"""

# Process each line
for idx, line in enumerate(lines):
	# if (line == 'ผลลัพธ์การเรียนรู้ที่คาดหวังระดับรายวิชา'):
	#   print(f'{idx} eieie\n\n\n')
	#   continue

	# print(f'line {idx}: {line}')
	compiled_pattern = re.compile(pattern, re.VERBOSE)

	match = compiled_pattern.match(line)

	if match:
		course_code = match.group('course_code')
		course_name = match.group('course_name')
		credits = match.group('credits')

		# print(f"Course Code: {course_code.replace('  ', '')}")
		# print(f"Course Name: {course_name}")
		# print(f"Credits: {credits}")

	# extract prerequisites
	patternPre = r'วิชาบังคับก่อน\s*:\s+(?P<course_pre_req>.*)'
	match_prerequisites = re.search(patternPre, line)
	# print(match_prerequisites)

	if match_prerequisites:
		course_pre_req = match_prerequisites.group('course_pre_req')
		# print(match_prerequisites)
		# print(f"course pre-req: {course_pre_req.replace('  ', '')}")
		# print()
		clean_course_code = remove_thai_chars(course_pre_req)
		pre_course_name = course_pre_req.replace(
			clean_course_code.replace('  ', ''), ''
		)
		print(clean_course_code, pre_course_name)
		print()
		# course = {
		# 'code': course_code,
		# 'name': course_name,
		# 'credits': credits,
		# 'prerequisites': prerequisites,
		# 'description': ''
		# }


# I wanna like this
# {
#   'code': 'ENG 23 2031',
#   'name': 'โครงสร้างข้อมูลและขั้นตอนวิธี',
#   'prereqs': 'ENG23 2001 การเขียนโปรแกรมคอมพิวเตอร์ 2',
#   'description': 'การวิเคราะห์ขั้นตอนวิธีเบื้องต้น ความซับซ้อนของขั้นตอนวิธี ขั้นตอนวิธีในการเรียงลำดับและค้นหาข้อมูล โครงสร้างข้อมูลลิงค์ลิสต์  คิว สแตก ไบนารีทรี บีทรีและฮีพ กลยุทธ์ของขั้นตอนวิธีผลลัพธ์การเรียนรู้ที่คาดหวังระดับรายวิชา'
# },
# {
#   'code': 'ENG 23 2032',
#   'name': 'เทคโนโลยีเชิงวัตถุ',
#   'prereqs': 'ENG 23 2001 การเขียนโปรแกรมคอมพิวเตอร์ 2 และ ENG23 2003 การแก้ปัญหาด้วยการโปรแกรม',
#   'description': 'แนคิดเชิงัตถุ การเขียนโปรแกรมเชิงัตถุ คลาและัตถุ การ่อุ้ม การืบทอด โพลีมอร์ฟิซึม อินเตอร์เฟายอักขระ การจัดการข้อผิดพลาด'
# }
