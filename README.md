# Course Data Dive 📚

This project extracts course data from PDF files of SUT (Suranaree University of Technology) and saves it in CSV and JSON formats.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Makefile Commands](#makefile-commands)

## Prerequisites

- Python 3.x
- Virtual environment (`venv`) module
- make cli (`optional`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pandakn/course-data-dive.git
   cd course-data-dive
   ```
2. Create and activate the virtual environment, then install the dependencies:
   ```bash
    make setup
   ```

## Usage

1. To extract course data from a PDF:
   ```bash
    make run
   ```
2. The extracted data will be saved as courses.csv and courses.json in the same directory as the PDF file:

   ##### JSON

   ```json
   [
     {
       "id": "ENG23 2031",
       "code": "ENG23 2031",
       "name": "โครงสร้างข้อมูลและขั้นตอนวิธี",
       "credit": "4(4-0-8)",
       "description": "การวิเคราะห์ขั้นตอนวิธีเบื้องต้น ความซับซ้อนของขั้นตอนวิธี ขั้นตอนวิธีในการเรียงลำดับและค้นหาข้อมูล โครงสร้างข้อมูลลิงค์ลิสต์ คิว สแตก ไบนารีทรี บีทรีและฮีพ กลยุทธ์ของขั้นตอนวิธี",
       "prerequisites": "ENG23 2001 การเขียนโปรแกรมคอมพิวเตอร์ 2",
       "prerequisites_list": ["ENG23 2001"]
     },
     {
       "id": "ENG23 2032",
       "code": "ENG23 2032",
       "name": "เทคโนโลยีเชิงวัตถุ",
       "credit": "4(3-3-9)",
       "description": "แนวคิดเชิงวัตถุ การเขียนโปรแกรมเชิงวัตถุ คลาสและวัตถุ การห่อหุ้ม การสืบทอด โพลีมอร์ฟิสซึม อินเตอร์เฟสสายอักขระ การจัดการข้อผิดพลาด",
       "prerequisites": "ENG23 2001 การเขียนโปรแกรมคอมพิวเตอร์ 2 และ  ENG23 2003 การแก้ปัญหาด้วยการโปรแกรม",
       "prerequisites_list": ["ENG23 2001", "ENG23 2003"]
     }
   ]
   ```

   ##### CSV

   | id         | code       | name                          | credit   | prerequisites                                                                    | description                                                                                                                                                                        |
   | ---------- | ---------- | ----------------------------- | -------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | ENG23 2031 | ENG23 2031 | โครงสร้างข้อมูลและขั้นตอนวิธี | 4(4-0-8) | ENG23 2001 การเขียนโปรแกรมคอมพิวเตอร์ 2                                          | การวิเคราะห์ขั้นตอนวิธีเบื้องต้น ความซับซ้อนของขั้นตอนวิธี ขั้นตอนวิธีในการเรียงลำดับและค้นหาข้อมูล โครงสร้างข้อมูลลิงค์ลิสต์ คิว สแตก ไบนารีทรี บีทรีและฮีพ กลยุทธ์ของขั้นตอนวิธี |
   | ENG23 2032 | ENG23 2032 | เทคโนโลยีเชิงวัตถุ            | 4(3-3-9) | ENG23 2001 การเขียนโปรแกรมคอมพิวเตอร์ 2 และ ENG23 2003 การแก้ปัญหาด้วยการโปรแกรม | แนวคิดเชิงวัตถุ การเขียนโปรแกรมเชิงวัตถุ คลาสและวัตถุ การห่อหุ้ม การสืบทอด โพลีมอร์ฟิสซึม อินเตอร์เฟสสายอักขระ การจัดการข้อผิดพลาด                                                 |

## Makefile Commands

- `make setup` : Create virtual environment and install dependencies
- `make test` : Run all tests
- `make lint` : Run linter (Ruff)
- `make format` : Format code with Ruff
- `make check` : Run linter and formatter check without making changes
- `make clean` : Remove virtual environment and cache files
- `make run` : Run the main application
