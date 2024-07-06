from typing import TypedDict, List


class Course(TypedDict):
	id: str
	code: str
	name: str
	credit: str
	prerequisites: str
	description: str
	prerequisites_list: List[str]
