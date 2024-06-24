import re


def remove_thai_chars(text):
	# Character class that matches Thai characters
	thai_chars = r'[\u0E00-\u0E7F]+'

	match = re.search(thai_chars, text)

	if match:
		return text[: match.start()].replace('  ', '')

	return text


def extract_prerequisites(prereq_text):
	# Regex pattern for prerequisite line
	pattern = r'วิชาบังคับก่อน\s*:\s+(?P<course_code>.*)'

	# pattern = r"วิชาบังคับก่อน\s*:\s*(?P<course_code>[\w]+)\s+(?P<course_name>.*)"

	# Match the text with the pattern
	match = re.search(pattern, prereq_text)

	# Check if there's a match
	if match:
		# Extract course code and name from the match groups
		course_code = match.group('course_code')

		return course_code.strip()

	else:
		# No prerequisites found
		return None


# 'วิชาบังคับก่อน : ENG23 2001 การเขียนโปรแกรมคอมพิเตอร์ 2'
# prereq_text = "วิชาบังคับก่อน :      ENG23     1001    การเขียนโปรแกรมคอมพิเตอร์ 1"
prereq_text = 'วิชาบังคับก่อน : ENG23 2001 การเขียนโปรแกรมคอมพิเตอร์ 2'

prerequisite_info = extract_prerequisites(prereq_text)
only_course_code = remove_thai_chars(prerequisite_info)

if prerequisite_info:
	print(prerequisite_info)
	print(only_course_code)
else:
	print('No prerequisites found')

# [
#   {
#     'code': 'ENG23 2001',
#     'name': 'การเขียนโปรแกรมคอมพิเตอร์ 2',
#   },
#   {
#     'code': 'ENG23 2003',
#     'name': 'การแก้ปัญาด้ยการโปรแกรม',
#   },
# ]
