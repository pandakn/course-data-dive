import csv
import json
import os
from logger import logger


def save_courses_to_csv(courses, csv_path):
	logger.info(f'Saving courses to CSV: {csv_path}')
	fieldnames = ['id', 'code', 'name', 'credit', 'prerequisites', 'description']

	with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for course in courses:
			if 'prerequisites_list' in course:
				continue

			writer.writerow(course)


def save_courses_to_json(courses, json_path):
	logger.info(f'Saving courses to JSON: {json_path}')
	with open(json_path, mode='w', encoding='utf-8') as jsonfile:
		json.dump(courses, jsonfile, ensure_ascii=False, indent=4)


def get_output_paths(pdf_path):
	base_path = os.path.dirname(pdf_path)
	csv_path = os.path.join(base_path, 'courses.csv')
	json_path = os.path.join(base_path, 'courses.json')

	return csv_path, json_path
