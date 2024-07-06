from extractor import CourseExtractor
from file_handler import save_courses_to_csv, save_courses_to_json, get_output_paths
from logger import logger


def analyze_courses(courses):
	count_dont_have_credit = sum(1 for course in courses if not course['credit'])
	count_dont_have_name = sum(1 for course in courses if not course['name'])
	count_dont_have_description = sum(
		1 for course in courses if not course['description']
	)
	count_dont_have_prerequisites = sum(
		1 for course in courses if not course['prerequisites']
	)

	# for idx, course in enumerate(courses):
	# 	logger.info(
	# 		f'Course {idx+1}:\n{json.dumps(course, indent=4, sort_keys=True, ensure_ascii=False)}\n'
	# 	)

	logger.info(f"Count don't have credit: {count_dont_have_credit}")
	logger.info(f"Count don't have name: {count_dont_have_name}")
	logger.info(f"Count don't have description: {count_dont_have_description}")
	logger.info(f"Count don't have prerequisites: {count_dont_have_prerequisites}")


def main():
	logger.info('Starting course extraction process')

	pdf_path = './courses/engineering/cpe/index.pdf'
	extractor = CourseExtractor()
	courses = extractor.extract_courses_from_pdf(pdf_path)

	analyze_courses(courses)

	csv_path, json_path = get_output_paths(pdf_path)
	save_courses_to_csv(courses, csv_path)
	save_courses_to_json(courses, json_path)

	logger.info('Course extraction process completed')


if __name__ == '__main__':
	main()
