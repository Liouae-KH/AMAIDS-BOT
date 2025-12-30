import os
import json
import logging
from typing import Final

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ==================== CONFIGURATION ====================
BOT_TOKEN: Final = os.environ.get('BOT_TOKEN')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== LOAD SPECIALTIES DATA ====================
with open('specialties.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# ==================== KEYBOARD BUILDERS ====================
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Specialty Information", callback_data="specialty_info")],
        [InlineKeyboardButton("Curriculum", callback_data="curriculum_menu")],
        [InlineKeyboardButton("Objectives and Competencies", callback_data="objectives")],
        [InlineKeyboardButton("Employability", callback_data="employability")],
        [InlineKeyboardButton("Further Study Pathways", callback_data="further_study")],
        [InlineKeyboardButton("Program Statistics", callback_data="statistics")]
    ]
    return InlineKeyboardMarkup(keyboard)

def curriculum_menu_keyboard():
    keyboard = []
    for i in range(1, 7):
        keyboard.append([InlineKeyboardButton(f"Semester {i}", callback_data=f"semester_{i}")])
    keyboard.append([InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def semester_courses_keyboard(semester_num):
    keyboard = []
    semester_key = f"semester{semester_num}"
    courses = data["curriculum"][semester_key]["courses"]
    
    for idx, course in enumerate(courses):
        course_name = course["name"]
        if len(course_name) > 30:
            course_name = course_name[:27] + "..."
        keyboard.append([InlineKeyboardButton(course_name, callback_data=f"course_{semester_num}_{idx}")])
    
    keyboard.append([InlineKeyboardButton("Back to Semesters", callback_data="curriculum_menu")])
    keyboard.append([InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def back_to_semester_keyboard(semester_num):
    keyboard = [
        [InlineKeyboardButton("Back to Semester Courses", callback_data=f"semester_{semester_num}")],
        [InlineKeyboardButton("Back to Semesters", callback_data="curriculum_menu")],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ==================== MESSAGE BUILDERS ====================
def build_specialty_info():
    text = f"""
UNIVERSITY INFORMATION

University: {data['university']}
Faculty: {data['faculty']}
Department: {data['department']}
Domain: {data['domain']}
Field: {data['field']}
Specialty: {data['specialty']}

ACADEMIC DETAILS

Academic Year: {data['academic_year']}
Degree Type: {data['degree_type']}
Duration: {data['duration']}
Total Credits: {data['total_credits']}

PROGRAM OVERVIEW

Description: {data['program_overview']['description']}
Structure: {data['program_overview']['structure']}
Weekly Hours: {data['program_overview']['weekly_hours']}
Total Hours: {data['program_overview']['total_hours']}
"""
    return text

def build_objectives():
    text = "PROGRAM OBJECTIVES\n\n"
    for idx, objective in enumerate(data['objectives'], 1):
        text += f"{idx}. {objective}\n"
    
    text += "\nTARGETED PROFILES\n\n"
    for idx, profile in enumerate(data['targeted_profiles'], 1):
        text += f"{idx}. {profile}\n"
    
    text += "\nCOMPETENCIES\n\n"
    competencies = data['competencies']
    
    text += "Mathematical Skills:\n"
    for skill in competencies['mathematical_skills']:
        text += f"- {skill}\n"
    
    text += "\nComputational Skills:\n"
    for skill in competencies['computational_skills']:
        text += f"- {skill}\n"
    
    text += "\nData Science Skills:\n"
    for skill in competencies['data_science_skills']:
        text += f"- {skill}\n"
    
    text += "\nSoft Skills:\n"
    for skill in competencies['soft_skills']:
        text += f"- {skill}\n"
    
    return text

def build_employability():
    text = "EMPLOYMENT OPPORTUNITIES\n\n"
    
    text += "REGIONAL OPPORTUNITIES (Ouargla Region)\n\n"
    regional = data['employability']['regional']
    
    text += "Energy Sector:\n"
    text += f"- {regional['energy_sector']}\n\n"
    
    text += "Technology Initiatives:\n"
    text += f"- {regional['technology_initiatives']}\n\n"
    
    text += "Education & Research:\n"
    text += f"- {regional['education_research']}\n\n"
    
    text += "NATIONAL OPPORTUNITIES\n\n"
    national = data['employability']['national']
    
    text += "Technology & IT:\n"
    text += f"- {national['technology_it']}\n\n"
    
    text += "Public Sector:\n"
    text += f"- {national['public_sector']}\n\n"
    
    text += "Finance & Banking:\n"
    text += f"- {national['finance_banking']}\n\n"
    
    text += "International Companies:\n"
    text += f"- {national['international_companies']}\n"
    
    return text

def build_further_study():
    text = "FURTHER STUDY PATHWAYS\n\n"
    
    text += "MASTERS PROGRAMS\n"
    for program in data['further_study_pathways']['masters_programs']:
        text += f"- {program}\n"
    
    text += "\nINTERDISCIPLINARY FIELDS\n"
    for field in data['further_study_pathways']['interdisciplinary_fields']:
        text += f"- {field}\n"
    
    text += "\nPROFESSIONAL CERTIFICATIONS\n"
    for cert in data['further_study_pathways']['professional_certifications']:
        text += f"- {cert}\n"
    
    text += f"\nRESEARCH & ACADEMIA\n"
    text += f"- {data['further_study_pathways']['research_academia']}\n"
    
    return text

def build_statistics():
    stats = data['program_statistics']
    text = f"""
PROGRAM STATISTICS

TEACHING HOURS
- Lecture Hours: {stats['total_lecture_hours']}
- Tutorial Hours: {stats['total_tutorial_hours']}
- Practical Hours: {stats['total_practical_hours']}
- Personal Work Hours: {stats['total_personal_work_hours']}
- Total Contact Hours: {stats['total_lecture_hours'] + stats['total_tutorial_hours'] + stats['total_practical_hours']}

CREDITS DISTRIBUTION
- Fundamental Units: {stats['credits_distribution']['fundamental']} credits ({stats['percentage_distribution']['fundamental']}%)
- Methodological Units: {stats['credits_distribution']['methodological']} credits ({stats['percentage_distribution']['methodological']}%)
- Discovery Units: {stats['credits_distribution']['discovery']} credits ({stats['percentage_distribution']['discovery']}%)
- Transversal Units: {stats['credits_distribution']['transversal']} credits ({stats['percentage_distribution']['transversal']}%)

TEACHING STAFF
- Professors: {data['teaching_staff_summary']['professors']}
- Associate Professors A: {data['teaching_staff_summary']['associate_professors_a']}
- Associate Professors B: {data['teaching_staff_summary']['associate_professors_b']}
- Assistant Professors A: {data['teaching_staff_summary']['assistant_professors_a']}
- Total Teaching Staff: {data['teaching_staff_summary']['total']}

MATERIAL RESOURCES
- Laboratory: {data['material_resources']['laboratory']}
- Equipment: {data['material_resources']['equipment'][0]['quantity']} {data['material_resources']['equipment'][0]['item']}s
"""
    return text

def build_semester_info(semester_num):
    semester_key = f"semester{semester_num}"
    semester_data = data["curriculum"][semester_key]
    
    text = f"""
SEMESTER {semester_num}

Total Credits: {semester_data['total_credits']}
Total Hours: {semester_data['total_hours']}

COURSES:
"""
    for idx, course in enumerate(semester_data['courses'], 1):
        text += f"{idx}. {course['name']} ({course['code']}) - {course['credits']} credits\n"
    
    text += "\nClick on any course to see detailed information."
    return text

def build_course_details(semester_num, course_idx):
    semester_key = f"semester{semester_num}"
    course = data["curriculum"][semester_key]["courses"][course_idx]
    
    text = f"""
COURSE DETAILS

Code: {course['code']}
Name: {course['name']}
Type: {course['type']}
Credits: {course['credits']}
Coefficient: {course['coefficient']}

TEACHING VOLUME (hours per week)
- Lecture: {course['volume']['lecture']}
- Tutorial: {course['volume']['tutorial']}
- Practical: {course['volume']['practical']}
- Personal Work: {course['volume']['personal_work']}
- Total Hours: {course['volume']['total_hours']}

OBJECTIVES
{course['objectives']}

PREREQUISITES
{course['prerequisites']}

COURSE CONTENT
"""
    for idx, chapter in enumerate(course['content'], 1):
        text += f"{idx}. {chapter}\n"
    
    text += f"\nEVALUATION"
    if 'evaluation' in course:
        text += f"\n- Continuous Assessment: {course['evaluation']['continuous']}%"
        text += f"\n- Final Exam: {course['evaluation']['exam']}%"
    
    text += f"\n\nREFERENCES"
    for ref in course['references']:
        text += f"\n- {ref}"
    
    if 'note' in course:
        text += f"\n\nNOTE: {course['note']}"
    
    return text

# ==================== HANDLERS ====================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
Welcome to the University Specialty Information Bot.

This bot provides detailed information about the Applied Mathematics for Artificial Intelligence and Data Science program.

Use the buttons below to navigate through the information.
"""
    await update.message.reply_text(welcome_text, reply_markup=main_menu_keyboard())

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    
    if callback_data == "main_menu":
        await query.edit_message_text(
            "Main Menu. Select an option:",
            reply_markup=main_menu_keyboard()
        )
    
    elif callback_data == "specialty_info":
        text = build_specialty_info()
        await query.edit_message_text(text, reply_markup=main_menu_keyboard())
    
    elif callback_data == "curriculum_menu":
        await query.edit_message_text(
            "Select a semester to view courses:",
            reply_markup=curriculum_menu_keyboard()
        )
    
    elif callback_data.startswith("semester_"):
        semester_num = int(callback_data.split("_")[1])
        text = build_semester_info(semester_num)
        await query.edit_message_text(
            text,
            reply_markup=semester_courses_keyboard(semester_num)
        )
    
    elif callback_data.startswith("course_"):
        parts = callback_data.split("_")
        semester_num = int(parts[1])
        course_idx = int(parts[2])
        text = build_course_details(semester_num, course_idx)
        await query.edit_message_text(
            text,
            reply_markup=back_to_semester_keyboard(semester_num)
        )
    
    elif callback_data == "objectives":
        text = build_objectives()
        await query.edit_message_text(text, reply_markup=main_menu_keyboard())
    
    elif callback_data == "employability":
        text = build_employability()
        await query.edit_message_text(text, reply_markup=main_menu_keyboard())
    
    elif callback_data == "further_study":
        text = build_further_study()
        await query.edit_message_text(text, reply_markup=main_menu_keyboard())
    
    elif callback_data == "statistics":
        text = build_statistics()
        await query.edit_message_text(text, reply_markup=main_menu_keyboard())
    
    else:
        await query.edit_message_text(
            "Invalid option. Returning to main menu.",
            reply_markup=main_menu_keyboard()
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")

# ==================== MAIN ====================
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_error_handler(error_handler)
    
    print("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()